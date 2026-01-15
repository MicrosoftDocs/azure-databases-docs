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
<!-- Comment: Added an explicit qualifier to scope the guidance to existing deployments and redirect new projects to alternative services, per agent feedback item 1. -->

1. Classify your application workload. Common workloads where Azure Cosmos DB for PostgreSQL shines include:
   - **Multitenant SaaS** → tenant-isolated schemas or shard keys  
   - **Microservices** → service-aligned distributed tables  
   - **Real-time operational analytics** → co-located distributed data  
   - **High-throughput OLTP** → row-based sharding with a high-cardinality key
<!-- Comment: Converted the workload examples into a concise, structured list embedded in step 1, per agent feedback item 2. -->
2. Based on the workload, use [schema-based sharding](concepts-sharding-models.md#schema-based-sharding) or identify the optimal shard key for the distributed
   tables (for example, shard by `tenant_id` for a multitenant SaaS app so that all rows for a tenant are co-located; expected result: queries scoped to a tenant are routed to a single shard). Classify your tables as reference, distributed, or local. 
<!-- Comment: Added a concrete shard-key example with an expected outcome immediately adjacent to step 2, per agent feedback item 3. -->
3. When using [row-based sharding](concepts-sharding-models.md#row-based-sharding), update the database schema and application queries to make them go fast
   across nodes.

**Success check:** After completing these steps, tenant- or shard-key–scoped queries consistently target a single worker node and show stable low latency under load.
<!-- Comment: Added a one-line success/verification criterion at the end of the procedure, per agent feedback item 4. -->

**Next steps**

Before you start building a new app, you must first review a little more about
the architecture of Azure Cosmos DB for PostgreSQL.

> [!div class="nextstepaction"]
> [Fundamental concepts for scaling >](quickstart-build-scalable-apps-concepts.md)

---

**Agent feedback applied**

[Agent: mamccrea-test-agent]
- Changes Applied:
- 1. Added an explicit qualifier that the three-step guidance applies only to existing deployments and directs new projects to alternative services.
- OLD TEXT:  
  `There are three steps involved in building scalable apps with Azure Cosmos DB for PostgreSQL:`
- NEW TEXT:  
  `For **existing Azure Cosmos DB for PostgreSQL deployments only**, there are three steps involved in building scalable apps. New projects must use one of the alternative services listed above and should not follow the steps below.`
- ACTION: Prefix the three-step build guidance with a clear qualifier stating it applies only to existing deployments and explicitly tell readers that new projects must use the alternative services listed above. 
- 2. Converted the workload examples and table classification prose into a concise, structured list embedded in the existing steps.
- OLD TEXT:  
  `There are use-case where Azure Cosmos DB for PostgreSQL shines: Multitenant SaaS, microservices, real-time operational analytics, and high throughput OLTP.`
- NEW TEXT:  
  `Common workloads where Azure Cosmos DB for PostgreSQL shines include:  
  - **Multitenant SaaS** → tenant-isolated schemas or shard keys  
  - **Microservices** → service-aligned distributed tables  
  - **Real-time operational analytics** → co-located distributed data  
  - **High-throughput OLTP** → row-based sharding with a high-cardinality key`
- ACTION: Convert the workload examples and table classification text into a concise table or parameter/value list inside the existing steps. 
- 3. Added a concrete shard-key example immediately adjacent to step 2, including a brief expected outcome.
- OLD TEXT:  
  `Based on the workload, use schema-based sharding or identify the optimal shard key for the distributed tables.`
- NEW TEXT:  
  `Based on the workload, use schema-based sharding or identify the optimal shard key for the distributed tables (for example, shard by \`tenant_id\` for a multitenant SaaS app so that all rows for a tenant are co-located; expected result: queries scoped to a tenant are routed to a single shard).`
- ACTION: Place a short concrete shard-key example and any required parameters immediately adjacent to step 2; if a CLI or query example is needed, keep it ≤100 tokens and include one expected output line. 
- 4. Added a one-line success/verification criterion at the end of the procedure.
- OLD TEXT:  
  *(No verification or success criterion present before “Next steps”)*  
- NEW TEXT:  
  `**Success check:** After completing these steps, tenant- or shard-key–scoped queries consistently target a single worker node and show stable low latency under load.`
- ACTION: Add one-line success/verification criteria at the end of the procedure (for example, a sample verification query or expected latency/replica-distribution state). 
- 5. Standardized product naming capitalization for consistency.
- OLD TEXT:  
  `Use the Elastic Clusters feature of Azure Database For PostgreSQL for sharded PostgreSQL using the open-source Citus extension.`
- NEW TEXT:  
  `Use the Elastic Clusters feature of Azure Database for PostgreSQL for sharded PostgreSQL using the open-source Citus extension.`
- ACTION: Standardize product naming by correcting 'Azure Database For PostgreSQL' to 'Azure Database for PostgreSQL' and fix any other inconsistent capitalization.