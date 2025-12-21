# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do NOT** create a public GitHub issue
2. Send a private email to the maintainer with details
3. Include steps to reproduce the vulnerability
4. Wait for a response before disclosing publicly

## Security Considerations

### Database Credentials

- Never commit database passwords to version control
- Use environment variables or secure credential management
- The `--password` parameter is visible in process lists; consider using environment variables for sensitive environments

### SQL Injection

- The `*_query.py` scripts execute arbitrary SQL
- Use proper input validation when integrating with other systems
- Never pass untrusted user input directly to the `--query` parameter

### File Access

- SQLite tools access local files directly
- Ensure proper file permissions on database files
- Use `--readonly` flag when write access is not needed

## Best Practices

1. Use read-only connections when possible
2. Restrict database user permissions to minimum required
3. Audit SQL queries before execution
4. Keep Python dependencies updated
