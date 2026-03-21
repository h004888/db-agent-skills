#!/usr/bin/env python3
"""Tests for pg_connect.py"""

import pytest
import sys
import json
from unittest.mock import MagicMock, patch
import importlib


class TestPgConnect:
    """Test cases for pg_connect.py"""

    def test_test_connection_success(self, mock_psycopg2, sample_connection_params):
        """Test successful database connection"""
        # Reload module to get fresh mocks
        if 'pg_connect' in sys.modules:
            del sys.modules['pg_connect']
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            ("14.5",),
            ("ISO, MDY",),
            (10485760,),
            (10,),
        ]

        from pg_connect import test_connection

        result = test_connection(
            host=sample_connection_params["host"],
            port=sample_connection_params["port"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
            database=sample_connection_params["database"]
        )

        assert result["success"] is True
        assert result["data"]["host"] == "localhost"
        assert result["data"]["port"] == 5432
        assert result["data"]["database"] == "test_db"
        assert "server_version" in result["data"]
        mock_psycopg2["connect"].assert_called_once()

    def test_test_connection_failure(self, mock_psycopg2, sample_connection_params):
        """Test failed database connection"""
        if 'pg_connect' in sys.modules:
            del sys.modules['pg_connect']

        import psycopg2
        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Connection refused")

        from pg_connect import test_connection

        result = test_connection(
            host="invalid_host",
            port=5432,
            user="postgres",
            password="wrong",
            database="invalid_db"
        )

        assert result["success"] is False
        assert "error" in result
        assert result["message"] == "Database connection failed"

    def test_test_connection_exception(self, mock_psycopg2, sample_connection_params):
        """Test connection with unexpected exception"""
        if 'pg_connect' in sys.modules:
            del sys.modules['pg_connect']

        mock_psycopg2["connect"].side_effect = Exception("Unknown error")

        from pg_connect import test_connection

        result = test_connection(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db"
        )

        assert result["success"] is False
        assert result["error"] == "Unknown error"

    def test_main_with_valid_args(self, mock_psycopg2, capsys):
        """Test main function with valid arguments"""
        if 'pg_connect' in sys.modules:
            del sys.modules['pg_connect']

        from pg_connect import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            ("14.5",),
            ("ISO, MDY",),
            (10485760,),
            (10,),
        ]

        with patch.object(sys, "argv", [
            "pg_connect.py",
            "--host", "localhost",
            "--port", "5432",
            "--user", "postgres",
            "--password", "password",
            "--database", "test_db"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True

    def test_main_with_defaults(self, mock_psycopg2, capsys):
        """Test main function with default parameters"""
        if 'pg_connect' in sys.modules:
            del sys.modules['pg_connect']

        from pg_connect import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            ("14.5",),
            ("ISO, MDY",),
            (10485760,),
            (10,),
        ]

        with patch.object(sys, "argv", [
            "pg_connect.py",
            "--password", "password",
            "--database", "test_db"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
            assert result["data"]["host"] == "localhost"
            assert result["data"]["port"] == 5432
            assert result["data"]["user"] == "postgres"
