---
title: Unified AI Database
description: Database for AI Era - Azure Cosmos DB is a NoSQL, relational, and vector database that provides unmatched reliability and flexibility for your operational data needs.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: overview
ms.date: 02/02/2026
ai-usage: ai-assisted
adobe-target: true
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ PostgreSQL
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Azure Cosmos DB - Database for the AI Era

> "OpenAI relies on Cosmos DB to dynamically scale their ChatGPT service – one of the fastest-growing consumer apps ever – enabling high reliability and low maintenance."
> – Satya Nadella, Microsoft chairman and chief executive officer

Today's applications are required to be highly responsive and always online. They must respond in real time to large changes in usage at peak hours, store ever increasing volumes of data, and make this data available to users in milliseconds. To achieve low latency and high availability, instances of these applications need to be deployed in datacenters that are close to their users.

The surge of AI-powered applications created another layer of complexity, because many of these applications integrate a multitude of data stores. For example, some organizations built applications that simultaneously connect to MongoDB, Postgres, Redis, and Gremlin. These databases differ in implementation workflow and operational performances, posing extra complexity for scaling applications.

Azure Cosmos DB simplifies and expedites your application development by being the single database for your operational data needs, from [geo-replicated distributed caching](https://medium.com/@marcodesanctis2/using-azure-cosmos-db-as-your-persistent-geo-replicated-distributed-cache-b381ad80f8a0) to back up to [vector indexing and search](vector-database.md). It provides the data infrastructure for modern applications like [AI agent](ai-agents.md), digital commerce, Internet of Things, and booking management. It can accommodate all your operational data models, including relational, document, vector, key-value, graph, and table.

## An AI database providing industry-leading capabilities...

## ...for free

Azure Cosmos DB is a fully managed NoSQL, relational, and vector database. It offers single-digit millisecond response times, automatic and instant scalability, along with guaranteed speed at any scale. Business continuity is assured with [SLA-backed](https://azure.microsoft.com/support/legal/sla/cosmos-db) availability and enterprise-grade security.

App development is faster and more productive thanks to:

- Turnkey global distribution & multi-region writes (99.999% SLA) with automatic failover
- Integrated vector + hybrid similarity search (DiskANN) storing embeddings with operational data for RAG, AI agents, and large language model (LLM) caching
- Hierarchical partition keys (subpartitioning) to scale multitenant & high-cardinality workloads beyond single logical partition limits
- Change feed (latest & all versions + deletes modes) for event-driven architectures (Azure Functions, Spark) & streaming pipelines
- No‑ETL HTAP via Azure Synapse Link or Fabric mirroring: isolated analytical store for near real-time insights
- Continuous backup & point‑in‑time restore (recover accidental deletes/corruption across regions)
- Autoscale & serverless throughput models plus RU-based cost governance
- Rich software development kits (SDKs) (.NET, Java, JavaScript/Node.js, Python, Go, Rust) & automatic indexing (no manual index maintenance for most workloads)


As a fully managed service, Azure Cosmos DB takes database administration off your hands with automatic management, updates, and patching. It also handles capacity management with cost-effective serverless and automatic scaling options that respond to application needs to match capacity with demand.

The following free options are available:

* [Azure Cosmos DB lifetime free tier](free-tier.md) provides 1000 [RU/s](request-units.md) of throughput and 25 GB of storage free.
* [Azure AI Advantage](ai-advantage.md) offers 40,000 [RU/s](request-units.md) of throughput for 90 days (equivalent of up to $6,000) to Azure AI or GitHub Copilot customers.
* [Try Azure Cosmos DB free](https://azure.microsoft.com/try/cosmosdb/) for 30 days without creating an Azure account; no commitment follows when the trial period ends.
* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account) gives you $200 in Azure credits for the first 30 days and 400 RU/s of provisioned throughput with 25-GB storage for 12 months.
* [Azure Cosmos DB emulator](emulator.md) provides a local environment that emulates the Azure Cosmos DB service for development and testing at no cost.

When you decide that Azure Cosmos DB is right for you, you can receive up to 63% discount on [Azure Cosmos DB prices through Reserved Capacity](reserved-capacity.md).

> [!TIP]
> To learn more about Azure Cosmos DB, join us every Thursday at 1PM Pacific on Azure Cosmos DB Live TV. See the [Upcoming session schedule and past episodes](https://www.youtube.com/@AzureCosmosDB/streams).

## ...for more than just AI apps

Besides AI, Azure Cosmos DB should also be your goto database for various use cases. These use cases include [retail and marketing](use-cases.md#retail-and-marketing), [IoT and telematics](use-cases.md#iot-and-telematics), [gaming](use-cases.md#gaming), [social](social-media-apps.md), and [personalization](use-cases.md#personalization), among others. Azure Cosmos DB is well positioned for solutions that handle massive amounts of data, reads, and writes at a global scale with near-real response times. Azure Cosmos DB's guaranteed high availability, high throughput, low latency, and tunable consistency are huge advantages when building these types of applications.

##### For what kinds of apps are Azure Cosmos DB a good fit?

- **Flexible Schema for Iterative Development.** For example, apps wanting to adopt flexible modern DevOps practices and accelerate feature deployment timelines.
- **Latency sensitive workloads.** For example, real-time Personalization.
- **Highly elastic workloads.** For example, concert booking platform.
- **High throughput workloads.** For example, IoT device state/logs.
- **Highly available mission critical workloads.** For example, customer-facing Web Apps.

##### For what kinds of apps are Azure Cosmos DB a poor fit?

- **Analytical workloads (OLAP).** For example, interactive, streaming, and batch analytics to enable Data Scientist / Data Analyst scenarios. Consider Microsoft Fabric instead.
- **Highly relational apps.** For example, white-label CRM applications. Consider Azure SQL, Azure Database for MySQL, or Azure Database for PostgreSQL instead.

## ...with unmatched reliability and flexibility

### Guaranteed speed at any scale

Gain unparalleled [SLA-backed](https://azure.microsoft.com/support/legal/sla/cosmos-db) speed and throughput, fast global access, and instant elasticity.

- Real-time access with fast read and write latencies globally, and throughput and consistency all backed by [SLAs](https://azure.microsoft.com/support/legal/sla/cosmos-db)
- Multi-region writes and data distribution to any Azure region with just a button.
- Independently and elastically scale storage and throughput across any Azure region – even during unpredictable traffic bursts – for unlimited scale worldwide.

### Simplified application development

Build fast with open-source APIs, multiple SDKs, schemaless data, and no-ETL analytics over operational data.

- Deeply integrated with key Azure services used in modern (cloud-native) app development including Azure Functions, IoT Hub, AKS (Azure Kubernetes Service), App Service, and more.
- Use Azure Cosmos DB as your unified AI database for data models like relational, document, vector, key-value, graph, and table.
- Build apps on API for NoSQL using the languages of your choice with SDKs for .NET, Java, Node.js, and Python. Or your choice of drivers for any of the other database APIs.
- Change feed makes it easy to track and manage changes to database containers and create triggered events with Azure Functions.
- Azure Cosmos DB's schema-less service automatically indexes all your data, regardless of the data model, to deliver blazing fast queries.

### Mission-critical ready

Guarantee business continuity, 99.999% availability, and enterprise-level security for every application.

- Azure Cosmos DB offers a comprehensive suite of [SLAs](https://azure.microsoft.com/support/legal/sla/cosmos-db) including industry-leading availability worldwide.
- Easily distribute data to any Azure region with automatic data replication. Enjoy zero downtime with multi-region writes or recovery point objective (RPO) 0 when using Strong consistency.
- Enjoy enterprise-grade encryption-at-rest with self-managed keys.
- Azure role-based access control keeps your data safe and offers fine-tuned control.

### Fully managed and cost-effective

End-to-end database management, with serverless and automatic scaling matching your application and total cost of ownership (TCO) needs.

- Fully managed database service. Automatic, no touch, maintenance, patching, and updates, saving developers time and money.
- Cost-effective options for unpredictable or sporadic workloads of any size or scale, enabling developers to get started easily without having to plan or manage capacity.
- Serverless model offers spiky workloads automatic and responsive service to manage traffic bursts on demand.
- Autoscale provisioned throughput automatically and instantly scales capacity for unpredictable workloads, while maintaining [SLAs](https://azure.microsoft.com/support/legal/sla/cosmos-db).

### Azure Synapse Link for Azure Cosmos DB

[Azure Synapse Link for Azure Cosmos DB](synapse-link.md) is a cloud-native hybrid transactional and analytical processing (HTAP) capability that enables analytics at near real-time over operational data in Azure Cosmos DB. Azure Synapse Link creates a tight seamless integration between Azure Cosmos DB and Azure Synapse Analytics.

- Reduced analytics complexity with No extract, transform, and load (ETL) jobs to manage.
- Near real-time insights into your operational data.
- No effect on operational workloads.
- Optimized for large-scale analytics workloads.
- Cost effective.
- Analytics for locally available, globally distributed, multi-region writes.
- Native integration with Azure Synapse Analytics.

### Azure Cosmos DB vs. Azure DocumentDB

Azure Cosmos DB and Azure DocumentDB are both powerful NoSQL database services designed to help you build successful applications with flexible JSON data models. Azure Cosmos DB is optimized for scale-out scenarios that require global distribution, massive scale, and instantaneous scaling. It offers a 99.999% availability service level agreement (SLA) with automatic failover across multiple regions. This reliability makes it well-suited for high-traffic web apps, IoT data collection, real-time gaming, and global online stores that need reliable performance worldwide.

Azure DocumentDB (vCore) is optimized for scale-up scenarios that prioritize rich query capabilities and familiar development experiences. Azure DocumentDB is powered by the open-source DocumentDB engine built on the PostgreSQL engine with full MongoDB wire protocol compatibility. Azure DocumentDB excels at complex aggregation pipelines, analytical queries, and advanced document database features. It's ideal for content management systems, analytics platforms, MongoDB migrations, and applications requiring sophisticated query operations with predictable vCore-based pricing.

Azure DocumentDB is also a good fit for multicloud portability scenarios. It's ideal when you need to sustain existing MongoDB-compatible tooling, drivers, or operational patterns across multiple cloud environments. This compatibility is especially valuable when refactoring to the Cosmos DB native API isn't immediately feasible.

| Characteristic | Azure Cosmos DB (RU/serverless) | Azure DocumentDB (vCore) |
|----------------|---------------------------------|---------------------------|
| Availability SLA | 99.999% (multi-region) | 99.995% |
| Scaling model | Horizontal scale-out (per region RU/s + serverless) | Vertical scale-up (provisioned vCores) |
| Global distribution | Turnkey multi-region writes & automatic failover | Regional deployments + optional geo-replicas |
| Query focus | Optimized for point reads & distributed queries | Advanced aggregation pipelines & complex joins |
| Cost model | Variable RU-based or serverless consumption | Predictable compute + storage |

For more detailed information, see [Azure DocumentDB vs. Azure Cosmos DB decision guide](../documentdb/compare-cosmos-db.md?context=/azure/cosmos-db/nosql/context/context).

> [!TIP]
> In most new application scenarios where you're flexible on drivers and need global scale, prefer the native **API for NoSQL** on Azure Cosmos DB for fastest feature velocity and turnkey global distribution. Choose **Azure DocumentDB** only when you require: (1) deep MongoDB aggregation & multi-document transaction fidelity, (2) PostgreSQL ecosystem alignment, or (3) multicloud portability using MongoDB-compatible drivers and tooling without refactoring.

## Related content

- [Get started with Azure Cosmos DB for NoSQL](quickstart-dotnet.md)
- [Get started with Azure DocumentDB](../documentdb/overview.md)
 