#!/usr/bin/env python3
"""MongoDB database info tool"""

import argparse
import json
import sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_database_info(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    uri: str = None,
    detailed: bool = False,
    collection: str = None
) -> dict:
    """Get MongoDB database and server information"""
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

        # Get server status
        server_info = client.server_info()
        server_status = client.admin.command('serverStatus')

        # Get database stats
        db = client[database]
        db_stats = db.command('dbStats')

        # Build result data
        data = {
            "database": database,
            "collections": db_stats.get('collections', 0),
            "documents": db_stats.get('objects', 0),
            "database_size_bytes": db_stats.get('dataSize', 0),
            "database_size_mb": round(db_stats.get('dataSize', 0) / (1024 * 1024), 2),
            "storage_size_bytes": db_stats.get('storageSize', 0),
            "storage_size_mb": round(db_stats.get('storageSize', 0) / (1024 * 1024), 2),
            "index_size_bytes": db_stats.get('indexSize', 0),
            "index_size_mb": round(db_stats.get('indexSize', 0) / (1024 * 1024), 2),
            "server_info": {
                "version": server_info['version'],
                "version_number": server_info.get('versionNumber', server_info.get('version')),
                "process": server_info.get('process', 'unknown'),
                "uptime_seconds": server_status.get('uptime', 0),
                "uptime_hours": round(server_status.get('uptime', 0) / 3600, 2),
                "connections_current": server_status.get('connections', {}).get('current', 0),
                "connections_available": server_status.get('connections', {}).get('available', 0),
            }
        }

        # Add collection-specific stats if requested
        if collection:
            try:
                coll_stats = db.command('collStats', collection)
                data["collection_stats"] = {
                    "name": collection,
                    "count": coll_stats.get('count', 0),
                    "size_bytes": coll_stats.get('size', 0),
                    "size_mb": round(coll_stats.get('size', 0) / (1024 * 1024), 2),
                    "average_object_size": coll_stats.get('avgObjSize', 0),
                    "storage_size_bytes": coll_stats.get('storageSize', 0),
                    "total_index_size_bytes": coll_stats.get('totalIndexSize', 0),
                }
            except Exception as e:
                data["collection_stats"] = {"error": str(e)}

        # Add detailed server status if requested
        if detailed:
            data["detailed_server_status"] = {
                "memory": server_status.get('mem', {}),
                "network": server_status.get('network', {}),
                "storage_engine": server_status.get('storageEngine', {}),
                "opcounters": server_status.get('opcounters', {}),
                "opcounters_replicated": server_status.get('opcountersReplicated', {}),
                "asserts": server_status.get('asserts', {}),
                "extra_info": server_status.get('extra_info', {}),
            }

        result = {
            "success": True,
            "data": data,
            "message": "Database information retrieved"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get database information"
        }


def main():
    parser = argparse.ArgumentParser(description="Get MongoDB database info")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--uri", default=None, help="Full connection URI")
    parser.add_argument("--detailed", action="store_true", help="Include detailed server status")
    parser.add_argument("--collection", default=None, help="Collection name for stats")

    args = parser.parse_args()

    result = get_database_info(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        uri=args.uri,
        detailed=args.detailed,
        collection=args.collection
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
