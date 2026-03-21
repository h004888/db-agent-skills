#!/usr/bin/env python3
"""Tests for pg_schema.py"""

import pytest
import sys
import json
from unittest.mock import MagicMock, patch


class TestPgSchema:
    """Test cases for pg_schema.py"""

    def test_get_table_schema_success(self, mock_psycopg2, sample_connection_params, sample_column_info):
        """Test successful schema retrieval"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.side_effect = [
            sample_column_info,  # columns
            [],  # primary keys
            [],  # indexes
            [],  # foreign keys
        ]

        from pg_schema import get_table_schema

        result = get_table_schema(
            host=sample_connection_params["host"],
            port=sample_connection_params["port"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
            database=sample_connection_params["database"],
            table="users"
        )

        assert result["success"] is True
        assert result["data"]["table"] == "users"
        assert len(result["data"]["columns"]) == 4
        assert result["data"]["columns"][0]["column_name"] == "id"
        assert result["data"]["columns"][0]["data_type"] == "integer"

    def test_get_table_schema_with_primary_key(self, mock_psycopg2, sample_connection_params, sample_column_info):
        """Test schema retrieval with primary key info"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.side_effect = [
            sample_column_info,  # columns
            [("id", "users_pkey")],  # primary keys
            [],  # indexes
            [],  # foreign keys
        ]

        from pg_schema import get_table_schema

        result = get_table_schema(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            table="users"
        )

        assert result["success"] is True
        id_column = result["data"]["columns"][0]
        assert id_column["is_primary_key"] is True
        assert id_column["primary_key_constraint"] == "users_pkey"

    def test_get_table_schema_with_indexes(self, mock_psycopg2, sample_connection_params, sample_column_info):
        """Test schema retrieval with index information"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        mock_cursor = mock_psycopg2["cursor"]

        # Mock fetchall calls in order:
        # 1. columns query
        # 2. primary keys query
        # 3. indexes query (main)
        # 4. index columns query (nested in loop)
        # 5. foreign keys query
        mock_cursor.fetchall.side_effect = [
            sample_column_info,  # columns
            [],  # primary keys
            [("users_email_idx", "CREATE INDEX users_email_idx ON users(email)", "btree")],  # indexes
            [("email",)],  # columns for index
            [],  # foreign keys
        ]
        mock_cursor.fetchone.return_value = (100,)  # row count

        from pg_schema import get_table_schema

        result = get_table_schema(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            table="users"
        )

        assert result["success"] is True
        assert len(result["data"]["indexes"]) == 1
        assert result["data"]["indexes"][0]["name"] == "users_email_idx"
        assert result["data"]["indexes"][0]["columns"] == ["email"]

    def test_get_table_schema_with_foreign_keys(self, mock_psycopg2, sample_connection_params, sample_column_info):
        """Test schema retrieval with foreign key information"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.side_effect = [
            sample_column_info,  # columns
            [],  # primary keys
            [],  # indexes
            [("fk_orders_user", "user_id", "users", "id", "public")],  # foreign keys
        ]

        from pg_schema import get_table_schema

        result = get_table_schema(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db",
            table="orders"
        )

        assert result["success"] is True
        assert len(result["data"]["foreign_keys"]) == 1
        assert result["data"]["foreign_keys"][0]["column"] == "user_id"
        assert result["data"]["foreign_keys"][0]["foreign_table"] == "users"

    def test_get_table_schema_failure(self, mock_psycopg2, sample_connection_params):
        """Test failed schema retrieval"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        import psycopg2
        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Connection failed")

        from pg_schema import get_table_schema

        result = get_table_schema(
            host="localhost",
            port=5432,
            user="postgres",
            password="wrong",
            database="test_db",
            table="users"
        )

        assert result["success"] is False
        assert "error" in result

    def test_main_with_valid_args(self, mock_psycopg2, sample_column_info, capsys):
        """Test main function with valid arguments"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        from pg_schema import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.side_effect = [
            sample_column_info,
            [],
            [],
            [],
        ]
        mock_cursor.fetchone.return_value = (100,)  # Row count

        with patch.object(sys, "argv", [
            "pg_schema.py",
            "--password", "password",
            "--database", "test_db",
            "--table", "users"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
            assert result["data"]["table"] == "users"

    def test_main_with_schema_arg(self, mock_psycopg2, sample_column_info, capsys):
        """Test main function with custom schema"""
        if 'pg_schema' in sys.modules:
            del sys.modules['pg_schema']

        from pg_schema import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.side_effect = [
            sample_column_info,
            [],
            [],
            [],
        ]
        mock_cursor.fetchone.return_value = (100,)  # Row count

        with patch.object(sys, "argv", [
            "pg_schema.py",
            "--password", "password",
            "--database", "test_db",
            "--table", "users",
            "--schema", "custom_schema"
        ]):
            try:
                main()
            except SystemExit:
                pass
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result["success"] is True
            assert result["data"]["schema"] == "custom_schema"
