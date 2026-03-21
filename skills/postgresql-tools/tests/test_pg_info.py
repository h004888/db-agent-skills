#!/usr/bin/env python3
"""Tests for pg_info.py"""

import pytest
import sys
import json
from unittest.mock import MagicMock, patch


class TestPgInfo:
    """Test cases for pg_info.py"""

    def test_get_database_info_success(self, mock_psycopg2, sample_connection_params):
        """Test successful database info retrieval"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            (10485760,),
            ("test_db", 1, 6, "en_US.UTF-8", "en_US.UTF-8", False, True, -1, 12345, 100, 1, 1663),
            (10,),
            (3,),
            (15,),
            (5242880,),
            ("14.5",),
            ("100",),
            ("ISO, MDY",),
        ]

        from pg_info import get_database_info

        result = get_database_info(
            host=sample_connection_params["host"],
            port=sample_connection_params["port"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
            database=sample_connection_params["database"]
        )

        assert result["success"] is True
        assert "server" in result["data"]
        assert "database" in result["data"]
        assert "size" in result["data"]
        assert "objects" in result["data"]
        assert result["data"]["objects"]["table_count"] == 10
        assert result["data"]["objects"]["view_count"] == 3
        assert result["data"]["objects"]["index_count"] == 15

    def test_get_database_info_size_calculation(self, mock_psycopg2, sample_connection_params):
        """Test database size is calculated correctly in MB"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5",),
            (10485760,),
            ("test_db", 1, 6, "en_US.UTF-8", "en_US.UTF-8", False, True, -1, 12345, 100, 1, 1663),
            (5,),
            (10,),
            (20,),
            (5242880,),
            ("14.5",),
            ("100",),
            ("ISO, MDY",),
        ]

        from pg_info import get_database_info

        result = get_database_info(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db"
        )

        assert result["success"] is True
        assert result["data"]["size"]["database_bytes"] == 10485760
        assert result["data"]["size"]["database_mb"] == 10.0
        assert result["data"]["size"]["tables_total_mb"] == 5.0

    def test_get_database_info_failure(self, mock_psycopg2, sample_connection_params):
        """Test failed database info retrieval"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        import psycopg2
        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Connection failed")

        from pg_info import get_database_info

        result = get_database_info(
            host="localhost",
            port=5432,
            user="postgres",
            password="wrong",
            database="test_db"
        )

        assert result["success"] is False
        assert "error" in result

    def test_get_database_info_exception(self, mock_psycopg2, sample_connection_params):
        """Test database info with unexpected exception"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        mock_psycopg2["connect"].side_effect = Exception("Unexpected error")

        from pg_info import get_database_info

        result = get_database_info(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db"
        )

        assert result["success"] is False
        assert result["error"] == "Unexpected error"

    def test_main_with_valid_args(self, mock_psycopg2, capsys):
        """Test main function with valid arguments"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        from pg_info import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            (10485760,),
            ("test_db", 1, 6, "en_US.UTF-8", "en_US.UTF-8", False, True, -1, 12345, 100, 1, 1663),
            (5,),
            (10,),
            (20,),
            (5242880,),
            ("14.5",),
            ("100",),
            ("ISO, MDY",),
        ]

        with patch.object(sys, "argv", [
            "pg_info.py",
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
            assert result["data"]["database"]["name"] == "test_db"

    def test_main_exit_code_on_success(self, mock_psycopg2):
        """Test exit code is 0 on success"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        from pg_info import main

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5 on x86_64",),
            (10485760,),
            ("test_db", 1, 6, "en_US.UTF-8", "en_US.UTF-8", False, True, -1, 12345, 100, 1, 1663),
            (5,),
            (10,),
            (20,),
            (5242880,),
            ("14.5",),
            ("100",),
            ("ISO, MDY",),
        ]

        with patch.object(sys, "argv", [
            "pg_info.py",
            "--password", "password",
            "--database", "test_db"
        ]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_with(0)

    def test_main_exit_code_on_failure(self, mock_psycopg2):
        """Test exit code is 1 on failure"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        import psycopg2
        from pg_info import main

        mock_psycopg2["connect"].side_effect = psycopg2.OperationalError("Failed")

        with patch.object(sys, "argv", [
            "pg_info.py",
            "--password", "wrong",
            "--database", "test_db"
        ]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_with(1)

    def test_database_object_counts(self, mock_psycopg2, sample_connection_params):
        """Test that object counts are retrieved correctly"""
        if 'pg_info' in sys.modules:
            del sys.modules['pg_info']

        mock_cursor = mock_psycopg2["cursor"]
        mock_cursor.fetchone.side_effect = [
            ("PostgreSQL 14.5",),
            (10485760,),
            ("test_db", 1, 6, "en_US.UTF-8", "en_US.UTF-8", False, True, -1, 12345, 100, 1, 1663),
            (25,),
            (5,),
            (100,),
            (10485760,),
            ("14.5",),
            ("100",),
            ("ISO, MDY",),
        ]

        from pg_info import get_database_info

        result = get_database_info(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="test_db"
        )

        assert result["success"] is True
        assert result["data"]["objects"]["table_count"] == 25
        assert result["data"]["objects"]["view_count"] == 5
        assert result["data"]["objects"]["index_count"] == 100
