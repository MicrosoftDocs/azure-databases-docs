---
title: 7.0 Supported Features and Syntax
titleSuffix: Azure Cosmos DB for MongoDB
description: Discover supported features and syntax in Azure Cosmos DB for MongoDB 7.0, including database commands, query language, and aggregation pipeline. Explore benefits and get started today.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: release-notes
ms.date: 08/20/2025
appliesto:
  - ✅ MongoDB
---

# Supported features and syntax in Azure Cosmos DB for MongoDB 7.0 server version

Azure Cosmos DB for MongoDB 7.0 enables you to use familiar MongoDB features with enterprise-grade capabilities such as global distribution, automatic sharding, and high availability. This article describes the supported features, syntax, and benefits of using Azure Cosmos DB for MongoDB 7.0.

## Protocol support

The supported operators and any limitations or exceptions are listed in this article. Any client driver that understands these protocols should be able to connect to Azure Cosmos DB for MongoDB. When you create Azure Cosmos DB for MongoDB accounts, the 3.6+ version of accounts has an endpoint in the format `*.mongo.cosmos.azure.com`. The 3.2 version of accounts has an endpoint in the format `*.documents.azure.com`.

> [!NOTE]
> This article lists only the supported server commands, and excludes client-side wrapper functions. Client-side wrapper functions such as `deleteMany()` and `updateMany()` internally use the `delete()` and `update()` server commands. Functions that use supported server commands are compatible with Azure Cosmos DB for MongoDB.

## Query language support

Azure Cosmos DB for MongoDB provides comprehensive support for MongoDB query language constructs. In the following sections, you can find the detailed list of currently supported operations, operators, stages, commands, and options.

## Database commands

Azure Cosmos DB for MongoDB supports the following database commands.

### Query and write operation commands

| | Supported |
| --- | --- |
| **`change streams`** | ✅ Yes |
| **`delete`** | ✅ Yes |
| **`eval`** | ✖️ No |
| **`find`** | ✅ Yes |
| **`findAndModify`** | ✅ Yes |
| **`getLastError`** | ✅ Yes |
| **`getMore`** | ✅ Yes |
| **`getPrevError`** | ✖️ No |
| **`insert`** | ✅ Yes |
| **`parallelCollectionScan`** | ✖️ No |
| **`resetError`** | ✖️ No |
| **`update`** | ✅ Yes |

### Transaction commands

> [!NOTE]
> Multi-document transactions are supported only within a single nonsharded collection. Cross-collection and cross-shard multi-document transactions aren't yet supported in the API for MongoDB.

| | Supported |
| --- | --- |
| **`abortTransaction`** | ✅ Yes |
| **`commitTransaction`** | ✅ Yes |

### Authentication commands

| | Supported |
| --- | --- |
| **`authenticate`** | ✅ Yes |
| **`getnonce`** | ✅ Yes |
| **`logout`** | ✅ Yes |

### Administration commands

| | Supported |
| --- | --- |
| **`cloneCollectionAsCapped`** | ✖️ No |
| **`collMod`** | ✖️ No |
| **`connectionStatus`** | ✖️ No |
| **`convertToCapped`** | ✖️ No |
| **`copydb`** | ✖️ No |
| **`create`** | ✅ Yes |
| **`createIndexes`** | ✅ Yes |
| **`currentOp`** | ✅ Yes |
| **`drop`** | ✅ Yes |
| **`dropDatabase`** | ✅ Yes |
| **`dropIndexes`** | ✅ Yes |
| **`filemd5`** | ✅ Yes |
| **`killCursors`** | ✅ Yes |
| **`killOp`** | ✖️ No |
| **`listCollections`** | ✅ Yes |
| **`listDatabases`** | ✅ Yes |
| **`listIndexes`** | ✅ Yes |
| **`reIndex`** | ✅ Yes |
| **`renameCollection`** | ✖️ No |

### Diagnostics commands

| | Supported |
| --- | --- |
| **`buildInfo`** | ✅ Yes |
| **`collStats`** | ✅ Yes |
| **`connPoolStats`** | ✖️ No |
| **`connectionStatus`** | ✖️ No |
| **`dataSize`** | ✖️ No |
| **`dbHash`** | ✖️ No |
| **`dbStats`** | ✅ Yes |
| **`explain`** | ✅ Yes |
| **`features`** | ✖️ No |
| **`hello`** | ✅ Yes |
| **`hostInfo`** | ✅ Yes |
| **`listDatabases`** | ✅ Yes |
| **`listCommands`** | ✖️ No |
| **`profiler`** | ✖️ No |
| **`serverStatus`** | ✖️ No |
| **`top`** | ✖️ No |
| **`whatsmyuri`** | ✅ Yes |

<a name="aggregation-pipeline"></a>

## Aggregation pipeline

Azure Cosmos DB for MongoDB supports the following aggregation commands.

### Aggregation commands

| | Supported |
| --- | --- |
| **`aggregate`** | ✅ Yes |
| **`count`** | ✅ Yes |
| **`distinct`** | ✅ Yes |
| **`mapReduce`** | ✖️ No |

### Aggregation stages

| | Supported |
| --- | --- |
| **`addFields`** | ✅ Yes |
| **`bucket`** | ✖️ No |
| **`bucketAuto`** | ✖️ No |
| **`changeStream`** | ✅ Yes |
| **`collStats`** | ✖️ No |
| **`count`** | ✅ Yes |
| **`currentOp`** | ✖️ No |
| **`facet`** | ✅ Yes |
| **`geoNear`** | ✅ Yes |
| **`graphLookup`** | ✖️ No |
| **`group`** | ✅ Yes |
| **`indexStats`** | ✖️ No |
| **`limit`** | ✅ Yes |
| **`listLocalSessions`** | ✖️ No |
| **`listSessions`** | ✖️ No |
| **`lookup`** | ❓Partial |
| **`match`** | ✅ Yes |
| **`merge`** | ✅ Yes |
| **`out`** | ✅ Yes |
| **`planCacheStats`** | ✅ Yes |
| **`project`** | ✅ Yes |
| **`redact`** | ✅ Yes |
| **`regexFind`** | ✅ Yes |
| **`regexFindAll`** | ✅ Yes |
| **`regexMatch`** | ✅ Yes |
| **`replaceRoot`** | ✅ Yes |
| **`replaceWith`** | ✅ Yes |
| **`sample`** | ✅ Yes |
| **`set`** | ✅ Yes |
| **`skip`** | ✅ Yes |
| **`sort`** | ✅ Yes |
| **`sortByCount`** | ✅ Yes |
| **`unset`** | ✅ Yes |
| **`unwind`** | ✅ Yes |

> [!NOTE]
> The `$lookup` aggregation doesn't support the [uncorrelated subqueries](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#join-conditions-and-uncorrelated-sub-queries) feature introduced in server version 3.6. Using the `$lookup` operator with the `let` and `pipeline` fields results in an error message indicating that "`let` isn't supported."

### Boolean expressions

| | Supported |
| --- | --- |
| **`and`** | ✅ Yes |
| **`not`** | ✅ Yes |
| **`or`** | ✅ Yes |

### Conversion expressions

| | Supported |
| --- | --- |
| **`convert`** | ✅ Yes |
| **`toBool`** | ✅ Yes |
| **`toDate`** | ✅ Yes |
| **`toDecimal`** | ✅ Yes |
| **`toDouble`** | ✅ Yes |
| **`toInt`** | ✅ Yes |
| **`toLong`** | ✅ Yes |
| **`toObjectId`** | ✅ Yes |
| **`toString`** | ✅ Yes |

### Set expressions

| | Supported |
| --- | --- |
| **`setEquals`** | ✅ Yes |
| **`setIntersection`** | ✅ Yes |
| **`setUnion`** | ✅ Yes |
| **`setDifference`** | ✅ Yes |
| **`setIsSubset`** | ✅ Yes |
| **`anyElementTrue`** | ✅ Yes |
| **`allElementsTrue`** | ✅ Yes |

### Comparison expressions

> [!NOTE]
> The API for MongoDB doesn't support comparison expressions that have an array literal in the query.

| | Supported |
| --- | --- |
| **`cmp`** | ✅ Yes |
| **`eq`** | ✅ Yes |
| **`gt`** | ✅ Yes |
| **`gte`** | ✅ Yes |
| **`lt`** | ✅ Yes |
| **`lte`** | ✅ Yes |
| **`ne`** | ✅ Yes |
| **`in`** | ✅ Yes |
| **`nin`** | ✅ Yes |

### Arithmetic expressions

| | Supported |
| --- | --- |
| **`abs`** | ✅ Yes |
| **`add`** | ✅ Yes |
| **`ceil`** | ✅ Yes |
| **`divide`** | ✅ Yes |
| **`exp`** | ✅ Yes |
| **`floor`** | ✅ Yes |
| **`ln`** | ✅ Yes |
| **`log`** | ✅ Yes |
| **`log10`** | ✅ Yes |
| **`mod`** | ✅ Yes |
| **`multiply`** | ✅ Yes |
| **`pow`** | ✅ Yes |
| **`round`** | ✅ Yes |
| **`sqrt`** | ✅ Yes |
| **`subtract`** | ✅ Yes |
| **`trunc`** | ✅ Yes |

### Trigonometry expressions

| | Supported |
| --- | --- |
| **`acos`** | ✅ Yes |
| **`acosh`** | ✅ Yes |
| **`asin`** | ✅ Yes |
| **`asinh`** | ✅ Yes |
| **`atan`** | ✅ Yes |
| **`atan2`** | ✅ Yes |
| **`atanh`** | ✅ Yes |
| **`cos`** | ✅ Yes |
| **`cosh`** | ✅ Yes |
| **`degreesToRadians`** | ✅ Yes |
| **`radiansToDegrees`** | ✅ Yes |
| **`sin`** | ✅ Yes |
| **`sinh`** | ✅ Yes |
| **`tan`** | ✅ Yes |
| **`tanh`** | ✅ Yes |

### String expressions

| | Supported |
| --- | --- |
| **`concat`** | ✅ Yes |
| **`indexOfBytes`** | ✅ Yes |
| **`indexOfCP`** | ✅ Yes |
| **`ltrim`** | ✅ Yes |
| **`rtrim`** | ✅ Yes |
| **`trim`** | ✅ Yes |
| **`split`** | ✅ Yes |
| **`strLenBytes`** | ✅ Yes |
| **`strLenCP`** | ✅ Yes |
| **`strcasecmp`** | ✅ Yes |
| **`substr`** | ✅ Yes |
| **`substrBytes`** | ✅ Yes |
| **`substrCP`** | ✅ Yes |
| **`toLower`** | ✅ Yes |
| **`toUpper`** | ✅ Yes |

### Text search operator

| | Supported |
| --- | --- |
| **`meta`** | ✖️ No |

### Array expressions

| | Supported |
| --- | --- |
| **`arrayElemAt`** | ✅ Yes |
| **`arrayToObject`** | ✅ Yes |
| **`concatArrays`** | ✅ Yes |
| **`filter`** | ✅ Yes |
| **`indexOfArray`** | ✅ Yes |
| **`isArray`** | ✅ Yes |
| **`objectToArray`** | ✅ Yes |
| **`range`** | ✅ Yes |
| **`reverseArray`** | ✅ Yes |
| **`reduce`** | ✅ Yes |
| **`size`** | ✅ Yes |
| **`slice`** | ✅ Yes |
| **`zip`** | ✅ Yes |
| **`in`** | ✅ Yes |

### Variable operators

| | Supported |
| --- | --- |
| **`map`** | ✅ Yes |
| **`let`** | ✅ Yes |

### System variables

| | Supported |
| --- | --- |
| **`$$CLUSTERTIME`** | ✅ Yes |
| **`$$CURRENT`** | ✅ Yes |
| **`$$DESCEND`** | ✅ Yes |
| **`$$KEEP`** | ✅ Yes |
| **`$$NOW`** | ✅ Yes |
| **`$$PRUNE`** | ✅ Yes |
| **`$$REMOVE`** | ✅ Yes |
| **`$$ROOT`** | ✅ Yes |

### Literal operator

| | Supported |
| --- | --- |
| **`literal`** | ✅ Yes |

### Date expressions

| | Supported |
| --- | --- |
| **`dayOfYear`** | ✅ Yes |
| **`dayOfMonth`** | ✅ Yes |
| **`dayOfWeek`** | ✅ Yes |
| **`year`** | ✅ Yes |
| **`month`** | ✅ Yes |
| **`week`** | ✅ Yes |
| **`hour`** | ✅ Yes |
| **`minute`** | ✅ Yes |
| **`second`** | ✅ Yes |
| **`millisecond`** | ✅ Yes |
| **`dateToString`** | ✅ Yes |
| **`isoDayOfWeek`** | ✅ Yes |
| **`isoWeek`** | ✅ Yes |
| **`dateFromParts`** | ✅ Yes |
| **`dateToParts`** | ✅ Yes |
| **`dateFromString`** | ✅ Yes |
| **`isoWeekYear`** | ✅ Yes |

### Conditional expressions

| | Supported |
| --- | --- |
| **`cond`** | ✅ Yes |
| **`ifNull`** | ✅ Yes |
| **`switch`** | ✅ Yes |

### Data type operator

| | Supported |
| --- | --- |
| **`type`** | ✅ Yes |

### Accumulator expressions

| | Supported |
| --- | --- |
| **`sum`** | ✅ Yes |
| **`avg`** | ✅ Yes |
| **`first`** | ✅ Yes |
| **`last`** | ✅ Yes |
| **`max`** | ✅ Yes |
| **`min`** | ✅ Yes |
| **`push`** | ✅ Yes |
| **`addToSet`** | ✅ Yes |
| **`stdDevPop`** | ✅ Yes |
| **`stdDevSamp`** | ✅ Yes |

### Merge operator

| | Supported |
| --- | --- |
| **`mergeObjects`** | ✅ Yes |

## Data types

Azure Cosmos DB for MongoDB supports documents that are encoded in MongoDB binary JSON (BSON) format. Versions 4.0 and later (4.0+) enhance the internal usage of this format to improve performance and reduce costs. Documents that are written or updated through an endpoint running 4.0+ benefit from this optimization.

In an [upgrade scenario to version 4.0 or later](upgrade-version.md), documents created before upgrading don't immediately benefit from the enhanced performance. To take advantage of the improvements, update these documents through a write operation using the 4.0 endpoint.

16-MB document support raises the size limit for documents from 2 MB to 16 MB. This limit applies only to collections created after enabling the feature. After you enable this feature for a database account, it can't be disabled.

To enable 16-MB document support, change the setting on the **Features** tab for the resource in the Azure portal or programmatically [add the `EnableMongo16MBDocumentSupport` capability](how-to-configure-capabilities.md).

We recommend that you enable Server Side Retry and avoid using wildcard indexes to ensure that requests in larger documents succeed. Raising your database or collection request units might also help performance.

| | Supported |
| --- | --- |
| **`Double`** | ✅ Yes |
| **`String`** | ✅ Yes |
| **`Object`** | ✅ Yes |
| **`Array`** | ✅ Yes |
| **`Binary Data`** | ✅ Yes |
| **`ObjectId`** | ✅ Yes |
| **`Boolean`** | ✅ Yes |
| **`Date`** | ✅ Yes |
| **`Null`** | ✅ Yes |
| **`32-bit Integer (int)`** | ✅ Yes |
| **`Timestamp`** | ✅ Yes |
| **`64-bit Integer (long)`** | ✅ Yes |
| **`MinKey`** | ✅ Yes |
| **`MaxKey`** | ✅ Yes |
| **`Decimal128`** | ✅ Yes |
| **`Regular Expression`** | ✅ Yes |
| **`JavaScript`** | ✅ Yes |
| **`JavaScript (with scope)`** | ✅ Yes |
| **`Undefined`** | ✅ Yes |

## Indexes and index properties

Azure Cosmos DB for MongoDB supports the following index commands and index properties.

### Indexes

| | Supported |
| --- | --- |
| **`Single Field Index`** | ✅ Yes |
| **`Compound Index`** | ✅ Yes |
| **`Multikey Index`** | ✅ Yes |
| **`Text Index`** | ✖️ No |
| **`2dsphere`** | ✅ Yes |
| **`2d Index`** | ✖️ No |
| **`Hashed Index`** | ✖️ No |

### Index properties

| | Supported |
| --- | --- |
| **`TTL`** | ✅ Yes |
| **`Unique`** | ✅ Yes |
| **`Partial`** | ❓Partial |
| **`Case Insensitive`** | ✖️ No |
| **`Sparse`** | ✖️ No |
| **`Background`** | ✅ Yes |

> [!TIP]
> `Partial` is supported only for unique indexes.

## Operators

Azure Cosmos DB for MongoDB supports the following operators.

### Logical operators

| | Supported |
| --- | --- |
| **`or`** | ✅ Yes |
| **`and`** | ✅ Yes |
| **`not`** | ✅ Yes |
| **`nor`** | ✅ Yes |

### Element operators

| | Supported |
| --- | --- |
| **`exists`** | ✅ Yes |
| **`type`** | ✅ Yes |

### Evaluation query operators

| | Supported |
| --- | --- |
| **`expr`** | ✅ Yes |
| **`jsonSchema`** | ✖️ No |
| **`mod`** | ✅ Yes |
| **`regex`** | ✅ Yes |
| **`text`** | ✖️ No |
| **`where`** | ✖️ No |

In `$regex` queries, left-anchored expressions allow index search. However, using the `i` modifier (case-insensitivity) and the `m` modifier (multiline) causes the collection to scan in all expressions.

When there's a need to include `$` or `|`, it's best to create two (or more) `$regex` queries.

For example, change the following original query:

`find({x:{$regex: /^abc$/})`

To this query:

`find({x:{$regex: /^abc/, x:{$regex:/^abc$/}})`

The first part of the modified query uses the index to restrict the search to documents that begin with `^abc`. The second part of the query matches the exact entries. The bar operator (`|`) acts as an `or` function. The query `find({x:{$regex: /^abc |^def/})` matches the documents in which field `x` has values that begin with `abc` or `def`. To use the index, break the query into two separate queries and join them with the `$or` operator: `find({$or: [{x: {$regex: /^abc/}}, {x: {$regex: /^def/}}]})`.

> [!TIP]
> The `text` command isn't supported. Use `$regex` instead.

### Array operators

| | Supported |
| --- | --- |
| **`all`** | ✅ Yes |
| **`elemMatch`** | ✅ Yes |
| **`size`** | ✅ Yes |

### Comment operator

| | Supported |
| --- | --- |
| **`comment`** | ✅ Yes |

### Projection operators

| | Supported |
| --- | --- |
| **`elemMatch`** | ✅ Yes |
| **`meta`** | ✖️ No |
| **`slice`** | ✅ Yes |

### Update operators

#### Field update operators

| | Supported |
| --- | --- |
| **`inc`** | ✅ Yes |
| **`mul`** | ✅ Yes |
| **`rename`** | ✅ Yes |
| **`setOnInsert`** | ✅ Yes |
| **`set`** | ✅ Yes |
| **`unset`** | ✅ Yes |
| **`min`** | ✅ Yes |
| **`max`** | ✅ Yes |
| **`currentDate`** | ✅ Yes |

#### Array update operators

| | Supported |
| --- | --- |
| **`$`** | ✅ Yes |
| **`$[]`** | ✅ Yes |
| **`$[\<identifier\>]`** | ✅ Yes |
| **`addToSet`** | ✅ Yes |
| **`pop`** | ✅ Yes |
| **`pullAll`** | ✅ Yes |
| **`pull`** | ✅ Yes |
| **`push`** | ✅ Yes |
| **`pushAll`** | ✅ Yes |

#### Update modifiers

| | Supported |
| --- | --- |
| **`each`** | ✅ Yes |
| **`slice`** | ✅ Yes |
| **`sort`** | ✅ Yes |
| **`position`** | ✅ Yes |

#### Bitwise update operator

| | Supported |
| --- | --- |
| **`bit`** | ✅ Yes |
| **`bitsAllSet`** | ✖️ No |
| **`bitsAnySet`** | ✖️ No |
| **`bitsAllClear`** | ✖️ No |
| **`bitsAnyClear`** | ✖️ No |

### Geospatial operators

| | Supported |
| --- | --- |
| **`$geoWithin`** | ✅ Yes |
| **`$geoIntersects`** | ✅ Yes |
| **`$near`** | ✅ Yes |
| **`$nearSphere`** | ✅ Yes |
| **`$geometry`** | ✅ Yes |
| **`$minDistance`** | ✅ Yes |
| **`$maxDistance`** | ✅ Yes |
| **`$center`** | ✖️ No |
| **`$centerSphere`** | ✖️ No |
| **`$box`** | ✖️ No |
| **`$polygon`** | ✖️ No |

## Sort operations

When you use the `findOneAndUpdate` operation, sort operations on a single field are supported. Sort operations on multiple fields aren't supported.

## Indexing

The API for MongoDB [supports various indexes](indexing.md) to enable sorting on multiple fields, improve query performance, and enforce uniqueness.

## Client-side field-level encryption

Client-level field encryption is a driver feature and works with Azure Cosmos DB for MongoDB. Explicit encryption, where the driver encrypts each field during write operations, is supported. Automatic encryption isn't supported. Explicit decryption and automatic decryption are supported.

The `mongocryptd` shouldn't be run because it isn't needed to perform any of the supported operations.

## GridFS

Azure Cosmos DB supports GridFS through any GridFS-compatible Mongo driver.

## Replication

Azure Cosmos DB supports automatic, native replication at the lowest layers. This logic is also extended to achieve low-latency, global replication. Azure Cosmos DB doesn't support manual replication commands.

## Retryable writes

The retryable writes feature enables MongoDB drivers to automatically retry certain write operations. The feature results in more stringent requirements for certain operations, which match MongoDB protocol requirements. With this feature enabled, update operations, including deletes, in sharded collections require the shard key to be included in the query filter or update statement.

For example, with a sharded collection, sharded on key `region`: To delete all the documents with the field `city = "NYC"`, the application needs to execute the operation for all shard key (**region**) values if Retryable writes are enabled.

- `db.coll.deleteMany({"region": "USA", "city": "NYC"})` - Succeeds with message `Success`
- `db.coll.deleteMany({"city": "NYC"})` - Fails with error `ShardKeyNotFound(61)`

> [!NOTE]
> The retryable writes feature doesn't support bulk unordered writes at this time. If you want to perform bulk writes with retryable writes enabled, perform bulk ordered writes.

To enable the feature, [add the EnableMongoRetryableWrites capability](how-to-configure-capabilities.md) to your database account. This feature can also be enabled on the **Features** tab in the Azure portal.

## Sharding

Azure Cosmos DB supports automatic, server-side sharding. It automatically manages shard creation, placement, and balancing. Azure Cosmos DB doesn't support manual sharding commands, which means that you don't have to invoke commands like `addShard`, `balancerStart`, and `moveChunk`. You need to specify the shard key only when you create the containers or query the data.

## Sessions

Azure Cosmos DB doesn't yet support server-side sessions commands.

## Time to Live

Azure Cosmos DB provides a Time to Live (TTL) feature based on the document's time stamp. Enable TTL for a collection in the [Azure portal](https://portal.azure.com).

### Custom TTL

This feature lets you specify a custom TTL value on a single field within a collection. Documents expire based on the value of this field.

On a collection that has TTL enabled on a field:

- Acceptable types are the binary JSON (BSON) data type and numeric types (integer, long, or double), which are interpreted as a Unix millisecond time stamp to determine expiration.

- If the TTL field is an array, then the smallest element of the array that is of an acceptable type is considered for document expiry.

- If the TTL field is missing from a document, the document doesn’t expire.

- If the TTL field isn't an acceptable type, the document doesn't expire.

#### Limitations of a custom TTL

- Only one field in a collection can have a TTL set on it.

- With a custom TTL field set, the `\_ts` field can't be used for document expiration.

- You can't use the `\_ts` field in addition.

#### Configuration

You can enable a custom TTL by updating the `EnableTtlOnCustomPath` capability for the account. Learn [how to configure capabilities](../../cosmos-db/mongodb/how-to-configure-capabilities.md).

### Set up the TTL

To set up the TTL, run this command: `db.coll.createIndex({"YOUR_CUSTOM_TTL_FIELD":1}, {expireAfterSeconds: 10})`

## Transactions

Multi-document transactions are supported within an unsharded collection. Multi-document transactions aren't supported across collections or in sharded collections. The timeout for transactions is a fixed 5 seconds.

## Manage users and roles

Azure Cosmos DB doesn't yet support users and roles. However, Azure Cosmos DB supports Azure role-based access control and read-write and read-only passwords and keys that can be obtained through the [Azure portal](https://portal.azure.com) (on the **Connection Strings** page).

## Write concerns

Some applications rely on a [write concern](https://docs.mongodb.com/manual/reference/write-concern/), which specifies the number of responses that are required during a write operation. Due to how Azure Cosmos DB handles replication in the background, all writes are automatically Quorum by default. Azure Cosmos DB ignores any write concern specified by client code. Learn how to [use consistency levels to maximize availability and performance](../consistency-levels.md).
