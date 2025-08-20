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

| | Supported |
| --- | --- |
| **`delete`** | ✅ Yes |
| **`find`** | ✅ Yes |
| **`findAndModify`** | ✅ Yes |
| **`getLastError`** | ✅ Yes |
| **`getMore`** | ✅ Yes |
| **`insert`** | ✅ Yes |
| **`update`** | ✅ Yes |

### Authentication commands

| | Supported |
| --- | --- |
| **`logout`** | ✅ Yes |
| **`authenticate`** | ✅ Yes |
| **`getnonce`** | ✅ Yes |

### Administration commands

| | Supported |
| --- | --- |
| **`dropDatabase`** | ✅ Yes |
| **`listCollections`** | ✅ Yes |
| **`drop`** | ✅ Yes |
| **`create`** | ✅ Yes |
| **`filemd5`** | ✅ Yes |
| **`createIndexes`** | ✅ Yes |
| **`listIndexes`** | ✅ Yes |
| **`dropIndexes`** | ✅ Yes |
| **`connectionStatus`** | ✅ Yes |
| **`reIndex`** | ✅ Yes |

### Diagnostics commands

| | Supported |
| --- | --- |
| **`buildInfo`** | ✅ Yes |
| **`collStats`** | ✅ Yes |
| **`dbStats`** | ✅ Yes |
| **`hostInfo`** | ✅ Yes |
| **`listDatabases`** | ✅ Yes |
| **`whatsmyuri`** | ✅ Yes |

<a name="aggregation-pipeline"></a>

## Aggregation pipeline</a>

### Aggregation commands

| | Supported |
| --- | --- |
| **`aggregate`** | ✅ Yes |
| **`count`** | ✅ Yes |
| **`distinct`** | ✅ Yes |

### Aggregation stages

| | Supported |
| --- | --- |
| **`$project`** | ✅ Yes |
| **`$match`** | ✅ Yes |
| **`$limit`** | ✅ Yes |
| **`$skip`** | ✅ Yes |
| **`$unwind`** | ✅ Yes |
| **`$group`** | ✅ Yes |
| **`$sample`** | ✅ Yes |
| **`$sort`** | ✅ Yes |
| **`$lookup`** | ✅ Yes |
| **`$out`** | ✅ Yes |
| **`$count`** | ✅ Yes |
| **`$addFields`** | ✅ Yes |

### Aggregation expressions

#### Boolean expressions

| | Supported |
| --- | --- |
| **`$and`** | ✅ Yes |
| **`$or`** | ✅ Yes |
| **`$not`** | ✅ Yes |

#### Set expressions

| | Supported |
| --- | --- |
| **`$setEquals`** | ✅ Yes |
| **`$setIntersection`** | ✅ Yes |
| **`$setUnion`** | ✅ Yes |
| **`$setDifference`** | ✅ Yes |
| **`$setIsSubset`** | ✅ Yes |
| **`$anyElementTrue`** | ✅ Yes |
| **`$allElementsTrue`** | ✅ Yes |

#### Comparison expressions

| | Supported |
| --- | --- |
| **`$cmp`** | ✅ Yes |
| **`$eq`** | ✅ Yes |
| **`$gt`** | ✅ Yes |
| **`$gte`** | ✅ Yes |
| **`$lt`** | ✅ Yes |
| **`$lte`** | ✅ Yes |
| **`$ne`** | ✅ Yes |

#### Arithmetic expressions

| | Supported |
| --- | --- |
| **`$abs`** | ✅ Yes |
| **`$add`** | ✅ Yes |
| **`$ceil`** | ✅ Yes |
| **`$divide`** | ✅ Yes |
| **`$exp`** | ✅ Yes |
| **`$floor`** | ✅ Yes |
| **`$ln`** | ✅ Yes |
| **`$log`** | ✅ Yes |
| **`$log10`** | ✅ Yes |
| **`$mod`** | ✅ Yes |
| **`$multiply`** | ✅ Yes |
| **`$pow`** | ✅ Yes |
| **`$sqrt`** | ✅ Yes |
| **`$subtract`** | ✅ Yes |
| **`$trunc`** | ✅ Yes |

#### String expressions

| | Supported |
| --- | --- |
| **`$concat`** | ✅ Yes |
| **`$indexOfBytes`** | ✅ Yes |
| **`$indexOfCP`** | ✅ Yes |
| **`$split`** | ✅ Yes |
| **`$strLenBytes`** | ✅ Yes |
| **`$strLenCP`** | ✅ Yes |
| **`$strcasecmp`** | ✅ Yes |
| **`$substr`** | ✅ Yes |
| **`$substrBytes`** | ✅ Yes |
| **`$substrCP`** | ✅ Yes |
| **`$toLower`** | ✅ Yes |
| **`$toUpper`** | ✅ Yes |

#### Array expressions

| | Supported |
| --- | --- |
| **`$arrayElemAt`** | ✅ Yes |
| **`$concatArrays`** | ✅ Yes |
| **`$filter`** | ✅ Yes |
| **`$indexOfArray`** | ✅ Yes |
| **`$isArray`** | ✅ Yes |
| **`$range`** | ✅ Yes |
| **`$reverseArray`** | ✅ Yes |
| **`$size`** | ✅ Yes |
| **`$slice`** | ✅ Yes |
| **`$in`** | ✅ Yes |

#### Date expressions

| | Supported |
| --- | --- |
| **`$dayOfYear`** | ✅ Yes |
| **`$dayOfMonth`** | ✅ Yes |
| **`$dayOfWeek`** | ✅ Yes |
| **`$year`** | ✅ Yes |
| **`$month`** | ✅ Yes |
| **`$week`** | ✅ Yes |
| **`$hour`** | ✅ Yes |
| **`$minute`** | ✅ Yes |
| **`$second`** | ✅ Yes |
| **`$millisecond`** | ✅ Yes |
| **`$isoDayOfWeek`** | ✅ Yes |
| **`$isoWeek`** | ✅ Yes |

#### Conditional expressions

| | Supported |
| --- | --- |
| **`$cond`** | ✅ Yes |
| **`$ifNull`** | ✅ Yes |

## Aggregation accumulators

| | Supported |
| --- | --- |
| **`$sum`** | ✅ Yes |
| **`$avg`** | ✅ Yes |
| **`$first`** | ✅ Yes |
| **`$last`** | ✅ Yes |
| **`$max`** | ✅ Yes |
| **`$min`** | ✅ Yes |
| **`$push`** | ✅ Yes |
| **`$addToSet`** | ✅ Yes |

## Operators

Following operators are supported with corresponding examples of their use. Consider this sample document used in the queries here:

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

| | Supported | Example |
| --- | --- |
| **`eq`** | ✅ Yes | `{ "Volcano Name": { $eq: "Rainier" } }` |
| **`gt`** | ✅ Yes | `{ "Elevation": { $gt: 4000 } }` |
| **`gte`** | ✅ Yes | `{ "Elevation": { $gte: 4392 } }` |
| **`lt`** | ✅ Yes | `{ "Elevation": { $lt: 5000 } }` |
| **`lte`** | ✅ Yes | `{ "Elevation": { $lte: 5000 } }` |
| **`ne`** | ✅ Yes | `{ "Elevation": { $ne: 1 } }` |
| **`in`** | ✅ Yes | `{ "Volcano Name": { $in: ["St. Helens", "Rainier", "Glacier Peak"] } }` |
| **`nin`** | ✅ Yes | `{ "Volcano Name": { $nin: ["Lassen Peak", "Hood", "Baker"] } }` |
| **`or`** | ✅ Yes | `{ $or: [ { Elevation: { $lt: 4000 } }, { "Volcano Name": "Rainier" } ] }` |
| **`and`** | ✅ Yes | `{ $and: [ { Elevation: { $gt: 4000 } }, { "Volcano Name": "Rainier" } ] }` |
| **`not`** | ✅ Yes | `{ "Elevation": { $not: { $gt: 5000 } } }`|
| **`nor`** | ✅ Yes | `{ $nor: [ { "Elevation": { $lt: 4000 } }, { "Volcano Name": "Baker" } ] }` |
| **`exists`** | ✅ Yes | `{ "Status": { $exists: true } }`|
| **`type`** | ✅ Yes | `{ "Status": { $type: "string" } }`|
| **`mod`** | ✅ Yes | `{ "Elevation": { $mod: [ 4, 0 ] } }` |
| **`regex`** | ✅ Yes | `{ "Volcano Name": { $regex: "^Rain"} }`|

### Notes

In the $regex queries, left-anchored expressions allow index search. However, using 'i' modifier (case-insensitivity) and 'm' modifier (multiline) causes the collection scan in all expressions.

When there's a need to include `$` or `|`, it's best to create two (or more) regex queries. For example, given the following original query: `find({x:{$regex: /^abc$/})`, it has to be modified as follows:

```mongodb
find({x:{$regex: /^abc/, x:{$regex:/^abc$/}})
```

The first part uses the index to restrict the search to those documents beginning with `^abc` and the second part matches the exact entries. The bar operator `|` acts as an "or" function - the query `find({x:{$regex: /^abc |^def/})` matches the documents in which field `x` has values that begin with `"abc"` or `"def"`. To utilize the index, break the query into two different queries joined by the $or operator: `find( {$or : [{x: $regex: /^abc/}, {$regex: /^def/}] })`.

### Update operators

#### Field update operators

| | Supported |
| --- | --- |
| **`$inc`** | ✅ Yes |
| **`$mul`** | ✅ Yes |
| **`$rename`** | ✅ Yes |
| **`$setOnInsert`** | ✅ Yes |
| **`$set`** | ✅ Yes |
| **`$unset`** | ✅ Yes |
| **`$min`** | ✅ Yes |
| **`$max`** | ✅ Yes |
| **`$currentDate`** | ✅ Yes |

#### Array update operators

| | Supported |
| --- | --- |
| **`$addToSet`** | ✅ Yes |
| **`$pop`** | ✅ Yes |
| **`$pullAll`** | ✅ Yes |
| **`$pull`** | ✅ Yes |
| **`$pushAll`** | ✅ Yes |
| **`$push`** | ✅ Yes |
| **`$each`** | ✅ Yes |
| **`$slice`** | ✅ Yes |
| **`$sort`** | ✅ Yes |
| **`$position`** | ✅ Yes |

> [!TIP]
> `$pull` with a condition isn't supported.

#### Bitwise update operator

| | Supported |
| --- | --- |
| **`$bit`** | ✅ Yes |

### Geospatial operators

| | Supported | Example |
| --- | --- | --- |
| **`$geoWithin`** | ✅ Yes | `{ "Location.coordinates": { $geoWithin: { $centerSphere: [ [ -121, 46 ], 5 ] } } }` |
| **`$geoIntersects`** | ✅ Yes |  `{ "Location.coordinates": { $geoIntersects: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` |
| **`$near`** | ✅ Yes | `{ "Location.coordinates": { $near: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` |
| **`$nearSphere`** | ✅ Yes | `{ "Location.coordinates": { $nearSphere : [ -121, 46  ], $maxDistance: 0.50 } }` |
| **`$geometry`** | ✅ Yes | `{ "Location.coordinates": { $geoWithin: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` |
| **`$minDistance`** | ✅ Yes | `{ "Location.coordinates": { $nearSphere : { $geometry: {type: "Point", coordinates: [ -121, 46 ]}, $minDistance: 1000, $maxDistance: 1000000 } } }` |
| **`$maxDistance`** | ✅ Yes | `{ "Location.coordinates": { $nearSphere : [ -121, 46  ], $maxDistance: 0.50 } }` |
| **`$center`** | ✅ Yes | `{ "Location.coordinates": { $geoWithin: { $center: [ [-121, 46], 1 ] } } }` |
| **`$centerSphere`** | ✅ Yes | `{ "Location.coordinates": { $geoWithin: { $centerSphere: [ [ -121, 46 ], 5 ] } } }` |
| **`$box`** | ✅ Yes | `{ "Location.coordinates": { $geoWithin: { $box:  [ [ 0, 0 ], [ -122, 47 ] ] } } }` |
| **`$polygon`** | ✅ Yes | `{ "Location.coordinates": { $near: { $geometry: { type: "Polygon", coordinates: [ [ [ -121.9, 46.7 ], [ -121.5, 46.7 ], [ -121.5, 46.9 ], [ -121.9, 46.9 ], [ -121.9, 46.7 ] ] ] } } } }` |

## Sort Operations

When you use the `findOneAndUpdate` operation, sort operations on a single field are supported, but sort operations on multiple fields aren't supported.

## Other operators

| | Supported | Example | Notes
| --- | --- | --- | --- |
| **`$all`** | ✅ Yes | `{ "Location.coordinates": { $all: [-121.758, 46.87] } }` |
| **`$elemMatch`** | ✅ Yes | `{ "Location.coordinates": { $elemMatch: {  $lt: 0 } } }` |
| **`$size`** | ✅ Yes | `{ "Location.coordinates": { $size: 2 } }` |
| **`$comment`** | ✅ Yes |  `{ "Location.coordinates": { $elemMatch: {  $lt: 0 } }, $comment: "Negative values"}` |
| **`$text`** | ✅ Yes | | Not supported. Use $regex instead.

## Unsupported operators

Azure Cosmos DB for MongoDB doesn't support the `$where` and `$eval` operators.

### Methods

Following methods are supported:

#### Cursor methods

| | Supported | Example | Notes |
| --- | --- | --- | --- |
| **`cursor.sort()`** | ✅ Yes | `cursor.sort({ "Elevation": -1 })` | Documents without sort key don't get returned |

## Unique indexes

Azure Cosmos DB indexes every field in documents that are written to the database by default. Unique indexes ensure that a specific field doesn't have duplicate values across all documents in a collection, similar to the way uniqueness is preserved on the default `_id` key. You can create custom indexes in Azure Cosmos DB by using the createIndex command, including the 'unique' constraint.

Unique indexes are available for all Azure Cosmos DB accounts using Azure Cosmos DB for MongoDB.

## Time-to-live (TTL)

Azure Cosmos DB only supports a time-to-live (TTL) at the collection level (_ts) in version 3.2. Upgrade to versions 3.6+ to take advantage of other forms of [TTL](time-to-live.md).  

## User and role management

Azure Cosmos DB doesn't yet support users and roles. However, Azure Cosmos DB supports Azure role-based access control and read-write and read-only passwords/keys that can be obtained through the [Azure portal](https://portal.azure.com) (Connection String page).

## Replication

Azure Cosmos DB supports automatic, native replication at the lowest layers. This logic is extended out to achieve low-latency, global replication as well. Azure Cosmos DB doesn't support manual replication commands.

## Write Concern

Some applications rely on a [Write Concern](https://docs.mongodb.com/manual/reference/write-concern/) that specifies the number of responses required during a write operation. Due to how Azure Cosmos DB handles replication in the background all writes are automatically Quorum by default. Any write concern specified by the client code is ignored. Learn more in [Using consistency levels to maximize availability and performance](../consistency-levels.md).

## Sharding

Azure Cosmos DB supports automatic, server-side sharding. It manages shard creation, placement, and balancing automatically. Azure Cosmos DB doesn't support manual sharding commands, which means that you don't have to invoke commands like `addShard`, `balancerStart`, and `moveChunk`. You only need to specify the shard key while creating the containers or querying the data.
