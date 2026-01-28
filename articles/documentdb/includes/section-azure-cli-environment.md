---
ms.topic: include
ms.date: 09/30/2025
---

Set up your Azure CLI environment to manage Azure DocumentDB resources in your subscription.

1. Start in an empty directory.

1. Sign in to Azure CLI.

    ```azurecli-interactive
    az login
    ```    

1. Check your target Azure subscription.

    ```azurecli-interactive
    az account show
    ```

    > [!NOTE]
    > If you aren't connected to the subscription you expected, use this command to change your subscription:
    >
    > ```azurecli-interactive
    > az account set --subscription "<subscription-name>"
    > ```
    >
    > For more information, see [manage Azure subscriptions with the Azure CLI](/cli/azure/manage-azure-subscriptions-azure-cli).
    >
    