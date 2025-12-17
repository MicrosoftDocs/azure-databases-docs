---
title: Service Quotas and Default Limits
description: Learn about Azure Cosmos DB service quotas and default limits for operations, storage, and throughput. Optimize your database performance today.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 09/03/2025
ms.custom: build-2023
ai-usage: ai-assisted
applies-to:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Azure Cosmos DB service quotas and default limits

This article explains the default quotas and limits for Azure Cosmos DB resources. It helps you manage operations, storage, and throughput effectively.

## Storage and database operations

After you create an Azure Cosmos DB account under your subscription, you can manage data in your account by [creating databases, containers, and items](resource-model.md).

### Provisioned throughput

You allocate throughput at the container level or the database level in terms of [request units (RUs) or request units per second (RU/s)](request-units.md). The following table lists the limits for storage and throughput per container/database. Storage refers to the combined amount of data and index storage.

| Resource | Limit |
| --- | --- |
| Maximum RUs per container ([dedicated throughput provisioned mode](resource-model.md#azure-cosmos-db-containers)) | 1,000,000 ¹ |
| Maximum RUs per database ([shared throughput provisioned mode](resource-model.md#azure-cosmos-db-containers)) | 1,000,000 ¹ |
| Maximum RUs per partition (logical & physical) | 10,000 |
| Maximum storage across all items per (logical) partition | 20 GB ²|
| Maximum number of distinct (logical) partition keys | Unlimited |
| Maximum storage per container | Unlimited |
| Maximum attachment size per Account (Attachment feature is being deprecated) | 2 GB |
| Minimum RU/s required per 1 GB | 1 RU/s |

¹ Increase Maximum RUs per container or database by [filing an Azure support ticket](create-support-request-quota-increase.md).

² To learn about best practices for managing workloads that have partition keys requiring higher limits for storage or throughput, see [Create a synthetic partition key](synthetic-partition-keys.md). If your workload reaches the logical partition limit of 20 GB in production, rearchitecting your application with a different partition key is recommended as a long-term solution. To give you time to rearchitect your application, request a temporary increase in the logical partition key limit for your existing application. [File an Azure support ticket](create-support-request-quota-increase.md) and select quota type **Temporary increase in container's logical partition key size**. Requesting a temporary increase is intended as a temporary mitigation and not recommended as a long-term solution, as **SLA guarantees are not honored when the limit is increased**. To remove the configuration, file a support ticket and select quota type **Restore container’s logical partition key size to default (20 GB)**. You can file this support ticket after deleting data to fit the 20-GB logical partition limit or rearchitecting your application with a different partition key.

### Minimum throughput limits

An Azure Cosmos DB container (or shared throughput database) using manual throughput must have a minimum throughput of 400 RU/s. As the container grows, Azure Cosmos DB requires a minimum throughput to ensure the resource (database or container) has sufficient resource for its operations.

Retrieve the current and minimum throughput of a container or a database from the Azure portal or the software development kits (SDKs). For more information, see [Allocate throughput on containers and databases](set-throughput.md).

The actual minimum RU/s might vary depending on your account configuration. You can use [Azure Monitor metrics](monitor.md#analyze-azure-cosmos-db-metrics) to view the history of provisioned throughput (RU/s) and storage on a resource.

#### Minimum throughput on container

Estimate the minimum throughput on a container using this section.

##### Manual throughput

To estimate the minimum RU/s required of a container with manual throughput, find the maximum of:

* 400 RU/s 
* Current storage in GB * 1 RU/s
* Highest RU/s ever provisioned on the container / 100

For example, a container is provisioned with 400 RU/s and 0-GB storage. You increase the throughput to 50,000 RU/s and import 20 GB of data. The minimum RU/s is now `MAX(400, 20 * 1 RU/s per GB, 50,000 RU/s / 100)` = 500 RU/s. Over time, the storage grows to 2,000 GB. The minimum RU/s is now `MAX(400, 2000 * 1 RU/s per GB, 50,000 / 100)` = 2000 RU/s.

##### Autoscale throughput

To estimate the minimum autoscale max RU/s required of a container with autoscale throughput, find the maximum of:

* 1000 RU/s 
* Current storage in GB * 10 RU/s
* Highest RU/s ever provisioned on the container / 10

For example, you have a container provisioned with 1000 RU/s and 0-GB storage. You increase the throughput to 50,000 RU/s and import 20 GB of data. The minimum max RU/s is now `MAX(1000, 20 * 10 RU/s per GB, 50,000 RU/s / 10)` = 5000 RU/s. Over time, the storage grows to 2,000 GB. The minimum max RU/s is now `MAX(1000, 2000 * 10 RU/s per GB, 50,000 / 10)` = 20,000 RU/s.

#### Minimum throughput on shared throughput database

Use this section to estimate the minimum throughput on a database sharing throughput across containers.

##### Manual throughput

To estimate the minimum RU/s required of a shared throughput database with manual throughput, find the maximum of:

* 400 RU/s 
* Current storage in GB * 1 RU/s
* Highest RU/s ever provisioned on the database / 100
* 400 + MAX(Container count - 25, 0) * 100 RU/s

For example, you have a database provisioned with 400 RU/s, 15 GB of storage, and 10 containers. The minimum RU/s is `MAX(400, 15 * 1 RU/s per GB, 400 / 100, 400 + 0 )` = 400 RU/s. If there were 30 containers in the database, the minimum RU/s would be `400 + MAX(30 - 25, 0) * 100 RU/s` = 900 RU/s.

##### Autoscale throughput

To estimate the minimum autoscale max RU/s required of a shared throughput database with autoscale throughput, find the maximum of:

* 1000 RU/s 
* Current storage in GB * 10 RU/s
* Highest RU/s ever provisioned on the database / 10
* 1000 + MAX(Container count - 25, 0) * 1000 RU/s

For example, you have a database provisioned with 1000 RU/s, 15 GB of storage, and 10 containers. The minimum max RU/s for autoscale database is `MAX(1000, 15 * 10 RU/s per GB, 1000 / 10, 1000 + 0 )` = 1000 RU/s. If there were 30 containers in the database, the minimum max RU/s would be `1000 + MAX(30 - 25, 0) * 1000 RU/s` = 5000 RU/s. 

In summary, here are the minimum provisioned RU limits when using provisioned throughput.

| Provisioning Type | Resource | Limit |
| --- | --- | --- |
| Manual throughput | Minimum RUs per container ([dedicated throughput provisioned mode with manual throughput](./set-throughput.md#set-throughput-on-a-container)) | 400 |
| Manual throughput | Minimum RUs per database ([shared throughput provisioned mode with manual throughput](./set-throughput.md#set-throughput-on-a-database) | 400 RU/s for first 25 containers. |
| Autoscale throughput | Minimum max RUs per container ([dedicated throughput provisioned mode with autoscale throughput](./provision-throughput-autoscale.md)) | 1000 |
| Autoscale throughput | Minimum max RUs per database ([shared throughput provisioned mode with autoscale throughput](./provision-throughput-autoscale.md)) | 1000 RU/s for first 25 containers. |

Azure Cosmos DB supports programmatic scaling of throughput (RU/s) per container or database through the SDKs or portal.

Each resource scales synchronously and immediately between the minimum RU/s and up to 100x the minimum RU/s, depending on the current RU/s provisioned and resource settings. If the requested throughput value is outside the range, scaling is performed asynchronously. Asynchronous scaling could take minutes to hours to complete depending on the requested throughput and data storage size in the container.  [Learn more.](scaling-provisioned-throughput-best-practices.md#background-on-scaling-rus)

### Serverless

[Serverless](serverless.md) lets you use your Azure Cosmos DB resources in a consumption-based fashion.

| Resource | Limit |
| --- | --- |
| Maximum storage across all items per (logical) partition | 20 GB ¹|
| Maximum number of distinct (logical) partition keys | Unlimited |
| Maximum storage per container | Unlimited |

¹ If your workload reaches the logical partition limit of 20 GB in production, rearchitecting your application with a different partition key is recommended as a long-term solution. To give you time to rearchitect your application, request a temporary increase in the logical partition key limit for your existing application. [File an Azure support ticket](create-support-request-quota-increase.md) and select quota type **Temporary increase in container's logical partition key size**. Requesting a temporary increase is intended as a temporary mitigation and not recommended as a long-term solution. To remove the configuration, file a support ticket and select quota type **Restore container’s logical partition key size to default (20 GB)**. You can file this support ticket after deleting data to fit the 20-GB logical partition limit or rearchitecting your application with a different partition key.

## Control plane

Azure Cosmos DB has a resource provider that lets you create, update, and delete resources in your Azure Cosmos DB account. The resource provider interfaces with the overall Azure Resource Management layer, which is the deployment and management service for Azure. 

Create and manage Azure Cosmos DB resources using:

- Azure portal
- Azure PowerShell
- Azure CLI
- Azure Resource Manager JSON/Bicep templates
- Azure REST API
- Azure Management SDKs
- Terraform
- Pulumi

This management layer can also be accessed from the Azure Cosmos DB data plane SDKs used in your applications to create and manage resources within an account. Data plane SDKs also make control plane requests during initial connection to the service to do things like enumerating databases and containers, and requesting account keys for authentication.

Each Azure Cosmos DB account has a **primary partition** that contains all the metadata for the account. It also has a small amount of throughput to support control plane operations. Control plane requests that create, read, update, or delete this metadata consumes this throughput. When the amount of throughput consumed by control plane operations exceeds this amount, operations are rate-limited, same as data plane operations within Azure Cosmos DB. However, unlike throughput for data operations, throughput for the primary partition can't be increased.

Some control plane operations don't consume primary partition throughput, such as Get or List Keys. However, unlike requests on data within your Azure Cosmos DB account, resource providers within Azure aren't designed for high request volumes. **Control plane operations that exceed the documented limits at sustained levels over consecutive 5-minute periods may experience request throttling as well as failed or incomplete operations on Azure Cosmos DB resources**. 

Control plane operations can be monitored by navigating the Insights tab for an Azure Cosmos DB account. For more information, see [Monitor Control Plane Requests](use-metrics.md#monitor-control-plane-requests). You can customize these insights, use Azure Monitor, and create a workbook to monitor [Metadata Requests](monitor-reference.md#request-metrics) and set alerts.

### Resource limits

The following table lists resource limits per subscription or account.

| Resource | Limit |
| --- | --- |
| Maximum number of accounts per subscription | 250 by default ¹ |
| Maximum number of databases & containers per account | 500 ² |
| Maximum throughput supported by an account for metadata operations | 240 RU/s |

¹ Default limits differ for Microsoft internal customers. Increase these limits by creating an [Azure Support request](create-support-request-quota-increase.md) up to a maximum of 1,000. Cosmos DB reserves the right to delete any empty database accounts, that is, no databases/collections.
² This limit can't be increased. The total count includes both databases and containers within an account (for example, 1 database and 499 containers, or 250 databases and 250 containers).

### Request limits

The following table lists request limits per 5-minute interval, per account, unless otherwise specified.

| Operation | Limit |
| --- | --- |
| Maximum List or Get Keys | 500 ¹ | 
| Maximum Create database & container | 500 |
| Maximum Get or List database & container | 500 ¹ |
| Maximum Update provisioned throughput | 25 |
| Maximum regional failover | 10 (per hour) ² |
| Maximum number of all operations (`PUT`, `POST`, `PATCH`, `DELETE`, `GET`) not defined previously | 500 |

¹ Use a [singleton client](best-practice-dotnet.md#checklist) for SDK instances, and cache keys, database, and container references between requests for the lifetime of that instance.
² Regional failovers only apply to single region writes accounts. Multi-region write accounts don't require or allow changing the write region.

Azure Cosmos DB automatically backs up your data at regular intervals. For details on backup retention intervals and windows, see [Online backup and on-demand data restore in Azure Cosmos DB](online-backup-and-restore.md).

## Per-account limits

Here are the limits per account.

### Provisioned throughput

| Resource | Limit |
| --- | --- |
| Maximum number of databases and containers per account | 500 |
| Maximum number of containers per database with shared throughput | 25 |
| Maximum number of regions | No limit (all Azure regions) |

### Serverless

| Resource | Limit |
| --- | --- |
| Maximum number of databases and containers per account | 500 |
| Maximum number of regions | 1 (any Azure region) |

## Per-container limits

Depending on the API you use, an Azure Cosmos DB container can represent a collection, a table, or a graph. Containers support configurations for [unique key constraints](unique-keys.md), [stored procedures, triggers, and user-defined functions (UDFs)](stored-procedures-triggers-udfs.md), and [indexing policies](how-to-manage-indexing-policy.md). The following table lists the limits specific to configurations within a container.

| Resource | Limit |
| --- | --- |
| Maximum length of database or container name | 255 |
| Maximum number of stored procedures per container | 100 ¹ |
| Maximum number of UDFs per container | 50 ¹ |
| Maximum number of unique keys per container|10 ¹ |
| Maximum number of paths per unique key constraint|16 ¹ |
| Maximum time-to-live (TTL) value | 2,147,483,647 |

¹ Increase any of these per-container limits by creating an [Azure Support request](create-support-request-quota-increase.md).

## Per-item limits

An Azure Cosmos DB item can represent a document in a collection, a row in a table, or a node or edge in a graph, depending on which API you use. The following table shows the limits per item in Azure Cosmos DB.

| Resource | Limit |
| --- | --- |
| Maximum size of an item | 2 MB (UTF-8 length of JSON representation) ¹ |
| Maximum length of partition key value | 2,048 bytes (101 bytes if large partition-key isn't enabled) |
| Maximum length of ID value | 1,023 bytes |
| Allowed characters for ID value | Service-side all Unicode characters except for '/' and '\\' are allowed. **WARNING: But for best interoperability we STRONGLY RECOMMEND to only use alpha-numerical ASCII characters in the ID value only**. There are known limitations in some versions of the Cosmos DB SDK, and connectors (Azure Data Factory, Spark, Kafka, etc.) and HTTP drivers or libraries. These limitations can prevent successful processing when the ID value contains nonalphanumerical ASCII characters. So, to increase interoperability, encode the ID value - [for example via Base64 + custom encoding of special characters allowed in Base64](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/78fc16c35c521b4f9a7aeef11db4df79c2545dee/Microsoft.Azure.Cosmos.Encryption/src/EncryptionProcessor.cs#L475-L489). - if you have to support nonalphanumerical ASCII characters in your service/application. |
| Maximum number of properties per item | No practical limit |
| Maximum length of property name | No practical limit |
| Maximum length of property value | No practical limit |
| Maximum length of string property value | No practical limit |
| Maximum length of numeric property value | IEEE754 double-precision 64-bit |
| Maximum level of nesting for embedded objects / arrays | 128 |
| Maximum TTL value |2147483647 |
| Maximum precision/range for numbers in [JSON (to ensure safe interoperability)](https://www.rfc-editor.org/rfc/rfc8259#section-6) | [Institute of Electrical and Electronics Engineers (IEEE) 754 binary64](https://www.rfc-editor.org/rfc/rfc8259#ref-IEEE754) |

¹ Large document sizes up to 16 MB are supported with Azure Cosmos DB for MongoDB only. For more information, see [MongoDB 4.2 feature documentation](mongodb/feature-support-42.md#data-types).

There are no restrictions on the item payloads (like number of properties and nesting depth), except for the length restrictions on partition key and ID values, and the overall size restriction of 2 MB. You might need to configure the indexing policy for containers with large or complex item structures to reduce RU consumption. See [Modeling items in Azure Cosmos DB](model-partition-example.md) for a real-world example, and patterns to manage large items.

## Per-request limits

Azure Cosmos DB supports [CRUD and query operations](/rest/api/cosmos-db/) for resources like containers, items, and databases. It also supports [transactional batch requests](/dotnet/api/microsoft.azure.cosmos.transactionalbatch) for items with the same partition key in a container.

| Resource | Limit |
| --- | --- |
| Maximum execution time for a single operation (like a stored procedure execution or a single query page retrieval)| 5 sec |
| Maximum request size (for example, stored procedure, CRUD)| 2 MB |
| Maximum response size (for example, paginated query) | 4 MB |
| Maximum number of operations in a transactional batch | 100 |

Azure Cosmos DB supports triggers during writes. The service allows one pretrigger and one post-trigger per write operation.

When a query operation reaches the execution timeout or response size limit, it returns a page of results and a continuation token to the client to resume execution. There's no practical limit on the duration a single query can run across pages/continuations.

Azure Cosmos DB uses hash-based message authentication codes (HMAC) for authorization. Use a primary key for fine-grained access control to resources. These resources can include containers, partition keys, or items. The following table lists limits for authorization tokens in Azure Cosmos DB.

| Resource | Limit |
| --- | --- |
| Maximum primary token expiry time | 15 min  |
| Minimum resource token expiry time | 10 min  |
| Maximum resource token expiry time | 24 h by default ¹ |
| Maximum clock skew for token authorization| 15 min |

¹ Increase it by [filing an Azure support ticket](create-support-request-quota-increase.md).

## Limits for autoscale provisioned throughput

See the [Autoscale](./provision-throughput-autoscale.md) article and [FAQ](./autoscale-faq.yml#how-do-i-lower-the-maximum-ru-s-) for a detailed explanation of throughput and storage limits with autoscale.

| Resource | Limit |
| --- | --- |
| Maximum RU/s the system can scale to |  `Tmax`, the autoscale max RU/s set by the user |
| Minimum RU/s the system can scale to | `0.1 * Tmax`|
| Current RU/s the system is scaled to  |  `0.1*Tmax <= T <= Tmax`, based on usage|
| Minimum billable RU/s per hour| `0.1 * Tmax` <br></br>Billing is per hour, based on the highest RU/s the system scaled to during the hour, or `0.1*Tmax`, whichever is higher. |
| Minimum autoscale max RU/s for a container  |  `MAX(1000, highest max RU/s ever provisioned / 10, current storage in GB * 10)` rounded up to nearest 1000 RU/s |
| Minimum autoscale max RU/s for a database  |  `MAX(1000, highest max RU/s ever provisioned / 10, current storage in GB * 10,  1000 + (MAX(Container count - 25, 0) * 1000))` rounded up to the nearest 1000 RU/s. <br></br>If your database has more than 25 containers, the system increases the minimum autoscale max RU/s by 1000 RU/s for each extra container. For example, if you have 30 containers, the lowest autoscale maximum RU/s you can set is 6000 RU/s (scaling between 600 and 6000 RU/s).|

## SQL query limits

Azure Cosmos DB supports querying items using [SQL](/cosmos-db/query/overview). The following table describes restrictions in query statements, such as the number of clauses or query length.

| Resource | Limit |
| --- | --- |
| Maximum length of SQL query | 512 KB |
| Maximum `JOIN` statements per query | 10¹ |
| Maximum UDFs per query| 10 ¹ |
| Maximum points per polygon| 4096 |
| Maximum explicitly included paths per container| 1500 ¹ |
| Maximum explicitly excluded paths per container| 1500 ¹ |
| Maximum properties in a composite index| 8 |
| Maximum number of paths in a composite index| 100 |

¹ You can increase these SQL query limits by creating an [Azure Support request](create-support-request-quota-increase.md).

## API for MongoDB-specific limits

Azure Cosmos DB supports the MongoDB wire protocol for applications written with MongoDB. Find the supported commands and protocol versions at [Supported MongoDB features and syntax](mongodb/feature-support-32.md).

The following table lists the limits specific to MongoDB feature support. Other service limits mentioned for the API for NoSQL also apply to the API for MongoDB.

| Resource | Limit |
| --- | --- |
| Maximum size of a document | 16 MB (UTF-8 length of JSON representation) ¹ |
| Maximum MongoDB query memory size (applies only to the 3.2 server version) | 40 MB |
| Maximum execution time for MongoDB operations (applies to the 3.2 server version) | 15 seconds |
| Maximum execution time for MongoDB operations (applies to the 3.6 and 4.0 server versions) | 60 seconds |
| Maximum level of nesting for embedded objects / arrays on index definitions | 6 |
| Idle connection timeout for server side connection closure ² | 30 minutes |
| Time limit for MongoDB shell in the Azure portal | 120 minutes in a 24 hour period |

¹ Large document sizes up to 16 MB require feature enablement in the Azure portal. Learn more in the [feature documentation](mongodb/feature-support-42.md#data-types).

² Set the idle connection timeout in the driver settings to 2-3 minutes because the [default timeout for Azure LoadBalancer is 4 minutes](/azure/load-balancer/load-balancer-tcp-idle-timeout). This timeout ensures that an intermediate load balancer idle doesn't close connections between the client machine and Azure Cosmos DB.

## Azure Cosmos DB free tier account limits

The following table lists the limits for [Azure Cosmos DB free tier accounts](optimize-dev-test.md#azure-cosmos-db-free-tier).

| Resource | Limit |
| --- | --- |
| Number of free tier accounts per Azure subscription | 1 |
| Duration of free-tier discount | Lifetime of the account. You must opt in during account creation. |
| Maximum RU/s for free | 1000 RU/s |
| Maximum storage for free | 25 GB |
| Maximum number of containers in a shared throughput database | 25 |

In addition to the previous table, the [per-account limits](#per-account-limits) also apply to free tier accounts. To learn more, see how to create a [free-tier account](free-tier.md).

## Related content

* [Global distribution](distribute-data-globally.md)
* [Partitioning](partitioning-overview.md) and [provisioned throughput](request-units.md)
