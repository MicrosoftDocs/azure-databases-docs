---
title: Service limits in Azure Cosmos DB for MongoDB vCore
description: This document outlines the service limits for vCore-based Azure Cosmos DB for MongoDB.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.custom:
  - ignite-2024
  - build-2025
ms.topic: limits-and-quotas
ms.date: 10/27/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Service limits in Azure Cosmos DB for MongoDB vCore

This document outlines the current hard and soft limits for Azure Cosmos DB for MongoDB vCore. Many of these limitations are temporary and will evolve over time as the service continues to improve. If any of these limits are an issue for your organization, [reach out to our team](mailto:mongodb-feedback@microsoft.com) for assistance.

## Query and execution limits

### MongoDB Execution Limits
- Maximum transaction lifetime: 30 seconds.
- Cursor lifetime: 10 minutes. Note: A cursorNotFound error might occur if the cursor exceeds its lifetime.
- Default query execution limit: 120 seconds. This can be overridden on a per-query basis using `maxTimeMS` in the respective MongoDB driver.
#### Example:
```javascript
db.collection.find({ field: "value" }).maxTimeMS(5000)
```

### Maximum MongoDB Query Size
- The maximum memory size for MongoDB queries depends on the tier. For example, for M80, the query memory size limit is approximately 150 MiB.
- In sharded clusters, if a query pulls data across nodes, the limit on that data size is 1 GB.

## Indexing limits

### General Indexing Limits
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

### Wildcard Indexing Limits
- For wildcard indexes, if the indexed field is an array of arrays, the entire embedded array is taken as a value instead of traversing its contents.

### Geospatial Indexing Limits
- No support for BigPolygons.
- Composite indexes don't support geospatial indexes.
- `$geoWithin` query doesn't support polygons with holes.
- The `key` field is required in the `$geoNear` aggregation stage.
- Indexes are recommended but not required for `$near`, `$nearSphere` query operators, and the `$geoNear` aggregation stage.

### Text Index Limits
- Only one text index can be defined on a collection.
- Supports simple text searches only; advanced search capabilities like regular expression searches aren't supported.
- `hint()` isn't supported in combination with a query using `$text` expression.
- Sort operations can't use the ordering of the text index.
- Tokenization for Chinese, Japanese, Korean isn't supported yet.
- Case insensitive tokenization isn't supported yet.

### Vector Search Limits
- Indexing vectors up to 2,000 dimensions in size.
- Indexing applies to only one vector per path.
- Only one index can be created per vector path.
- `HNSW` and `DiskANN` are available on M30 and greater cluster tiers. 

## Cluster and shard limits

### Cluster tier
- Maximum: M200 / 64 vCores / 256 GiB RAM per physical shard. [Reach out to our team](mailto:mongodb-feedback@microsoft.com) for higher tiers.

### Physical shards
- Maximum: 10. [Reach out to our team](mailto:mongodb-feedback@microsoft.com) for more shards.

### Collection limits
-	Collections per cluster: 1,000
-	Unsharded collection size: 32 TiB

[Reach out to our team](mailto:mongodb-feedback@microsoft.com) for the higher values support.

### Secondary regions
- Maximum: One secondary region. [Reach out to our team](mailto:mongodb-feedback@microsoft.com) for more regions.

### Free Tier limits
The following limitations can be overridden by upgrading to a paid tier
- Maximum storage: 32 GiB.
- Backup / Restore not supported (available in M25+)
- High availability (HA) not supported (available in M30+)
- HNSW vector indexes not supported (available in M40+)
- Diagnostic logging not supported (available in M40+)
- Microsoft Entra ID not supported
- No service-level-agreement provided (requires HA to be enabled)
- Free tier clusters are paused after 60 days of inactivity where there are no connections to the cluster.
- Transition from a paid tier account to a free tier accounts isn't supported.

### M10/M20/M25 limits
M10, M20, and M25 have the following limitations:
- Supports one physical shard (node) only.
- Designed for Dev/Test use cases; in-region high availability (HA) isn't supported.
- Supported storage sizes include 32 GiB, 64 GiB, and 128 GiB.
- Once cluster is scaled to M30 tier or higher, the cluster can't be scaled back down to M10, M20, or M25 compute tier.

### Customer-managed key data encryption limitations
The following are the current limitations for configuring [the customer-managed key (CMK)](./database-encryption-at-rest.md#data-encryption-in-azure-cosmos-db-for-mongodb-vcore) in an Azure Cosmos DB for MongoDB vCore:

- The instance of Azure Key Vault and user-assigned managed identity must be in the same Azure region and in the same [Microsoft tenant](/entra/identity-platform/developer-glossary#tenant) as the Azure Cosmos DB for MongoDB vCore cluster.
- After you create a cluster, you can't change the data encryption mode from system-managed key to customer-managed key or vice versa.
    - You can create [a replica cluster or perform cluster restore](./how-to-data-encryption.md#change-data-encryption-mode-on-existing-clusters) and choose a different encryption mode.
- [Add physical shard operation](./how-to-scale-cluster.md#increase-the-number-of-physical-shards) isn't supported on clusters with CMK enabled.

## Replication and in-region HA (high availability) limits

### Cross-region and same region replication
- The following configurations are the same on both primary and replica clusters and can't be changed on the replica cluster:
  - Storage and physical shard count
  - User accounts
- The following features aren't available on replica clusters:
  - Point-in-time restore (PITR)
  - In-region high availability (HA)
- Replication isn't available on clusters with [burstable compute](./burstable-tier.md) or [Free tier](./free-tier.md) clusters.

## Authentication and access control (RBAC)

- You can create up to 100 total users/roles per cluster. [Reach out to our team](mailto:mongodb-feedback@microsoft.com) to increase the default limit on your cluster.

### Microsoft Entra ID authentication

The [Microsoft Entra ID authentication](./entra-authentication.md) feature has these current limitations:
- This feature doesn't support Entra ID groups.
- When native DocumentDB authentication method is disabled, MongoDB Shell isn't supported in the Azure portal's **Quick start**.
    - You can [use MongoDB Shell with Entra ID authentication](./how-to-configure-entra-authentication.md?#connect-to-the-cluster-using-entra-id-in-mongodb-shell) outside of the Azure portal. 

### Native DocumentDB secondary users

[The native secondary users](./secondary-users.md) feature has these limitations:
- The `Updateuser` command now only supports password updates and can't modify other object fields.
- The `Roleinfo` command isn't supported. Alternatively, you can use `usersInfo`.
- Assigning roles to specific databases or collections isn't supported, only cluster level is supported.

## Miscellaneous limits

### Portal Mongo shell usage
- The Portal Mongo shell can be used for 120 minutes within a 24-hour window.

## Next steps

- Get started by [creating a cluster](quickstart-portal.md).
- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB vCore](migration-options.md).
