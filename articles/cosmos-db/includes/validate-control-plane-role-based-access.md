---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/10/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
ms.custom:
  - sfi-ropc-nochange
---

Validate that you correctly granted access using application code and the Azure Management SDK in your preferred programming language.

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

public class CosmosDB {
    public static void main(String[] args) {
        AzureProfile profile = new AzureProfile(AzureEnvironment.AZURE);
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
          .build();

        CosmosManager manager = CosmosManager.authenticate(credential, profile);
    }
}
```

> [!IMPORTANT]
> This code sample uses the [`com.azure.resourcemanager/azure-resourcemanager-cosmos`](https://mvnrepository.com/artifact/com.azure.resourcemanager/azure-resourcemanager-cosmos) and [`com.azure/azure-identity`](https://mvnrepository.com/artifact/com.azure/azure-identity) libraries from Maven.
