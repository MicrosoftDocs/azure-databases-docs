---
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: include
ms.date: 08/23/2024
---

1. Create a shell variable for *resourceGroupName* if it doesn't already exist.

    ```azurecli-interactive
    # Variable for resource group name
    resourceGroupName="msdocs-cosmos-gremlin-quickstart"
    ```

1. Use `az group delete` to delete the resource group.

    ```azurecli-interactive
    az group delete \
        --name $resourceGroupName
    ```
