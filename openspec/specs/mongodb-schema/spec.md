## ADDED Requirements

### Requirement: Schema Inference
MongoDB is schemaless, so the script must infer schema from sample documents.

#### Scenario: Basic Schema Inference
- **WHEN** `get_collection_schema()` is called on a collection
- **THEN** Sample N documents and extract field names and BSON types

#### Scenario: Deep Schema Analysis
- **WHEN** `--deep` flag is provided
- **THEN** Use aggregation pipeline to analyze 100+ documents for field presence statistics

### Requirement: Field Type Detection
The script must correctly identify BSON field types.

#### Scenario: Primitive Types
- **WHEN** Field value is a primitive type (string, number, boolean, null)
- **THEN** Return BSON type: string, int, long, double, boolean, null

#### Scenario: Date Types
- **WHEN** Field value is a date (ISODate)
- **THEN** Return BSON type: date

#### Scenario: ObjectId
- **WHEN** Field value is an ObjectId
- **THEN** Return BSON type: objectId

#### Scenario: Embedded Documents
- **WHEN** Field value is an embedded document (nested object)
- **THEN** Return BSON type: object with nested field structure

#### Scenario: Arrays
- **WHEN** Field value is an array
- **THEN** Return BSON type: array with element type if homogeneous

### Requirement: Sample Documents
The script must return actual sample documents for reference.

#### Scenario: Return Sample Documents
- **WHEN** Schema is requested
- **THEN** Include 1-3 sample documents in the output

### Requirement: Output Format
The script must return JSON output in consistent format.

#### Scenario: Success Output
- **WHEN** Schema inference succeeds
- **THEN** Return JSON with success, data (collection, sample_size, fields, sample_documents), and message
