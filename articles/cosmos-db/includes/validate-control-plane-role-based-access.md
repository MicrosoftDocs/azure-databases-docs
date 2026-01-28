---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/10/2025
ms.custom:
  - sfi-ropc-nochange
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
dev_langs:
  - python
  - javascript
  - typescript
  - csharp
  - go
  - java
---

Validate that you correctly granted access using application code and the Azure Management SDK.

```csharp
using Azure.Identity;
using Azure.ResourceManager;

DefaultAzureCredential credential = new();

ArmClient client = new(credential);
```

```javascript
const { CosmosDBManagementClient } = require('@azure/arm-cosmosdb');
const { DefaultAzureCredential } = require('@azure/identity');

const subscriptionId = "<subscription-id>";

const credential = new DefaultAzureCredential();

const client = new CosmosDBManagementClient(credential, subscriptionId);
```

```typescript
import { CosmosDBManagementClient } from '@azure/arm-cosmosdb';
import { TokenCredential, DefaultAzureCredential } from '@azure/identity';

let subscriptionId: string = "<subscription-id>";

let credential: TokenCredential = new DefaultAzureCredential();

const client: CosmosDBManagementClient = new CosmosDBManagementClient(credential, subscriptionId);
```

```python
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.identity import DefaultAzureCredential

subscription_id = "<subscription-id>"

credential = DefaultAzureCredential()

client = CosmosDBManagementClient(credential=credential, subscription=subscription_id)
```

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
