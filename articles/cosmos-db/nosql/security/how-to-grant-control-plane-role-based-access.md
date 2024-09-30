---
title: Use control plane role-based access control
titleSuffix: Azure Cosmos DB for NoSQL
description: Grant access to manage account resources using role-based access control, Microsoft Entra, and Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/01/2024
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
#Customer Intent: As a security user, I want to grant an identity control-plane access to Azure Cosmos DB for NoSQL, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use control plane role-based access control with Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/how-to-grant-control-plane-role-based-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage an Azure Cosmos DB for NoSQL account and its resources.

[!INCLUDE[Grant control plane role-based access](../../includes/security-overview.md)]

## Validate control plane access in code

Finally, validate that you correctly granted access using application code and the Azure Management SDK in your preferred programming language.

### [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.ResourceManager;

DefaultAzureCredential credential = new();

ArmClient client = new(credential);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.ResourceManager.CosmosDB`](https://www.nuget.org/packages/Azure.ResourceManager.CosmosDB) and [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) libraries from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { CosmosDBManagementClient } = require('@azure/arm-cosmosdb');
const { DefaultAzureCredential } = require('@azure/identity');

const subscriptionId = "<subscription-id>";

const credential = new DefaultAzureCredential();

const client = new CosmosDBManagementClient(credential, subscriptionId);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/arm-cosmosdb`](https://www.npmjs.com/package/@azure/arm-cosmosdb) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) libraries from npm.

### [TypeScript](#tab/typescript)

```typescript
import { CosmosDBManagementClient } from '@azure/arm-cosmosdb';
import { TokenCredential, DefaultAzureCredential } from '@azure/identity';

let subscriptionId: string = "<subscription-id>";

let credential: TokenCredential = new DefaultAzureCredential();

const client: CosmosDBManagementClient = new CosmosDBManagementClient(credential, subscriptionId);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/arm-cosmosdb`](https://www.npmjs.com/package/@azure/arm-cosmosdb) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) libraries from npm.

### [Python](#tab/python)

```python
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.identity import DefaultAzureCredential

subscription_id = "<subscription-id>"

credential = DefaultAzureCredential()

client = CosmosDBManagementClient(credential=credential, subscription=subscription_id)
```

> [!IMPORTANT]
> This code sample uses the [`azure-mgmt-cosmosdb`](https://pypi.org/project/azure-mgmt-cosmosdb/) and [`azure-identity`](https://pypi.org/project/azure-identity/) libraries from PyPI.

### [Go](#tab/go)

```go
package main

import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/cosmos/armcosmos"
)

const subscriptionId = "<subscription-id>"

func main() {
    credential, _ := azidentity.NewDefaultAzureCredential(nil)
    
    client, _ := armcosmos.NewDatabaseClient(subscriptionId, credential, nil)
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/resourcemanager/cosmos/armcosmos`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/cosmos/armcosmos) and [`azure/azure-sdk-for-go/sdk/azidentity`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) libraries from Go.

### [Java](#tab/java)

```java
package com.example;

import com.azure.core.management.profile.AzureProfile;
import com.azure.core.management.AzureEnvironment;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.resourcemanager.cosmos.CosmosManager;

public class NoSQL {
    public static void main(String[] args) {
        AzureProfile profile = new AzureProfile(AzureEnvironment.AZURE);
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
          .build();

        CosmosManager manager = CosmosManager.authenticate(credential, profile);
    }
}
```

> [!IMPORTANT]
> This code sample uses the [`com.azure.resourcemanager/azure-resourcemanager-cosmos](https://mvnrepository.com/artifact/com.azure.resourcemanager/azure-resourcemanager-cosmos) and [`com.azureazure-identity`](https://mvnrepository.com/artifact/com.azure/azure-identity) libraries from Maven.

## Next step

> [!div class="nextstepaction"]
> [Grant your identity data plane role-based access](how-to-grant-data-plane-role-based-access.md)
