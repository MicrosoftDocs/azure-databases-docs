---
title: Service release notes
description: Explore Azure DocumentDB release notes with feature updates, engine enhancements, and infrastructure improvements grouped by date. Stay current with the latest capabilities.
author: avijitgupta
ms.author: avijitgupta
ms.topic: release-notes
ms.date: 11/20/2025
ai-usage: ai-assisted
ms.custom:
  - references_regions 
---

# Azure DocumentDB release notes

Azure DocumentDB continuously evolves with new features, performance improvements, and infrastructure enhancements. This article provides a comprehensive history of feature releases, engine updates, and service improvements for Azure DocumentDB. Each release includes details about new capabilities, query operator enhancements, and infrastructure changes to help you stay current with the latest developments.

> [!NOTE]
> Items tagged as **\[Preview\]** require a support request to enable them on your cluster.

## Latest

> [!IMPORTANT]
> Azure Cosmos DB for MongoDB (vCore) is now **Azure DocumentDB (with MongoDB compatibility)**, powered by the open-source DocumentDB project.

This **November 18, 2025** release renames the service from **Azure Cosmos DB for MongoDB (vCore)** to **Azure DocumentDB** along with other feature changes.

### Enhancements

- Index Advisor feature in Visual Studio Code: Built-in guidance for index tuning, performance insights, and query optimization. For more information, see [Index Advisor feature](index-advisor.md).

- MongoDB Migration extension for Visual Studio Code: End-to-end online migration experience for various workloads. For more information, see [migrate using Visual Studio Code extension](how-to-migrate-vs-code-extension.md).

- **\[Preview\]** Premium SSD v2 support: Next-generation storage delivering better performance at no extra cost. For more information, see [high performance storage](high-performance-storage.md).

- Reserved instances support: Save on costs over one-year or three-year terms. For more information, see [Azure DocumentDB pricing](https://azure.microsoft.com/pricing/details/document-db/).

- Advanced full-text search: fuzzy search and proximity matching supported. For more information, see [hybrid search](hybrid-search.md)

- Azure Cosmos DB for MongoDB to Azure DocumentDB migration: Integrated path for users moving from Azure Cosmos DB for MongoDB to Azure DocumentDB.

## October 10, 2025

This **October 10, 2025** release introduces schema validation with `$jsonSchema`, enhanced TTL index performance, and general availability of customer-managed keys and Microsoft Entra ID authentication.

### Engine enhancements (1017)

- **\[Preview\]** Add support for index pushdown for sort queries that filter on the `_id` field.

- **\[Preview\]** Add schema validation support for [`$jsonSchema`](./operators/evaluation-query/$jsonschema.md) during rule creation or modification.

- **\[Preview\]** Add schema enforcement with CSFLE (client side field level encryption) integration.

- **\[Preview\]** Time-to-live (TTL) index uses ordered index scan via index hints. TTL index performs batch deletions continuously for up to 60 seconds, instead of once every 60 seconds.

### Infrastructure enhancements (1017)

- Includes features from API version `2025-09-01`:

  - Data API

  - Microsoft Entra ID authentication

  - Ability to disable native auth.

  - Customer-managed key (CMK)

## August 29, 2025

This release focuses on query performance improvements with index hints, enhanced commands, and bug fixes for aggregation operators.

### Engine Enhancements (0829)

- Introduced support for index hints. This feature allows you to explicitly specify an index during query execution.

- **\[Preview\]** Enabled index-only scans on ordered indexes for count queries where filters can be pushed down to the index and no projections are applied.

- **\[Preview\]** Improved parallel index build performance.

- Improved point lookup queries for more efficient execution.

- Enhanced `usersInfo` and `connectionStatus` commands to return all supported roles (`ReadWrite`, `UserAdmin`, `Root`) and privilege sets (`dbAdmin`, `userAdmin`, `clusterMonitor`, `clusterManager`, `hostManager`).

- Improved query planning performance by introducing a custom planner for insert operations.

- Fix bug in `$lastN` and `$bottomN`.

- Fixed Response type of update to add compatibility to C++ drivers requiring response in 32 bit.

- Enhanced error messages for output stages `$merge` and `$out`.

### Infrastructure Enhancements (0909)

- [Customer-managed keys (CMK)](database-encryption-at-rest.md) support general availability.

- [Microsoft Entra ID](how-to-connect-role-based-access-control.md) support general availability.

## July 15, 2025

This release brings index optimization improvements, HNSW index support for M30 tier, and enhanced TTL index behavior for better performance.

### Engine Enhancements (0715)

- **\[Preview\]** Enabled index pushdown optimization for `$sort` on any field.

- Enabled index pushdown optimization for `$limit`.

- **\[Preview\]** Added support for composite indexes on filter conditions.

- Added support for Hierarchical navigable small world (HNSW) index for M30 cluster tier.

- Enhanced TTL index behavior to continue processing even if the cluster becomes read-only due to disk full.

- Improvements to parallel build for faster index creation on sharded and unsharded collection.

### Infrastructure Enhancements (0730)

- **\[Preview\]** Added support for CMK, allowed only during provisioning phase.

## May 05, 2025

This release includes v8 engine with enhanced data type conversion, improved ranking operators, and pipeline validation improvements.

- [v8 released](quickstart-portal.md).

  - Support `$convert` on binData to binData, string to binData and binData to string (except with format: auto).

  - Added support for `$toUUID` to simplify string-to-UUID conversion.

  - `$rank` and `$denseRank` now treat `null` and missing values the same while calculating rankings, aligning behavior with `$sort`.

  - Pipeline Size Enforcement - Aggregation throws an error if the pipeline stage limit is exceeded.

  - `$getField` now accepts any valid expression that resolves to a string, not just string constants.

### Infrastructure Enhancements (0520)

- **\[Preview\]** [Microsoft Entra ID](how-to-connect-role-based-access-control.md) support.

## March 23, 2025

This release adds exact vector search, expanded collation support across aggregation stages, and UUID conversion capabilities.

### Engine Enhancements (0323)

- Added support for [exact search](enn-vector-search.md) in vector search queries.

- Added support for the listDatabases command.

- Added support for type aggregation operator `$toUUID`.

- Added support for **partial** filter pushdown for `$in` predicates.

- Added support for the `$dateFromString` operator with full functionality.

- Extended syntax for `$getField` aggregation operator. Now the value of 'field' could be an expression that resolves to a string.

- Added support for top-level aggregate command let variables in the `$geoNear` stage.

- Backend command support for statement time out is now available.

- Introduced support for the `$toUUID` aggregation operator.

- Implemented full functionality for the `$dateFromString` operator.

- Extended `$getField` operator to accept expressions resolving to a string for the field parameter.

- Extended collation support to aggregation stages: `$project`, `$redact`, `$set`, `$addFields`, `$replaceRoot`.

- Enabled collation support with comparison operators (`$expr`, `$in`, `$cmp`, `$eq`, `$ne`, `$lt`, `$lte`, `$gt`, `$gte`).

- Enabled default support for unique index truncation using a new operator class.

- Introduced collation support with set operators in aggregation (`$setEquals`, `$setUnion`, `$setIntersection`, `$setDifference`, `$setIsSubset`).

### Infrastructure Enhancements (0212)

- Expanded regional availability.

  - `South India`

  - `South Central US`

## February 12, 2025

This release introduces the open-source PostgreSQL 17 build, optimized aggregation performance, and general availability of autoscale with geo-replica promotion support.

### Engine Enhancements (0212)

- Introduced open-source build of `pg_documentdb` targeting PostgreSQL 17.

- Added support for pushing `$graphLookup` recursive Common Table Expression (CTE) JOIN filters to the index, improving query efficiency.

- Enabled support for the following aggregation stages and commands: `currentOp`, `collStats`, `dbStats`, and `indexStats`.

- Improved `$lookup` performance by allowing `$unwind` to be inlined when `preserveNullAndEmptyArrays` is enabled.

- Optimized aggregation by skipping document loading when the `$group` expression is a constant.

### Infrastructure Enhancements (0212)

- [Autoscale](autoscale.md) generally available.

- **\[Preview\]** [Change stream](change-streams.md) support for Kafka Debezium connector & Pymongo driver.

- Enabled [Promotion for Geo-Replica](cross-region-replication.md#replica-cluster-promotion).

- Expanded regional availability.

  - `Switzerland West`

  - `Jio India West`

## January 23, 2025

This release marks a significant milestone with the open-source release of the Azure DocumentDB engine.

- We open sourced the engine behind Azure DocumentDB! For more information, see [https://github.com/documentdb](https://github.com/documentdb/documentdb#introduction).

## October 14, 2024

This release enables background index builds by default, expands `$setWindowFields` capabilities, and adds support for the `$fill` aggregation stage.

- Index builds to run in background by default.

- Support for more options with `$setWindowFields`.

  - `$integral`.

  - `$derivative`.

  - `$expMovingAvg`.

  - `$linearFill`.

  - `$locf`.

  - `$documentNumber`.

  - `$shift`.

  - Added support for more operators with `$group`.

    - `$top`, `$topN`, `$bottom`, `$bottomN`, `$first`, `$firstN`, `$last`, `$lastN`, `$maxN`, `$minN`.

  - `$max`.

  - `$min`.

- Support added for aggregation operators.

  - `$toHashedIndexKey`.

- Support added for aggregation stages.

  - `$fill`.

- Added support for `wallTime` with ChangeStreams.

## September 16, 2024

- Gated Preview for [ChangeStream](change-streams.md).

- Gated Preview for Runtime support of Collation with `$find` / `$aggregate` queries.

- [Large Index keys](how-to-create-indexes.md#enable-large-index-keys-by-default) enabled as default option for indexing.

- Added support for `$DbRef` with more fields `$ref`/`$id`/`$db`, with limitation of the option with `elemMatch`.

- Support added for trigonometric aggregation operators.

- Support for more options with `$setWindowFields`.

  - `$count`.

  - `$addToSet`.

  - `$push`.

  - `$avg`.

  - `$rank`.

  - `$denseRank`.

  - `$covariancePop`

  - `$covarianceSamp`

- Support for `$let` with following.

  - `$lookup`.

  - `$find`.

  - `$aggregate`.

- Support for `$merge` aggregation stage with following.

  - whenMatched: `replace` / `keepExisting` / `merge` / `fail`.

  - whenNotMatched: `insert` / `discard` / `fail`.

## August 05, 2024

- [Geospatial support](geospatial-support.md) is now generally available.

- [v7 released](how-to-upgrade-cluster.md).

- Support for TLS1.3 for mongo connections.

- Support for accumulators

  - `$mergeObjects`.

- Support for aggregation operators

  - `$bitAnd`.

  - `$bitOr`.

  - `$bitXor`.

  - `$bitNot`.

  - `$let`.

- Support for aggregation stage

  - `$bucket`.

  - `$vectorSearch`.

  - `$setWindowFields` (Only with `$sum` window accumulator).

- Geospatial query operators

  - `$minDistance`.

  - `$maxDistance`.

  - `$near`.

  - `$nearSphere`.

## July 02, 2024

This release adds new customer activity and request metrics, plus preview support for geospatial operators and accumulator enhancements.

- Metrics added

  - Customer Activity.

  - Requests.

- **\[Preview\]** Support for accumulators

  - `$mergeObjects`.

- **\[Preview\]** Support for aggregation operator

  - `$let`.

- **\[Preview\]** Geospatial query operators

  - `$minDistance`.

  - `$maxDistance`.

### May 06, 2024

This release introduces geospatial aggregation, large index key support, geo-replicas, and performance improvements for group and distinct operations.

- Query operator enhancements.

  - `$geoNear` aggregation. Aggregation stage can be enabled through Flag - `Geospatial support`
  
  - Support for accumulators

    - `$push`.

    - `$addToSet`.

    - `$tsSecond`/`$tsIncrement`.

    - `$map`/`$reduce`.

  - Support for date expressions

    - `$dateAdd`.

    - `$dateSubtract`.

    - `$dateDiff`.

  - Support for aggregation operators

    - `$maxN`/`$minN`.

    - `$sortArray`.

    - `$zip`.

- Creating indexes with large index keys: values larger than 2.7 KB.

- Geo replicas enabling cross-region disaster recovery and reads scaling.

- Improved performance of group and distinct.

- Improved performance for `$geoWithin` queries with `$centerSphere` when radius is greater than π.

## April 16, 2024

This release adds `$graphLookup` support and significant performance improvements for existence checks, range queries, and indexed scans.

- Query operator enhancements.

  - `$centerSphere` with index pushdown along with support for GeoJSON coordinates.

  - `$graphLookup` support.

- Performance improvements.

  - `$exists`, `{ $eq: null }`, `{ $ne: null }` by adding new index terms.

  - scans with `$in`/`$nq`/`$ne` in the index.

  - compare partial (**range**) queries.

## March 18, 2024

This release adds portal support for private endpoints, HNSW vector indexing for M40+ tiers, and preview of geospatial queries with background index builds.

- [Private Endpoint](how-to-private-link.md) support enabled on Portal.

- [HNSW](vector-search.md) vector index on M40 & larger cluster tiers.

- **\[Preview\]** Enable Geo-spatial queries.

- Query operator enhancements.

  - `$centerSphere` with index pushdown.

  - `$min` & `$max` operator with `$project`.

  - `$binarySize` aggregation operator.

- **\[Preview\]** Ability to build indexes in background (except Unique indexes).

## March 03, 2024

This release contains enhancements to the **Explain** plan and various vector filtering abilities.

- Allows filtering by metadata columns while performing vector searches.

- The `Explain` plan offers two different modes

  | | Description |
  | --- | --- |
  | **`allShardsQueryPlan`** | This mode is a new explain mode to view the query plan for all shards involved in the query execution. This mode offers a comprehensive perspective for distributed queries. |
  | **`allShardsExecution`** | This mode presents an alternative explain mode to inspect the execution details across all shards involved in the query. This mode provides you with comprehensive information to use in performance optimization. |

- Free tier support is available in more regions. These regions now include **East US 2**. For more information, see [Azure DocumentDB pricing](https://azure.microsoft.com/pricing/details/document-db/).

- The ability to build indexes in the background is now available in preview.

## Related content

- [Azure updates for Azure DocumentDB](https://azure.microsoft.com/updates?category=databases&query=Cosmos%20DB%20MongoDB)
