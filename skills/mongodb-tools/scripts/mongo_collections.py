#!/usr/bin/env python3
"""MongoDB collection listing tool"""

import argparse
import json
import sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def list_collections(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    uri: str = None,
    include_system: bool = False
) -> dict:
    """List all collections in the database"""
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

        # Get all collection names
        collection_names = db.list_collection_names()

        collections = []
        for name in collection_names:
            # Skip system collections unless requested
            if not include_system and name.startswith('system.'):
                continue

            # Get collection stats
            try:
                stats = db.command('collStats', name)
                collection_type = 'collection'
                document_count = stats.get('count', 0)
            except Exception:
                document_count = 0

            # Check if it's a view
            try:
                view_info = db.command('listCollections', filter={'name': name})
                if view_info.get('cursor', {}).get('firstBatch'):
                    first_batch = view_info['cursor']['firstBatch'][0]
                    if first_batch.get('type') == 'view':
                        collection_type = 'view'
            except Exception:
                pass

            collections.append({
                "name": name,
                "type": collection_type,
                "document_count": document_count
            })

        result = {
            "success": True,
            "data": {
                "database": database,
                "collection_count": len(collections),
                "collections": collections
            },
            "message": f"Found {len(collections)} collections"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list collections"
        }


def main():
    parser = argparse.ArgumentParser(description="List MongoDB collections")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--uri", default=None, help="Full connection URI")
    parser.add_argument("--all", action="store_true", help="Include system collections")

    args = parser.parse_args()

    result = list_collections(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        uri=args.uri,
        include_system=args.all
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
