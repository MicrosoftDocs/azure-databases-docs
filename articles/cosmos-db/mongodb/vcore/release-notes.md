---
title: Service release notes
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Includes a list of all feature updates, grouped by release date, for the Azure Cosmos DB for MongoDB vCore service.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: release-notes
ms.date: 07/30/2025

#Customer intent: As a database administrator, I want to review the release notes, so I can understand what new features are released for the service.
---

# Release notes for Azure Cosmos DB for MongoDB vCore

This article contains release notes for the API for MongoDB vCore. These release notes are composed of feature release dates, and feature updates.

## Latest release: July 15, 2025

### Engine Enhancements_0715

- [Preview] Enabled index pushdown optimization for $sort on any field.
- Enabled index pushdown optimization for $limit.
- [Preview] Added support for composite indexes on filter conditions.
- Added support for HNSW index for M30 SKU.
- Enhanced TTL index behavior to continue processing even if the cluster becomes read-only due to disk full.
- Improvements to parallel build for faster index creation on sharded collection.

#### Infrastructure Enhancements_0715

- [Preview] Added support for CMK, allowed only during provisioning phase.

## Previous releases

### May 05, 2025

### Engine Enhancements_0505

- [MongoDB vCore v8 released](quickstart-portal.md).
  - Support $convert on binData to binData, string to binData and binData to string (except with format: auto).
  - Added support for `$toUUID` to simplify string-to-UUID conversion.
  - `$rank` and `$denseRank` now treat `null` and missing values the same while calculating rankings, aligning behavior with $sort.
  - Pipeline Size Enforcement- Aggregation throws an error if the pipeline stage limit is exceeded.
  - $getField now accepts any valid expression that resolves to a string, not just string constants.

#### Infrastructure Enhancements_0520

- [EntraID](entra-authentication.md) support (Preview).

### March 23, 2025

#### Engine Enhancements_0323

- Added support for [exact search](enn-vector-search.md) in vector search queries.
- Added support for the listDatabases command.
- Added support for type aggregation operator $toUUID.
- Added support for Partial filter pushdown for $in predicates.
- Added support for the $dateFromString operator with full functionality.
- Extended syntax for $getField aggregation operator. Now the value of 'field' could be an expression that resolves to a string.
- Added support for top-level aggregate command let variables in the $geoNear stage.
- Backend command support for statement time-out is now available.
- Introduced support for the $toUUID aggregation operator.
- Implemented full functionality for the $dateFromString operator.
- Extended $getField operator to accept expressions resolving to a string for the field parameter.
- Extended collation support to aggregation stages: $project, $ redact, $set, $addFields, $replaceRoot.
- Enabled collation support with comparison operators ($expr, $ in, $cmp, $eq, $ne, $lt, $lte, $gt, $gte).
- Enabled default support for unique index truncation using a new operator class.
- Introduced collation support with set operators in aggregation ($setEquals, $setUnion, $setIntersection, $setDifference,
  $setIsSubset).

#### Infrastructure Enhancements_0212

- Expanded regional availability.
  - South India
  - South Central US

### February 12, 2025

#### Engine Enhancements_0212

- Introduced open-source build of pg_documentdb targeting PostgreSQL 17.
- Added support for pushing $graphLookup recursive CTE JOIN filters to the index, improving query efficiency.
- Enabled support for the following aggregation stages and commands: currentOp, collStats, dbStats, and indexStats.
- Improved $lookup performance by allowing $unwind to be inlined when preserveNullAndEmptyArrays is enabled.
- Optimized aggregation by skipping document loading when the $group expression is a constant.

#### Infrastructure Enhancements_0212

- GAed [Autoscale SKU](autoscale.md).
- [Change stream](change-streams.md) support for Kafka Debezium connector & Pymongo driver. (Preview)
- Enabled [Promotion for Geo-Replica](cross-region-replication.md#replica-cluster-promotion).
- Expanded regional availability.
  - Switzerland West
  - Jio India West

### January 23, 2025

- We open sourced the engine behind Azure Cosmos DB for MongoDB vCore!
Check it out here: [DocumentDB](https://github.com/microsoft/documentdb/blob/main/README.md)

### October 14, 2024

- Index builds to run in background by default.
- Support for more options with $setWindowFields.
  - $integral.
  - $derivative.
  - $expMovingAvg.
  - $linearFill.
  - $locf.
  - $documentNumber.
  - $shift.
  - Added support for more operators with $group.
    - $top, $topN, $bottom, $bottomN, $first, $firstN, $last, $lastN, $maxN, $minN.
  - $max.
  - $min.
- Support added for aggregation operators.
  - $toHashedIndexKey.
- Support added for aggregation stages.
  - $fill.
- Added support for `wallTime` with ChangeStreams.

### September 16, 2024

- Gated Preview for [ChangeStream](change-streams.md).
- Gated Preview for Runtime support of Collation with $find / $ aggregate queries.
- [Large Index keys](how-to-create-indexes.md#enable-large-index-keys-by-default) enabled as default option for indexing.
- Added support for $DbRef with additional fields $ref/$id/$db, with limitation of the option with `elemMatch`.
- Support added for trigonometric aggregation operators.
- Support for more options with $setWindowFields.
  - $count.
  - $addToSet.
  - $push.
  - $avg.
  - $rank.
  - $denseRank.
  - $covariancePop
  - $covarianceSamp
- Support for $let with following.
  - $lookup.
  - $find.
  - $aggregate.
- Support for $merge aggregation stage with following.
  - whenMatched: "replace" / "keepExisting" / "merge" / "fail".
  - whenNotMatched: "insert" / "discard" / "fail".

### August 05, 2024

- [Geospatial support](geospatial-support.md) is now GA.
- [MongoDB vCore v7 released](how-to-upgrade-cluster.md).
- Support for TLS1.3 for mongo connections.
- Support for accumulators
  - $mergeObjects.
- Support for aggregation operators
  - $bitAnd.
  - $bitOr.
  - $bitXor.
  - $bitNot.
  - $let.
- Support for aggregation stage
  - $bucket.
  - $vectorSearch.
  - $setWindowFields (Only with $ sum window accumulator).
- Geospatial query operators
  - $minDistance.
  - $maxDistance.
  - $near.
  - $nearSphere.

### July 02, 2024

- Metrics added
  - Customer Activity.
  - Requests.

- Support for accumulators [Preview]
  - $mergeObjects.

- Support for aggregation operator [Preview]
  - $let.

- Geospatial query operators [Preview]
  - $minDistance.
  - $maxDistance.

### May 06, 2024

- Query operator enhancements.
  - $geoNear aggregation. Aggregation stage can be enabled through Flag - `Geospatial support for vCore "MongoDB for CosmosDB"`  (Preview feature)
  
  - Support for accumulators
    - $push.
    - $addToSet.
    - $tsSecond/$tsIncrement.
    - $map/$ reduce.
  - Support for date expressions
    - $dateAdd.
    - $dateSubtract.
    - $dateDiff.
  - Support for aggregation operators
    - $maxN/minN.
    - $sortArray.
    - $zip.

- Creating indexes with large index keys: values larger than 2.7 KB.
- Geo replicas enabling cross-region disaster recovery and reads scaling.
- Improved performance of group and distinct.
- Improved performance for $geoWithin queries with $centerSphere when radius is greater than π.

### April 16, 2024

- Query operator enhancements.
  - $centerSphere with index pushdown along with support for GeoJSON coordinates.
  - $graphLookup support.

- Performance improvements.
  - $exists, { $eq: null}, {$ne: null} by adding new index terms.
  - scans with $in/$nq/$ne in the index.
  - compare partial (Range) queries.

### March 18, 2024

- [Private Endpoint](how-to-private-link.md) support enabled on Portal.
- [HNSW](vector-search.md) vector index on M40 & larger cluster tiers.
- Enable Geo-spatial queries. (Preview)
- Query operator enhancements.
  - $centerSphere with index pushdown.
  - $min & $max operator with $project.
  - $binarySize aggregation operator.
- Ability to build indexes in background (except Unique indexes). (Preview)

### March 03, 2024

This release contains enhancements to the **Explain** plan and various vector filtering abilities.

- The API for MongoDB vCore allows filtering by metadata columns while performing vector searches.
- The `Explain` plan offers two different modes

  | | Description |
  | --- | --- |
  | **`allShardsQueryPlan`** | This mode is a new explain mode to view the query plan for all shards involved in the query execution. This mode offers a comprehensive perspective for distributed queries. |
  | **`allShardsExecution`** | This mode presents an alternative explain mode to inspect the execution details across all shards involved in the query. This mode provides you with comprehensive information to use in performance optimization. |

- Free tier support is available in more regions. These regions now include **East US 2**. For more information, see [Azure Cosmos DB pricing](https://azure.microsoft.com/pricing/details/cosmos-db/mongodb/).

- The ability to build indexes in the background is now available in preview.

## Related content

- [Azure updates for Azure Cosmos DB for MongoDB vCore](https://azure.microsoft.com/updates?category=databases&query=Cosmos%20DB%20MongoDB).
