---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/11/2024
ms.custom: subject-msia
---

Managed identities are one of many types of identity resources in Microsoft Entra ID for applications to use when connecting to services that support Microsoft Entra authentication. Managed identities can be used in lieu of traditional resource-owned credentials like keys. In Azure, managed identities provide a way for your applications to obtain a Microsoft Entra token to authenticate to Azure Cosmos DB without you needing to write a large amount of authentication code. For more information, see [managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

[!INCLUDE[Sign in Azure CLI](sign-in-azure-cli.md)]

## Create an Azure service with a system-assigned managed identity

Create a new Azure service with a system-assigned managed identity. You can use any type of Azure host service including, but not limited to:

- Azure Container Apps
- Azure Container Instances
- Azure Virtual Machines
- Azure Service Fabric
- Azure App Service
- Azure Spring Apps
- Azure Functions
- Azure Kubernetes Service

This section creates an [Azure Container Instances](/azure/container-instances) resource.

1. Use [`az container create`](/cli/azure/container#az-container-create) to create a new Azure Cosmos DB account. Configure the account to use a system-assigned managed identity by using the `assign-identity` parameter.

    ```azurecli-interactive
    az container create `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-new-container>" `
        --image mcr.microsoft.com/dotnet/samples:aspnetapp-chiseled
        --assign-identity
    ```

    > [!NOTE]
    > Use the `capabilities` parameter to enable features or change the API for your account. For example, if you are creating an Azure Cosmos DB for Table account, use `--capabilities EnableTable`.

1. Get the details for the system-assigned managed identity using [`az container show`](/cli/azure/container#az-container-show) and a JMESPath query.

    ```azurecli-interactive
    az container show `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-existing-container>" `
        --query "identity"
    ```

1. Review the output from the command. It should include the unique identifiers for the identity and tenant.

    ```json
    {
      "principalId": "bbbbbbbb-1111-2222-3333-cccccccccccc",
      "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
      "type": "SystemAssigned",
      "userAssignedIdentities": null
    }
    ```

## Create a user-assigned managed identity

Create a user-assigned managed identity that can be used with one or more Azure services in a portable manner.

1. Use [`az identity create`](/cli/azure/identity#az-identity-create) to create a new user-assigned managed identity in your Azure resource group.

    ```azurecli-interactive
    az identity create `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-new-managed-identity>"
    ```

1. Get the list of user-assigned managed identities in your resource group using [`az identity list`](/cli/azure/identity#az-identity-list)

    ```azurecli-interactive
    az identity list `
        --resource-group "<name-of-existing-resource-group>"    
    ```

1. Review the output from the command. Record the value of the `id` field as this fully qualified resource identifier is used to assign the user-assigned managed identity to your Azure Cosmos DB account.

    ```json
    {
      "clientId": "11112222-bbbb-3333-cccc-4444dddd5555",
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned",
      "location": "<azure-location>",
      "name": "msdocs-identity-example-user-assigned",
      "principalId": "cccccccc-dddd-eeee-3333-444444444444",
      "resourceGroup": "msdocs-identity-example",
      "systemData": null,
      "tags": {},
      "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
      "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned`. This example uses fictituous data and your identifier would be distinct from this example.

## Create an Azure service with a user-assigned managed identity

Assign the previously created user-assigned managed identity to a new Azure host service.

This section creates an [Azure App Services](/azure/app-service) web app resource.

1. Create a new app service plan using [`az appservice plan create`](/cli/azure/appservice/plan#az-appservice-plan-create).

    ```azurecli-interactive
    az appservice plan create `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-new-plan>"
    ```

1. Assign the user-assigned managed identity to a new web app with [`az webapp create`](/cli/azure/webapp#az-webapp-create). Use the `id` field recorded earlier in this guide as the value of the `ssign-identity` parameter.

    ```azurecli-interactive
    az webapp create `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-existing-web-app>" `
        --plan "<name-of-existing-plan>" `
        --assign-identity "<resource-id-recorded-earlier>"
    ```

1. Get the details for all identities assigned to this account using [`az webapp show`](/cli/azure/webapp#az-webapp-show) and a JMESPath query.

    ```azurecli-interactive
    az webapp show `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-existing-account>" `
        --query "identity"   
    ```

1. Review the output from the command. It should include both the system-assigned and user-assigned managed identities.

    ```json
    {
      "principalId": null,
      "tenantId": null,
      "type": "UserAssigned",
      "userAssignedIdentities": {
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned": {
          "clientId": "11112222-bbbb-3333-cccc-4444dddd5555",
          "principalId": "cccccccc-dddd-eeee-3333-444444444444"
        }
      }
    }
    ```
