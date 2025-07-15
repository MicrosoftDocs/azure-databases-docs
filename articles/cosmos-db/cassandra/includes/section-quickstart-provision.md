---
ms.service: azure-cosmos-db
ms.subservice: cassandra
ms.topic: include
ms.date: 07/15/2025
---

Start by creating an API for Apache Cassandra account. Once the account is created, get the credentials for the account. You use these credentials to connect to the account using the client library.

#### [](#tab/azure-cli)

1. TODO

#### [](#tab/azure-portal)

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Enter *Azure Cosmos DB* in the global search bar.

1. Within **Services**, select **Azure Cosmos DB**.

1. In the **Azure Cosmos DB** pane, select **Create**, and then **Azure Cosmos DB for Apache Cassandra** within the **Others** tab.

1. Select **Request unit (RU) database account** for the account type.

1. Within the **Basics** pane, configure the following options, and then select **Review + create**:

    | | Value |
    | --- | --- |
    | **Workload Type** | *Learning* |
    | **Subscription** | Select your Azure subscription |
    | **Resource Group** | Create a new resource group or select an existing resource group |
    | **Account Name** | Provide a globally unique name |
    | **Availability Zones** | *Disable* |
    | **Location** | Select a supported Azure region for your subscription |

    > [!TIP]
    > You can leave any unspecified options to their default values. You can also configure the account to limit total account throughput to 1,000 request units per second (RU/s) or enable free tier to minimize your costs.

1. On the **Review + create** pane, wait for validation of your account to finish successfully, and then select **Create**.

1. The portal automatically navigates to the **Deployment** pane. Wait for the deployment to complete.

1. Once the deployment is complete, select **Go to resource** to navigate to the new Azure Cosmos DB for NoSQL account.

---
