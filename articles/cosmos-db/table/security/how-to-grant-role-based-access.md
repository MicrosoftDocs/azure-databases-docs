---
title: Use role-based access control (RBAC)
titleSuffix: Azure Cosmos DB for Table
description: Grant access to run queries, manage entities, and perform operations using role-based access control (RBAC), Microsoft Entra, and Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 09/11/2024
#Customer Intent: As a security user, I want to grant an identity data-plane access to Azure Cosmos DB for Table, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use role-based access control with Azure Cosmos DB for Table

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/how-to-grant-role-based-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage data in an Azure Cosmos DB for Table account. The steps in this article only cover data plane access to perform operations on individual items and run queries.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An existing Azure Cosmos DB for Table account.
- One or more existing identities in Microsoft Entra ID.

[!INCLUDE[Sign in Azure CLI](../../includes/sign-in-azure-cli.md)]

## Create role-based access control definition

First, you must create a role definition with a list of `dataActions` to grant access to read, query, and manage data in Azure Cosmos DB for Table.

1. Create a new Bicep file to define your role definition. Name the file *rbac-definition.bicep*. Add these `dataActions` to the definition:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | |
    | **`Microsoft.DocumentDB/databaseAccounts/tables/*`** | |
    | **`Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*`** | |

    ```bicep
    metadata description = 'Create RBAC definition for data plane access to Azure Cosmos DB for Table.'
    
    @description('Name of the Azure Cosmos DB for Table account.')
    param accountName string
    
    @description('Name of the role definition.')
    param roleDefinitionName string = 'API for Table Data Plane Owner'
        
    resource account 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' existing = {
      name: accountName
    }
    
    resource definition 'Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions@2023-04-15' = {
      name: guid('nosql-role-definition', account.id)
      parent: account
      properties: {
        roleName: roleDefinitionName
        type: 'CustomRole'
        assignableScopes: [
          account.id
        ]
        permissions: [
          {
            dataActions: [
              'Microsoft.DocumentDB/databaseAccounts/readMetadata'
              'Microsoft.DocumentDB/databaseAccounts/tables/*'
              'Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*'
            ]
          }
        ]
      }
    }
    
    output definitionId string = definition.id
    ```

1. Create a new Bicep parameters file named *`rbac-definition.bicepparam`*. In this parameters file, assign the name of your existing Azure Cosmos DB for Table account to the `accountName` parameter.

    ```bicep
    using './rbac-definition.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create). Specify the name of the Bicep template, parameters file, and Azure resource group.

    ```azurecli-interactive
    az deployment group create `
        --resource-group "<name-of-existing-resource-group>" `
        --parameters rbac-definition.bicepparam `
        --template-file rbac-definition.bicep
    ```

1. Review the output from the deployment. The output contains the unique identifier of the role definition in the `properties.outputs.definitionId.value` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    {
      "properties": {
        "outputs": {
          "definitionId": {
            "type": "String",
            "value": "/subscriptions/5e6451f0-384a-4ec0-a4a1-bff59cf4837d/resourceGroups/sidandrews-rbac/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-table-account/tableRoleDefinitions/dddddddd-9999-0000-1111-eeeeeeeeeeee"
          }
        }
      }
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/5e6451f0-384a-4ec0-a4a1-bff59cf4837d/resourceGroups/sidandrews-rbac/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-table-account/tableRoleDefinitions/dddddddd-9999-0000-1111-eeeeeeeeeeee`. This example uses fictituous data and your identifier would be distinct from this example. This is a subset of the typical JSON outputted from the deployment for clarity.

## Assign role-based access control permission

Now, assign the newly defined role to an identity so that your applications can access data in Azure Cosmos DB for Table.

> [!IMPORTANT]
> This assignment task requires you to have the unique identifier of any identity you want to grant role-based access control permissions. If you do not have a unique identifier for an identity, follow the instructions in the [create managed identity](how-to-create-managed-identities.md) or [get signed-in identity](how-to-get-signed-in-identity.md) guides.

1. Create another Bicep file to assign a role to an identity. Name this file *rbac-assignment.bicep*.

    ```bicep
    metadata description = 'Assign RBAC role for data plane access to Azure Cosmos DB for Table.'
    
    @description('Name of the Azure Cosmos DB for Table account.')
    param accountName string
    
    @description('Id of the role definition to assign to the targeted principal in the context of the account.')
    param roleDefinitionId string
    
    @description('Id of the identity/principal to assign this role in the context of the account.')
    param identityId string
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' existing = {
      name: accountName
    }
    
    resource assignment 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2023-04-15' = {
      name: guid(roleDefinitionId, identityId, account.id)
      parent: account
      properties: {
        principalId: identityId
        roleDefinitionId: roleDefinitionId
        scope: account.id
      }
    }
    
    output id string = assignment.id
    ```

1. Create a new Bicep parameters file named *`rbac-assignment.bicepparam`*. In this parameters file; assign the name of your existing Azure Cosmos DB for Table account to the `accountName` parameter, the previously recorded role definition identifiers to the `roleDefinitionId` parameter, and the unique identifier for your identity to the `identityId` parameter.

    ```bicep
    using './rbac-assignment.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    param roleDefinitionId = '<id-of-new-role-definition>'
    param identityId = '<id-of-existing-identity>'
    ```

1. Deploy this Bicep template using `az deployment group create`.

    ```azurecli-interactive
    az deployment group create `
        --resource-group "<name-of-existing-resource-group>" `
        --parameters rbac-assignment.bicepparam `
        --template-file rbac-assignment.bicep
    ```

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access using a managed identity.

## Validate role-based access control in code

Finally, validate that you correctly granted access using application code and the Azure SDK in your preferred programming language.

### [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.Data.Tables;
using Azure.Core;

string endpoint = "<account-endpoint>";

TokenCredential credential = new DefaultAzureCredential();

TableServiceClient client = new(new Uri(endpoint), credential);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) and [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) libraries from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { TableServiceClient } = require('@azure/data-tables');
const { DefaultAzureCredential } = require('@azure/identity');

const endpoint = '<account-endpoint>';

const credential = new DefaultAzureCredential();

const client = new TableServiceClient(endpoint, credential);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [TypeScript](#tab/typescript)

```typescript
import { TableServiceClient } from '@azure/data-tables';
import { TokenCredential, DefaultAzureCredential } from '@azure/identity';

let endpoint: string = '<account-endpoint>';

let credential: TokenCredential = new DefaultAzureCredential();

const client: TableServiceClient = new TableServiceClient(endpoint, credential);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [Python](#tab/python)

```python
from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential

endpoint = "<account-endpoint>"

credential = DefaultAzureCredential()

client = TableServiceClient(endpoint, credential=credential)
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) and [`azure-identity`](https://pypi.org/project/azure-identity/) packages from PyPI.

---

> [!WARNING]
> If you are using a user-assigned managed identity, you will need to specify the unique identifier of the managed identity as part of creating the credentials object.

## Next step

> [!div class="nextstepaction"]
> [Data actions reference](reference-data-actions.md)
