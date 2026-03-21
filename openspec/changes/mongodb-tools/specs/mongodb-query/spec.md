## ADDED Requirements

### Requirement: Find Operations
The script SHALL support MongoDB find queries.

#### Scenario: Basic Find
- **WHEN** Query is a simple find (no aggregation)
- **THEN** Execute `db.collection.find(query)` and return results

#### Scenario: Find with Projection
- **WHEN** `--fields` option is provided
- **THEN** Apply projection to return only specified fields

#### Scenario: Find with Limit
- **WHEN** `--limit` option is provided
- **THEN** Apply limit to query results

#### Scenario: Find with Sort
- **WHEN** `--sort` option is provided
- **THEN** Apply sort to query results

### Requirement: Aggregate Operations
The script SHALL support MongoDB aggregation pipelines.

#### Scenario: Aggregation Pipeline
- **WHEN** Query starts with `{ $aggregate: [...] }` or detected as aggregation
- **THEN** Execute `db.collection.aggregate(pipeline)`

### Requirement: Write Operations
The script SHALL support insert, update, and delete operations.

#### Scenario: Insert Document
- **WHEN** Query starts with `insertOne` or `insertMany`
- **THEN** Execute insert and return inserted IDs

#### Scenario: Update Documents
- **WHEN** Query starts with `updateOne`, `updateMany`, or `findOneAndUpdate`
- **THEN** Execute update and return matched/affected count

#### Scenario: Delete Documents
- **WHEN** Query starts with `deleteOne`, `deleteMany`, or `findOneAndDelete`
- **THEN** Execute delete and return deleted count

### Requirement: Read-Only Mode
The script SHALL support a read-only mode that blocks write operations.

#### Scenario: Read-Only Blocks Writes
- **WHEN** `--readonly` flag is provided with write query
- **THEN** Return error: "Write operations not allowed in read-only mode"

#### Scenario: Read-Only Allows Reads
- **WHEN** `--readonly` flag is provided with read query
- **THEN** Execute find/aggregate normally

### Requirement: BSON Type Serialization
The script SHALL serialize BSON types to JSON-compatible formats.

#### Scenario: ObjectId Serialization
- **WHEN** Document contains ObjectId
- **THEN** Convert to string `$oid: "..."`

#### Scenario: ISODate Serialization
- **WHEN** Document contains ISODate
- **THEN** Convert to string `$date: "ISO-8601"`

### Requirement: Output Format
The script SHALL return JSON output in consistent format.

#### Scenario: Find/Aggregate Success
- **WHEN** Query returns documents
- **THEN** Return JSON with success, data (operation, collection, row_count, columns, rows), and message

#### Scenario: Write Success
- **WHEN** Insert, update, or delete succeeds
- **THEN** Return JSON with success, data (operation, affected_rows, inserted_ids), and message
