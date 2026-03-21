## 1. Project Setup

- [x] 1.1 Create `skills/mongodb-tools/` directory structure
- [x] 1.2 Create `skills/mongodb-tools/scripts/` directory
- [x] 1.3 Create `skills/mongodb-tools/references/` directory
- [x] 1.4 Create `skills/mongodb-tools/tests/` directory
- [x] 1.5 Add dependency note to `pyproject.toml` or `requirements.txt`

## 2. SKILL.md Documentation

- [x] 2.1 Create `SKILL.md` with usage instructions
- [x] 2.2 Document connection parameters
- [x] 2.3 Document each script's purpose and usage
- [x] 2.4 Add examples for each script
- [x] 2.5 Document output format

## 3. Core Scripts

### 3.1 mongo_connect.py

- [x] 3.1.1 Implement `test_connection()` function
- [x] 3.1.2 Handle authentication with username/password
- [x] 3.1.3 Support `--uri` option for connection string
- [x] 3.1.4 Return server version and connection status
- [x] 3.1.5 Implement `--ping` flag for quick test
- [x] 3.1.6 Add `--readonly` support (read preferences)

### 3.2 mongo_collections.py

- [x] 3.2.1 Implement `list_collections()` function
- [x] 3.2.2 Return collection names, types, document counts
- [x] 3.2.3 Include system collections option (`--all`)
- [x] 3.2.4 Handle collection stats if available

### 3.3 mongo_schema.py

- [x] 3.3.1 Implement `get_collection_schema()` function
- [x] 3.3.2 Sample N documents from collection
- [x] 3.3.3 Extract field names and BSON types
- [x] 3.3.4 Support `--deep` flag for aggregation-based schema
- [x] 3.3.5 Handle embedded documents (recursive display)
- [x] 3.3.6 Handle arrays and nested structures

### 3.4 mongo_query.py

- [x] 3.4.1 Implement `execute_query()` function
- [x] 3.4.2 Support `find()` operations
- [x] 3.4.3 Support `aggregate()` operations
- [x] 3.4.4 Support write operations (insert, update, delete)
- [x] 3.4.5 Implement `--readonly` mode to block writes
- [x] 3.4.6 Support `--limit` and `--skip` options
- [x] 3.4.7 Handle projection with `--fields`
- [x] 3.4.8 JSON serialize BSON types (ObjectId, ISODate)

### 3.5 mongo_info.py

- [x] 3.5.1 Implement `get_database_info()` function
- [x] 3.5.2 Return database stats (collections, documents, size)
- [x] 3.5.3 Return server status info
- [x] 3.5.4 Support `--detailed` for full serverStatus

### 3.6 mongo_indexes.py

- [x] 3.6.1 Implement `list_indexes()` function
- [x] 3.6.2 Return index names, keys, types
- [x] 3.6.3 Show unique, sparse, TTL properties
- [x] 3.6.4 Calculate index size if available

## 4. References

- [x] 4.1 Create `references/common_queries.md`
- [x] 4.2 Add CRUD examples (insert, find, update, delete)
- [x] 4.3 Add aggregation pipeline examples
- [x] 4.4 Add index management examples
- [x] 4.5 Add common query operators examples

## 5. Testing

- [x] 5.1 Create `tests/conftest.py` with mock fixtures
- [x] 5.2 Create `tests/test_mongo_connect.py`
- [x] 5.3 Create `tests/test_mongo_collections.py`
- [x] 5.4 Create `tests/test_mongo_schema.py`
- [x] 5.5 Create `tests/test_mongo_query.py`
- [x] 5.6 Create `tests/test_mongo_info.py`
- [x] 5.7 Create `tests/test_mongo_indexes.py`
- [x] 5.8 Run all tests and verify 100% pass

## 6. Documentation & Cleanup

- [x] 6.1 Update `README.md` to include mongodb-tools
- [x] 6.2 Update `README_EN.md` to include mongodb-tools
- [x] 6.3 Verify all scripts import correctly
- [x] 6.4 Final test run to confirm everything works
