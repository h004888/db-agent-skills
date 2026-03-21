## Why

Mở rộng bộ công cụ database tools cho AI agent để hỗ trợ MongoDB - một trong những NoSQL database phổ biến nhất. Các skill hiện tại (MySQL, PostgreSQL, SQL Server, SQLite, DM8) đều là SQL databases. MongoDB sử dụng document model hoàn toàn khác, cần cách tiếp cận riêng.

## What Changes

Thêm mongodb-tools skill mới với 6 scripts Python để thao tác với MongoDB database:

```
mongodb-tools/
├── SKILL.md                    # Hướng dẫn sử dụng
├── scripts/
│   ├── mongo_connect.py       # Test connection + ping
│   ├── mongo_collections.py   # List collections
│   ├── mongo_schema.py        # Show sample document(s)
│   ├── mongo_query.py         # find(), aggregate()
│   ├── mongo_info.py          # serverStatus, stats
│   └── mongo_indexes.py       # List indexes
└── references/
    └── common_queries.md      # MongoDB query examples
```

## Capabilities

### New Capabilities

- `mongodb-connect`: Kết nối và kiểm tra kết nối MongoDB với ping
- `mongodb-collections`: Liệt kê tất cả collections trong database
- `mongodb-schema`: Trích xuất và hiển thị cấu trúc document (schema inference từ samples)
- `mongodb-query`: Thực thi MongoDB queries (find, aggregate, update, insert, delete)
- `mongodb-info`: Lấy thông tin database và server
- `mongodb-indexes`: Liệt kê indexes trên collection

## Impact

- **New dependency**: `pymongo` (Python MongoDB driver)
- **New directory**: `skills/mongodb-tools/`
- **Pattern consistency**: Cùng output format JSON với các skill khác
- **Schemaless handling**: Sample document approach thay vì DESCRIBE table

## Technical Notes

### MongoDB vs SQL Structure

| SQL | MongoDB |
|-----|---------|
| Database | Database |
| Tables | Collections |
| Rows | Documents (BSON) |
| Columns | Fields |
| Schema | Schemaless (inferred from samples) |

### Connection Parameters

```
host, port, username, password, authSource, database
+ optional: replicaSet, tls, maxPoolSize
```

### Schema Inference

Vì MongoDB không có schema cố định, `mongo_schema.py` sẽ:
1. Lấy N sample documents từ collection
2. Trích xuất field names và BSON types
3. Trả về cấu trúc " inferred schema"

### Dependencies

```bash
pip install pymongo
# hoặc
pip install pymongo[srv]  # cho mongodb+srv:// connections
```
