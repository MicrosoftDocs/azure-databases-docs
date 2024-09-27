---
title: Disable key-based authentication
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to disable key-based auth with Azure Cosmos DB for NoSQL to prevent an account from being used with insecure authentication methods.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/01/2024
zone_pivot_groups: azure-interface-cli-powershell-bicep
#Customer Intent: As a security user, I want to disable key-based auth in an Azure Cosmos DB for NoSQL account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable key-based authentication with Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/how-to-disable-key-based-authentication/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Prepare' location is currently highlighted.
:::image-end:::

This article covers the process of disabling key-based authorization (or resource owner password credential auth) for an Azure Cosmos DB for NoSQL account. Disabling key-based authorization prevents your account from being used without the more secure Microsoft Entra authentication method. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

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
    --name "<name-of-existing-nosql-account>" \
    --resource-type "Microsoft.DocumentDB/databaseAccounts" \
    --set properties.disableLocalAuth=true \
    --set properties.disableKeyBasedMetadataWriteAccess=true
```

::: zone-end

::: zone pivot="azure-interface-bicep"

First, create a new account with key-based authentication disabled so that applications are required to use Microsoft Entra authentication.

1. Create a new Bicep file to deploy your new account with key-based authentication disabled. Name the file *deploy-new-account.bicep*.

    ```bicep
    metadata description = 'Deploys a new Azure Cosmos DB for NoSQL account with key-based auth disabled.'
    
    @description('Name of the API for NoSQL account.')
    param name string = 'nosql-${uniqueString(resourceGroup().id)}'
    
    @description('Primary location for the API for NoSQL account.')
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
        disableLocalAuth: true,
        disableKeyBasedMetadataWriteAccess: true
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
    ResourceName = "<name-of-existing-nosql-account>"
    ResourceType = "Microsoft.DocumentDB/databaseAccounts"
}
$resource = Get-AzResource @parameters

$resource.Properties.DisableLocalAuth = $true
$resource.Properties.DisableKeyBasedMetadataWriteAccess = $true

$resource | Set-AzResource -Force
```

::: zone-end

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for NoSQL using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

### [C#](#tab/csharp)

```csharp
using Microsoft.Azure.Cosmos;

string connectionString = "AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;";

CosmosClient client = new(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`Microsoft.Azure.Cosmos`](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) library from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { CosmosClient } = require('@azure/cosmos');

const connectionString = 'AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;';

const client = new CosmosClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/cosmos`](https://www.npmjs.com/package/@azure/cosmos) package from npm.

### [TypeScript](#tab/typescript)

```typescript
import { CosmosClient } from '@azure/cosmos'

let connectionString: string = 'AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;';

const client: CosmosClient = new CosmosClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/cosmos`](https://www.npmjs.com/package/@azure/cosmos) package from npm.

### [Python](#tab/python)

```python
from azure.cosmos import CosmosClient

connection_string = "AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;"

client = CosmosClient(connection_string)
```

> [!IMPORTANT]
> This code sample uses the [`azure-cosmos`](https://pypi.org/project/azure-cosmos/) package from PyPI.

### [Go](#tab/go)

```go
package main

import (
    "github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos"
)

const connectionString = "AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;"

func main() {
    client, _ := azcosmos.NewClientFromConnectionString(connectionString, nil)
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/data/azcosmos`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) package from Go.

### [Java](#tab/java)

```java
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;

public class NoSQL{
    public static void main(String[] args){
        CosmosClient client = new CosmosClientBuilder()
            .endpoint("<nosql-endpoint>")
            .key("<key>")
            .buildClient();
    }
}
```

> [!IMPORTANT]
> This code samples uses the [`com.azure/azure-cosmos`](https://mvnrepository.com/artifact/com.azure/azure-cosmos) package from Maven.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity control plane role-based access](how-to-grant-control-plane-role-based-access.md)
