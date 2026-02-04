---
title: Build scalable apps - Azure Cosmos DB for PostgreSQL
description: How to build relational apps that scale
ms.author: jonels
author: jonels-msft
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.custom: build-2023, build-2023-dataai
ms.topic: quickstart
recommendations: false
ms.date: 10/01/2023
appliesto:
  - ✅ PostgreSQL
---

# Build scalable apps in Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

For **existing Azure Cosmos DB for PostgreSQL deployments only**, there are three steps involved in building scalable apps. New projects must use one of the alternative services listed above and should not follow the steps below.

1. Classify your application workload. Common workloads where Azure Cosmos DB for PostgreSQL shines include:
   - **Multitenant SaaS** → tenant-isolated schemas or shard keys  
   - **Microservices** → service-aligned distributed tables  
   - **Real-time operational analytics** → co-located distributed data  
   - **High-throughput OLTP** → row-based sharding with a high-cardinality key
2. Based on the workload, use [schema-based sharding](concepts-sharding-models.md#schema-based-sharding) or identify the optimal shard key for the distributed
   tables (for example, shard by `tenant_id` for a multitenant SaaS app so that all rows for a tenant are co-located; expected result: queries scoped to a tenant are routed to a single shard). Classify your tables as reference, distributed, or local. 
3. When using [row-based sharding](concepts-sharding-models.md#row-based-sharding), update the database schema and application queries to make them go fast
   across nodes.

**Success check:** After completing these steps, tenant- or shard-key–scoped queries consistently target a single worker node and show stable low latency under load.

**Next steps**

Before you start building a new app, you must first review a little more about
the architecture of Azure Cosmos DB for PostgreSQL.

> [!div class="nextstepaction"]
> [Fundamental concepts for scaling >](quickstart-build-scalable-apps-concepts.md)
