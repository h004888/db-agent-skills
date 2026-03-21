#!/usr/bin/env python3
"""Pytest configuration and shared fixtures for postgresql-tools tests"""

import sys
import os

# Add scripts directory to path for imports
scripts_path = os.path.join(os.path.dirname(__file__), "..", "scripts")
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

import pytest
from unittest.mock import MagicMock, patch
import importlib


@pytest.fixture
def mock_psycopg2():
    """Mock psycopg2 module with fresh mocks for each test"""
    mock_connect = MagicMock()
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    with patch("psycopg2.connect", mock_connect):
        yield {
            "connect": mock_connect,
            "connection": mock_connection,
            "cursor": mock_cursor
        }


@pytest.fixture
def sample_connection_params():
    """Sample connection parameters for testing"""
    return {
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "test_password",
        "database": "test_db"
    }


@pytest.fixture
def sample_table_list():
    """Sample table list data"""
    return [
        ("users", "BASE TABLE", "public", 5),
        ("orders", "BASE TABLE", "public", 8),
        ("products", "BASE TABLE", "public", 12),
        ("user_view", "VIEW", "public", 3),
    ]


@pytest.fixture
def sample_column_info():
    """Sample column information"""
    return [
        ("id", "integer", None, "NO", None, 32, 0, None, "NO", "YES"),
        ("name", "character varying", "'John Doe'", "YES", 255, None, None, None, "NO", "YES"),
        ("email", "character varying", None, "NO", 255, None, None, None, "NO", "YES"),
        ("created_at", "timestamp without time zone", "CURRENT_TIMESTAMP", "YES", None, None, None, 6, "NO", "YES"),
    ]


@pytest.fixture
def sample_query_result():
    """Sample SELECT query result"""
    return [
        (1, "John Doe", "john@example.com"),
        (2, "Jane Smith", "jane@example.com"),
        (3, "Bob Wilson", "bob@example.com"),
    ]
