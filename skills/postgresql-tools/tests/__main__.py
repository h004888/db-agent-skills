#!/usr/bin/env python3
"""Run all tests for postgresql-tools"""

import pytest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
