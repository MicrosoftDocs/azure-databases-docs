---
title: Disable key-based authentication (preview)
titleSuffix: Azure Cosmos DB for Table
description: Learn how to disable key-based auth with Azure Cosmos DB for Table to prevent an account from being used with insecure authentication methods.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 04/11/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
appliesto:
- ✅ Table
ms.custom: sfi-ropc-nochange
#Customer Intent: As a security user, I want to disable key-based auth in an Azure Cosmos DB for Table account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable key-based authentication with Azure Cosmos DB for Table (preview)

This article covers the process of disabling key-based authorization (or resource owner password credential auth) for an Azure Cosmos DB for Table account.

[!INCLUDE[Disable key-based authentication](../../includes/disable-key-based-authentication.md)]

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for Table using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

### [C#](#tab/csharp)

```csharp
using Azure.Data.Tables;
using Azure.Core;

string connectionString = "AccountEndpoint=<table-endpoint>;AccountKey=<key>;";

TableServiceClient client = new(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) and [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) libraries from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { TableServiceClient } = require('@azure/data-tables');

const connectionString = 'AccountEndpoint=<table-endpoint>;AccountKey=<key>;';

const client = new TableServiceClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [TypeScript](#tab/typescript)

```typescript
import { TableServiceClient } from '@azure/data-tables';

let connectionString: string = 'AccountEndpoint=<table-endpoint>;AccountKey=<key>;';

const client: TableServiceClient = new TableServiceClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [Python](#tab/python)

```python
from azure.data.tables import TableServiceClient

connection_string = "AccountEndpoint=<table-endpoint>;AccountKey=<key>;"

client = TableServiceClient(endpoint, connection_string)
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) and [`azure-identity`](https://pypi.org/project/azure-identity/) packages from PyPI.

### [Go](#tab/go)

```go
package main

import (
    "github.com/Azure/azure-sdk-for-go/sdk/data/aztables"
)

const connectionString = "AccountEndpoint=<table-endpoint>;AccountKey=<key>;"

func main() {
  client, _ := aztables.NewServiceClientFromConnectionString(connectionString, nil)
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/data/aztables`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) package from Go.

### [Java](#tab/java)

```java
import com.azure.data.tables.TableServiceClient;
import com.azure.data.tables.TableServiceClientBuilder;

public class Table{
    public static void main(String[] args){
        TableServiceClient tableServiceClient = new TableServiceClientBuilder()
            .connectionString("AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;")
            .buildClient();
    }
}
```

> [!IMPORTANT]
> This code samples uses the [`com.azure/azure-data-tables`](https://mvnrepository.com/artifact/com.azure/azure-data-tables) package from Maven.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity control plane role-based access](how-to-grant-control-plane-role-based-access.md)
