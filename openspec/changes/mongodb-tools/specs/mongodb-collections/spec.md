## ADDED Requirements

### Requirement: List Collections
The script SHALL retrieve and display all collections in the specified database.

#### Scenario: List All User Collections
- **WHEN** Connected to a database with collections
- **THEN** Return list of collection names with document counts

#### Scenario: Include System Collections
- **WHEN** `--all` flag is provided
- **THEN** Include system collections (starting with `system.`) in the list

#### Scenario: Empty Database
- **WHEN** Database has no collections
- **THEN** Return empty list with collection_count=0

### Requirement: Collection Metadata
The script SHALL return useful metadata for each collection.

#### Scenario: Collection with Metadata
- **WHEN** Listing collections
- **THEN** Return for each collection: name, type, document_count

### Requirement: Output Format
The script SHALL return JSON output in consistent format.

#### Scenario: Success Output
- **WHEN** Successfully retrieved collection list
- **THEN** Return JSON with success, data (database, collection_count, collections array), and message
