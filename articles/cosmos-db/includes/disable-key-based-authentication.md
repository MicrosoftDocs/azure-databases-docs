---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 04/09/2025
zone_pivot_groups: azure-interface-cli-powershell-bicep
---

Disabling key-based authorization prevents your account from being used without the more secure Microsoft Entra authentication method. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

::: zone pivot="azure-interface-cli,azure-interface-bicep"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-shell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Disable key-based authentication

::: zone pivot="azure-interface-cli"

First, disable key-based authentication to your existing account so that applications are required to use Microsoft Entra authentication. Use [`az resource update`](/cli/azure/resource#az-resource-update) to modify `properties.disableLocalAuth` of the existing account.

```azurecli-interactive
az resource update \
    --resource-group "<name-of-existing-resource-group>" \
    --name "<name-of-existing-account>" \
    --resource-type "Microsoft.DocumentDB/databaseAccounts" \
    --set properties.disableLocalAuth=true
```

::: zone-end

::: zone pivot="azure-interface-bicep"

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

::: zone pivot="azure-interface-shell"

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
