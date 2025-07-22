---
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: include
ms.date: 07/21/2025
---

Now, get the password for the client library to use to create a connection to the recently created account.

#### [Azure CLI](#tab/azure-cli)

1. Use `az cosmosdb show` to get the host for the account.

    ```azurecli-interactive
    az cosmosdb show \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --query "{host:name}"
    ```

1. Record the value of the `host` property from the previous commands' output. This property' value is the **host** you use later in this guide to connect to the account with the library.

1. Use `az cosmosdb keys list` to get the **keys** for the account.

    ```azurecli-interactive
    az cosmosdb keys list \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --type "keys"
    ```

1. Record the value of the `primaryMasterKey` property from the previous commands' output. This property's value is the **key** you use later in this guide to connect to the account with the library.

#### [Azure portal](#tab/azure-portal)

1. In the resource menu for the account, select the **Overview** option.

1. Record the value of the name of the account. This property's value is the **host** you use later in this guide to connect to the account with the library.

1. In the resource menu for the account again, select the **Connection strings** option within the **Settings** section.
 
1. Expose and record the value of the **PRIMARY KEY** field on this page. This property's value is the **key** you use later in this guide to connect to the account with the library.

---
