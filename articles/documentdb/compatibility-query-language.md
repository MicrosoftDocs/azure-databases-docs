---
title: MongoDB Query Language (MQL) Compatibility
description: Learn about MongoDB Query Language (MQL) compatibility in Azure DocumentDB, including supported operators, commands, and features across versions 5.0-8.0.
author: suvishodcitus
ms.author: suvishod
ms.topic: concept-article
ms.date: 11/05/2025
ai-usage: ai-assisted
---

# MongoDB Query Language (MQL) compatibility in Azure DocumentDB

Azure DocumentDB provides comprehensive MongoDB Query Language (MQL) compatibility, combining MongoDB's familiar features with Azure's enterprise capabilities. This article provides a version-wise overview of MQL compatibility and feature support across versions 5.0-8.0, including operators, commands, indexes, and the MongoDB wire protocol. Applications can run without code changes, using the same client drivers, SDKs, and tools. Users benefit from Azure's scalability, security, and integration with other Azure services.

## Network protocol support

Azure DocumentDB service uses the MongoDB wire protocol, which provides seamless compatibility with existing tools and drivers. Any client driver that supports the MongoDB wire protocol can connect to Azure DocumentDB, so applications can run without code changes.

Developers can keep the same client drivers, software development kits (SDKs), and tools. As a user, you also gain Azure's scalability, security, and deep integration with other services within the Azure platform.

## Query language support

In addition to protocol support, Azure DocumentDB provides comprehensive support for MongoDB query language constructs as well. 

### Compatibility philosophy

Overall product compatibility is determined by evaluating the number of MongoDB operators (Aggregation Stages, Aggregation Operators, Query, and Projection Operators and Update Operators) supported by the service. MongoDB commands and admin operations are excluded from this calculation because Azure DocumentDB, as a PaaS offering, supports most these commands in-house, eliminating the need for user intervention. These commands aren't exposed to users; however, based on usage patterns and customer feedback, a subset of commonly used commands is available to simplify the user experience.

The overall product compatibility today stands at **99.02%**. The compatibility summary table below details support for each operator type:

| | Total | Supported | Percentage |
| --- | --- | --- | --- |
| **Aggregation Stages** | 60 | 58 | 96.67% |
| **Aggregation Operators** | 181 | 181 | 100% |
| **Query and Projection Operators** | 45 | 44 | 97.78% |
| **Update Operators** | 22 | 22 | 100% |

The following section presents a comprehensive breakdown of supported database operators, commands, and more features, offering a clear view of the product’s compatibility and functionality across various scenarios.

## Operators

The table here lists the operators that are currently supported in Azure DocumentDB:

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
> This article lists only the supported server-side commands and doesn't include client-side wrapper functions. Client-side wrapper functions, such as `deleteMany()` and `updateMany()`, internally invoke the corresponding server commands (`delete()` and `update()`). Any function that relies on supported server commands is compatible with Azure DocumentDB.

## Database commands

Azure DocumentDB supports the following database commands:

| Category | Command | Feature (v5.0) | Feature (v6.0) | Feature (v7.0) | Feature (v8.0) |
| --- | --- | --- | --- | --- | --- |
| Administrative Commands | `cloneCollectionAsCapped` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `collMod` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `compact` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `convertToCapped` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `create` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `createIndexes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `currentOp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `drop` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `dropDatabase` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `dropIndexes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `filemd5` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `getDefaultRWConcern` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `getClusterParameter` | *N/A*¹ | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `getParameter` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `killCursors` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `killOp` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `listCollections` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `listDatabases` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `listIndexes` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `reIndex` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `renameCollection` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `setIndexCommitQuorum` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `setParameter` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Administrative Commands | `setDefaultRWConcern` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `validateDBMetadata` | ❌ No | ❌ No | ❌ No | ❌ No |
| Administrative Commands | `dropConnections` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `fsync` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `fsyncUnlock` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `logRotate` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `rotateCertificates` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `setFeatureCompatibilityVersion` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `shutdown` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `compactStructuredEncryptionData` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Administrative Commands | `setUserWriteBlockMode` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Aggregation Commands | `aggregate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Commands | `count` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Commands | `distinct` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Aggregation Commands | `mapReduce` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Authentication Commands | `authenticate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Authentication Commands | `logout` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Diagnostic Commands | `buildInfo` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `collStats` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `connPoolStats` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `connectionStatus` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `dataSize` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `dbHash` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `dbStats` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `explain` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `getCmdLineOpts` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `getLog` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `hello` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `hostInfo` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `listCommands` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `lockInfo` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `ping` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `profile` | *N/A*² | *N/A*² | *N/A*² | *N/A*² |
| Diagnostic Commands | `serverStatus` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `shardConnPoolStats` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Diagnostic Commands | `top` | ❌ No | ❌ No | ❌ No | ❌ No |
| Diagnostic Commands | `validate` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Diagnostic Commands | `whatsmyuri` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Geospatial Commands | `geoSearch` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Query and Write Operation Commands | `bulkWrite` | ❌ No | ❌ No | ❌ No | ❌ No |
| Query and Write Operation Commands | `delete` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query and Write Operation Commands | `find` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query and Write Operation Commands | `findAndModify` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query and Write Operation Commands | `getLastError` | *N/A*⁴ | *N/A*⁴ | *N/A*⁴ | *N/A*⁴ |
| Query and Write Operation Commands | `getMore` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query and Write Operation Commands | `insert` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query and Write Operation Commands | `resetError` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Query and Write Operation Commands | `update` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Query Plan Cache Commands | *N/A*⁵ | | | | |
| Replication Commands | *N/A*⁶ | | | | |
| Role Management Commands | *N/A*⁷ | | | | |
| Session Commands | `abortTransaction` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Session Commands | `commitTransaction` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Session Commands | `endSessions` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Session Commands | `killAllSessions` | ❌ No | ❌ No | ❌ No | ❌ No |
| Session Commands | `killAllSessionsByPattern` | ❌ No | ❌ No | ❌ No | ❌ No |
| Session Commands | `killSessions` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Session Commands | `refreshSessions` | ❌ No | ❌ No | ❌ No | ❌ No |
| Session Commands | `startSession` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Sharding Commands | `enableSharding` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Sharding Commands | `isdbgrid` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Sharding Commands | `reshardCollection` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Sharding Commands | `shardCollection` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Sharding Commands | `unsetSharding` | *N/A*³ | *N/A*³ | *N/A*³ | *N/A*³ |
| Sharding Commands | `addShardToZone` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `clearJumboFlag` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `abortUnshardCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `removeShard` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `removeShardFromZone` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `setShardVersion` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `mergeChunks` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `abortMoveCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `getShardMap` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `analyzeShardKey` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `medianKey` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `checkMetadataConsistency` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `shardingState` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `cleanupReshardCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `flushRouterConfig` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `balancerCollectionStatus` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `balancerStart` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `balancerStatus` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `balancerStop` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `configureCollectionBalancing` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `listShards` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `split` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `moveChunk` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `updateZoneKeyRange` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `movePrimary` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `moveRange` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `abortReshardCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `commitReshardCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `refineCollectionShardKey` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `configureQueryAnalyzer` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `transitionFromDedicatedConfigServer` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `transitionToDedicatedConfigServer` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| Sharding Commands | `unshardCollection` | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ | *N/A*⁸ |
| System Events Auditing Commands | `logApplicationMessage` | ❌ No | ❌ No | ❌ No | ❌ No |
| User Management Commands | `createUser` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| User Management Commands | `dropUser` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| User Management Commands | `usersInfo` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| User Management Commands | `dropAllUsersFromDatabase` | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ |
| User Management Commands | `grantRolesToUser` | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ |
| User Management Commands | `revokeRolesFromUser` | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ |
| User Management Commands | `updateUser` | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ | *N/A*⁷ |

> [!NOTE]
>
> 1. `getClusterParameter` isn't supported in v5.0.
> 1. Azure fully manages Azure DocumentDB, a PaaS service, for commands like `dropConnections`, `fsync`, `logRotate`, etc.
> 1. Deprecated in MongoDB version 5.0.
> 1. Deprecated in MongoDB version 5.1.
> 1. Being a PaaS service, the database engine manages query plan caching for you.
> 1. Azure manages replication, removing the necessity to replicate manually.
> 1. As a fully managed service, this capability is provided through Microsoft Entra ID.
> 1. As a PaaS offering, Azure handles shard management and rebalancing. You only need to shard your collections. Azure takes care of the rest.
>

## Index types

Azure DocumentDB supports the following index types:

| Index | Description | Supported |
| --- | --- | --- |
| Single Field Index | Indexes a single field for faster lookups. | ✅ Yes |
| Compound Index | Indexes multiple fields in one index. | ✅ Yes |
| Multikey Index | Indexes array fields by indexing each element. | ✅ Yes |
| Text Index | Supports text search on string fields. | ✅ Yes |
| Wildcard Index | Dynamically indexes all or selected fields. | ✅ Yes |
| Geospatial Index | Supports spatial queries on GeoJSON data. | ✅ Yes |
| Hashed Index | Indexes hashed field values, often for sharding. | ✅ Yes |
| Vector Index (only in DocumentDB) | Enables similarity search on vector data. | ✅ Yes, with [vector search](vector-search.md) |

> [!NOTE]
> Creating a **unique index** obtains an exclusive lock on the collection for the entire duration of the build process. These indexes block read and write operations on the collection until the operation is completed.

## Index properties

Azure DocumentDB supports the following index properties:

| Index Property | Description | Supported |
| --- | --- | --- |
| time-to-live (TTL) | Automatically deletes documents after a specified time-to-live period. | ✅ Yes |
| Unique | Ensures that all values in the indexed field are unique. | ✅ Yes |
| Partial | Indexes only documents that match a specified filter condition. | ✅ Yes |
| Case Insensitive | Supports case-insensitive indexing for string fields. | ✅ Yes |
| Sparse | Indexes only documents that contain the indexed field. | ✅ Yes |
| Background | Allows the index to be created in the background without blocking operations. | ✅ Yes |

## Related content

- [MongoDB Query Language (MQL) commands](commands/index.md)
- [MongoDB Query Language (MQL) operators](operators/index.md)
- [MongoDB feature compatibility](compatibility-features.md)
