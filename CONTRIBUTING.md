# Contributing to My Agent Skills

感谢您对本项目的兴趣！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请 [创建 Issue](https://github.com/huangzt/my-agent-skills/issues/new)。

### 提交代码

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 添加新的数据库 Skill

1. 在 `skills/` 目录下创建新的技能目录
2. 遵循现有技能的目录结构：
   ```
   new-db-tools/
   ├── SKILL.md
   ├── scripts/
   │   ├── *_connect.py
   │   ├── *_tables.py
   │   ├── *_schema.py
   │   ├── *_query.py
   │   └── *_info.py
   └── references/
       └── common_queries.md
   ```
3. 确保脚本输出 JSON 格式
4. 测试跨平台兼容性

## 代码规范

- Python 脚本使用 UTF-8 编码
- 输出使用 JSON 格式
- 错误处理要完整
- 支持跨平台（Windows/macOS/Linux）

## 许可证

贡献的代码将采用 [MIT License](LICENSE)。
