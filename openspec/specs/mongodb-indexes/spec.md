## ADDED Requirements

### Requirement: List Indexes
The script must retrieve all indexes defined on a collection.

#### Scenario: List All Indexes
- **WHEN** `list_indexes()` is called for a collection
- **THEN** Return all indexes including `_id` (default) and user-created indexes

#### Scenario: Empty Collection
- **WHEN** Collection has no user-defined indexes (only `_id`)
- **THEN** Return only the `_id_` index

### Requirement: Index Metadata
For each index, return useful metadata.

#### Scenario: Index Properties
- **WHEN** Listing indexes
- **THEN** Return for each index: name, keys, unique, sparse, ttl, background

### Requirement: Index Types
The script must identify different index types.

#### Scenario: Index Types Detection
- **WHEN** Index has special properties
- **THEN** Identify: unique, sparse, ttl, text, 2dsphere, 2d, hashed

### Requirement: Output Format
The script must return JSON output in consistent format.

#### Scenario: Success Output
- **WHEN** Index listing succeeds
- **THEN** Return JSON with success, data (collection, index_count, indexes array), and message
