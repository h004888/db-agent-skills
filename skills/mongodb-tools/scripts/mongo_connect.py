#!/usr/bin/env python3
"""MongoDB connection test tool"""

import argparse
import json
import sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def test_connection(
    host: str = "localhost",
    port: int = 27017,
    username: str = None,
    password: str = None,
    auth_source: str = "admin",
    database: str = "test",
    uri: str = None,
    ping: bool = False,
    readonly: bool = False
) -> dict:
    """Test MongoDB connection and optionally ping"""
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

        # Set read preference if readonly
        if readonly:
            client.admin.command('setParameter', 1, journal=True)

        # Get server info
        server_info = client.server_info()

        # Ping if requested
        ping_result = False
        if ping:
            ping_result = client.admin.command('ping')['ok'] == 1

        # Get database stats
        db = client[database]
        db_stats = db.command('dbStats')

        result = {
            "success": True,
            "data": {
                "host": host,
                "port": port,
                "database": database,
                "server_version": server_info['version'],
                "server_status": server_info.get('process', 'unknown'),
                "ping": ping_result,
                "readonly": readonly,
                "database_size_bytes": db_stats.get('dataSize', 0),
                "database_size_mb": round(db_stats.get('dataSize', 0) / (1024 * 1024), 2),
                "collections": db_stats.get('collections', 0),
                "documents": db_stats.get('objects', 0)
            },
            "message": "Connection successful"
        }

        client.close()
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Connection failed"
        }


def main():
    parser = argparse.ArgumentParser(description="Test MongoDB connection")
    parser.add_argument("--host", default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--username", default=None, help="MongoDB username")
    parser.add_argument("--password", default=None, help="MongoDB password")
    parser.add_argument("--authSource", default="admin", help="Authentication database")
    parser.add_argument("--database", default="test", help="Database name")
    parser.add_argument("--uri", default=None, help="Full connection URI (mongodb://...)")
    parser.add_argument("--ping", action="store_true", help="Perform ping test")
    parser.add_argument("--readonly", action="store_true", help="Read-only mode")

    args = parser.parse_args()

    result = test_connection(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        auth_source=args.authSource,
        database=args.database,
        uri=args.uri,
        ping=args.ping,
        readonly=args.readonly
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
