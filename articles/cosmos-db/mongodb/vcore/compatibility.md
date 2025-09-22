---
title: MongoDB Query Language Features and Compatibility
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Provide a version-wise overview of the operators, commands, and features supported in Azure Cosmos DB for MongoDB (vCore).
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 09/22/2025
ai-usage: ai-assisted
---

# MongoDB Query Language (MQL) features and compatibility

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Azure Cosmos DB for MongoDB (vCore) combines MongoDB's familiar features with Azure Cosmos DB's enterprise capabilities. This article provides an overview of compatibility and feature support, including the MongoDB wire protocol and query language constructs.

Applications can run without code changes, using the same client drivers, SDKs, and tools. Users benefit from Azure's scalability, security, and integration with other Azure services.

## Network Protocol Support

Azure Cosmos DB for MongoDB (vCore) service uses the MongoDB wire protocol, which provides seamless compatibility with existing tools and drivers. Any client driver that supports the MongoDB wire protocol can connect to Azure Cosmos DB for MongoDB (vCore), so applications can run without code changes.

Developers can keep the same client drivers, software development kits (SDKs), and tools. As a user, you also gain Azure's scalability, security, and deep integration with other services within the Azure platform.

## Query Language Support

In addition to protocol support, Azure Cosmos DB for MongoDB (vCore) provides comprehensive support for MongoDB query language constructs as well. 

### Compatibility Philosophy

Overall product compatibility is determined by evaluating the number of MongoDB operators (Aggregation Stages, Aggregation Operators, Query, and Projection Operators and Update Operators) supported by the service. MongoDB commands and admin operations are excluded from this calculation because Azure Cosmos DB for MongoDB (vCore), as a PaaS offering, supports most these commands in-house, eliminating the need for user intervention. These commands aren't exposed to users; however, based on usage patterns and customer feedback, a subset of commonly used commands is available to simplify the user experience.

The overall product compatibility today stands at **99.02%**. The compatibility summary table below details support for each operator type:

| | Total | Supported | Percentage |
| --- | --- | --- | --- |
| **Aggregation Stages** | 60 | 58 | 96.67% |
| **Aggregation Operators** | 181 | 181 | 100% |
| **Query and Projection Operators** | 45 | 44 | 97.78% |
| **Update Operators** | 22 | 22 | 100% |


The following section presents a comprehensive breakdown of supported database operators, commands, and more features, offering a clear view of the product’s compatibility and functionality across various scenarios.

## Operators

The table here lists the operators that are currently supported in vCore based Azure Cosmos DB for MongoDB:

| Category | Operator | Supported (v5.0) | Supported (v6.0) | Supported (v7.0) | Supported (v8.0) |
| --- | --- | --- | --- | --- | --- |
| Comparison Query Operators | `$eq` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$gt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$gte` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$in` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$lt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$lte` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$ne` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Query Operators | `$nin` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Logical Query Operators | `$and` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Logical Query Operators | `$not` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Logical Query Operators | `$nor` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Logical Query Operators | `$or` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Element Query Operators | `$exists` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Element Query Operators | `$type` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$expr` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$jsonSchema*` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$mod` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$regex` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$text` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Evaluation Query Operators | `$where` | | | | Deprecated in Mongo version 8.0 |
| Geospatial Operators | `$geoIntersects` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$geoWithin` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$box` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$center` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$centerSphere` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$geometry` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$maxDistance` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$minDistance` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$polygon` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$near` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Operators | `$nearSphere` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Query Operators | `$all` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Query Operators | `$elemMatch` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Query Operators | `$size` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Query Operators | `$bitsAllClear` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Query Operators | `$bitsAllSet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Query Operators | `$bitsAnyClear` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Query Operators | `$bitsAnySet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Projection Operators | `$` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Projection Operators | `$elemMatch` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Projection Operators | `$meta` | ❌ No | ❌ No | ❌ No | ❌ No |
| Projection Operators | `$slice` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Query Operators | `$comment` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Query Operators | `$rand` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Query Operators | `$natural` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$currentDate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$inc` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$min` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$max` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$mul` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$rename` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$set` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$setOnInsert` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Field Update Operators | `$unset` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$[]` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$[identifier]` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$addToSet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$pop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$pull` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$push` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$pullAll` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$each` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$position` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$slice` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Update Operators | `$sort` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Update Operators | `$bit` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$abs` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$add` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$ceil` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$divide` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$exp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$floor` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$ln` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$log` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$log10` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$mod` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$multiply` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$pow` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$round` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$sqrt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$subtract` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Arithmetic Expression Operators | `$trunc` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$arrayElemAt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$arrayToObject` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$concatArrays` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$filter` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$firstN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$in` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$indexOfArray` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$isArray` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$lastN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$map` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$maxN` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$minN` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$objectToArray` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$range` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$reduce` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$reverseArray` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$size` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$slice` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$sortArray` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Array Expression Operators | `$zip` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Operators | `$bitAnd` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Operators | `$bitNot` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Operators | `$bitOr` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bitwise Operators | `$bitXor` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Boolean Expression Operators | `$and` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Boolean Expression Operators | `$not` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Boolean Expression Operators | `$or` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$cmp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$eq` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$gt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$gte` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$lt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$lte` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Comparison Expression Operators | `$ne` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Custom Aggregation Expression Operators | `$accumulator` | | | | Deprecated in Mongo version 8.0 |
| Custom Aggregation Expression Operators | `$function` | | | | Deprecated in Mongo version 8.0 |
| Data Size Operators | `$bsonSize` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Data Size Operators | `$binarySize` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateAdd` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateDiff` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateFromParts` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateFromString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateSubtract` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateToParts` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateToString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dateTrunc` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dayOfMonth` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dayOfWeek` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$dayOfYear` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$hour` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$isoDayOfWeek` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$isoWeek` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$isoWeekYear` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$millisecond` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$minute` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$month` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$second` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$toDate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$week` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Date Expression Operators | `$year` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Literal Expression Operator | `$literal` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Operators | `$getField` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Operators | `$rand` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Miscellaneous Operators | `$sampleRate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Object Expression Operators | `$mergeObjects` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Object Expression Operators | `$objectToArray` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Object Expression Operators | `$setField` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$allElementsTrue` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$anyElementTrue` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$setDifference` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$setEquals` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$setIntersection` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$setIsSubset` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Set Expression Operators | `$setUnion` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$concat` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$dateFromString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$dateToString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$indexOfBytes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$indexOfCP` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$ltrim` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$regexFind` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$regexFindAll` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$regexMatch` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$replaceOne` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$replaceAll` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$rtrim` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$split` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$strLenBytes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$strLenCP` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$strcasecmp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$substr` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$substrBytes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$substrCP` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$toLower` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$toString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$trim` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| String Expression Operators | `$toUpper` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Text Expression Operator | `$meta` | ❌ No | ❌ No | ❌ No | ❌ No |
| Timestamp Expression Operators | `$tsIncrement` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Timestamp Expression Operators | `$tsSecond` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$sin` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$cos` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$tan` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$asin` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$acos` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$atan` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$atan2` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$asinh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$acosh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$atanh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$sinh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$cosh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$tanh` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$degreesToRadians` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Trigonometry Expression Operators | `$radiansToDegrees` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$convert` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$isNumber` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toBool` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toDate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toDecimal` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toDouble` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toInt` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toLong` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toObjectId` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$toString` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Type Expression Operators | `$type` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$accumulator` | | | | Deprecated in Mongo version 8.0 |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$addToSet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$avg` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$bottom` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$bottomN` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$count` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$first` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$firstN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$last` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$lastN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$max` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$maxN` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$median` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$mergeObjects` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$min` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$percentile` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$push` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$stdDevPop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$stdDevSamp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$sum` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$top` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (`$group`, `$bucket`, `$bucketAuto`, `$setWindowFields`) | `$topN` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$avg` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$first` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$last` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$max` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$median` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$min` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$percentile` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$stdDevPop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$stdDevSamp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Accumulators (in Other Stages) | `$sum` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variable Expression Operators | `$let` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$sum` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$push` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$addToSet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$count` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$max` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$min` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$avg` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$stdDevPop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$bottom` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$bottomN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$covariancePop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$covarianceSamp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$denseRank` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$derivative` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$documentNumber` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$expMovingAvg` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$first` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$integral` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$last` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$linearFill` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$locf` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$minN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$rank` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$shift` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$stdDevSamp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$top` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Window Operators | `$topN` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Conditional Expression Operators | `$cond` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Conditional Expression Operators | `$ifNull` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Conditional Expression Operators | `$switch` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$addFields` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$bucket` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$bucketAuto` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$changeStream` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$changeStreamSplitLargeEvent` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$collStats` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$count` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$densify` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$documents` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$facet` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$fill` | | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$geoNear` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$graphLookup` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$group` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$indexStats` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$limit` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$listSampledQueries` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$listSearchIndexes` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$listSessions` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$lookup` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$match` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$merge` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$out` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$planCacheStats` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$project` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$redact` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$replaceRoot` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$replaceWith` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$sample` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$search` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$searchMeta` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$set` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$setWindowFields` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$skip` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$sort` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$sortByCount` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$unionWith` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$unset` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$unwind` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$shardedDataDistribution` | ❌ No | ❌ No | ❌ No | ❌ No |
| Aggregation Pipeline Stages | `$currentOp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Pipeline Stages | `$listLocalSessions` | ❌ No | ❌ No | ❌ No | ❌ No |
| Variables in Aggregation Expressions | `NOW` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `ROOT` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `REMOVE` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `CURRENT` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `CLUSTER_TIME` | ❌ No | ❌ No | ❌ No | ❌ No |
| Variables in Aggregation Expressions | `DESCEND` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `PRUNE` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `KEEP` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Variables in Aggregation Expressions | `SEARCH_META` | ❌ No | ❌ No | ❌ No | ❌ No |
| Variables in Aggregation Expressions | `USER_ROLES` | ❌ No | ❌ No | ❌ No | ❌ No |

> [!NOTE]
> `AvgObjsize` and `size` in `collStats` & `dbStats` only works with documents that are sized less than 2 kilobytes.
> 
> Schema validation supports: `insert`, `update`, `findAndModify`, and the `$merge` / `$out` stages in aggregation. Use `bypassDocumentValidation` to skip validation if needed.
> 
> This article lists only the supported server-side commands and doesn't include client-side wrapper functions. Client-side wrapper functions, such as `deleteMany()` and `updateMany()`, internally invoke the corresponding server commands (`delete()` and `update()`). Any function that relies on supported server commands is compatible with Azure Cosmos DB for MongoDB (vCore).

## Database commands

Azure Cosmos DB for MongoDB (vCore) supports the following database commands:

<table>
<tr><td rowspan="2"><b>Category</b></td><td rowspan="2"><b>Command</b></td><td colspan="4"><b>Feature</b></td></tr>
<tr><td><b>v5.0</b></td><td><b>v6.0</b></td><td><b>v7.0</b></td><td><b>v8.0</b></td></tr>

<tr><td rowspan="34">Administrative Commands</td><td><code>cloneCollectionAsCapped</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>collMod</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>compact</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>convertToCapped</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>create</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>createIndexes</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>currentOp</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>drop</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>dropDatabase</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>dropIndexes</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>filemd5</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>getDefaultRWConcern</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>getClusterParameter</code></td><td></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>getParameter</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>killCursors</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>killOp</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>listCollections</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>listDatabases</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>listIndexes</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>reIndex</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>renameCollection</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>setIndexCommitQuorum</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>setParameter</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>setDefaultRWConcern</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>validateDBMetadata</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>dropConnections</code></td><td colspan="4" rowspan="9">Azure fully manages Azure Cosmos DB for MongoDB (vCore), a PaaS service.</td></tr>
<tr><td><code>fsync</code></td><td colspan="4"></td></tr>
<tr><td><code>fsyncUnlock</code></td><td colspan="4"></td></tr>
<tr><td><code>logRotate</code></td><td colspan="4"></td></tr>
<tr><td><code>rotateCertificates</code></td><td colspan="4"></td></tr>
<tr><td><code>setFeatureCompatibilityVersion</code></td><td colspan="4"></td></tr>
<tr><td><code>shutdown</code></td><td colspan="4"></td></tr>
<tr><td><code>compactStructuredEncryptionData</code></td><td colspan="4"></td></tr>
<tr><td><code>setUserWriteBlockMode</code></td><td colspan="4"></td></tr>

<tr><td rowspan="4">Aggregation Commands</td><td><code>aggregate</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>count</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>distinct</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>mapReduce</code></td><td colspan="4">Deprecated in Mongo version 5.0</td></tr>

<tr><td rowspan="2">Authentication Commands</td><td><code>authenticate</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>logout</code></td><td colspan="4">Deprecated in Mongo version 5.0</td></tr>

<tr><td rowspan="21">Diagnostic Commands</td><td><code>buildInfo</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>collStats</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>connPoolStats</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>connectionStatus</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>dataSize</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>dbHash</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>dbStats</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>explain</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>getCmdLineOpts</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>getLog</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>hello</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>hostInfo</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>listCommands</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>lockInfo</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>ping</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>profile</code></td><td colspan="4">Azure fully manages Azure Cosmos DB for MongoDB (vCore), a PaaS service.</td></tr>
<tr><td><code>serverStatus</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>shardConnPoolStats</code></td><td colspan="4">Deprecated in Mongo version 5.0. Alternative: connPoolStats</td></tr>
<tr><td><code>top</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>validate</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>whatsmyuri</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>

<tr><td rowspan="1">Geospatial Commands</td><td><code>geoSearch</code></td><td colspan="4">Deprecated in Mongo version 5.0</td></tr>

<tr><td rowspan="9">Query and Write Operation Commands</td><td><code>bulkWrite</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>delete</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>find</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>findAndModify</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>getLastError</code></td><td colspan="4">Deprecated in Mongo version 5.1</td></tr>
<tr><td><code>getMore</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>insert</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>resetError</code></td><td colspan="4">Deprecated in Mongo version 5.0</td></tr>
<tr><td><code>update</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>

<tr><td rowspan="1">Query Plan Cache Commands</td><td colspan="5">Being a PaaS service, the database engine manages query plan caching for you.</td></tr>

<tr><td rowspan="1">Replication Commands</td><td colspan="5">Azure manages replication, removing the necessity for customers to replicate manually.</td></tr>

<tr><td rowspan="1">Role Management Commands</td><td colspan="5">As a fully managed service, this capability is provided through Microsoft Entra ID.</td></tr>

<tr><td rowspan="8">Session Commands</td><td><code>abortTransaction</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>commitTransaction</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>endSessions</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>killAllSessions</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>killAllSessionsByPattern</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>killSessions</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>refreshSessions</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>
<tr><td><code>startSession</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>

<tr><td rowspan="39">Sharding Commands</td><td><code>enableSharding</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>isdbgrid</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>reshardCollection</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>shardCollection</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>unsetSharding</code></td><td colspan="4">Deprecated in Mongo version 5.0</td></tr>
<tr><td><code>addShard</code></td><td rowspan="34" colspan="4">As a PaaS offering, Azure handles shard management and rebalancing. Users only need to shard their collections, and Azure takes care of the rest.</td></tr>
<tr><td><code>addShardToZone</code></td></tr>
<tr><td><code>clearJumboFlag</code></td></tr>
<tr><td><code>abortUnshardCollection</code></td></tr>
<tr><td><code>removeShard</code></td></tr>
<tr><td><code>removeShardFromZone</code></td></tr>
<tr><td><code>setShardVersion</code></td></tr>
<tr><td><code>mergeChunks</code></td></tr>
<tr><td><code>abortMoveCollection</code></td></tr>
<tr><td><code>getShardMap</code></td></tr>
<tr><td><code>analyzeShardKey</code></td></tr>
<tr><td><code>medianKey</code></td></tr>
<tr><td><code>checkMetadataConsistency</code></td></tr>
<tr><td><code>shardingState</code></td></tr>
<tr><td><code>cleanupReshardCollection</code></td></tr>
<tr><td><code>flushRouterConfig</code></td></tr>
<tr><td><code>balancerCollectionStatus</code></td></tr>
<tr><td><code>balancerStart</code></td></tr>
<tr><td><code>balancerStatus</code></td></tr>
<tr><td><code>balancerStop</code></td></tr>
<tr><td><code>configureCollectionBalancing</code></td></tr>
<tr><td><code>listShards</code></td></tr>
<tr><td><code>split</code></td></tr>
<tr><td><code>moveChunk</code></td></tr>
<tr><td><code>updateZoneKeyRange</code></td></tr>
<tr><td><code>movePrimary</code></td></tr>
<tr><td><code>moveRange</code></td></tr>
<tr><td><code>abortReshardCollection</code></td></tr>
<tr><td><code>commitReshardCollection</code></td></tr>
<tr><td><code>refineCollectionShardKey</code></td></tr>
<tr><td><code>configureQueryAnalyzer</code></td></tr>
<tr><td><code>transitionFromDedicatedConfigServer</code></td></tr>
<tr><td><code>transitionToDedicatedConfigServer</code></td></tr>
<tr><td><code>unshardCollection</code></td></tr>

<tr><td rowspan="1">System Events Auditing Commands</td><td><code>logApplicationMessage</code></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td><td><img src="media/compatibility/no-icon.svg" alt="No"></td></tr>

<tr><td rowspan="7">User Management Commands</td><td><code>createUser</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>dropUser</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>usersInfo</code></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td><code>dropAllUsersFromDatabase</code></td><td rowspan="4" colspan="4">As a fully managed service, this capability is provided through Microsoft Entra ID.</td></tr>
<tr><td><code>grantRolesToUser</code></td></tr>
<tr><td><code>revokeRolesFromUser</code></td></tr>
<tr><td><code>updateUser</code></td></tr>

</table>


## Index Types and their Properties

vCore based Azure Cosmos DB for MongoDB supports the following indexes and index properties:

### Indexes

<table>
<tr><td>Command</td><td>Description</td><td>Supported</td></tr>
<tr><td>Single Field Index</td><td>Indexes a single field for faster lookups.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Compound Index</td><td>Indexes multiple fields in one index.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Multikey Index</td><td>Indexes array fields by indexing each element.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Text Index</td><td>Supports text search on string fields.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Wildcard Index</td><td>Dynamically indexes all or selected fields.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Geospatial Index</td><td>Supports spatial queries on GeoJSON data.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Hashed Index</td><td>Indexes hashed field values, often for sharding.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Vector Index (only available in Cosmos DB)</td><td>Enables similarity search on vector data.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"> Yes, with <a href="vector-search.md">vector search</a></td></tr>
</table>

> [!NOTE]
> Creating a **unique index** obtains an exclusive lock on the collection for the entire duration of the build process. These indexes block read and write operations on the collection until the operation is completed.


### Index properties

<table>
<tr><td>Command</td><td>Description</td><td>Supported</td></tr>
<tr><td>time-to-live (TTL)</td><td>Automatically deletes documents after a specified time-to-live period.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Unique</td><td>Ensures that all values in the indexed field are unique.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Partial</td><td>Indexes only documents that match a specified filter condition.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Case Insensitive</td><td>Supports case-insensitive indexing for string fields.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Sparse</td><td>Indexes only documents that contain the indexed field.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
<tr><td>Background</td><td>Allows the index to be created in the background without blocking operations.</td><td><img src="media/compatibility/yes-icon.svg" alt="Yes"></td></tr>
</table>

## Next steps

> [!div class="nextstepaction"]
> [Migration options for Azure Cosmos DB for MongoDB (vCore)](migration-options.md)
