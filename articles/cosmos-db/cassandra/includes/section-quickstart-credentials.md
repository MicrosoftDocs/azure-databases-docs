---
ms.service: azure-cosmos-db
ms.subservice: cassandra
ms.topic: include
ms.date: 07/18/2025
ms.custom: sfi-ropc-nochange
---

Now, get the password for the client library to use to create a connection to the recently created account.

#### [Azure CLI](#tab/azure-cli)

1. Use `az cosmosdb show` to get the contactPoint and username for the account.

    ```azurecli-interactive
    az cosmosdb show \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --query "{username:name,contactPoint:documentEndpoint}"
    ```

1. Record the value of the `contactPoint` and `username` properties from the previous commands' output. These properties' values are the **contact point** and **password** you use later in this guide to connect to the account with the library.

1. Use `az cosmosdb keys list` to get the **keys** for the account.

    ```azurecli-interactive
    az cosmosdb keys list \
        --resource-group "<resource-group-name>" \
        --name "<account-name>" \
        --type "keys"
    ```

1. Record the value of the `primaryMasterKey` property from the previous commands' output. This property's value is the **password** you use later in this guide to connect to the account with the library.

#### [Azure portal](#tab/azure-portal)

1. In the resource menu for the account, select the **Connection strings** option within the **Settings** section.

1. Record the value of the **CONTACT POINT** field on this page. This property's value is the **contact point** you use later in this guide to connect to the account with the library.
 
1. Record the value of the **USERNAME** field on this page. This property's value is the **username** you use later in this guide to connect to the account with the library.

1. Expose and record the value of the **PRIMARY PASSWORD** field on this page. This property's value is the **password** you use later in this guide to connect to the account with the library.

---
