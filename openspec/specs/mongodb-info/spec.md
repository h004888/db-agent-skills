## ADDED Requirements

### Requirement: Database Stats
The script must return statistics about the database.

#### Scenario: Database Statistics
- **WHEN** `get_database_info()` is called
- **THEN** Return: Database name, Collections count, Documents count, Total size, Index size, Storage size

### Requirement: Server Status
The script must return MongoDB server status information.

#### Scenario: Basic Server Status
- **WHEN** Connected to MongoDB server
- **THEN** Return: Server version, Process (mongos or mongod), Uptime, Connections current

#### Scenario: Detailed Server Status
- **WHEN** `--detailed` flag is provided
- **THEN** Return full `serverStatus()` output including memory, network stats, storage engine, OpCounters

### Requirement: Collection Statistics
The script must support getting stats for specific collections.

#### Scenario: Collection Stats
- **WHEN** `--collection` option is provided
- **THEN** Return `db.collection.stats()` output

### Requirement: Output Format
The script must return JSON output in consistent format.

#### Scenario: Success Output
- **WHEN** Information retrieval succeeds
- **THEN** Return JSON with success, data (database, collections, documents, database_size_*, index_size_*, server_info), and message
