---
title: Fleets Overview
titleSuffix: Azure Cosmos DB for NoSQL
description: Fleets, in Azure Cosmos DB, provide a solution for independent software vendor (ISV) customers to manage multitenant applications effectively, balancing cost, performance, and security.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 05/07/2025
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Azure Cosmos DB fleets overview

Building multitenant applications often requires trade-offs between cost, performance, and security isolation. Customers who need strong performance and security isolation in B2B applications often isolate each tenant with a dedicated database account. However, as the application grows and more tenants onboard, capacity management and observability for these resources at scale becomes difficult.

**Azure Cosmos DB fleets** is a new way to organize and manage multitenant workloads at scale. With fleets, you can model each of your B2B tenants as its own database account, ensuring strong performance and security isolation. At the same time, you can simplify management by sharing throughput (RU/s) and monitoring usage at the fleet level using two new capabilities: pools and fleet analytics.

- **Pools** let you share RU/s across multiple accounts, **even if they span different subscriptions and resource groups within a fleet**. While the resources in each account retain its own dedicated RU/s, pools allow accounts to use extra RU/s when needed from the shared pool. This helps avoid overprovisioning by letting tenants scale up temporarily through shared capacity. 

- **Fleet analytics** enables you to export usage data to Microsoft Fabric or an Azure Storage account for long-term analysis of accounts within your fleet. You can track trends like which accounts are most active, how resources scale over time, and when access keys were last rotated. Using built-in dashboards or writing custom queries helps to get deeper insights into your fleet's performance and usage.

## Concepts

A fleet resource maps to one multitenant application and is a grouping entity for multiple Azure Cosmos DB accounts where one account maps to one tenant. Within a fleet, multiple accounts with similar performance characteristics can be grouped together under a fleetspace to share a pool for performance and cost benefits. 

There are a few key concepts to understand: 

- **Fleet**: A high-level entity that organizes and manages multiple database accounts across different subscriptions and/or resource groups within fleetspaces. One fleet corresponds to one multitenant application. 

- **Fleetspace**: A logical grouping of database accounts within a fleet, where RU/s can optionally be shared among all resources in database accounts within the fleetspace​. Each database account within a fleet must be a part of a fleetspace. 

    > [!IMPORTANT]
    > Accounts belong to only one fleetspace and one fleet. Accounts already in a fleetspace within a fleet can't be added to another fleet unless they're removed first.

- **[Pooling](fleet-pools.md)**: This setting is an optional setting that can be configured at the fleetspace level when using fleets. You can set pool RU/s which are the total RU/s available within a fleetspace that any resource in the fleets’ database accounts can use.  

- **Fleetspace account[s]**: These accounts are database accounts within a fleetspace in a fleet. When pooling is configured for the fleetspace, these resources consume RU/s from the pool.

- **Fleet Analytics**: Offers cost, usage, and settings data for all accounts within a fleet aggregated at a one-hour grain for trend analysis and integrated with Fabric OneLake/ADLS storage accounts.

:::image source="media/fleet/hierarchy.png" alt-text="Diagram of the resource hierarchy of a fleet, fleetspaces, and pools.":::

## Default limits

| | Limit |
| --- | --- |
| **Maximum number of database accounts per fleetspace** | `1000`¹ |
| **Maximum pool request units per second (RU/s)** | `1,000,000 RU/s`¹ |
| **Maximum pool request units a partition can consume (RU/s)** | `5,000 RU/s`¹ |

¹To increase these limits, please file an Azure Support ticket.

## Getting started

To get started with Azure Cosmos DB fleets, create a fleet [here](https://portal.azure.com/#view/Microsoft_Azure_DocumentDB/CreateFleet.ReactView).

Creating fleets, fleetspaces, and adding database accounts can be done via the Azure portal or the Azure CLI.

## Next step

> [!div class="nextstepaction"]
> [Create a fleet](how-to-create-fleet.md)
