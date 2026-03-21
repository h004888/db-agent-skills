# MongoDB Common Queries Reference

## Find Operations

### Basic Find
```javascript
db.users.find({})
db.users.findOne({})
```

### Find with Filter
```javascript
db.users.find({age: {"$gte": 18}})
db.users.find({name: "John", age: {"$gte": 18}})
```

### Find with Projection
```javascript
db.users.find({}, {name: 1, email: 1})
db.users.find({}, {password: 0})
```

### Find with Limit and Skip
```javascript
db.users.find({}).limit(10)
db.users.find({}).skip(20).limit(10)
```

### Find with Sort
```javascript
db.users.find({}).sort({name: 1})
db.users.find({}).sort({age: -1, name: 1})
```

## Query Operators

### Comparison Operators
```javascript
{"$eq": value}      // Equal
{"$ne": value}      // Not equal
{"$gt": value}      // Greater than
{"$gte": value}     // Greater than or equal
{"$lt": value}      // Less than
{"$lte": value}     // Less than or equal
{"$in": [a, b]}     // In array
{"$nin": [a, b]}    // Not in array
```

### Logical Operators
```javascript
{"$and": [{condition1}, {condition2}]}
{"$or": [{condition1}, {condition2}]}
{"$not": {field: {"$operator": value}}}
{"$nor": [{condition1}, {condition2}]}
```

### Element Operators
```javascript
{"$exists": true}                    // Field exists
{"$exists": false}                   // Field doesn't exist
{"$type": "string"}                  // Field type
{"$type": "objectId"}                // ObjectId type
```

### String Operators
```javascript
{"$regex": "pattern"}
{"$regex": "^John"}
{"$options": "i"}  // Case insensitive
```

### Array Operators
```javascript
{"$in": [value1, value2]}           // Value in array
{"$all": [value1, value2]}           // Contains all
{"$size": 3}                         // Array size
```

## Insert Operations

### Insert One Document
```javascript
db.users.insertOne({
  name: "John",
  email: "john@example.com",
  age: 25
})
```

### Insert Many Documents
```javascript
db.users.insertMany([
  {name: "John", email: "john@example.com"},
  {name: "Jane", email: "jane@example.com"}
])
```

## Update Operations

### Update One
```javascript
db.users.updateOne(
  {name: "John"},
  {"$set": {age: 26}}
)
```

### Update Many
```javascript
db.users.updateMany(
  {status: "inactive"},
  {"$set": {status: "archived"}}
)
```

### Update with Increment
```javascript
db.users.updateOne(
  {name: "John"},
  {"$inc": {age: 1}}
)
```

### Update with Array Push
```javascript
db.users.updateOne(
  {name: "John"},
  {"$push": {tags: "premium"}}
)
```

### Update with Array Pull (Remove)
```javascript
db.users.updateOne(
  {name: "John"},
  {"$pull": {tags: "premium"}}
)
```

### FindOneAndUpdate
```javascript
db.users.findOneAndUpdate(
  {name: "John"},
  {"$set": {age: 27}},
  {returnNewDocument: true}
)
```

## Delete Operations

### Delete One
```javascript
db.users.deleteOne({name: "John"})
```

### Delete Many
```javascript
db.users.deleteMany({status: "inactive"})
```

## Aggregation Pipeline

### Basic Aggregation
```javascript
db.orders.aggregate([
  {$match: {status: "completed"}},
  {$group: {_id: "$customer", total: {$sum: "$amount"}}},
  {$sort: {total: -1}},
  {$limit: 10}
])
```

### Count Documents
```javascript
db.orders.aggregate([
  {$match: {status: "completed"}},
  {$count: "completed_orders"}
])
```

### Average Calculation
```javascript
db.orders.aggregate([
  {$group: {
    _id: "$customer",
    avgAmount: {$avg: "$amount"}
  }}
])
```

### Lookup (Join)
```javascript
db.orders.aggregate([
  {$lookup: {
    from: "users",
    localField: "customerId",
    foreignField: "_id",
    as: "customer_info"
  }}
])
```

## Index Management

### Create Index
```javascript
db.users.createIndex({email: 1}, {unique: true})
db.users.createIndex({name: "text", bio: "text"})
```

### Create Compound Index
```javascript
db.users.createIndex({lastName: 1, firstName: 1})
```

### Create Geospatial Index
```javascript
db.places.createIndex({location: "2dsphere"})
```

### Drop Index
```javascript
db.users.dropIndex("email_1")
db.users.dropIndexes()  // Drop all non-default indexes
```

### List Indexes
```javascript
db.users.getIndexes()
```

## Common Tasks

### Duplicate Documents
```javascript
db.users.aggregate([
  {$group: {
    _id: "$email",
    count: {$sum: 1},
    docs: {$push: "$_id"}
  }},
  {$match: {count: {$gt: 1}}}
])
```

### Update Embedded Document
```javascript
db.users.updateOne(
  {name: "John"},
  {"$set": {"address.city": "New York"}}
)
```

### Rename Field
```javascript
db.users.updateMany({}, {$rename: {"oldname": "newname"}})
```

### Remove Field
```javascript
db.users.updateMany({}, {$unset: {tempField: ""}})
```

### Check Collection Size
```javascript
db.users.stats()
db.users.countDocuments({})
```
