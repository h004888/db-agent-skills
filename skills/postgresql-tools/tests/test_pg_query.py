#!/usr/bin/env python3
"""Tests for pg_query.py"""

import pytest
import sys
import json
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestPgQuery:
    """Test cases for pg_query.py"""

    def test_execute_select_query_success(self, mock_psycopg2, sample_connection_params, sample_query_result):
        """Test successful SELECT query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",), ("name",), ("email",)]
        mock_cursor.fetchall.return_value = sample_query_result

        from pg_query import execute_query

        result = execute_query(
            host=sample_connection_params["host"],
            port=sample_connection_params["port"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
            database=sample_connection_params["database"],
            query="SELECT * FROM users"
        )

        assert result["success"] is True
        assert result["data"]["row_count"] == 3
        assert result["data"]["columns"] == ["id", "name", "email"]
        assert result["data"]["rows"][0]["id"] == 1
        assert result["data"]["rows"][0]["name"] == "John Doe"

    def test_execute_insert_query_success(self, mock_psycopg2, sample_connection_params):
        """Test successful INSERT query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.rowcount = 1
        mock_cursor.fetchall.return_value = []

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="INSERT INTO users (name) VALUES ('John')"
        )

        assert result["success"] is True
        assert result["data"]["affected_rows"] == 1
        mock_psycopg2["connection"].commit.assert_called_once()

    def test_execute_update_query_success(self, mock_psycopg2, sample_connection_params):
        """Test successful UPDATE query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.rowcount = 5

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="UPDATE users SET active = true"
        )

        assert result["success"] is True
        assert result["data"]["affected_rows"] == 5

    def test_execute_delete_query_success(self, mock_psycopg2, sample_connection_params):
        """Test successful DELETE query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.rowcount = 2

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="DELETE FROM users WHERE id = 1"
        )

        assert result["success"] is True
        assert result["data"]["affected_rows"] == 2

    def test_execute_query_with_datetime(self, mock_psycopg2, sample_connection_params):
        """Test query returning datetime values"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",), ("created_at",)]
        mock_cursor.fetchall.return_value = [
            (1, datetime(2024, 1, 15, 10, 30, 0)),
            (2, datetime(2024, 1, 16, 14, 45, 0)),
        ]

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="SELECT * FROM logs"
        )

        assert result["success"] is True
        assert "2024-01-15" in result["data"]["rows"][0]["created_at"]

    def test_execute_readonly_mode_allows_select(self, mock_psycopg2, sample_connection_params):
        """Test that readonly mode allows SELECT queries"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",)]
        mock_cursor.fetchall.return_value = [(1,), (2,)]

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="SELECT id FROM users",
            readonly=True
        )

        assert result["success"] is True
        assert result["data"]["row_count"] == 2

    def test_execute_readonly_mode_blocks_write(self, mock_psycopg2, sample_connection_params):
        """Test that readonly mode blocks write operations"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="DELETE FROM users",
            readonly=True
        )

        assert result["success"] is False
        assert "Read-only mode" in result["error"]

    def test_execute_query_failure(self, mock_psycopg2, sample_connection_params):
        """Test failed query execution"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        import psycopg2
        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Query failed")

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="wrong",
            database="test_db",
            query="SELECT * FROM users"
        )

        assert result["success"] is False
        assert "error" in result

    def test_execute_with_clause(self, mock_psycopg2, sample_connection_params, sample_query_result):
        """Test query starting with WITH (CTE)"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",), ("name",)]
        mock_cursor.fetchall.return_value = sample_query_result

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="WITH temp AS (SELECT id FROM users) SELECT * FROM temp"
        )

        assert result["success"] is True

    def test_execute_explain_query(self, mock_psycopg2, sample_connection_params):
        """Test EXPLAIN query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("QUERY PLAN",)]
        mock_cursor.fetchall.return_value = [("Seq Scan on users",)]

        from pg_query import execute_query

        result = execute_query(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            query="EXPLAIN SELECT * FROM users"
        )

        assert result["success"] is True
        assert result["data"]["row_count"] == 1

    def test_main_with_select_query(self, mock_psycopg2, sample_query_result, capsys):
        """Test main function with SELECT query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        from pg_query import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",), ("name",), ("email",)]
        mock_cursor.fetchall.return_value = sample_query_result

        with patch.object(sys, "argv", [
            "pg_query.py",
            "--password", "password",
            "--database", "test_db",
            "--query", "SELECT * FROM users"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
            assert result["data"]["row_count"] == 3

    def test_main_with_insert_query(self, mock_psycopg2, capsys):
        """Test main function with INSERT query"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        from pg_query import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.rowcount = 1

        with patch.object(sys, "argv", [
            "pg_query.py",
            "--password", "password",
            "--database", "test_db",
            "--query", "INSERT INTO users (name) VALUES ('Test')"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
            assert result["data"]["affected_rows"] == 1

    def test_main_with_readonly_flag(self, mock_psycopg2, capsys):
        """Test main function with readonly flag"""
        if 'pg_query' in sys.modules:
            del sys.modules['pg_query']

        from pg_query import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.description = [("id",)]
        mock_cursor.fetchall.return_value = [(1,)]

        with patch.object(sys, "argv", [
            "pg_query.py",
            "--password", "password",
            "--database", "test_db",
            "--query", "SELECT id FROM users",
            "--readonly"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
