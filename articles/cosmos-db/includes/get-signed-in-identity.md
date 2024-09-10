---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/09/2024
ms.custom: subject-msia
---

The current Azure CLI session could be signed in with a human identity (your account), a managed identity, a workload identity, or a service principal. No matter what type of identity you use with Azure CLI, to steps to get the details of the identity can be similar. For more information, see [Microsoft Entra identity fundamentals](/entra/fundamentals/identity-fundamental-concepts#identity).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- Latest version of Azure CLI. [Install Azure CLI](/cli/azure/install-azure-cli).

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

## Get signed in account identity

Use the Azure CLI to query the graph for information about your account's unique identifier.

1. Get the details for the currently logged-in account using [`az ad signed-in-user`](/cli/azure/ad/signed-in-user#az-ad-signed-in-user-show).

    ```azurecli-interactive
    az ad signed-in-user show
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Jayden Philips",
      "givenName": "Jayden",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<jayden@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Philips",
      "userPrincipalName": "<jayden@adventure-works.com>"
    }
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources.
