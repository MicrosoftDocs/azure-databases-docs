---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/10/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
---

Disabling key-based authorization prevents your account from being used without the more secure Microsoft Entra ID authentication method. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

::: zone pivot="azure-cli"

First, disable key-based authentication to your existing account so that applications are required to use Microsoft Entra ID authentication. Use [`az resource update`](/cli/azure/resource#az-resource-update) to modify `properties.disableLocalAuth` of the existing account.

```azurecli-interactive
az resource update \
    --resource-group "<name-of-existing-resource-group>" \
    --name "<name-of-existing-account>" \
    --resource-type "Microsoft.DocumentDB/databaseAccounts" \
    --set properties.disableLocalAuth=true
```

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

First, create a new account with key-based authentication disabled so that applications are required to use Microsoft Entra authentication.

1. Create a new Bicep file to deploy your new account with key-based authentication disabled. Name the file *deploy-new-account.bicep*.

    ```bicep
    metadata description = 'Deploys a new Azure Cosmos DB account with key-based auth disabled.'
    
    @description('Name of the Azure Cosmos DB account.')
    param name string = 'csms-${uniqueString(resourceGroup().id)}'
    
    @description('Primary location for the Azure Cosmos DB account.')
    param location string = resourceGroup().location
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
      name: name
      location: location
      kind: 'GlobalDocumentDB'
      properties: {
        databaseAccountOfferType: 'Standard'
        locations: [
          {
            locationName: location
          }
        ]
        disableLocalAuth: true
      }
    }
    ```

1. Use [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create) to deploy the Bicep file with the new account.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --template-file deploy-new-account.bicep
    ```

::: zone-end

::: zone pivot="azure-powershell"

First, disable key-based authentication to your existing account so that applications are required to use Microsoft Entra authentication. Use [`Get-AzResource`](/powershell/module/az.resources/get-azresource) and [`Set-AzResource`](/powershell/module/az.resources/set-azresource) to respectively read and update the existing account.

```azurepowershell-interactive
$parameters = @{
    ResourceGroupName = "<name-of-existing-resource-group>"
    ResourceName = "<name-of-existing-account>"
    ResourceType = "Microsoft.DocumentDB/databaseAccounts"
}
$resource = Get-AzResource @parameters

$resource.Properties.DisableLocalAuth = $true

$resource | Set-AzResource -Force
```

::: zone-end

::: zone pivot="azure-portal"

Use these steps to create a new Azure Cosmos DB for NoSQL account with key-based authentication disabled so that applications are required to only use Microsoft Entra authentication.

1. When setting up a new Azure Cosmos DB for NoSQL account, navigate to the **Security** section of the account creation process. 

1. Then, select **Disable** for the **Key-based authentication** option.

    :::image source="media/disable-key-based-authentication/security-step-toggle.png" alt-text="Screenshot of the option to disable key-based authentication when creating a new account in the Azure portal.":::

::: zone-end

> [!IMPORTANT]
> Modifying an Azure Cosmos DB account requires an Azure role with at least the `Microsoft.DocumentDb/databaseAccounts/*/write` permission. For more information, see [permissions for Azure Cosmos DB](/azure/role-based-access-control/permissions/databases#microsoftdocumentdb).
