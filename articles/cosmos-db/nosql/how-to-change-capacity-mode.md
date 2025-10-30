---
title: Change from serverless to provisioned throughput
titleSuffix: Azure Cosmos DB for NoSQL
description: Review the steps on how to change the capacity mode of a serverless Azure Cosmos DB for NoSQL account to a provisioned capacity account.
author: richagaur
ms.author: richagaur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 05/08/2025
#Customer Intent: As an administrator, I want to change the capacity mode, so that I can migrate from serverless to provisioned capacity.
ms.custom:
  - build-2025
---
 
# Change from serverless to provisioned capacity mode in Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin](../includes/appliesto-nosql-mongodb-cassandra-gremlin.md)]

Azure Cosmos DB for NoSQL accounts in serverless capacity mode can be changed to provisioned capacity mode. Changing from serverless to provisioned capacity mode converts all containers within the account to manual provisioned throughput containers in-place. The containers' throughput is determined according to the following formula: 
            `Throughput(RU/s) = number of partitions * 5000`.

You can also change the throughput or provisioning mode from manual to autoscale once the migration is complete.

> [!WARNING]
> Changing capacity mode from serverless to provisioned throughput is an irreversible operation. Once migrated, the capacity mode can't be changed back to serverless.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Change capacity mode

Follow these steps to change the capacity mode using Azure portal.

1. In the Azure portal, navigate to your API for NoSQL account.

1. Select the **Change capacity mode to provisioned throughput** option in the **Overview** section of the account page.

1. Review the changes and select **Confirm** to start the migration.

1. Monitor the status using the **state** field in the **Overview** section. The status indicates that the account is **updating** while the migration is in progress.

1. Once the migration is complete, the **capacity mode** field is now set to **provisioned throughput**.

## Limitations

- This is one time migration that is; the account can't be reversed to serverless capacity mode again.
- There's no SLA associated with the duration of migration. 
- Any management operation can't be executed while the migration is in progress.
- In cases where you need to restore a deleted Cosmos DB account, the account is restored to provisioned throughput if the capacity mode was changed from serverless to provisioned, irrespective of the backup timestamp. 
- In cases where you need to restore a deleted serverless container within an existing account, which was migrated from serverless to provisioned throughput, contact Microsoft support.

## Related content

- [Chose between autoscale and manual throughput](../how-to-choose-offer.md).
- [Choose between serverless and provisioned throughput](../throughput-serverless.md).

