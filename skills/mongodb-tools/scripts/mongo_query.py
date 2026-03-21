#!/usr/bin/env python3
"""MongoDB query execution tool"""

import argparse
import json
import sys
import re
from datetime import datetime
from bson import ObjectId, json_util
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def serialize_value(value):
    """Serialize BSON value to JSON-compatible format"""
    if isinstance(value, ObjectId):
        return {"$oid": str(value)}
    elif isinstance(value, datetime):
        return {"$date": value.isoformat()}
    elif isinstance(value, bytes):
        return {"$binary": value.hex()}
    else:
        return value


def serialize_document(doc: dict) -> dict:
    """Serialize a document for JSON output"""
    result = {}
    for key, value in doc.items():
        result[key] = serialize_value(value)
    return result


def serialize_results(documents: list) -> list:
    """Serialize a list of documents"""
    return [serialize_document(doc) for doc in documents]


class QueryParser:
    """Parse MongoDB query commands"""

    WRITE_OPERATIONS = ['insertOne', 'insertMany', 'updateOne', 'updateMany',
                       'deleteOne', 'deleteMany', 'findOneAndUpdate',
                       'findOneAndDelete', 'findOneAndReplace', 'replaceOne']

    READ_OPERATIONS = ['find', 'aggregate', 'count', 'distinct', 'findOne']

    @staticmethod
    def detect_operation(query) -> str:
        """Detect if query is a read or write operation"""
        query_str = str(query).lower()

        # Check for write operations
        for op in QueryParser.WRITE_OPERATIONS:
            if op.lower() in query_str:
                return 'write'

        # Check for read operations
        for op in QueryParser.READ_OPERATIONS:
            if op.lower() in query_str:
                return 'read'

        return 'read'  # Default to read

    @staticmethod
    def is_aggregation(query) -> bool:
        """Check if query is an aggregation pipeline"""
        if isinstance(query, dict):
            return '$aggregate' in query or 'pipeline' in str(query).lower()
        return False


def execute_query(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    collection: str = None,
    query: str = "{}",
    uri: str = None,
    readonly: bool = False,
    limit: int = None,
    skip: int = None,
    fields: str = None,
    sort: str = None
) -> dict:
    """Execute MongoDB query"""
    try:
        # Build connection
        if uri:
            client = MongoClient(uri, server_api=ServerApi('1'))
        else:
            if username and password:
                connection_params = {
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'authSource': auth_source,
                    'server_api': ServerApi('1')
                }
            else:
                connection_params = {
                    'host': host,
                    'port': port,
                    'server_api': ServerApi('1')
                }
            client = MongoClient(**connection_params)

        db = client[database]
        coll = db[collection]

        # Parse query string to dict
        try:
            query_dict = json.loads(query)
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON query",
                "message": "Query must be valid JSON"
            }

        # Check readonly mode
        operation_type = QueryParser.detect_operation(query_dict)
        if readonly and operation_type == 'write':
            client.close()
            return {
                "success": False,
                "error": "Write operations not allowed in read-only mode",
                "message": "Query blocked by readonly mode"
            }

        # Build projection
        projection = None
        if fields:
            field_list = [f.strip() for f in fields.split(',')]
            projection = {f: 1 for f in field_list}

        # Build sort
        sort_list = None
        if sort:
            sort_parts = sort.split(',')
            sort_list = []
            for part in sort_parts:
                part = part.strip()
                if part.endswith(' ASC') or part.endswith(' asc'):
                    sort_list.append((part.rsplit(' ', 1)[0], 1))
                elif part.endswith(' DESC') or part.endswith(' desc'):
                    sort_list.append((part.rsplit(' ', 1)[0], -1))
                else:
                    sort_list.append((part, 1))

        # Execute query
        result = None
        operation = "unknown"

        # Handle different operation types
        query_lower = str(query_dict).lower()

        if 'insertone' in query_lower or '{"insertone"' in query_lower:
            operation = "insertOne"
            doc = query_dict.get('document', query_dict.get('insertOne', {}))
            if isinstance(doc, str):
                doc = json.loads(doc)
            result = coll.insert_one(doc if isinstance(doc, dict) else doc)
            response_data = {
                "operation": operation,
                "inserted_id": str(result.inserted_id),
                "affected_rows": 1
            }

        elif 'insertmany' in query_lower:
            operation = "insertMany"
            docs = query_dict.get('documents', query_dict.get('insertMany', []))
            if isinstance(docs, str):
                docs = json.loads(docs)
            result = coll.insert_many(docs)
            response_data = {
                "operation": operation,
                "inserted_ids": [str(id) for id in result.inserted_ids],
                "affected_rows": len(result.inserted_ids)
            }

        elif 'updateone' in query_lower:
            operation = "updateOne"
            filter_doc = query_dict.get('filter', query_dict.get('updateOne', {}).get('filter', {}))
            update_doc = query_dict.get('update', query_dict.get('updateOne', {}).get('update', {}))
            result = coll.update_one(filter_doc, update_doc)
            response_data = {
                "operation": operation,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        elif 'updatemany' in query_lower:
            operation = "updateMany"
            filter_doc = query_dict.get('filter', query_dict.get('updateMany', {}).get('filter', {}))
            update_doc = query_dict.get('update', query_dict.get('updateMany', {}).get('update', {}))
            result = coll.update_many(filter_doc, update_doc)
            response_data = {
                "operation": operation,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        elif 'deleteone' in query_lower:
            operation = "deleteOne"
            filter_doc = query_dict.get('filter', query_dict.get('deleteOne', {}))
            result = coll.delete_one(filter_doc)
            response_data = {
                "operation": operation,
                "deleted_count": result.deleted_count
            }

        elif 'deletemany' in query_lower:
            operation = "deleteMany"
            filter_doc = query_dict.get('filter', query_dict.get('deleteMany', {}))
            result = coll.delete_many(filter_doc)
            response_data = {
                "operation": operation,
                "deleted_count": result.deleted_count
            }

        elif '$aggregate' in query_dict:
            operation = "aggregate"
            pipeline = query_dict['$aggregate']
            cursor = coll.aggregate(pipeline)
            documents = list(cursor)
            response_data = {
                "operation": operation,
                "row_count": len(documents),
                "rows": serialize_results(documents)
            }

        elif 'aggregate' in query_lower:
            operation = "aggregate"
            pipeline = query_dict.get('pipeline', query_dict.get('aggregate', []))
            cursor = coll.aggregate(pipeline)
            documents = list(cursor)
            response_data = {
                "operation": operation,
                "row_count": len(documents),
                "rows": serialize_results(documents)
            }

        else:
            # Default to find
            operation = "find"
            cursor = coll.find(query_dict)

            if projection:
                cursor = cursor.project(projection)
            if sort_list:
                cursor = cursor.sort(sort_list)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)

            documents = list(cursor)
            columns = list(documents[0].keys()) if documents else []

            response_data = {
                "operation": operation,
                "collection": collection,
                "row_count": len(documents),
                "columns": columns,
                "rows": serialize_results(documents)
            }

        result = {
            "success": True,
            "data": response_data,
            "message": f"{operation} completed successfully"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Query execution failed"
        }


def main():
    parser = argparse.ArgumentParser(description="Execute MongoDB queries")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--collection", required=True, help="Collection name")
    parser.add_argument("--query", required=True, help="Query as JSON string")
    parser.add_argument("--uri", default=None, help="Full connection URI")
    parser.add_argument("--readonly", action="store_true", help="Read-only mode (blocks writes)")
    parser.add_argument("--limit", type=int, default=None, help="Limit results")
    parser.add_argument("--skip", type=int, default=None, help="Skip results")
    parser.add_argument("--fields", default=None, help="Comma-separated field list for projection")
    parser.add_argument("--sort", default=None, help="Sort specification (field ASC|DESC)")

    args = parser.parse_args()

    result = execute_query(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        collection=args.collection,
        query=args.query,
        uri=args.uri,
        readonly=args.readonly,
        limit=args.limit,
        skip=args.skip,
        fields=args.fields,
        sort=args.sort
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
