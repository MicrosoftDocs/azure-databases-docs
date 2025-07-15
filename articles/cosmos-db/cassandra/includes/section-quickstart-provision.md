---
ms.service: azure-cosmos-db
ms.subservice: cassandra
ms.topic: include
ms.date: 07/15/2025
---

Start by creating an API for Apache Cassandra account. Once the account is created, create the keyspace and table resources.

#### [Azure CLI](#tab/azure-cli)

1. If you don't already have a target resource group, use the `az group create` command to create a new resource group in your subscription.

    ```azurecli-interactive
    az group create \
        --name "<resource-group-name>" \
        --location "<location>"
    ```

1. Use the `az cosmosdb create` command to create a new Azure Cosmos DB for Apache Cassandra account with default settings.

    ```azurecli-interactive
    az cosmosdb create \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --locations "regionName=<location>" \
        --capabilities "EnableCassandra"
    ```

1. Create a new keyspace using `az cosmosdb cassandra keyspace create` named `cosmicworks`.

    ```azurecli-interactive
    az cosmosdb cassandra keyspace create \
        --resource-group "<resource-group-name>" \
        --account-name "<account-name>" \
        --name "cosmicworks"
    ```

1. Use the `az cosmosdb cassandra table create` command to create a new table named `products`.

    ```azurecli-interactive
    az cosmosdb cassandra table create \
        --resource-group "<resource-group-name>" \
        --account-name "<account-name>" \
        --keyspace-name "cosmicworks" \
        --name "products" \
        --schema '{"columns": [{"name": "id", "type": "uuid"}, {"name": "name", "type": "text"}, {"name": "category", "type": "text"}],"partitionKeys": [{"name": "category"}]}'
    ```

#### [Azure portal](#tab/azure-portal)

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

1. Once the deployment is complete, select **Go to resource** to navigate to the new API for Apache Cassandra account.

1. In the resource menu, select the **Data Explorer** option.

1. In the Data Explorer, select **+ New Table**.

1. In the **Add Table** dialog, configure the following options, and then select **OK**:

    | | Value |
    | --- | --- |
    | **Keyspace** | *Create new* |
    | **Keyspace name** | `cosmicworks` |
    | **Table name** | `products` |
    | **Table schema** | `(id uuid, name text, category text, PRIMARY KEY (id))`

    > [!TIP]
    > You can leave any unspecified options to their default values.

---
