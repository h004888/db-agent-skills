# My Agent Skills

[中文](README.md)

A collection of database utility skills for AI agents, compatible with [OpenSkills](https://github.com/numman-ali/openskills) system.

## Included Skills

| Skill | Database | Dependency |
|-------|----------|------------|
| [mysql-tools](skills/mysql-tools) | MySQL | `pip install mysql-connector-python` |
| [mssql-tools](skills/mssql-tools) | SQL Server | `pip install pymssql` |
| [dm8-tools](skills/dm8-tools) | Dameng DM8 | `pip install jaydebeapi JPype1` |
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

### Option 1: With OpenSkills

```bash
# Install OpenSkills
npm i -g openskills

# Install skills
openskills install huangzt/my-agent-skills

# Sync to AGENTS.md
openskills sync
```

### Option 2: Direct Script Usage

```bash
# Clone repository
git clone https://github.com/huangzt/my-agent-skills.git

# Install dependency (MySQL example)
pip install mysql-connector-python

# Use scripts
python skills/mysql-tools/scripts/mysql_connect.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

## Platform Support

- ✅ Windows
- ✅ macOS
- ✅ Linux

## License

Apache-2.0
