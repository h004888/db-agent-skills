# My Agent Skills

## Các skill có sẵn

| Skill | Database | Phụ thuộc |
|-------|----------|-----------|
| [mysql-tools](skills/mysql-tools) | MySQL | `pip install pymysql` |
| [mssql-tools](skills/mssql-tools) | SQL Server | `pip install pymssql` |
| [dm8-tools](skills/dm8-tools) | DM8 (达梦) | `pip install jaydebeapi JPype1` |
| [postgresql-tools](skills/postgresql-tools) | PostgreSQL | `pip install psycopg2` |
| [sqlite-tools](skills/sqlite-tools) | SQLite | Không cần cài (built-in Python) |

## Cấu trúc mỗi skill

```
skill-name/
├── SKILL.md              # File chính của skill (hướng dẫn sử dụng)
├── scripts/              # Các script Python
│   ├── *_connect.py      # Kiểm tra kết nối
│   ├── *_tables.py       # Liệt kê tất cả bảng
│   ├── *_schema.py       # Xem cấu trúc bảng
│   ├── *_query.py        # Thực thi SQL query
│   └── *_info.py         # Thông tin database
├── references/           # Tài liệu tham khảo SQL
└── assets/               # Driver và tài nguyên (nếu có)
```

## Cách sử dụng

### Cách 1: Dùng trực tiếp script

```bash
# Clone repo
git clone https://github.com/huangzt/my-agent-skills.git

# Cài đặt phụ thuộc (ví dụ MySQL)
pip install pymysql

# Chạy script
python skills/mysql-tools/scripts/mysql_connect.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

## Hỗ trợ nền tảng

- ✅ Windows
- ✅ macOS
- ✅ Linux

## Giấy phép

[MIT License](LICENSE) - Tự do sử dụng, chỉnh sửa và phân phối.
