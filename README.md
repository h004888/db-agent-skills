# My Agent Skills

[![GitHub stars](https://img.shields.io/github/stars/huangzt/my-agent-skills.svg)](https://github.com/huangzt/my-agent-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/huangzt/my-agent-skills.svg)](https://github.com/huangzt/my-agent-skills/network)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

[English](README_EN.md)

为 AI 代理提供的数据库工具技能集，兼容 [OpenSkills](https://github.com/numman-ali/openskills) 系统。

## 包含的技能

| 技能 | 数据库 | 依赖 |
|------|--------|------|
| [mysql-tools](skills/mysql-tools) | MySQL | `pip install pymysql` |
| [mssql-tools](skills/mssql-tools) | SQL Server | `pip install pymssql` |
| [dm8-tools](skills/dm8-tools) | 达梦 DM8 | `pip install jaydebeapi JPype1` |
| [sqlite-tools](skills/sqlite-tools) | SQLite | 无需安装（Python 内置） |

## 每个技能包含

```
skill-name/
├── SKILL.md              # 技能主文件（使用说明）
├── scripts/              # Python 工具脚本
│   ├── *_connect.py      # 连接测试
│   ├── *_tables.py       # 列出所有表
│   ├── *_schema.py       # 查看表结构
│   ├── *_query.py        # 执行 SQL 查询
│   └── *_info.py         # 数据库信息
├── references/           # SQL 参考文档
└── assets/               # 驱动等资源（如有）
```

## 使用方式

### 方式一：配合 OpenSkills 使用

```bash
# 安装 OpenSkills
npm i -g openskills

# 安装技能
openskills install huangzt/my-agent-skills

# 同步到 AGENTS.md
openskills sync
```

### 方式二：直接使用脚本

```bash
# 克隆仓库
git clone https://github.com/huangzt/my-agent-skills.git

# 安装依赖（以 MySQL 为例）
pip install mysql-connector-python

# 使用脚本
python skills/mysql-tools/scripts/mysql_connect.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

## 平台支持

- ✅ Windows
- ✅ macOS
- ✅ Linux

## 许可证

[MIT License](LICENSE) - 您可以自由使用、修改和分发本项目。
