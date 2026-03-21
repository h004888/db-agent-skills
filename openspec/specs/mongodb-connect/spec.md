## ADDED Requirements

### Requirement: Connection Test
The script must successfully connect to a MongoDB instance and verify connectivity.

#### Scenario: Successful Connection
- **WHEN** Valid connection parameters (host, port, username, password, database) are provided
- **THEN** Return success=true with server version and connection metadata

#### Scenario: Failed Connection - Invalid Credentials
- **WHEN** Invalid username or password is provided
- **THEN** Return success=false with authentication error message

#### Scenario: Failed Connection - Host Unreachable
- **WHEN** MongoDB server is not reachable at provided host:port
- **THEN** Return success=false with connection timeout error

### Requirement: Connection with URI
The script must support MongoDB connection string format.

#### Scenario: Connection via URI
- **WHEN** `--uri` option is provided with valid mongodb:// or mongodb+srv:// connection string
- **THEN** Parse URI and establish connection

### Requirement: Ping Operation
The script must support a quick ping operation to test connectivity.

#### Scenario: Ping Test
- **WHEN** `--ping` flag is provided
- **THEN** Execute `db.admin().ping()` and return result

### Requirement: Output Format
The script must return JSON output in consistent format.

#### Scenario: Success Output
- **WHEN** Connection succeeds
- **THEN** Return JSON with success, data (host, port, database, server_version, ping), and message

#### Scenario: Failure Output
- **WHEN** Connection fails
- **THEN** Return JSON with success=false, error message, and message
