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
ms.date: 09/23/2024
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

First, disable key-based authentication to your account so that applications are required to use Microsoft Entra authentication.

### [New account](#tab/new-account)

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

### [Existing account](#tab/existing-account)

1. Create a JSON file named *update-existing-account-props.json* with the changes you wish to make to the properties of the existing account. In this example, we're setting the `properties.disableLocalAuth` property to `true`.

    ```json
    {
      "properties": {
        "disableLocalAuth": true
      }
    }
    ```

1. Patch the existing account using [`az resource patch`](/cli/azure/resource#az-resource-patch). Provide the name of your existing resource group and Azure Cosmos DB for Table account.

    ```azurecli-interactive
    az resource patch \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-table-account>" \
        --resource-type "Microsoft.DocumentDB/databaseAccounts" \
        --properties @update-existing-account-props.json \
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

client = TableServiceClient.from_connection_string(conn_str=connection_string)
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) package from PyPI.

---

## Next step

> [!div class="nextstepaction"]
> [Grant your identity data plane role-based access](how-to-grant-data-plane-role-based-access.md)
