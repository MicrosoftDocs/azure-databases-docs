---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 10/28/2025
ai-usage: ai-generated
---

## Azure Cosmos DB vs. Azure DocumentDB

Azure Cosmos DB and Azure DocumentDB are both powerful NoSQL database services designed to help you build successful applications with flexible JSON data models. Azure Cosmos DB is optimized for **scale-out scenarios** that require global distribution, massive scale, and instantaneous scaling. It offers a 99.999% availability service level agreement (SLA) with automatic failover across multiple regions. This reliability makes it perfect for high-traffic web apps, IoT data collection, real-time gaming, and global online stores that need reliable performance worldwide.

Azure DocumentDB is optimized for **scale-up scenarios** that prioritize rich query capabilities and familiar development experiences. Azure DocumentDB is powered by the open-source DocumentDB engine. DocumentDB is built on the PostgreSQL engine with full MongoDB wire protocol compatibility. Azure DocumentDB excels at complex aggregation pipelines, analytical queries, and advanced document database features. It's ideal for content management systems, analytics platforms, MongoDB migrations, and applications requiring sophisticated query operations with predictable vCore-based pricing.

| | Azure Cosmos DB | Azure DocumentDB |
| --- | --- | --- |
| **Scaling model** | Horizontal (RU-based) | Vertical (vCore-based) |
| **Availability SLA** | 99.999% (multi-region) | 99.995% |
| **Query complexity** | Optimized for point reads and simple queries | Advanced aggregation pipelines and complex joins |
| **Global distribution** | Turn-key multi-region with automatic failover | Regional deployment with geo-replicas |
| **Pricing model** | Variable (RU-based) or serverless | Predictable (compute + storage) |

For more detailed information about the differences between Azure DocumentDB and Azure Cosmos DB, see [Azure DocumentDB vs. Azure Cosmos DB decision guide](../../documentdb/compare-cosmos-db.md?context=/azure/cosmos-db/nosql/context/context).
