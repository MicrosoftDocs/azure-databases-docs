---
title: Disable key-based authentication
titleSuffix: Azure Cosmos DB for Table
description: Learn how to disable key-based auth with Azure Cosmos DB for Table to prevent an account from being used with insecure authentication methods.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 09/25/2024
zone_pivot_groups: azure-interface-cli-powershell-bicep
#Customer Intent: As a security user, I want to disable key-based auth in an Azure Cosmos DB for Table account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable key-based authentication with Azure Cosmos DB for Table

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/how-to-disable-key-based-authentication/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article covers the process of disabling key-based authorization (or resource owner password credential auth) for an Azure Cosmos DB for Table account. Disabling key-based authorization prevents your account from being used without the more secure Microsoft Entra authentication method. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Disable key-based authentication

::: zone pivot="azure-interface-cli"

First, disable key-based authentication to your existing account so that applications are required to use Microsoft Entra authentication. Use [`az resource update`](/cli/azure/resource#az-resource-update) to modify `properties.disableLocalAuth` of the existing account.

```azurecli-interactive
az resource update \
    --resource-group "<name-of-existing-resource-group>" \
    --name "<name-of-existing-table-account>" \
    --resource-type "Microsoft.DocumentDB/databaseAccounts" \
    --set properties.disableLocalAuth=true
```

::: zone-end

::: zone pivot="azure-interface-bicep"

First, create a new account with key-based authentication disabled so that applications are required to use Microsoft Entra authentication.

1. Create a new Bicep file to deploy your new account with key-based authentication disabled. Name the file *deploy-new-account.bicep*.

    ```bicep
    metadata description = 'Deploys a new Azure Cosmos DB for Table account with key-based auth disabled.'
    
    @description('Name of the API for Table account.')
    param name string = 'table-${uniqueString(resourceGroup().id)}'
    
    @description('Primary location for the API for Table account.')
    param location string = resourceGroup().location
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2021-06-15' = {
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
        capabilities: [
          {
            name: 'EnableTable'
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
    ResourceName = "<name-of-existing-table-account>"
    ResourceType = "Microsoft.DocumentDB/databaseAccounts"
}
$resource = Get-AzResource @parameters

$resource.Properties.DisableLocalAuth = $true

$resource | Set-AzResource -Force
```

::: zone-end

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for Table using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

### [C#](#tab/csharp)

```csharp
using Azure.Data.Tables;

string connectionString = "DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<key>;EndpointSuffix=<suffix>;";

TableServiceClient client = new(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) library from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { TableServiceClient } = require('@azure/data-tables');

const connectionString = 'DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<key>;EndpointSuffix=<suffix>;';

const client = new TableServiceClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) package from npm.

### [TypeScript](#tab/typescript)

```typescript
import { TableServiceClient } from '@azure/data-tables';

let connectionString: string = 'DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<key>;EndpointSuffix=<suffix>;';

const client: TableServiceClient = TableServiceClient.fromConnectionString(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) package from npm.

### [Python](#tab/python)

```python
from azure.data.tables import TableServiceClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<key>;EndpointSuffix=<suffix>;"

client = TableServiceClient.from_connection_string(conn_str=connection_string)
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) package from PyPI.

### [Go](#tab/go)

```go
package main

import(
  "github.com/Azure/azure-sdk-for-go/sdk/data/aztables"
)

const (
  connectionString = "DefaultEndpointsProtocol=https;AccountName=<account-name>;AccountKey=<key>;EndpointSuffix=<suffix>;"
)

func main() {
  client, _ := aztables.NewServiceClientFromConnectionString(connectionString, nil)
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/data/aztables`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) package from Go.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity data plane role-based access](how-to-grant-data-plane-role-based-access.md)
