# My Agent Skills

[Vietnamese](README.md)

## Included Skills

| Skill | Database | Dependency |
|-------|----------|------------|
| [mysql-tools](skills/mysql-tools) | MySQL | `pip install pymysql` |
| [mssql-tools](skills/mssql-tools) | SQL Server | `pip install pymssql` |
| [dm8-tools](skills/dm8-tools) | DM8 (Dameng) | `pip install jaydebeapi JPype1` |
| [postgresql-tools](skills/postgresql-tools) | PostgreSQL | `pip install psycopg2` |
| [mongodb-tools](skills/mongodb-tools) | MongoDB | `pip install pymongo` |
| [sqlite-tools](skills/sqlite-tools) | SQLite | Built-in (no install needed) |

## Each Skill Contains

```
skill-name/
├── SKILL.md              # Main skill file (instructions)
├── scripts/              # Python utility scripts
│   ├── *_connect.py      # Connection test
│   ├── *_tables.py       # List all tables
│   ├── *_schema.py       # View table schema
│   ├── *_query.py        # Execute SQL queries
│   └── *_info.py         # Database info
├── references/           # SQL reference docs
└── assets/               # Drivers and resources (if any)
```

## Usage

### Option 1: Direct Script Usage

```bash
# Clone repository
git clone https://github.com/huangzt/my-agent-skills.git

# Install dependency (MySQL example)
pip install pymysql

# Use scripts
python skills/mysql-tools/scripts/mysql_connect.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

## Platform Support

- ✅ Windows
- ✅ macOS
- ✅ Linux

## License

[MIT License](LICENSE) - Free to use, modify, and distribute.
