---
title: Choose an API in Azure Cosmos DB
description: Learn which Azure Cosmos DB API to choose for new applications, migrations, or specialized workloads. Prescriptive guidance for NoSQL,  and migrations from MongoDB, Apache Cassandra, Gremlin, Table, and PostgreSQL.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: overview
ms.date: 10/20/2025
adobe-target: true
ai-usage: ai-assisted
applies-to:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ MongoDB (vCore)
  - ✅ PostgreSQL
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Choose an API in Azure Cosmos DB

Azure Cosmos DB is a fully managed NoSQL, relational, and vector database for modern app development.  Azure Cosmos DB takes database administration off your hands with automatic management, updates, and patching. It also handles capacity management with cost-effective serverless and automatic scaling options that respond to application needs to match capacity with demand. The Azure Cosmos DB API for NoSQL is native to Azure Cosmos DB.  You can build new applications with the APIs for NoSQL or migrate your existing data. To run the migrated apps, change the connection string of your application and continue to run as before. When migrating existing apps, make sure to evaluate the migration guide to choose an API that fits your requirements.  This article helps you choose an API based on your workload and team requirements.


[!IMPORTANT]
> **For most new applications, choose the Azure Cosmos DB API for NoSQL.**  It’s the native API and provides the broadest Azure Cosmos DB capabilities and platform integration.
>
> If you need **MongoDB** feature fidelity (for example, complex aggregations or multi‑document transactions) or are lifting‑and‑shifting MongoDB, choose **Azure DocumentDB**.
>

[!NOTE]
> **API choice is fixed per account.** You cannot switch APIs after account creation.  To use a different API, create a new Azure Cosmos DB account with that API.

## TL;DR – Start here

> **In ~80–90% of new applications, choose the Azure Cosmos DB API for NoSQL.**  
> Choose **Azure DocumentDB** only when high MongoDB feature fidelity (aggregation pipelines, multi-document transactions, ecosystem tooling), developing apps on a multicloud environment, or a lift‑and‑shift Mongo migration is a hard requirement.

### Why API for NoSQL is the default
- Fastest feature velocity.
- SQL‑like querying over JSON (simple, expressive).
- Turnkey global distribution & multi-region writes.
- Autoscale + integrated analytical store.
- Native vector search (similarity + embeddings).
- Deep Azure integration (monitoring, security, governance).

### Choosing between API for NoSQL and Azure DocumentDB

| If you… | Pick | Why |
|---|---|---|
| Are building greenfield and flexible on drivers/protocol | API for NoSQL | Broadest feature surface & future-proof. |
| Need Mongo-specific aggregations or multi-doc transactions without refactor | DocumentDB | High Mongo fidelity; minimal code changes. |
| Want unified Cosmos DB query dialect across services | API for NoSQL | Single consistent model. |
| Have mixed team skills / unsure / flexible on API | API for NoSQL | Simpler long-term evolution. |
|  Building hybrid / multicloud apps| DocumentDB | Mongo protocol + ecosystem enable cross‑cloud code reuse.|
| Have an existing sizable Mongo estate you’re lifting | DocumentDB | Low-friction migration path. |


### Migration quick map

| Source workload | Recommended target | Notes |
|---|---|---|
| Existing MongoDB (replica sets / sharded) | Azure DocumentDB | Lowest friction; keep aggregation & multi‑document transaction semantics. |
| Cassandra cluster needing unchanged CQL | Azure Managed Instance for Apache Cassandra | Use Managed Instance for deeper operational parity. |
| Cassandra (refactor acceptable) | API for NoSQL | More native features; simpler global distribution. |
| Azure Table Storage | API for NoSQL (modernize) | Recommended long-term destination; if zero-code change is required temporarily, land on Table API first, then migrate to NoSQL. |
| Gremlin graph app (Analytical workloads) | Microsoft Fabric Graph | Preferred for existing large scale, analytical, AI-integrated graph workloads|
| Relational PostgreSQL needing scale-out | Azure Database PostGreSQL| True distributed relational model. |
| Other relational (Oracle / SQL Server) modernizing to JSON / key-value | API for NoSQL | Document model + global distribution + vector search. |

## Considerations when choosing an API

Based on your workload, you must choose the API that fits your requirement. The following image shows a flow chart on how to choose the right API when building new apps or migrating existing apps to Azure Cosmos DB:

:::image type="complex" source="media/choose-api/choose api.png" alt-text="Diagram of the decision tree to choose an API in Azure Cosmos DB.":::
    Diagram of the decision tree to choose an API in Azure Cosmos DB. Half of the diagram illustrates how many existing open-source database workloads can use the corresponding APIs for Azure Cosmos DB. The other half of the diagram illustrates how new applications can either use the API for NoSQL, or use your existing skills with APIs for open-source databases.
:::image-end:::

## API for NoSQL

The Azure Cosmos DB API for NoSQL stores data in document format. It offers the best end-to-end experience as we have full control over the interface, service, and the SDK client libraries. Any new feature that is rolled out to Azure Cosmos DB is first available on API for NoSQL accounts. NoSQL accounts provide support for querying items using the Structured Query Language (SQL) syntax, one of the most familiar and popular query languages to query JSON objects. To learn more, see the [Azure Cosmos DB API for NoSQL](/training/modules/intro-to-azure-cosmos-db-core-api/) training module and [getting started with SQL queries](nosql/query/getting-started.md) article.

If you're migrating from other databases such as Oracle, DynamoDB, HBase, etc. and if you want to use the modernized technologies to build your apps, API for NoSQL is the recommended option. API for NoSQL supports analytics and offers performance isolation between operational and analytical workloads.


## Capacity planning when migrating data

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.

- For more information about estimating request units if you know typical request rates for your current database workload, see  [capacity planner for API for NoSQL](./sql/estimate-ru-with-capacity-planner.md).

## Related content

- [Get started with Azure Cosmos DB for NoSQL](nosql/quickstart-dotnet.md)
- [Get started with Azure DocumentDB](mongodb/vcore/introduction.md)

