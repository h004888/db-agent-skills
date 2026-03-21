#!/usr/bin/env python3
"""Tests for pg_tables.py"""

import pytest
import sys
import json
from unittest.mock import MagicMock, patch


class TestPgTables:
    """Test cases for pg_tables.py"""

    def test_list_tables_success(self, mock_psycopg2, sample_connection_params, sample_table_list):
        """Test successful table listing"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.return_value = sample_table_list

        from pg_tables import list_tables

        result = list_tables(
            host=sample_connection_params["host"],
            port=sample_connection_params["port"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
            database=sample_connection_params["database"]
        )

        assert result["success"] is True
        assert result["data"]["table_count"] == 4
        assert len(result["data"]["tables"]) == 4
        assert result["data"]["tables"][0]["table_name"] == "users"
        assert result["data"]["tables"][0]["table_type"] == "BASE TABLE"

    def test_list_tables_empty(self, mock_psycopg2, sample_connection_params):
        """Test listing tables when database is empty"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchall.return_value = []

        from pg_tables import list_tables

        result = list_tables(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="empty_db"
        )

        assert result["success"] is True
        assert result["data"]["table_count"] == 0
        assert result["data"]["tables"] == []

    def test_list_tables_failure(self, mock_psycopg2, sample_connection_params):
        """Test failed table listing"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        import psycopg2
        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Connection failed")

        from pg_tables import list_tables

        result = list_tables(
            host="localhost",
            port=5432,
            user="postgres",
            password="wrong",
            database="test_db"
        )

        assert result["success"] is False
        assert "error" in result

    def test_list_tables_row_count(self, mock_psycopg2, sample_connection_params, sample_table_list):
        """Test that row counts are fetched for each table"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        mock_cursor = mock_psycopg2["cursor"]

        # Track if we're getting tables or row counts
        call_count = [0]

        def fetchall_side_effect():
            call_count[0] += 1
            if call_count[0] == 1:
                return sample_table_list
            # Subsequent calls are for row counts
            return []

        mock_cursor.fetchall.side_effect = fetchall_side_effect
        mock_cursor.fetchone.side_effect = [(100,), (250,), (500,)]

        from pg_tables import list_tables

        result = list_tables(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db"
        )

        assert result["success"] is True
        assert result["data"]["tables"][0]["row_count"] == 100

    def test_main_with_valid_args(self, mock_psycopg2, sample_table_list, capsys):
        """Test main function with valid arguments"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        from pg_tables import main

        mock_cursor = mock_psycopg2["cursor"]

        call_count = [0]
        def fetchall_side_effect():
            call_count[0] += 1
            if call_count[0] == 1:
                return sample_table_list
            return []

        mock_cursor.fetchall.side_effect = fetchall_side_effect
        mock_cursor.fetchone.side_effect = [(100,), (250,), (500,)]

        with patch.object(sys, "argv", [
            "pg_tables.py",
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
            assert result["data"]["table_count"] == 4

    def test_main_exit_code_on_success(self, mock_psycopg2, sample_table_list):
        """Test exit code is 0 on success"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        from pg_tables import main

        mock_cursor = mock_psycopg2["cursor"]

        call_count = [0]
        def fetchall_side_effect():
            call_count[0] += 1
            if call_count[0] == 1:
                return sample_table_list
            return []

        mock_cursor.fetchall.side_effect = fetchall_side_effect
        mock_cursor.fetchone.side_effect = [(100,), (250,), (500,)]

        with patch.object(sys, "argv", [
            "pg_tables.py",
            "--password", "password",
            "--database", "test_db"
        ]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_with(0)

    def test_main_exit_code_on_failure(self, mock_psycopg2):
        """Test exit code is 1 on failure"""
        if 'pg_tables' in sys.modules:
            del sys.modules['pg_tables']

        import psycopg2
        from pg_tables import main

        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Failed")

        with patch.object(sys, "argv", [
            "pg_tables.py",
            "--password", "wrong",
            "--database", "test_db"
        ]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_with(1)
