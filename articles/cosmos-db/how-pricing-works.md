---
title: Pricing Model
description: Learn about the pricing model for Azure Cosmos DB and how it simplifies your cost management and cost planning.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 06/25/2025
ms.custom: cosmos-db-video
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Pricing model for Azure Cosmos DB

The pricing model for Azure Cosmos DB simplifies cost management and planning. With Azure Cosmos DB, you pay for the operations you perform against the database and for the storage consumed by your data.

>
> [!VIDEO https://www.youtube.com/embed/aFCsCLwgczA?si=VAd1_TOO25vhjLd5]


- **Database operations**: The way you get charged for your database operations depends on the type of Azure Cosmos DB account you use.

  - **Provisioned throughput**: [Provisioned throughput](set-throughput.md), also called reserved throughput, provides high performance at any scale. You specify the throughput that you need in [Request Units](request-units.md) per second (RU/s), and Azure Cosmos DB dedicates the resources required to provide the configured throughput. You can [provision throughput on either a database or a container](set-throughput.md). Based on your workload needs, you can scale throughput up or down at any time or use [autoscale](provision-throughput-autoscale.md) (although there's a minimum throughput required on a database or a container to guarantee the SLAs). You're billed hourly for the maximum provisioned throughput for a given hour.

    > [!NOTE]
    > Because the provisioned throughput model dedicates resources to your container or database, you're charged for the throughput you have provisioned even if you don't run any workloads.

  - **Serverless**: In [serverless](serverless.md) mode, you don't have to provision any throughput when creating resources in your Azure Cosmos DB account. At the end of your billing period, you get billed for the number of Request Units that were consumed by your database operations.

- **Storage**: You're billed a flat rate for the total amount of storage (in GBs) consumed by your data and indexes for a given hour. Storage is billed on a consumption basis, so you don't have to reserve any storage in advance. You're billed only for the storage you consume. The smallest amount of data billed for any non empty container is 1 GB.

The pricing model for Azure Cosmos DB is consistent across all APIs. For more information, see the [Azure Cosmos DB pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/), [Understanding your Azure Cosmos DB bill](understand-your-bill.md), and [Total Cost of Ownership (TCO) with Azure Cosmos DB](total-cost-ownership.md).

If you deploy your Azure Cosmos DB account to a nongovernment region in the US, there's a minimum price for both database and container-based throughput in provisioned throughput mode. There's no minimum price in serverless mode. The pricing varies depending on the region you're using, see the [Azure Cosmos DB pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/) for the latest pricing information.

## Try Azure Cosmos DB for free

Azure Cosmos DB offers many options for developers to it for free. These options include:

* **Azure Cosmos DB free tier**: Azure Cosmos DB free tier makes it easy to get started, develop and test your applications, or even run small production workloads for free. When free tier is enabled on an account, you get the first 1000 RU/s and 25 GB of storage in the account free, for the lifetime of the account. You can have up to one free tier account per Azure subscription and must opt in when creating the account. To learn more, see [Azure Cosmos DB lifetime free tier](free-tier.md).

* **Azure free account**: Azure offers a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) that gives you $200 in Azure credits for the first 30 days and a limited quantity of free services for 12 months. For more information, see [Azure free account](/azure/cost-management-billing/manage/avoid-charges-free-account). Azure Cosmos DB is a part of Azure free account. Specifically for Azure Cosmos DB, this free account offers 25-GB storage and 400 RU/s of provisioned throughput for the entire year.

* **Azure Cosmos DB emulator**: Azure Cosmos DB emulator provides a local environment that emulates the Azure Cosmos DB service for development purposes. Emulator is offered at no cost and with high fidelity to the cloud service. Using Azure Cosmos DB emulator, you can develop and test your applications locally, without creating an Azure subscription or incurring any costs. You can develop your applications by using the emulator locally before going into production. After you're satisfied with the functionality of the application against the emulator, you can switch to using the Azure Cosmos DB account in the cloud and significantly save on cost. For more information about dev/test, see [using Azure Cosmos DB for development and testing](emulator.md).

## Pricing with reserved capacity

Azure Cosmos DB [reserved capacity](reserved-capacity.md) helps you save money when using the provisioned throughput mode by prepaying for Azure Cosmos DB resources for either one year or three years. You can significantly reduce your costs with one-year or three-year upfront commitments and save between 20-65% discounts when compared to the regular pricing.

Reserved capacity provides a billing discount and doesn't affect the runtime state of your Azure Cosmos DB resources. Reserved capacity is available consistently to all APIs, which includes MongoDB, Cassandra, SQL, Gremlin, and Azure Tables and all regions worldwide. You can learn more about reserved capacity in [Azure Cosmos DB pricing & discounts with Reserved Capacity](reserved-capacity.md) article and buy reserved capacity from the [Azure portal](https://portal.azure.com).

## Next steps

You can learn more about optimizing the costs for your Azure Cosmos DB resources in the following articles:

* Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
  * If all you know is the number of vCores and servers in your existing database cluster, see [Convert the number of vCores or vCPUs in your nonrelational database to Azure Cosmos DB RU/s](convert-vcore-to-request-unit.md)
  * If you know typical request rates for your current database workload, see [Estimate RU/s using the Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)
* [Optimize development and testing cost in Azure Cosmos DB](optimize-dev-test.md)
* [Understand your Azure Cosmos DB bill](understand-your-bill.md)
* [Optimize provisioned throughput cost in Azure Cosmos DB](optimize-cost-throughput.md)
* [Optimize storage cost in Azure Cosmos DB](optimize-cost-storage.md)
* [Optimize request cost in Azure Cosmos DB](optimize-cost-reads-writes.md)
* [Optimize multi-region cost in Azure Cosmos DB](optimize-cost-regions.md)
* [Azure Cosmos DB pricing & discounts with Reserved Capacity](reserved-capacity.md)
* [What is the Azure Cosmos DB emulator?](emulator.md)
