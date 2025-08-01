---
title: Azure Cosmos DB Lifetime Free Tier
description: Use the Azure Cosmos DB lifetime free tier to get started, develop, test your applications. With free tier, you get the first 1000 RU/s and 25 GB of storage in the account for free.
author: meredithmooreux
ms.author: merae
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 06/24/2025
---

# Azure Cosmos DB lifetime free tier

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

> [!NOTE]
> To learn about the free tier for **vCore cluster and/or vector database in Azure Cosmos DB for MongoDB**, see [Build applications for free with Azure Cosmos DB for MongoDB (vCore) Free Tier](mongodb/vcore/free-tier.md).
> 
> Free tier is currently not available for serverless accounts.

Azure Cosmos DB free tier makes it easy to get started, develop, test your applications, or even run small production workloads for free. When free tier is enabled on an account, you get the first 1000 RU/s and 25 GB of storage in the account for free. The throughput and storage consumed beyond these limits are billed at regular price. Free tier is available for all API accounts with provisioned throughput, autoscale throughput, single, or multiple write regions.

Free tier lasts indefinitely for the lifetime of the account and it comes with all the [benefits and features](introduction.md#with-unmatched-reliability-and-flexibility) of a regular Azure Cosmos DB account. These benefits include unlimited storage and throughput (RU/s), SLAs, high availability, turnkey global distribution in all Azure regions, and more.

You can have up to one free tier Azure Cosmos DB account per an Azure subscription, and you must opt in when creating the account. If you don't see the option to apply the free tier discount, another account in the subscription has already been enabled with free tier. If you create an account with free tier and then delete it, you can apply free tier for a new account. When creating a new account, it’s recommended to enable the free tier discount if it’s available.

If you decide that Azure Cosmos DB is right for you, you can receive up to 63% discount on [Azure Cosmos DB prices through Reserved Capacity](reserved-capacity.md).

## Free tier with shared throughput database

In the shared throughput model, when you provision throughput on a database, the throughput is shared across all the containers in the database. When using the free tier, you can provision a shared database with up to 1000 RU/s for free. All containers in the database share the throughput.

Just like the regular account, in the free tier account, a shared throughput database can have a max of 25 containers.
Any other databases with shared throughput or containers with dedicated throughput beyond 1000 RU/s are billed at the regular pricing.

## Free tier with Azure discount

The Azure Cosmos DB free tier is compatible with the [Azure free account](optimize-dev-test.md#azure-free-account). To opt in, create an Azure Cosmos DB free tier account in your Azure free account subscription. For the first 12 months, you get a combined discount of 1400 RU/s (1000 RU/s from Azure Cosmos DB free tier and 400 RU/s from Azure free account) and 50 GB of storage (25 GB from Azure Cosmos DB free tier and 25 GB from Azure free account). After the 12 months expire, you'll continue to get 1000 RU/s and 25 GB from the Azure Cosmos DB free tier, for the lifetime of the Azure Cosmos DB account. For an example of how the charges are stacked, see [Billing examples with free tier accounts](understand-your-bill.md#azure-free-tier).

> [!NOTE]
> Azure Cosmos DB free tier is different from the Azure free account. The Azure free account offers Azure credits and resources for free for a limited time. When using Azure Cosmos DB as a part of this free account, you get 25-GB storage and 400 RU/s of provisioned throughput for 12 months.

## Best practices to keep your account free

To keep your account free of charge, your account shouldn't have any more RU/s or storage consumption other than the one offered by the Azure Cosmos DB free tier.

For example, the following are some options that don’t result in any monthly charge:

* One database with a max of 1000 RU/s provisioned throughput.
* Two containers, one with a max of 400 RU/s, and other with a max of 600 RU/s provisioned throughput.
* Account with two regions that has one container with a max of 500 RU/s provisioned throughput.

## Create an account with free tier

You can create a free tier account from the Azure portal, PowerShell, CLI, or Azure Resource Manager (ARM) templates. You can choose free tier while creating the account, you can’t set it after the account is created.

### Azure portal

When creating the account using the Azure portal, set the **Apply Free Tier Discount** option to **Apply**. See [create a new account with free tier](nosql/quickstart-portal.md) article for step-by-step guidance.

### ARM template

To create a free tier account by using an ARM template, set the property `"enableFreeTier": true`. For the complete template, see [deploy an ARM template with free tier](manage-with-templates.md#free-tier) example.

### Azure CLI

To create an account with free tier using the Azure CLI, set the `--enable-free-tier` parameter to *true*:

```azurecli-interactive
# Create a free tier account for API for NoSQL
az cosmosdb create \
    -n "Myaccount" \
    -g "MyResourcegroup" \
    --enable-free-tier true \
    --default-consistency-level "Session"
```

### PowerShell

To create an account with free tier using Azure PowerShell, set the `-EnableFreeTier` parameter to *true*:

```powershell-interactive
# Create a free tier account for API for NoSQL. 
New-AzCosmosDBAccount -ResourceGroupName "MyResourcegroup" `
    -Name "myaccount" `
    -ApiKind "sql" `
    -EnableFreeTier $true `
    -DefaultConsistencyLevel "Session" `
    -Location "East US" `
```

### Unable to create a free-tier account

If the option to create a free-tier account is disabled or if you receive an error saying you can't create a free-tier account, another account in the subscription has already been enabled with free tier. To find the existing free-tier account and the resource group it is in, use the Azure CLI.

## Next steps

After you create a free tier account, you can start building apps with Azure Cosmos DB.

* [Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for .NET](create-sql-api-dotnet-v4.md)
* [Quickstart: Use Azure Cosmos DB for MongoDB (RU) with Node.js](mongodb/quickstart-nodejs.md)
* [Tutorial: Create a Jupyter Notebook to analyze data in your Azure Cosmos DB for NoSQL account](nosql/tutorial-create-notebook-vscode.md)
* [Understand your Azure Cosmos DB bill](understand-your-bill.md)
