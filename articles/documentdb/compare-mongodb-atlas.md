---
title: Compare to MongoDB Atlas
description: Compare Azure DocumentDB vs MongoDB Atlas. Learn about global distribution, 99.999% availability, and seamless Azure integration for MongoDB workloads.
author: suvishodcitus
ms.author: suvishod
ms.topic: product-comparison
ms.date: 11/11/2025
ai-usage: ai-assisted
---

# Compare Azure DocumentDB to MongoDB Atlas

Azure DocumentDB is a fully managed enterprise-grade MongoDB-compatible database and vector database for modern app development, including AI applications. With its predictable low costs, Open-source project, and 99.03% MongoDB compatibility, it's ideal for any MongoDB application running on Azure.

## Platform and compatibility

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Compatible with MongoDB tools and drivers** | ✅ Yes | ✅ Yes | |
| **Open-source** | ✅ Yes | ❌ No | *MongoDB is [no longer open-source](https://en.wikipedia.org/wiki/Server_Side_Public_License) since 2018. [DocumentDB](https://github.com/documentdb/documentdb), the database engine powering Azure DocumentDB is open-source.* |
| **MongoDB wire protocol support** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports the latest MongoDB wire protocol including v8, v7, v6, and v5. MongoDB Atlas only supports versions v8 and v7. MongoDB Atlas doesn't support older versions such as v5 and v6.* |
| **Supported on cloud providers** | ✅ Yes | ✅ Yes | *Azure DocumentDB is supported exclusively on Azure. MongoDB wire protocol compatibility enables you to remain vendor-agnostic for other tiers of your application. MongoDB Atlas is supported on Azure, Amazon Web Services (AWS), and Google Cloud.* |
| **Database supported in on-premises and hybrid deployments** | ❌ No | ✅ Yes | *Azure DocumentDB is a cloud-native service.* |

## Availability and performance

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Global distribution** | ✅ Yes | ✅ Yes | |
| **High performance storage** | ✅ Yes | ✅ Yes | *Azure DocumentDB includes **Premium SSD v2** at no extra charge. MongoDB Atlas charges more for high performance storage.* |
| **99.995% availability SLA** | ✅ Yes | ✅ Yes| *Azure DocumentDB and MongoDB Atlas offer a 99.995% availability service level agreement (SLA).* |
| **SLA covers cloud platform** | ✅ Yes | ❌ No | *The SLA for Azure DocumentDB covers the full stack; database, infrastructure, networking, and the rest of the underlying Azure cloud platform. MongoDB Atlas' SLA doesn't include the underlying cloud platform. For more information, see the MongoDB Atlas SLA.* |
| **Instantaneous and automatic scaling** | ✅ Yes | ❌ No | *Azure DocumentDB autoscale tiers automatically and instantaneously scale with zero performance effect. MongoDB ​​​Atlas can take more time to scale up or down.* |
| **Multi-region writes** | ✅ Yes | ✅ Yes | *In Azure DocumentDB with multiple regions in read-write mode, document updates can occur in any region. In MongoDB Atlas multi-region zones, different write regions can be configured per shard. Data within a single shard is writable in a single region.​​* |
| **Limitless scale** | ✅ Yes | ✅ Yes | ​*Azure DocumentDB and MongoDB Atlas deployments support scaling through sharding​.* |
| **Independent scaling for throughput and storage** | ✅ Yes | ❌ No | |
| **Terabytes of maximum storage per node** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports up to 64 TB of storage per node. MongoDB Atlas only supports up to 4 TB. Storage and compute are scaled independently in Azure DocumentDB. In MongoDB Atlas, they're scaled in a locked-in range that can cause overprovisioning.* |

## Development and deployment options

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Dev/test dedicated clusters** | ✅ Yes | ❌ No | *Dev and test workloads are supported with clusters not configured for high availability in Azure DocumentDB saving significant costs. MongoDB Atlas clusters must always be configured for high availability incurring unnecessary compute costs.* |
| **Choice of instance configuration** | ❌ No | ✅ Yes | |
| **Free tier** | ✅ Yes | ✅ Yes | *Azure DocumentDb offers a free tier with 32-GB storage forever. MongoDB Atlas only supports a free tier with 512-MB storage.* |
| **Live migration** | ✅ Yes | ✅ Yes | |
| **Pause and resume clusters** | ❌ No | ✅ Yes | |
| **Reserved instances** | ✅ Yes | ❌ No | *Azure DocumentDB allows cost savings of up to 40% for a one-year commitment and up to 60% for a three-year commitment.* |
| **Transparent total cost of ownership (TCO)** | ✅ Yes | ❌ No | *Azure DocumentDB pricing shown at provisioning is the final cost. MongoDB Atlas has extra charges for backups, data transfer/networking, support, and licensing.* |
| **Replica set configuration** | ✅ Yes | ✅ Yes | |
| **Managed sharding support** | ✅ Yes | ✅ Yes | *Azure fully manages and support sharding for Azure DocumentDB. MongoDB Atlas supports multiple sharding methodologies to fit various use cases. Sharding strategy can be changed without impacting the application.* |

## Data features and capabilities

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Vector search for AI applications** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports [vector search](vector-search.md) to seamlessly combine geospatial filtering and/ or text filtering with your vector search, enhancing the efficiency of your vector search queries. MongoDB Atlas supports vector search exclusively in dedicated instances.* |
| **Integrated text search, geospatial processing** | ✅ Yes | ✅ Yes | |
| **Support for MongoDB multi-document ACID transactions** | ✅ Yes | ✅ Yes | |
| **BSON (Binary JSON) data type support** | ✅ Yes | ✅ Yes | |
| **Support for MongoDB aggregation pipeline** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports aggregation pipelines in v5, v6, and v7 versions of the MongoDB wire protocol.* |
| **16 MB maximum document size** | ✅ Yes | ✅ Yes | |
| **Unlimited nesting depth** | ✅ Yes | ❌ No | *Azure DocumentDB doesn't have a fixed upper limit to nesting. MongoDB Atlas supports nesting up to 100 levels.* |
| **JSON schema for data governance controls** | ❌ No | ✅ Yes | |
| **Blend data with joins and unions for analytics queries** | ✅ Yes | ✅ Yes | |
| **Multi-document ACID transactions across collections and partitions** | ✅ Yes | ✅ Yes | |
| **Integrated text search** | ✅ Yes | ✅ Yes | |
| **Advanced text search** | ✅ Yes | ✅ Yes | *Advanced text search is built in to Azure DocumentDB for no extra cost and doesn't require an extract, transform, load (ETL) solution. MongoDB Atlas requires Atlas search at an extra cost to use advanced text search.** |

## Integration and tooling

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Azure integrations** | ✅ Yes | ✅ Yes | *Azure DocumentDB includes multiple native first-party integrations with other Azure services. MongoDB Atlas has some integrations with native Azure services.* |
| **Data explorer** | ❌ No | ✅ Yes | *MongoDB Atlas uses native MongoDB tools such as Compass and Atlas Data Explorer while also including support for tools like Robo3T.* |
| **SQL-based connectivity** | ❌ No | ✅ Yes | |
| **Native data visualization without external BI tools** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports Power BI. MongoDB Atlas supports Atlas Charts.* |
| **Performance recommendations** | ✅ Yes | ✅ Yes | *Azure DocumentDB users can use Index Advisor to make performance recommendations for common queries. Azure DocumentDB also uses native Microsoft performance profiling tools.* |
| **Embeddable database with sync for mobile devices** | ✅ Yes | ❌ No | *This feature is available in a gated preview for Azure DocumentDB. This feature is deprecated in MongoDB Atlas. This feature isn't implemented in Azure DocumentDB due to low demand. |

## Security and compliance

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Granular role-based access control** | ✅ Yes | ✅ Yes | *Azure DocumentDB supports native and seamless integration with Microsoft Entra ID. MongoDB Atlas does support manual integration with Microsoft Entra ID.* |
| **Microsoft managed security and compliance posture** | ✅ Yes | ❌ No | In Azure DocumentDB, Microsoft is responsible for compliance and security posture. In MongoDB Atlas, MongoDB manages compliance and security, not Microsoft. |
| **Encryption of data in-flight** | ✅ Yes | ✅ Yes | |
| **Encryption of data at rest** | ✅ Yes | ✅ Yes | |
| **Client-side field level encryption** | ✅ Yes | ✅ Yes | |
| **Lightweight Directory Access Protocol (LDAP) Integration** | ✅ Yes | ✅ Yes | |
| **Database-level auditing** | ✅ Yes | ✅ Yes | |

## Back up and support

| | Azure DocumentDB | MongoDB Atlas | Notes |
| --- | --- | --- | --- |
| **Expert support** | ✅ Yes | ✅ Yes | *Azure offers 24x7 support provided by Microsoft for Azure Cosmos DB. An Azure Support contract covers all Azure products, including Azure Cosmos DB, which allows you to work with one support team without extra support costs. MongoDB Atlas provides 24x7 support provided by MongoDB with various SLA options available.* |
| **Continuous backup with on-demand restore** | ✅ Yes | ✅ Yes | |

## Related content

- [Get started with Azure DocumentDB](quickstart-nodejs.md)
- [Build a vector search application with Azure DocumentDB](quickstart-nodejs-vector-search.md)
