---
title: Burstable tier
titleSuffix: Introduction to Burstable Tier on Azure Cosmos DB for MongoDB (vCore)
description: Introduction to Burstable Tier on vCore-based Azure Cosmos DB for MongoDB.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 05/29/2025
appliesto:
  - ✅ MongoDB (vCore)
ms.custom:
  - build-2025
---

# Burstable tiers on vCore-based Azure Cosmos DB for MongoDB

## What is burstable compute?

Burstable tier offers an intelligent solution tailored for small database workloads. By providing minimal CPU performance during idle periods, these clusters optimize resource utilization. However, the real brilliance lies in their ability to seamlessly scale up to full CPU power in response to increased traffic or workload demands. This adaptability ensures peak performance precisely when it's needed, all while delivering substantial cost savings.

By reducing the initial price point of the service, Azure Cosmos DB's Burstable Cluster Tier aims to facilitate user onboarding and exploration of MongoDB for vCore at significantly reduced prices. This democratization of access empowers businesses of all sizes to harness the power of Cosmos DB without breaking the bank. Whether you're a startup, a small business, or an enterprise, this tier opens up new possibilities for cost-effective scalability.

Provisioning a burstable tier is as straightforward as provisioning regular tiers; you only need to choose ["M10", "M20", or "M25"](./compute-storage.md#compute-in-azure-cosmos-db-for-mongodb-vcore) in the cluster tier option. Here's a quick start guide that offers step-by-step instructions on how to set up an [Azure Cosmos DB for MongoDB vCore](./quickstart-portal.md) cluster.

## Next steps

In this article, we delved into the Burstable Tier of Azure Cosmos DB for MongoDB (vCore). Now, let's expand our knowledge by exploring the product further and examining the diverse migration options available for moving your MongoDB to Azure.

- [Check out burstable tiers restrictions](./limits.md#m10m20m25-limits)

> [!div class="nextstepaction"]
> [Migration options for Azure Cosmos DB for MongoDB (vCore)](migration-options.md)
