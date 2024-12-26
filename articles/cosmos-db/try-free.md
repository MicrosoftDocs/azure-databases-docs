---
title: |
  Try Azure Cosmos DB free
description: |
  Try Azure Cosmos DB free. No credit card required. Test your apps, deploy, and run small workloads free for 30 days. Upgrade your account at any time.
author: meredithmooreux
ms.author: merae
ms.service: azure-cosmos-db
ms.custom: references_regions
ms.topic: overview
ms.date: 09/19/2024
---

# Try Azure Cosmos DB free

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

[Try Azure Cosmos DB](https://aka.ms/trycosmosdb) for free before you commit with an Azure Cosmos DB sandbox account. There's no credit card required to get started. Your sandbox account is free for 30 days.  Your data is deleted at the expiration date.   

You can also upgrade your active trial sandbox account to a paid Azure subscription  at any time during the 30-day trial period.  You can only have one Try Azure Cosmos DB sandbox account at a time.  If you're using the API for NoSQL, after you upgrade to a paid Azure subscription and create a new Azure Cosmos DB account you can migrate the data from your Try Azure Cosmos DB sandbox account to your upgraded Azure subscription and Azure Cosmos DB account before the trial ends.

This article walks you through how to create your Try Azure Cosmos DB sandbox account, limits, and upgrading your account. It will also explain how to migrate your data from your Azure Cosmos DB sandbox to your own account using the API for NoSQL.

When you decide that Azure Cosmos DB is right for you, you can receive up to a 63% discount on  [Azure Cosmos DB prices through Reserved Capacity](reserved-capacity.md).

<br>

> [!VIDEO https://www.youtube.com/embed/7EFcxFGRB5Y?si=e7BiJ-JGK7WH79NG]

## Limits to free account

### [NoSQL / Cassandra/ Gremlin / Table](#tab/nosql+cassandra+gremlin+table)

The following table lists the limits for the [Try Azure Cosmos DB](https://aka.ms/trycosmosdb) for free trial sandbox.

| Resource | Limit |
| --- | --- |
| Duration of the trial | 30 days¹² |
| Maximum containers per subscription | 1 |
| Maximum throughput per container | 5,000 |
| Maximum throughput per shared-throughput database | 20,000 |
| Maximum total storage per account | 10 GB |

¹ A new Try Azure Cosmos DB sandbox account can be requested after expiration.

² After expiration, the information stored in your account is deleted. You can upgrade your account prior to expiration and migrate the information stored to an enterprise subscription.

> [!NOTE]
> The Try Azure Cosmos DB sandbox account supports global distribution in only the  **East US**, **North Europe**, **Southeast Asia**, and **North Central US** regions. By default, the Try Azure Cosmos DB sandbox account is created in East US.  Azure support tickets can't be created for Try Azure Cosmos DB sandbox accounts. If the account exceeds the maximum resource limits, it's automatically deleted.  Don’t use personal or sensitive data in your sandbox database during the trial period.

### [MongoDB](#tab/mongodb)

The following table lists the limits for the [Try Azure Cosmos DB](https://aka.ms/trycosmosdb) free trial sandbox.

| Resource | Limit |
| --- | --- |
| Duration of the trial | 30 days¹²  |
| Maximum containers per subscription | 3 |
| Maximum throughput per container | 5,000 |
| Maximum throughput per shared-throughput database | 20,000 |
| Maximum total storage per account | 10 GB |

¹ A new Try Azure Cosmos DB sandbox account can be requested after expiration
² After expiration, the information stored in your account is deleted. You can upgrade your account prior to expiration and migrate the information stored to an enterprise subscription.

> [!NOTE]
> The Try Azure Cosmos DB sandbox account supports global distribution in only the  **East US**, **North Europe**, **Southeast Asia**, and **North Central US** regions. By default, the Try Azure Cosmos DB sandbox account is created in East US.  Azure support tickets can't be created for Try Azure Cosmos DB sandbox accounts. If the account exceeds the maximum resource limits, it's automatically deleted.  Don’t use personal or sensitive data in your sandbox database during the trial period.

---

## Create your Try Azure Cosmos DB account

From the [Try Azure Cosmos DB home page](https://aka.ms/trycosmosdb), select an API. Azure Cosmos DB provides five APIs: NoSQL and MongoDB for document data, Gremlin for graph data, Azure Table, and Cassandra.

> [!NOTE]
> Not sure which API will best meet your needs? To learn more about the APIs for Azure Cosmos DB, see [Choose an API in Azure Cosmos DB](choose-api.md).

:::image type="content" source="media/try-free/try-cosmos-db-page.png" lightbox="media/try-free/try-cosmos-db-page.png" alt-text="Screenshot of the API options including NoSQL and MongoDB on the Try Azure Cosmos DB page.":::

## Launch a Quick Start

Launch the Quickstart in Data Explorer in Azure portal to start using Azure Cosmos DB or get started with our documentation.

* [API for NoSQL](nosql/quickstart-portal.md)
* [API for MongoDB](mongodb/quickstart-python.md#object-model)
* [API for Apache Cassandra](cassandra/adoption.md)
* [API for Apache Gremlin](gremlin/quickstart-console.md)
* [API for Table](table/quickstart-dotnet.md)

You can also get started with one of the learning resources in the Data Explorer.

:::image type="content" source="media/try-free/data-explorer.png" lightbox="media/try-free/data-explorer.png" alt-text="Screenshot of the Azure Cosmos DB Data Explorer landing page.":::

## Upgrade your account

Your Try Azure Cosmos DB sandbox account is free for 30 days. After expiration, a new sandbox account can be created. You can upgrade your active Try Azure Cosmos DB account at any time during the 30 day trial period.  If you're using the API for NoSQL, after you upgrade to a paid Azure subscription and create a new Azure Cosmos DB account you can migrate the data from your Try Azure Cosmos DB sandbox account to your upgraded Azure subscription and Azure Cosmos DB account before the trial ends. Here are the steps to start an upgrade.

### Start upgrade

1. From either the Azure portal or the Try Azure Cosmos DB free page, select the option to **Upgrade** your account.

    :::image type="content" source="media/try-free/upgrade-account.png" lightbox="media/try-free/upgrade-account.png" alt-text="Screenshot of the confirmation page for the account upgrade experience.":::

1. Choose to either **Sign up for an Azure account** or **Sign in** and create a new Azure Cosmos DB account following the instructions in the next section.

### Create a new account

> [!NOTE]
> While this example uses API for NoSQL, the steps are similar for the APIs for MongoDB, Cassandra, Gremlin, or Table.

[!INCLUDE[Create NoSQL account](includes/create-nosql-account.md)]

### Move data to new account

If you desire, you can migrate your existing data from the free sandbox account to the newly created account.

#### [NoSQL](#tab/nosql)

1. Navigate back to the **Upgrade** page from the [Start upgrade](#start-upgrade) section of this guide. Select **Next** to move on to the third step and move your data.

    :::image type="content" source="media/try-free/account-creation-options.png" lightbox="media/try-free/account-creation-options.png" alt-text="Screenshot of the sign-in/sign-up experience to upgrade your current account.":::

1. Locate your **Primary Connection string** for the Azure Cosmos DB account you created for your data. This information can be found within the **Keys** page of your new account.

    :::image type="content" source="media/try-free/account-keys.png" lightbox="media/try-free/account-keys.png" alt-text="Screenshot of the Keys page for an Azure Cosmos DB account.":::

1. Back in the **Upgrade** page from the [Start upgrade](#start-upgrade) section of this guide, insert the connection string of the new Azure Cosmos DB account in the **Connection string** field.

    :::image type="content" source="media/try-free/migrate-data.png" lightbox="media/try-free/migrate-data.png" alt-text="Screenshot of the migrate data options in the portal.":::

1. Select **Next** to move the data to your account. Provide your email address to be notified by email once the migration has been completed.

#### [MongoDB / Cassandra / Gremlin / Table](#tab/mongodb+cassandra+gremlin+table)

> [!IMPORTANT]
> Data migration is not available for the APIs for MongoDB, Cassandra, Gremlin, or Table.

---

## Delete your account

There can only be one free Try Azure Cosmos DB sandbox account per Microsoft account. You may want to delete your account or to try different APIs, you'll have to create a new account. Here’s how to delete your account.

1. Go to the [Try Azure Cosmos DB](https://aka.ms/trycosmosdb) page.

1. Select **Delete my account**.

    :::image type="content" source="media/try-free/delete-account.png" lightbox="media/try-free/delete-account.png" alt-text="Screenshot of the confirmation page for the account deletion experience.":::

## Comments

Use the **Feedback** icon in the command bar of the Data Explorer to give the product team any comments you have about the Try Azure Cosmos DB sandbox experience.

## Next steps

After you create a Try Azure Cosmos DB sandbox account, you can start building apps with Azure Cosmos DB with the following articles:

* Use [API for NoSQL to build a console app using .NET](nosql/quickstart-dotnet.md) to manage data in Azure Cosmos DB.
* Use [API for MongoDB to build a sample app using Python](mongodb/quickstart-python.md) to manage data in Azure Cosmos DB.
* [Create a notebook](nosql/tutorial-create-notebook-vscode.md) and analyze your data.
* Learn more about [understanding your Azure Cosmos DB bill](understand-your-bill.md)
* Get started with Azure Cosmos DB with one of our quickstarts:
  * [Get started with Azure Cosmos DB for NoSQL](nosql/quickstart-portal.md)
  * [Get started with Azure Cosmos DB for MongoDB](mongodb/quickstart-python.md#object-model)
  * [Get started with Azure Cosmos DB for Cassandra](cassandra/adoption.md)
  * [Get started with Azure Cosmos DB for Gremlin](gremlin/quickstart-console.md)
  * [Get started with Azure Cosmos DB for Table](table/quickstart-dotnet.md)
* Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for [capacity planning](sql/estimate-ru-with-capacity-planner.md).
* If all you know is the number of vCores and servers in your existing database cluster, see [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md).
* If you know typical request rates for your current database workload, see [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md).
