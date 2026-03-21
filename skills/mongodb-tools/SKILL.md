---
name: mongodb-tools
description: "MongoDB database tools for AI agents. Supports connection testing, collection management, schema inference, query execution, and index analysis. Works with MongoDB 4.0+."
---

# MongoDB Tools Skill

Tools for MongoDB database operations including connection testing, collection listing, schema inference, query execution, and index analysis.

## Quick Start

### Prerequisites

```bash
pip install pymongo
```

### Connection Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--host` | MongoDB server address | localhost |
| `--port` | MongoDB server port | 27017 |
| `--username` | Database username | (none) |
| `--password` | Database password | (none) |
| `--authSource` | Authentication database | admin |
| `--database` | Database name | test |
| `--uri` | Full connection URI (alternative) | (none) |

### Platform Compatibility

- ✅ Windows
- ✅ macOS
- ✅ Linux

## Available Scripts

### 1. Test Connection

```bash
python skills/mongodb-tools/scripts/mongo_connect.py \
  --host localhost --port 27017 --username root --password YOUR_PASSWORD --database YOUR_DB
```

With ping:
```bash
python skills/mongodb-tools/scripts/mongo_connect.py --host localhost --database test --password PASS --ping
```

### 2. List Collections

```bash
python skills/mongodb-tools/scripts/mongo_collections.py \
  --host localhost --database test --password PASS
```

Include system collections:
```bash
python skills/mongodb-tools/scripts/mongo_collections.py --host localhost --database test --password PASS --all
```

### 3. View Schema

```bash
python skills/mongodb-tools/scripts/mongo_schema.py \
  --host localhost --database test --collection users --password PASS
```

Deep analysis:
```bash
python skills/mongodb-tools/scripts/mongo_schema.py --host localhost --database test --collection users --password PASS --deep
```

### 4. Execute Query

```bash
python skills/mongodb-tools/scripts/mongo_query.py \
  --host localhost --database test --collection users --password PASS \
  --query '{"name": {"$exists": true}}'
```

With limit:
```bash
python skills/mongodb-tools/scripts/mongo_query.py --host localhost --database test --collection users --password PASS \
  --query '{}' --limit 10 --fields name,email
```

Read-only mode (blocks write operations):
```bash
python skills/mongodb-tools/scripts/mongo_query.py --host localhost --database test --collection users --password PASS \
  --query '{"_id": {"$oid": "..."}}' --readonly
```

### 5. Database Info

```bash
python skills/mongodb-tools/scripts/mongo_info.py \
  --host localhost --database test --password PASS
```

Detailed server status:
```bash
python skills/mongodb-tools/scripts/mongo_info.py --host localhost --database test --password PASS --detailed
```

### 6. List Indexes

```bash
python skills/mongodb-tools/scripts/mongo_indexes.py \
  --host localhost --database test --collection users --password PASS
```

## Output Format

All scripts output JSON format:

```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

Error format:
```json
{
  "success": false,
  "error": "Error message here",
  "message": "Operation failed"
}
```

## MongoDB Query Examples

See `references/common_queries.md` for more MongoDB query examples.

### Find Documents
```javascript
db.users.find({age: {"$gte": 18}}, {name: 1, email: 1})
```

### Insert Document
```javascript
db.users.insertOne({name: "John", email: "john@example.com"})
```

### Update Document
```javascript
db.users.updateOne({_id: ObjectId("...")}, {$set: {name: "Jane"}})
```

### Delete Document
```javascript
db.users.deleteOne({_id: ObjectId("...")})
```

### Aggregation Pipeline
```javascript
db.orders.aggregate([
  {$match: {status: "completed"}},
  {$group: {_id: "$customer", total: {$sum: "$amount"}}}
])
```

## Notes

- MongoDB is schemaless - "schema" is inferred from sample documents
- BSON types are automatically serialized to JSON-compatible formats
- Use `--readonly` flag to prevent accidental write operations
- ObjectId values should be passed as strings (e.g., `"507f1f77bcf86cd799439011"`)
