---
title: Service limits and Quotas Reference
description: Comprehensive reference of Azure DocumentDB service limits, quotas, and constraints including query, indexing, cluster, and authentication limits. Learn about MongoDB execution limits, indexing constraints, and cluster tier specifications.
author: gahl-levy
ms.author: gahllevy
ms.topic: limits-and-quotas
ms.date: 11/05/2025
---

# Azure DocumentDB service limits and quotas reference

This document outlines the current hard and soft limits for Azure DocumentDB clusters and operations. Learn about query execution limits, indexing constraints, cluster configurations, and authentication boundaries that help you plan and optimize your Azure DocumentDB deployments effectively.

## Query and execution limitations

The following limits apply to query operations and command execution in Azure DocumentDB clusters.

### MongoDB execution limitations

- Maximum transaction lifetime: 30 seconds.

- Cursor lifetime: 10 minutes. Note: A cursorNotFound error might occur if the cursor exceeds its lifetime.

- Default query execution limit: 120 seconds. This limit can be overridden on a per-query basis using `maxTimeMS` in the respective MongoDB driver.

#### Example

```mongodb
db.collection.find({ field: "value" }).maxTimeMS(5000)
```

### Maximum MongoDB query size

- The maximum memory size for MongoDB queries depends on the tier. For example, for M80, the query memory size limit is approximately 150 MiB.

- In sharded clusters, if a query pulls data across nodes, the limit on that data size is 1 GB.

## Indexing limitations

Azure DocumentDB enforces various indexing limits to ensure optimal performance and resource utilization across different index types and operations.

### General indexing limitations

- Maximum number of compound index fields: 32.

- Maximum size for `_id` field value: 2 KB.

- Maximum size for index path: 256B.

- Default maximum: 64.

  - Configurable up to: 300 indexes per collection.

- Sorting is done in memory and doesn't push down to the index.

- Maximum level of nesting for embedded objects/arrays on index definitions: 6.

- A single index build can be in progress on the same collection.

- The number of simultaneous index builds on different collections is configurable (default: 2).

- Use the `currentOp` command to view the progress of long-running index builds.

- Unique index builds are done in the foreground and block writes in the collection.

### Wildcard indexing limitations

- For wildcard indexes, if the indexed field is an array of arrays, the entire embedded array is taken as a value instead of traversing its contents.

### Geospatial indexing limitations

- No support for BigPolygons.

- Composite indexes don't support geospatial indexes.

- `$geoWithin` query doesn't support polygons with holes.

- The `key` field is required in the `$geoNear` aggregation stage.

- Indexes are recommended but not required for `$near`, `$nearSphere` query operators, and the `$geoNear` aggregation stage.

### Text index limitations

- Only one text index can be defined on a collection.

- Supports simple text searches only; advanced search capabilities like regular expression searches aren't supported.

- `hint()` isn't supported in combination with a query using `$text` expression.

- Sort operations can't use the ordering of the text index.

- Tokenization for Chinese, Japanese, Korean isn't supported.

- Case insensitive tokenization isn't supported.

### Vector search limitations

- Indexing vectors up to 16,000 dimensions in size (with [Product Quantization](./product-quantization.md))

- Indexing applies to only one vector per path.

- Only one index can be created per vector path.

- `HNSW` and `DiskANN` are available on M30 and greater cluster tiers. 

## Cluster and shard limitations

Azure DocumentDB imposes specific limits on cluster configuration, physical sharding, and collection management to ensure optimal performance and resource allocation.

### Cluster tier

- Maximum: M200 / 64 vCores / 256-GiB RAM per physical shard.

### Physical shards

- Maximum: 10.

### Collection limitations

-	Collections per cluster: 1,000

-	Unsharded collection size: 32 TiB

### Secondary regions

- Maximum: One secondary region.

### Free tier limitations

The following limitations can be overridden by upgrading to a paid tier

- Maximum storage: 32 GiB.

- Backup / Restore not supported (available in M25+)

- High availability (HA) not supported (available in M30+)

- Hierarchical navigable small world (HNSW) vector indexes not supported (available in M40+)

- Diagnostic logging not supported (available only in paid tiers)

- Microsoft Entra ID not supported

- No service-level-agreement provided (requires HA to be enabled)

- Free tier clusters are paused after 60 days of inactivity where there are no connections to the cluster.

- Transition from a paid tier account to a free tier accounts isn't supported.

### Tier limits

M10, M20, and M25 service tiers have the following limitations:

- Supports one physical shard (node) only.

- Designed for Dev/Test use cases; in-region high availability (HA) isn't supported.

- Supported storage sizes include 32 GiB, 64 GiB, and 128 GiB.

- Once cluster is scaled to M30 tier or higher, the cluster can't be scaled back down to M10, M20, or M25 compute tier.

### Customer-managed key data encryption limitations

The following are the current limitations for configuring [the customer-managed key (CMK)](./database-encryption-at-rest.md#data-encryption-in-azure-documentdb) in an Azure DocumentDB:

- The instance of Azure Key Vault and user-assigned managed identity must be in the same Azure region and in the same [Microsoft tenant](/entra/identity-platform/developer-glossary#tenant) as the Azure DocumentDB cluster.

- After you create a cluster, you can't change the data encryption mode from system-managed key to customer-managed key or vice versa.

    - You can create [a replica cluster or perform cluster restore](./how-to-data-encryption.md#change-data-encryption-mode-on-existing-clusters) and choose a different encryption mode.

- [Add physical shard operation](./how-to-scale-cluster.md#increase-the-number-of-physical-shards) isn't supported on clusters with CMK enabled.

## Replication and in-region high availability limits

Azure DocumentDB provides built-in replication and high availability (HA) features with specific limitations to ensure data consistency and performance across different deployment scenarios.

### Cross-region and same region replication

- The following configurations are the same on both primary and replica clusters and can't be changed on the replica cluster:

  - Storage and physical shard count

  - User accounts

- The following features aren't available on replica clusters:

  - Point-in-time restore (PITR)

  - In-region high availability (HA)

- Replication isn't available on clusters with [burstable compute](./compute-storage.md#what-is-burstable-compute) or [Free tier](./free-tier.md) clusters.

## Authentication and access control (role-based access control)

Azure DocumentDB enforces authentication and access control limits to maintain security and manage resource allocation across user accounts and roles.

- You can create up to 100 total users/roles per cluster.

### Microsoft Entra ID authentication

The [Microsoft Entra ID authentication](./how-to-connect-role-based-access-control.md) feature has these current limitations:

- This feature doesn't support Microsoft Entra ID groups.

- When native DocumentDB authentication method is disabled, MongoDB Shell isn't supported in the Azure portal's **Quick start**.
    - You can [use MongoDB Shell with Microsoft Entra ID authentication](./how-to-connect-role-based-access-control.md#connect-using-microsoft-entra-id-in-mongodb-compass-or-mongodb-shell) outside of the Azure portal. 

### Native DocumentDB secondary users

[The native secondary users](./secondary-users.md) feature has these limitations:

- The `Updateuser` command now only supports password updates and can't modify other object fields.

- The `Roleinfo` command isn't supported. Alternatively, you can use `usersInfo`.

- Assigning roles to specific databases or collections isn't supported, only cluster level is supported.

## Miscellaneous limitations

Azure DocumentDB has more operational and feature-specific limits that apply to various aspects of cluster management and functionality.

### Portal Mongo shell usage

- The Portal Mongo shell can be used for 120 minutes within a 24-hour window.

### Document size and depth

- Maximum Binary JavaScript Object Notation (BSON) document size: 16 MB per document.

- No fixed maximum nesting depth limit is enforced.

  - Deeply nested document structures might affect query and read performance, increase processing overhead, and reduce maintainability.

### Batch limits

- Both batch operation types (write and bulk) are supported.

  - A batch refers to a **single request** to the server.

- Maximum writes per batch operation: **25,000 writes**.

- Batch operations exceeding 25,000 writes will **fail**.

- No limit on the total number of batch operations.

## Related content

- [Create a cluster](quickstart-portal.md).
- [Migrate from MongoDB to Azure DocumentDB](migration-options.md).
