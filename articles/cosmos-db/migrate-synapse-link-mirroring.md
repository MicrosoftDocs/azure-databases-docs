---
title: Migrate Azure Synapse Link to Mirroring for Fabric
titleSuffix: Azure Cosmos DB
description: Understand the conceptual differences between Azure Synapse Link and Mirroring for Fabric, and learn about migration considerations when moving between solutions.
author: jilmal
ms.author: jmaldonado
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 12/05/2025
---

# Migrate Azure Synapse Link to Azure Cosmos DB Mirroring for Microsoft Fabric

[!INCLUDE[NoSQL](includes/appliesto-nosql-mongo.md)]

Azure Synapse Link for Cosmos DB will be retired by 2028. Customers should begin preparations for migrating to Microsoft Fabric with Azure Cosmos DB Mirroring which provides the same zero-ETL hybrid transactional and analytical processing (HTAP) scenarios and provides significant benefits and features not possible with Synapse Link and Cosmos DB's analytical store.

Mirroring to Microsoft Fabric delivers superior analytical performance with open Delta Parquet format, seamless integration with the entire Microsoft Fabric ecosystem, unified data management in OneLake. Migrate from Azure Synapse Link to unlock these enhanced capabilities and future-proof your analytics infrastructure.

## Cosmos DB Mirroring for Fabric architecture

Mirroring replicates Azure Cosmos DB data into Microsoft Fabric OneLake:

* **OneLake replication**: Operational data is incrementally replicated into Fabric OneLake in near real-time using the continuous backup infrastructure to capture and replicate changes
* **Storage format**: Data is stored in open-source Delta Parquet format in OneLake
* **Query engines**: All Fabric compute engines (Spark, SQL, Power BI Direct Lake, and more) can access the data
* **Storage location**: Data is stored in OneLake, a unified logical data lake built on Azure Data Lake Storage Gen2

:::image type="content" source="./media/analytics-and-bi/fabric-mirroring-cosmos-db.png" alt-text="Diagram of Azure Cosmos DB mirroring in Microsoft Fabric." border="false":::

## Feature comparison matrix

| Feature | Mirroring for Fabric | Azure Synapse Link |
|---------|---------------------|-------------------|
| **Data format** | Open Delta Parquet | Proprietary columnar |
| **Storage location** | Fabric OneLake | Azure Cosmos DB analytical store |
| **Analytical TTL** | No (manual management required) | Yes (configurable per container) |
| **Schema nesting limits** | No limits | Yes (1,000 properties, 127 levels) |
| **Mixed data type handling** | Values with mismatched types show as NULL (first-seen type determines column type) | Values with mismatched types show as NULL (well-defined schema mode) |
| **Query engines** | Fabric Spark, Fabric SQL, Power BI | Synapse Spark, Synapse SQL |
| **Custom partitioning** | No | Yes |
| **Change feed support** | No (not currently supported on mirrored data) | Yes |
| **Multi-region write support** | Not supported | Not recommended for production |
| **Private endpoints** | No (requires public network access) | Yes (for analytical store) |
| **Customer-managed keys** | No (not supported in OneLake) | Yes (with managed identity) |
| **Network isolation** | Not supported | Supported |
| **Data sharing** | Through Fabric workspace and OneLake | Through Synapse workspace |
| **Open data access** | Yes (Delta Parquet accessible by external tools) | No (proprietary format) |
| **Backup dependency** | Requires continuous backup (7-day or 30-day) | No specific requirement |
| **APIs supported** | NoSQL only | NoSQL, MongoDB, Gremlin |


## Schema handling

**Mirroring for Fabric:**

* No nesting or property limits
* New columns added automatically; previous rows show NULL for new columns
* Nested JSON objects stored as JSON strings (use `OPENJSON`, `CROSS APPLY`, `OUTER APPLY` to expand)
* **Type handling**:
  * First value determines column data type
  * No automatic type conversion between incompatible types
  * Mixed types result in NULL values for mismatched data (for example, `Price` with `14` as integer makes subsequent `10.99` float values show as NULL)
  * To ensure accurate data representation, maintain consistent data types in your schema design or handle type conversions at the application layer

**Azure Synapse Link:**

* Maximum 1,000 properties across all nested levels (127 levels deep)
* **Schema modes**:
  * **Well-defined** (default for NoSQL API): First document defines base schema
  * **Full fidelity** (default for MongoDB API): Handles polymorphic schemas with mixed data types
* **Type evolution** (well-defined mode):
  * Allowed: `NULL` to any type, `integer` to `float`, `float` to `integer`
  * Incompatible types (for example, `integer` to `string`) show as NULL
  * Example: `"code": 123` then `"code": "123"` results in NULL for the second value
  * Arrays must contain single data type
* To ensure accurate data representation, migrate to a new container or add a new property (for example, `status2`)

## Data synchronization

**Mirroring for Fabric:**
* Automatically fails over to new read regions in disaster recovery scenarios
* Mirrors from the geographically closest Azure region to Fabric's capacity region

**Azure Synapse Link:**
* Controlled by the auto-sync process, which is fully managed
* Regional availability follows Azure Cosmos DB's global distribution


## Backup and restore considerations

**Mirroring for Fabric:**
* Requires continuous backup enabled on the Azure Cosmos DB account (7-day or 30-day)
* Stopping and restarting replication reseeds all target warehouse tables from scratch
* No incremental restore capability; replication always starts fresh
* OneLake data is subject to Fabric's data protection and disaster recovery policies
* You can't disable continuous backup once enabled on accounts using mirroring

**Azure Synapse Link:**
* Analytical store data is automatically synced from transactional store
* If you restore a container, you can rebuild the analytical store by reenabling Azure Synapse Link
* Analytical store follows the retention defined by analytical TTL
* When `analytical TTL` equals or exceeds `transactional TTL`, restored data can fully rebuild the analytical store
* When `analytical TTL` is less than `transactional TTL`, some historical data might be lost in restoration

## Pricing and cost model

**Mirroring for Fabric:**

* **Storage**: Free up to a limit based on capacity size (for example, an F64 capacity includes 64 TB of free storage exclusively for mirroring). Storage billed above that.
* **Query compute**: Compute for querying data using SQL, Power BI, or Spark is charged at regular Fabric capacity rates
* **Continuous backup prerequisite**: 7-day continuous backup mode is free of cost and 30-day continuous backup incurs standard Azure Cosmos DB charges
* **Data egress**: Charged only if your Azure Cosmos DB account is in a different region than your Fabric capacity

**Azure Synapse Link:**

* **Replication compute**: The fully managed synchronization of operational data updates to the analytical store from the transactional store is billed as analytical write operations
* **Storage**: Charged for the volume of data retained in the analytical store every month, including historical data as defined by analytical TTL
* **Query compute**: Charged for Azure Synapse Analytics runtime costs when using Spark pools and serverless SQL pools to query the data
* **Data egress**: No charges when Synapse queries route to analytical store in the same region (default behavior). Charges apply only if you manually configure queries to access analytical store in a different region



## Migration considerations

### Migrating from Azure Synapse Link to Mirroring for Fabric

When planning a migration from Azure Synapse Link to Mirroring for Fabric, consider the following:

#### Prerequisites and account configuration

1. **Continuous backup requirement**:
   * You must enable continuous backup (7-day or 30-day) on your Azure Cosmos DB account
   * You can't disable continuous backup once enabled
   * Continuous backup has specific limitations, including lack of support for multi-region write accounts
   * You can enable both analytical store and continuous backup on the same account

1. **Network configuration changes**:
   * Source Azure Cosmos DB account must enable public network access for all networks
   * Private endpoints aren't supported for source accounts

1. **Authentication updates**:
   * Prepare read-write account keys or Microsoft Entra ID with appropriate RBAC permissions
   * Required RBAC permissions: `Microsoft.DocumentDB/databaseAccounts/readMetadata` and `Microsoft.DocumentDB/databaseAccounts/readAnalytics`
   * Read-only keys and managed identities aren't supported for mirroring connections

#### Data retention strategy changes

> [!NOTE] Mirrored data in Fabric is read-only and maintains a 1:1 copy of the source database.

1. **Analytical TTL replacement**:
   * Identify containers using analytical TTL for data retention
   * Design alternative retention strategies using Fabric capabilities

1. **Cold storage implementation in Fabric**:
   * Since Mirroring doesn't provide native TTL capabilities and mirrored data is read-only, you need to implement custom cold storage solutions using Fabric capabilities and downstream processing. Mirrored data maintains a 1:1 copy of your source data, so retention policies must be applied to Delta tables created from the mirrored data, not to the mirrored data itself.

#### Query and application migration

1. **Query language compatibility**:
   * Synapse SQL queries might need modification for Fabric SQL analytics endpoint
   * Review T-SQL limitations in Fabric
   * Nested data handling requires different approaches (OPENJSON instead of direct column access)
   * Update queries to account for JSON string representation of nested objects

1. **Spark workload migration**:
   * Synapse Spark notebooks can be adapted for Fabric Spark
   * Update connection strings and authentication methods
   * Review Delta Lake-specific optimizations available in Fabric (V-Order, predictive optimization)
   * Test performance characteristics as execution engines differ

1. **Power BI integration**:
   * Migrate from Synapse SQL pool connections to Direct Lake mode in Fabric
   * Direct Lake provides faster performance and eliminates data duplication
   * Update data refresh schedules and gateway configurations if needed

#### Schema and data considerations

1. **Schema flexibility**:
   * Mirroring removes the 1,000-property and 127-level nesting limits
   * Review if your data models benefit from this increased flexibility
   * Nested data is represented as JSON strings; plan for flattening operations where needed

1. **Custom partitioning**:
   * Custom partitioning from Synapse Link isn't supported in Mirroring
   * Evaluate query patterns and consider alternative optimization strategies
   * Use Delta table partitioning within OneLake for similar benefits

1. **Change feed considerations**:
   * Azure Cosmos DB change feed isn't currently supported on mirrored data in Fabric
   * If you rely on change feed for downstream processing, you need to maintain separate change feed consumers
   * Mirroring tracks inserts, updates, and deletes automatically through the replication process
   * Soft-delete operations using TTL aren't supported; deletes are immediately reflected in mirrored data

#### Operational changes

1. **Monitoring and diagnostics**:
   * Migrate from Azure Monitor metrics for Synapse Link to Fabric monitoring tools
   * Update alerting rules and dashboards
   * Replication status is monitored through the Fabric portal instead of Azure portal

1. **Security and compliance**:
   * Review and update role-based access control policies
   * Fabric workspace permissions automatically grant access to mirrored data
   * Implement row-level security, column-level security, or dynamic data masking in Fabric as needed
   * Update compliance documentation to reflect OneLake storage instead of analytical store

1. **Cost management**:
   * Evaluate total cost of ownership including storage, compute, and Power BI licensing
   * Consider costs for any custom cold storage solutions you implement
   * See the [Pricing and cost model](#pricing-and-cost-model) section for detailed comparison

## Decision framework

### Mirroring for Fabric (Recommended)

Mirroring for Fabric is the recommended analytics solution for Azure Cosmos DB. Choose Mirroring when you need:

* Open data format (Delta Parquet) for multi-platform access and future flexibility
* Unified data estate with other Fabric lakehouses and warehouses
* Direct Lake mode for Power BI with real-time reporting and superior performance
* No schema nesting constraints for complex data models
* Integration with Fabric AI and Copilot features for advanced analytics
* Simplified analytics across multiple data sources in OneLake
* GraphQL API access for modern application integration
* Better analytical query performance for large-scale workloads

### Azure Synapse Link considerations

If you currently use Azure Synapse Link, consider migrating to Mirroring for Fabric. However, Azure Synapse Link might remain suitable for specific scenarios:

* You have strict network isolation requirements with private endpoint dependencies
* Customer-managed key encryption is mandatory for analytical data
* You rely heavily on custom partitioning for existing query patterns
* You need built-in analytical TTL and can't implement alternative retention strategies

### Migration planning

For existing Azure Synapse Link deployments:

* Plan your migration to Mirroring for Fabric to take advantage of enhanced capabilities
* Evaluate network security requirements and plan for public network access
* Design data retention strategies using Fabric capabilities to replace analytical TTL
* Test workloads in Mirroring to validate performance improvements
* Gradually migrate workloads based on priority, starting with new analytics projects

## Next steps

* [Mirroring Azure Cosmos DB in Microsoft Fabric](/fabric/database/mirrored-database/azure-cosmos-db?context=/azure/cosmos-db/context/context)
* [Tutorial: Get started with mirroring in Microsoft Fabric](/fabric/database/mirrored-database/azure-cosmos-db-tutorial?context=/azure/cosmos-db/context/context)
* [Limitations in Microsoft Fabric mirrored databases from Azure Cosmos DB](/fabric/database/mirrored-database/azure-cosmos-db-limitations?context=/azure/cosmos-db/context/context)
