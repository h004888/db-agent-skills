#!/usr/bin/env python3
"""MongoDB index listing tool"""

import argparse
import json
import sys
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.server_api import ServerApi


def list_indexes(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    collection: str = None,
    uri: str = None
) -> dict:
    """List all indexes on a collection"""
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

        # Get all indexes
        indexes = coll.list_indexes()

        index_list = []
        for idx in indexes:
            index_info = {
                "name": idx['name'],
                "keys": idx.get('key', {}),
                "unique": idx.get('unique', False),
                "sparse": idx.get('sparse', False),
                "background": idx.get('background', False),
                "ttl": idx.get('expireAfterSeconds', None),
                "version": idx.get('v', None),
            }

            # Determine index type
            keys = idx.get('key', {})
            if '2dsphere' in keys.values():
                index_info["type"] = "2dsphere"
            elif '2d' in keys.values():
                index_info["type"] = "2d"
            elif 'text' in keys.values():
                index_info["type"] = "text"
            elif 'hashed' in keys.values():
                index_info["type"] = "hashed"
            elif index_info.get('unique'):
                index_info["type"] = "unique"
            else:
                index_info["type"] = "standard"

            # Try to get index size
            try:
                stats = db.command('collStats', collection, index_details=True)
                if 'indexDetails' in stats:
                    for idx_detail in stats['indexDetails']:
                        if idx_detail.get('name') == idx['name']:
                            index_info['size_bytes'] = idx_detail.get('size', 0)
                            index_info['size_mb'] = round(idx_detail.get('size', 0) / (1024 * 1024), 4)
                            break
            except Exception:
                pass

            index_list.append(index_info)

        result = {
            "success": True,
            "data": {
                "collection": collection,
                "database": database,
                "index_count": len(index_list),
                "indexes": index_list
            },
            "message": f"Found {len(index_list)} indexes on {collection}"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list indexes for {collection}"
        }


def main():
    parser = argparse.ArgumentParser(description="List MongoDB indexes")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--collection", required=True, help="Collection name")
    parser.add_argument("--uri", default=None, help="Full connection URI")

    args = parser.parse_args()

    result = list_indexes(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        collection=args.collection,
        uri=args.uri
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
