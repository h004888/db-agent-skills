## Context

Xây dựng MongoDB skill cho AI agent tương tự các SQL skills đã có. MongoDB là NoSQL document database, hoạt động theo mô hình khác biệt so với SQL databases.

## Goals / Non-Goals

**Goals:**
- Tạo 6 scripts Python cho các thao tác MongoDB cơ bản
- Duy trì consistency với format output JSON của các skill khác
- Hỗ trợ authentication và connection options phổ biến
- Schema inference đơn giản bằng sample documents

**Non-Goals:**
- Async operations (dùng PyMongo thay vì Motor)
- Advanced sharding/replica set management
- GUI hoặc interactive mode
- Backup/restore functionality

## Decisions

### 1. Dùng PyMongo thay vì Motor

**Quyết định:** PyMongo (synchronous)

**Rationale:**
- CLI tools không cần async operations
- Đơn giản hơn, dễ debug hơn Motor
- AI agent gọi script → đợi result → parse JSON (không cần non-blocking)

### 2. Schema Inference bằng Sample Documents

**Quyết định:** Lấy N sample documents để trích xuất "schema"

**Rationale:**
- MongoDB schemaless - không có DESCRIBE table
- AI agent cần biết cấu trúc document để viết queries
- Sample approach đơn giản, nhanh, đủ dùng

### 3. Output Format giữ nguyên JSON structure

```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

**Rationale:**
- Consistency với các skill SQL
- AI agent dễ parse và xử lý

### 4. Connection String vs Parameters

**Quyết định:** Dùng individual parameters (host, port, user, password, database)

**Rationale:**
- Thống nhất với các skill khác (mysql-tools, postgresql-tools)
- Dễ parse từ AI agent
- Connection string chỉ hỗ trợ khi cần (--uri option)

### 5. Scripts Design

| Script | Main Function | MongoDB Operation |
|--------|--------------|------------------|
| `mongo_connect.py` | `test_connection()` | `ping()`, `server_info()` |
| `mongo_collections.py` | `list_collections()` | `list_collection_names()` |
| `mongo_schema.py` | `get_collection_schema()` | `find().limit()` |
| `mongo_query.py` | `execute_query()` | `find()`, `aggregate()`, `update*()` |
| `mongo_info.py` | `get_database_info()` | `stats()`, `serverStatus()` |
| `mongo_indexes.py` | `list_indexes()` | `index_information()` |

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| BSON types không serialize được JSON | Custom JSON encoder cho ObjectId, ISODate, Binary |
| Embedded documents phức tạp | Flatten option hoặc recursive display |
| Large collections | Sample size nhỏ (mặc định 5 docs) |
| Authentication phức tạp (x509, ldap) | Hỗ trợ basic auth trước, mở rộng sau |
