---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/16/2024
---

## Sign in to Azure CLI

Sign in to the Azure CLI interactively for a flexible experience that supports the most possible authentication scenarios in an intuitive manner.

1. Open a command prompt with access to the Azure CLI.

1. Use the [`az login`](/cli/azure/reference-index#az-login) command to sign in interactively with a browser.

    ```azurecli-interactive
    az login
    ```

    > [!NOTE]
    > Alternatively, use [`az login --service-principal`](/cli/azure/authenticate-azure-cli-service-principal) or [`az login --identity`](/cli/azure/authenticate-azure-cli-managed-identity) to sign in with a service principal or managed identity respectively. For more information, see [Azure CLI authentication methods](/cli/azure/authenticate-azure-cli).

1. If you have access to multiple Azure subscriptions, select the subscription you wish to use as the context of your Azure CLI session.

1. Validate that you're signed in with the correct subscription using [`az account show`](/cli/azure/account#az-account-show).

    ```azurecli-interactive
    az account show
    ```
