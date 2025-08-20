---
title: 3.2 Supported Features and Syntax
titleSuffix: Azure Cosmos DB for MongoDB
description: Discover supported features and syntax in Azure Cosmos DB for MongoDB 3.2, including database commands, query language, and aggregation pipeline. Explore benefits and get started today.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: release-notes
ms.date: 08/20/2025
appliesto:
  - ✅ MongoDB
---

# Supported features and syntax in Azure Cosmos DB for MongoDB 3.2 server version

Azure Cosmos DB for MongoDB 3.2 enables you to use familiar MongoDB features with enterprise-grade capabilities such as global distribution, automatic sharding, and high availability. This article describes the supported features, syntax, and benefits of using Azure Cosmos DB for MongoDB 3.2.

> [!IMPORTANT]
> Version 3.2 of the Azure Cosmos DB for MongoDB has no current plans for end-of-support. The minimum notice for a future end-of-support is three years.

## Protocol Support

All new accounts for Azure Cosmos DB for MongoDB are compatible with MongoDB server version **3.6**. This article covers MongoDB version 3.2. The supported operators and any limitations or exceptions are listed here. Any client driver that understands these protocols should be able to connect to Azure Cosmos DB for MongoDB.

Azure Cosmos DB for MongoDB also offers a seamless upgrade experience for qualifying accounts. Learn more on the [MongoDB version upgrade guide](upgrade-version.md).

## Query language support

Azure Cosmos DB for MongoDB provides comprehensive support for MongoDB query language constructs. Here you can find the detailed list of currently supported operations, operators, stages, commands, and options.

## Database commands

Azure Cosmos DB for MongoDB supports the following database commands:

> [!NOTE]
> This article only lists the supported server commands and excludes client-side wrapper functions. Client-side wrapper functions such as `deleteMany()` and `updateMany()` internally utilize the `delete()` and `update()` server commands. Functions utilizing supported server commands are compatible with Azure Cosmos DB for MongoDB.

### Query and write operation commands

- `delete`
- `find`
- `findAndModify`
- `getLastError`
- `getMore`
- `insert`
- `update`

### Authentication commands

- `logout`
- `authenticate`
- `getnonce`

### Administration commands

- `dropDatabase`
- `listCollections`
- `drop`
- `create`
- `filemd5`
- `createIndexes`
- `listIndexes`
- `dropIndexes`
- `connectionStatus`
- `reIndex`

### Diagnostics commands

- `buildInfo`
- `collStats`
- `dbStats`
- `hostInfo`
- `listDatabases`
- `whatsmyuri`

<a name="aggregation-pipeline"></a>

## Aggregation pipeline</a>

### Aggregation commands

- `aggregate`
- `count`
- `distinct`

### Aggregation stages

- `$project`
- `$match`
- `$limit`
- `$skip`
- `$unwind`
- `$group`
- `$sample`
- `$sort`
- `$lookup`
- `$out`
- `$count`
- `$addFields`

### Aggregation expressions

#### Boolean expressions

- `$and`
- `$or`
- `$not`

#### Set expressions

- `$setEquals`
- `$setIntersection`
- `$setUnion`
- `$setDifference`
- `$setIsSubset`
- `$anyElementTrue`
- `$allElementsTrue`

#### Comparison expressions

- `$cmp`
- `$eq`
- `$gt`
- `$gte`
- `$lt`
- `$lte`
- `$ne`

#### Arithmetic expressions

- `$abs`
- `$add`
- `$ceil`
- `$divide`
- `$exp`
- `$floor`
- `$ln`
- `$log`
- `$log10`
- `$mod`
- `$multiply`
- `$pow`
- `$sqrt`
- `$subtract`
- `$trunc`

#### String expressions

- `$concat`
- `$indexOfBytes`
- `$indexOfCP`
- `$split`
- `$strLenBytes`
- `$strLenCP`
- `$strcasecmp`
- `$substr`
- `$substrBytes`
- `$substrCP`
- `$toLower`
- `$toUpper`

#### Array expressions

- `$arrayElemAt`
- `$concatArrays`
- `$filter`
- `$indexOfArray`
- `$isArray`
- `$range`
- `$reverseArray`
- `$size`
- `$slice`
- `$in`

#### Date expressions

- `$dayOfYear`
- `$dayOfMonth`
- `$dayOfWeek`
- `$year`
- `$month`
- `$week`
- `$hour`
- `$minute`
- `$second`
- `$millisecond`
- `$isoDayOfWeek`
- `$isoWeek`

#### Conditional expressions

- `$cond`
- `$ifNull`

## Aggregation accumulators

- `$sum`
- `$avg`
- `$first`
- `$last`
- `$max`
- `$min`
- `$push`
- `$addToSet`

## Operators

Following operators are supported with corresponding examples of their use. Consider this sample document used in the queries below:

```json
{
  "Volcano Name": "Rainier",
  "Country": "United States",
  "Region": "US-Washington",
  "Location": {
    "type": "Point",
    "coordinates": [
      -121.758,
      46.87
    ]
  },
  "Elevation": 4392,
  "Type": "Stratovolcano",
  "Status": "Dendrochronology",
  "Last Known Eruption": "Last known eruption from 1800-1899, inclusive"
}
```

| Operator | Example |
| --- | --- |
| `eq` | `{ "Volcano Name": { $eq: "Rainier" } }` |
| `gt` | `{ "Elevation": { $gt: 4000 } }` |
| `gte` | `{ "Elevation": { $gte: 4392 } }` |
| `lt` | `{ "Elevation": { $lt: 5000 } }` |
| `lte` | `{ "Elevation": { $lte: 5000 } }` |
| `ne` | `{ "Elevation": { $ne: 1 } }` |
| `in` | `{ "Volcano Name": { $in: ["St. Helens", "Rainier", "Glacier Peak"] } }` |
| `nin` | `{ "Volcano Name": { $nin: ["Lassen Peak", "Hood", "Baker"] } }` |
| `or` | `{ $or: [ { Elevation: { $lt: 4000 } }, { "Volcano Name": "Rainier" } ] }` |
| `and` | `{ $and: [ { Elevation: { $gt: 4000 } }, { "Volcano Name": "Rainier" } ] }` |
| `not` | `{ "Elevation": { $not: { $gt: 5000 } } }`|
| `nor` | `{ $nor: [ { "Elevation": { $lt: 4000 } }, { "Volcano Name": "Baker" } ] }` |
| `exists` | `{ "Status": { $exists: true } }`|
| `type` | `{ "Status": { $type: "string" } }`|
| `mod` | `{ "Elevation": { $mod: [ 4, 0 ] } }` |
| `regex` | `{ "Volcano Name": { $regex: "^Rain"} }`|

### Notes

In the $regex queries, left-anchored expressions allow index search. However, using 'i' modifier (case-insensitivity) and 'm' modifier (multiline) causes the collection scan in all expressions.

When there's a need to include `$` or `|`, it's best to create two (or more) regex queries. For example, given the following original query: `find({x:{$regex: /^abc$/})`, it has to be modified as follows:

```mongodb
find({x:{$regex: /^abc/, x:{$regex:/^abc$/}})
```

The first part uses the index to restrict the search to those documents beginning with `^abc` and the second part matches the exact entries. The bar operator `|` acts as an "or" function - the query `find({x:{$regex: /^abc |^def/})` matches the documents in which field `x` has values that begin with `"abc"` or `"def"`. To utilize the index, break the query into two different queries joined by the $or operator: `find( {$or : [{x: $regex: /^abc/}, {$regex: /^def/}] })`.

### Update operators

#### Field update operators

- `$inc`
- `$mul`
- `$rename`
- `$setOnInsert`
- `$set`
- `$unset`
- `$min`
- `$max`
- `$currentDate`

#### Array update operators

- `$addToSet`
- `$pop`
- `$pullAll`
- `$pull`  (Note: $pull with condition isn't supported)
- `$pushAll`
- `$push`
- `$each`
- `$slice`
- `$sort`
- `$position`

#### Bitwise update operator

- `$bit`

### Geospatial operators

| Operator | Example | Supported |
| --- | --- | --- |
| `$geoWithin` | `{ "Location.coordinates": { $geoWithin: { $centerSphere: [ [ -121, 46 ], 5 ] } } }` | Yes |
| `$geoIntersects` |  `{ "Location.coordinates": { $geoIntersects: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` | Yes |
| `$near` | `{ "Location.coordinates": { $near: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` | Yes |
| `$nearSphere` | `{ "Location.coordinates": { $nearSphere : [ -121, 46  ], $maxDistance: 0.50 } }` | Yes |
| `$geometry` | `{ "Location.coordinates": { $geoWithin: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` | Yes |
| `$minDistance` | `{ "Location.coordinates": { $nearSphere : { $geometry: {type: "Point", coordinates: [ -121, 46 ]}, $minDistance: 1000, $maxDistance: 1000000 } } }` | Yes |
| `$maxDistance` | `{ "Location.coordinates": { $nearSphere : [ -121, 46  ], $maxDistance: 0.50 } }` | Yes |
| `$center` | `{ "Location.coordinates": { $geoWithin: { $center: [ [-121, 46], 1 ] } } }` | Yes |
| `$centerSphere` | `{ "Location.coordinates": { $geoWithin: { $centerSphere: [ [ -121, 46 ], 5 ] } } }` | Yes |
| `$box` | `{ "Location.coordinates": { $geoWithin: { $box:  [ [ 0, 0 ], [ -122, 47 ] ] } } }` | Yes |
| `$polygon` | `{ "Location.coordinates": { $near: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` | Yes |

## Sort Operations

When you use the `findOneAndUpdate` operation, sort operations on a single field are supported, but sort operations on multiple fields aren't supported.

## Other operators

| Operator | Example | Notes
| --- | --- | --- |
| `$all` | `{ "Location.coordinates": { $all: [-121.758, 46.87] } }` |
| `$elemMatch` | `{ "Location.coordinates": { $elemMatch: {  $lt: 0 } } }` |
| `$size` | `{ "Location.coordinates": { $size: 2 } }` |
| `$comment` |  `{ "Location.coordinates": { $elemMatch: {  $lt: 0 } }, $comment: "Negative values"}` |
| `$text` |  | Not supported. Use $regex instead.

## Unsupported operators

The `$where` and the `$eval` operators aren't supported by Azure Cosmos DB.

### Methods

Following methods are supported:

#### Cursor methods

| Method | Example | Notes |
| --- | --- | --- |
| `cursor.sort()` | `cursor.sort({ "Elevation": -1 })` | Documents without sort key don't get returned |

## Unique indexes

Azure Cosmos DB indexes every field in documents that are written to the database by default. Unique indexes ensure that a specific field doesn't have duplicate values across all documents in a collection, similar to the way uniqueness is preserved on the default `_id` key. You can create custom indexes in Azure Cosmos DB by using the createIndex command, including the 'unique' constraint.

Unique indexes are available for all Azure Cosmos DB accounts using Azure Cosmos DB for MongoDB.

## Time-to-live (TTL)

Azure Cosmos DB only supports a time-to-live (TTL) at the collection level (_ts) in version 3.2. Upgrade to versions 3.6+ to take advantage of other forms of [TTL](time-to-live.md).  

## User and role management

Azure Cosmos DB doesn't yet support users and roles. However, Azure Cosmos DB supports Azure role-based access control (Azure RBAC) and read-write and read-only passwords/keys that can be obtained through the [Azure portal](https://portal.azure.com) (Connection String page).

## Replication

Azure Cosmos DB supports automatic, native replication at the lowest layers. This logic is extended out to achieve low-latency, global replication as well. Azure Cosmos DB doesn't support manual replication commands.

## Write Concern

Some applications rely on a [Write Concern](https://docs.mongodb.com/manual/reference/write-concern/) that specifies the number of responses required during a write operation. Due to how Azure Cosmos DB handles replication in the background all writes are automatically Quorum by default. Any write concern specified by the client code is ignored. Learn more in [Using consistency levels to maximize availability and performance](../consistency-levels.md).

## Sharding

Azure Cosmos DB supports automatic, server-side sharding. It manages shard creation, placement, and balancing automatically. Azure Cosmos DB doesn't support manual sharding commands, which means you don't have to invoke commands such as shardCollection, addShard, balancerStart, moveChunk etc. You only need to specify the shard key while creating the containers or querying the data.
