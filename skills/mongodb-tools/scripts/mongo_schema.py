#!/usr/bin/env python3
"""MongoDB schema inference tool"""

import argparse
import json
import sys
from datetime import datetime
from bson import ObjectId, DBRef, Binary, Code
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_bson_type(value) -> str:
    """Get BSON type name for a value"""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, ObjectId):
        return "objectId"
    elif isinstance(value, datetime):
        return "date"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    elif isinstance(value, Binary):
        return "binary"
    elif isinstance(value, DBRef):
        return "dbRef"
    elif isinstance(value, Code):
        return "code"
    else:
        return str(type(value).__name__)


def flatten_document(doc: dict, parent_key: str = '', sep: str = '.') -> dict:
    """Flatten a nested document for schema analysis"""
    items = []
    for k, v in doc.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict) and v:
            items.extend(flatten_document(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_collection_schema(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    collection: str = None,
    uri: str = None,
    sample_size: int = 5,
    deep: bool = False
) -> dict:
    """Infer schema from sample documents in a collection"""
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

        # Get sample documents
        samples = list(coll.find().limit(sample_size))

        # Serialize samples (convert ObjectId, datetime, etc.)
        serialized_samples = []
        for doc in samples:
            serialized_doc = {}
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    serialized_doc[key] = {"$oid": str(value)}
                elif isinstance(value, datetime):
                    serialized_doc[key] = {"$date": value.isoformat()}
                elif isinstance(value, Binary):
                    serialized_doc[key] = {"$binary": value.hex()}
                elif isinstance(value, bytes):
                    serialized_doc[key] = {"$binary": value.hex()}
                else:
                    serialized_doc[key] = value
            serialized_samples.append(serialized_doc)

        # Build field schema from samples
        fields = {}

        for doc in samples:
            flat_doc = flatten_document(doc)
            for field, value in flat_doc.items():
                if field not in fields:
                    bson_type = get_bson_type(value)

                    if isinstance(value, dict) and bson_type == "object":
                        # Recursively get nested schema
                        nested_fields = {}
                        for nested_key, nested_value in value.items():
                            nested_fields[nested_key] = {
                                "bson_type": get_bson_type(nested_value)
                            }
                        fields[field] = {
                            "bson_type": "object",
                            "fields": nested_fields
                        }
                    elif isinstance(value, list):
                        # Get element type if possible
                        element_types = set()
                        for item in value if isinstance(value, list) else []:
                            element_types.add(get_bson_type(item))
                        fields[field] = {
                            "bson_type": "array",
                            "element_types": list(element_types)
                        }
                    else:
                        fields[field] = {
                            "bson_type": bson_type
                        }

        # Deep analysis using aggregation (if requested)
        field_stats = {}
        if deep:
            try:
                pipeline = [
                    {"$sample": {"size": min(100, coll.count_documents({}))}},
                    {"$project": {"fieldPaths": {"$objectToArray": "$$ROOT"}}},
                    {"$unwind": "$fieldPaths"},
                    {"$group": {
                        "_id": "$fieldPaths.k",
                        "count": {"$sum": 1},
                        "types": {"$addToSet": {"$type": "$fieldPaths.v"}}
                    }}
                ]
                stats = list(coll.aggregate(pipeline))
                for stat in stats:
                    field_stats[stat['_id']] = {
                        "present_in": stat['count'],
                        "types_seen": stat['types']
                    }
            except Exception:
                pass

        result = {
            "success": True,
            "data": {
                "collection": collection,
                "database": database,
                "sample_size": len(samples),
                "fields": fields,
                "sample_documents": serialized_samples,
                "deep_analysis": field_stats if deep else {}
            },
            "message": f"Schema inference complete for {collection}"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get schema for {collection}"
        }


def main():
    parser = argparse.ArgumentParser(description="Infer MongoDB collection schema")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--collection", required=True, help="Collection name")
    parser.add_argument("--uri", default=None, help="Full connection URI")
    parser.add_argument("--sample-size", type=int, default=5, help="Number of sample documents")
    parser.add_argument("--deep", action="store_true", help="Deep schema analysis")

    args = parser.parse_args()

    result = get_collection_schema(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        collection=args.collection,
        uri=args.uri,
        sample_size=args.sample_size,
        deep=args.deep
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
