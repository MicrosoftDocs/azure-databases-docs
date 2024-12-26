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

This article covers the process of disabling key-based authorization (or resource owner password credential auth) for an Azure Cosmos DB for NoSQL account.

[!INCLUDE[Disable key-based authentication](../../includes/disable-key-based-authentication.md)]

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
