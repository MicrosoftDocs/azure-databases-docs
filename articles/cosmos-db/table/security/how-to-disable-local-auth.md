---
title: Disable local authentication
titleSuffix: Azure Cosmos DB for Table
description: Learn how to disable local auth with Azure Cosmos DB for Table to prevent an account from being used with insecure authentication methods.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 09/09/2024
#Customer Intent: As a security user, I want to disable local auth in an Azure Cosmos DB for Table account, so that my developers or applications can no longer access the account in an insecure manner.
---

# Disable local authentication with Azure Cosmos DB for Table

:::image type="complex" source="media/how-to-disable-local-auth/map.svg" border="false" alt-text="Diagram of the current location ('Prepare') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Solution. The 'Prepare' location is currently highlighted.
:::image-end:::

This article covers the process of disabling local auth for an Azure Cosmos DB for Table account. This procedure is a step that should be performed on new accounts in secure workloads. Alternatively, perform this procedure on existing accounts being migrated to a secure workload pattern.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

## Disable key-based authentication

TODO

### [New account](#tab/new-account)

1. TODO. Name file *deploy-new-account.bicep*.

    ```bicep
    metadata description = 'Deploys a new Azure Cosmos DB for Table account with local auth disabled.'
    
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

1. TODO. [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create).

    ```azurecli-interactive
    az deployment group create `
        --resource-group "<name-of-existing-resource-group>" `
        --template-file deploy-new-account.bicep
    ```

### [Existing account](#tab/existing-account)

1. TODO. Name file *update-existing-account-props.json*.

    ```json
    {
      "properties": {
        "disableLocalAuth": true
      }
    }
    ```

1. TODO. Use [`az resource patch`](/cli/azure/resource#az-resource-patch).

    ```azurecli-interactive
    az resource patch `
        --resource-group "<name-of-existing-resource-group>" `
        --name "<name-of-existing-table-account>" `
        --resource-type "Microsoft.DocumentDB/databaseAccounts" `
        --properties @update-existing-account-props.json `
        --is-full-object
    ```

---

## Validate that authentication is disabled

Attempt to use the Azure SDK to connect to Azure Cosmos DB for Table using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

### [C#](#tab/csharp)

```csharp
using Azure.Data.Tables;

string connectionString = "<account-ropc-connection-string>";

TableServiceClient client = new(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) library from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { TableServiceClient } = require('@azure/data-tables');

const connectionString = '<account-ropc-connection-string>';

const client = new TableServiceClient(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) package from npm.

### [TypeScript](#tab/typescript)

```typescript
import { TableServiceClient } from '@azure/data-tables';

let connectionString: string = '<account-ropc-connection-string>';

const client: TableServiceClient = TableServiceClient.fromConnectionString(connectionString);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) package from npm.

### [Python](#tab/python)

```python
from azure.data.tables import TableServiceClient

connection_string = "<account-ropc-connection-string>"

with TableServiceClient.from_connection_string(conn_str=connection_string) as table_service_client:
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) package from PyPI.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity role-based access](how-to-grant-role-based-access.md)
