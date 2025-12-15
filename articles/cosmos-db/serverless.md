---
title: Serverless Consumption-Based Account Type
titleSuffix: Azure Cosmos DB
description: Learn how to use Azure Cosmos DB based on consumption by choosing the serverless account type. Learn how the serverless model compares to the provisioned throughput model.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.custom: build-2023
ms.topic: concept-article
ms.date: 07/24/2025
---

# Azure Cosmos DB serverless account type

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

For an Azure Cosmos DB pricing option that's based on only the resources that you use, choose the Azure Cosmos DB serverless account type. With the serverless option, you're charged only for the [request units (RUs)](request-units.md) that your database operations consume and for the storage that your data consumes. Serverless containers can serve thousands of requests per second with no minimum charge and no capacity planning required.

> [!IMPORTANT]
> Do you have any feedback about serverless? We want to hear it! Feel free to drop a message to the Azure Cosmos DB serverless team: [azurecosmosdbserverless@service.microsoft.com](mailto:azurecosmosdbserverless@service.microsoft.com).

Every database operation in Azure Cosmos DB has a cost that's expressed in [RUs](request-units.md). How you're charged for this cost depends on the type of Azure Cosmos DB account you choose:

- **Provisioned throughput**: In the [provisioned throughput](set-throughput.md) account type, you commit to a certain amount of throughput (expressed in RUs per second or *RU/s*) that's provisioned on your databases and containers. The cost of your database operations is then deducted from the number of RUs that are available every second. For each billing period, you're billed for the amount of throughput that you provisioned.

- **Serverless**: In the serverless account type, you don't have to configure provisioned throughput when you create containers in your Azure Cosmos DB account. For each billing period, you're billed for the number of RUs that your database operations consumed.

## Use cases

The Azure Cosmos DB serverless option best fits scenarios in which you expect *intermittent and unpredictable traffic* and long idle times. Because provisioning capacity in these types of scenarios isn't required and might be cost-prohibitive, Azure Cosmos DB serverless should be considered in the following use cases:

- You're getting started with Azure Cosmos DB.
- You're running applications that have one of the following patterns:
  - Bursting, intermittent traffic that is hard to forecast.
  - Low (less than 10 percent) average-to-peak traffic ratio.
- You're developing, testing, prototyping, or offering your users a new application, and you don't yet know the traffic pattern.
- You're integrating with a serverless compute service, like [Azure Functions](/azure/azure-functions/functions-overview).

For more information, see [How to choose between provisioned throughput and serverless](throughput-serverless.md).

### Best practices for multi-tenant applications

When designing multi-tenant applications on Azure Cosmos DB, two isolation models are recommended:

#### Partition key per tenant
In this model, each tenant is represented as a logical partition key within a container. This approach:
- Scales efficiently as the number of tenants increases
- Reduces per-tenant cost by sharing throughput and storage
- Works well for business-to-consumer (B2C) applications with many smaller tenants

For more information, see the [partition-key-per-tenant](https://aka.ms/CosmosMultitenancy#partition-key-per-tenant-model) model.

#### Database account per tenant
In this model, each tenant has a dedicated Azure Cosmos DB account. This approach:
- Provides strong isolation boundaries
- Allows per-tenant settings such as regional configuration, customer-managed keys, and point-in-time restore
- Works well for business-to-business (B2B) applications that require differentiated configurations

For more information, see the [database-account-per-tenant](https://aka.ms/CosmosMultitenancy#database-account-per-tenant-model) model.

> [!Note]
Avoid designing multi-tenant applications with a container-per-tenant or database-per-tenant approach. These patterns can introduce [scalability challenges](concepts-limits.md#serverless-1) as your customer base grows. Instead, use one of the recommended models above to ensure predictable performance and cost efficiency.

For a detailed walkthrough, see [Multi tenancy in Azure Cosmos DB](https://aka.ms/CosmosMultitenancy).

## Use serverless resources

Azure Cosmos DB serverless is a new account type in Azure Cosmos DB. When you create an Azure Cosmos DB account, you choose between *provisioned throughput* and *serverless* options.

To get started with using the serverless model, you must create a new serverless account.

Any container that's created in a serverless account is a serverless container. Serverless containers have the same capabilities as containers that are created in a provisioned throughput account type. You read, write, and query your data exactly the same way. But a serverless account and a serverless container also have other specific characteristics:

- A serverless account can run only in a single Azure region. It isn't possible to add more Azure regions to a serverless account after you create the account.
- Provisioning throughput isn't required on a serverless container, so the following statements apply:
  - You can't pass any throughput when you create a serverless container or an error is returned.
  - You can't read or update the throughput on a serverless container or an error is returned.
  - You can't create a shared throughput database in a serverless account or an error is returned.
- A serverless container begins with a throughput of 5,000 RU/s. Each physical partition within a serverless container can handle up to 5,000 RU/s, meaning the maximum throughput of the container depends on the total number of physical partitions. To learn more, see [Azure Cosmos DB serverless performance](serverless-performance.md).

## Monitor your consumption

If you've used the Azure Cosmos DB provisioned throughput model before, you might find that the serverless model is more cost-effective when your traffic doesn't justify provisioned capacity. The tradeoff is that your costs become less predictable because you're billed based on the number of requests that your database processes. Because of the lack of predictability when you use the serverless option, it's important to monitor your current consumption.

You can monitor consumption by viewing a chart in your Azure Cosmos DB account in the Azure portal. For your Azure Cosmos DB account, go to the **Metrics** pane. On the **Overview** tab, view the chart that's named **Request Units consumed**. The chart shows how many RUs your account consumed for different periods of time.

:::image type="content" source="./media/serverless/request-units-consumed.png" alt-text="Screenshot that shows a chart of the consumed request units.":::

You can use the same [chart in Azure Monitor](monitor-request-unit-usage.md). When you use Azure Monitor, you can [set up alerts](/azure/azure-monitor/alerts/alerts-metric-overview) so that you're notified when your RU consumption passes a threshold that you set.

## High availability

Azure Cosmos DB serverless extends high availability support with availability zones in [designated regions](/azure/reliability/availability-zones-region-support). The associated service-level agreements (SLAs) are aligned with the [single-region writes with availability zone](../articles/cosmos-db/high-availability.md#slas) configuration, ensuring reliability for your deployments.

## Next steps

- [Azure Cosmos DB serverless account performance](serverless-performance.md)
- [How to choose between provisioned throughput and serverless](throughput-serverless.md)
- [Pricing model in Azure Cosmos DB](how-pricing-works.md)
- [Multi tenancy in Azure Cosmos DB](https://aka.ms/CosmosMultitenancy)
