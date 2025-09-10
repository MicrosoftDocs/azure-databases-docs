---
title: Use data plane role-based access control (preview)
titleSuffix: Azure Cosmos DB for Table
description: Grant access to run queries, manage entities, and perform operations using role-based access control (RBAC), Microsoft Entra, and Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.reviewer: stefarroyo
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.date: 04/09/2025
zone_pivot_groups: azure-interface-cli-powershell-bicep
appliesto:
  - ✅ Table
#Customer Intent: As a security user, I want to grant an identity data-plane access to Azure Cosmos DB for Table, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use role-based access control with Azure Cosmos DB for Table (preview)

:::image type="complex" source="media/how-to-grant-data-plane-role-based-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Reference. The 'Role-based access control' location is currently highlighted.
:::image-end:::

This article walks through the steps to grant an identity access to manage data in an Azure Cosmos DB for Table account. The steps in this article only cover data plane access to perform operations on individual items and run queries.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An existing Azure Cosmos DB for Table account.
- One or more existing identities in Microsoft Entra ID.

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Prepare role definition

First, you must prepare a role definition with a list of `dataActions` to grant access to read, query, and manage data in Azure Cosmos DB for Table.

### [Built-in definition](#tab/built-in-definition)

::: zone pivot="azure-cli,azure-interface-bicep"

First, get the resource identifier of the existing Azure Cosmos DB for Table account using [`az cosmsodb show`](/cli/azure/cosmosdb#az-cosmosdb-show) and store it in a variable. Then, list all of the role definitions associated with your Azure Cosmos DB for Table account using [`az rest`](/cli/azure/reference-index#az-rest). Finally, review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

```azurecli-interactive
resourceId=$( \
    az cosmosdb show \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-table-account>" \
        --query "id" \
        --output tsv \
)

az rest \
    --method "GET" \
    --url $resourceId/tableRoleDefinitions?api-version=2023-04-15
```

```json
[
  ...,
  {
    "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/tableRoleDefinitions/00000000-0000-0000-0000-000000000002",
    "name": "00000000-0000-0000-0000-000000000002",
    "properties": {
      "assignableScopes": [
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
      ],
      "permissions": [
        {
          "dataActions": [
            "Microsoft.DocumentDB/databaseAccounts/readMetadata",
            "Microsoft.DocumentDB/databaseAccounts/tables/*",
            "Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*"
          ],
          "notDataActions": []
        }
      ],
      "roleName": "Cosmos DB Built-in Data Contributor",
      "type": "BuiltInRole"
    },
    "type": "Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions"
  }
  ...
]
```

> [!NOTE]
> In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/tableRoleDefinitions/00000000-0000-0000-0000-000000000002`. This example uses fictitious data and your identifier would be distinct from this example. This example output is truncated.

::: zone-end

::: zone pivot="azure-powershell"

Use [`Get-AzCosmosDBAccount`](/powershell/module/az.cosmosdb/get-azcosmosdbaccount) to get the resource identifier of the existing Azure Cosmos DB for Table account and store it in a variable. Then, use [`Invoke-AzRestMethod`](/powershell/module/az.accounts/invoke-azrestmethod) to list all of the role definitions associated with your Azure Cosmos DB for Table account. Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `Id` property. Record this value as it is required to use in the assignment step later in this guide.

```azurepowershell-interactive
$parameters = @{
    ResourceGroupName = "<name-of-existing-resource-group>"
    Name = "<name-of-existing-table-account>"
}
$resourceId = (
    Get-AzCosmosDBAccount @parameters |
        Select-Object -Property Id -First 1
).Id

$parameters = @{
  Path = "$resourceId/tableRoleDefinitions?api-version=2023-04-15"
  Method = "GET"
}
Invoke-AzRestMethod @parameters
```

```output
StatusCode : 200
Content    : {
               "value": [
                ...,
                {
                  "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/tableRoleDefinitions/00000000-0000-0000-0000-000000000002",
                  "name": "00000000-0000-0000-0000-000000000002",
                  "properties": {
                    "assignableScopes": [
                      "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
                    ],
                    "permissions": [
                      {
                        "dataActions": [
                          "Microsoft.DocumentDB/databaseAccounts/readMetadata",
                          "Microsoft.DocumentDB/databaseAccounts/tables/*",
                          "Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*"
                        ],
                        "notDataActions": []
                      }
                    ],
                    "roleName": "Cosmos DB Built-in Data Contributor",
                    "type": "BuiltInRole"
                  },
                  "type": "Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions"
                }
                ...
               ]
             }
...
```

> [!NOTE]
> In this example, the `Id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/tableRoleDefinitions/00000000-0000-0000-0000-000000000002`. This example uses fictitious data and your identifier would be distinct from this example. This example output is truncated.

::: zone-end

### [Custom definition](#tab/custom-definition)

::: zone pivot="azure-cli"

1. Create a new JSON file named *role-definition.json*. In this file, create a resource definition specifying the data actions listed here:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Can read account-level metadata |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Can perform any container-level data operations |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Can perform any operation on items with containers |

    ```json
    {
      "properties": {
        "roleName": "Azure Cosmos DB for Table Data Plane Owner",
        "type": "CustomRole",
        "assignableScopes": [
          "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/sidandrews-rbac/providers/Microsoft.DocumentDB/databaseAccounts/sidandrews-rbac-table/"
        ],
        "permissions": [
          {
            "dataActions": [
              "Microsoft.DocumentDB/databaseAccounts/readMetadata",
              "Microsoft.DocumentDB/databaseAccounts/tables/*",
              "Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*"
            ]
          }
        ]
      }
    }
    ```

1. Now create or update a role definition using `az cosmosdb show` and `az rest` together to issue an HTTP `PUT` request. As part of this request, specify a unique GUID for your role definition.

    ```azurecli-interactive
    resourceId=$( \
        az cosmosdb show \
            --resource-group "<name-of-existing-resource-group>" \
            --name "<name-of-existing-table-account>" \
            --query "id" \
            --output tsv \
    )
    
    az rest \
        --method "PUT" \
        --url $resourceId/tableRoleDefinitions/d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4?api-version=2023-04-15 \
        --body @role-definition.json
    ```

    > [!NOTE]
    > In this example, the unique GUID specified was `d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4`. You can specify any unique GUID for your own role definition.

1. The output should now indicate that the request is queued. Now, wait for the enqueued role definition deployment to finish. This task can take a few minutes.

    ```json
    {
      "status": "Enqueued"
    }
    ```

1. Finally, check the list of role definitions using `az rest` again.

    ```azurecli-interactive
    resourceId=$( \
        az cosmosdb show \
            --resource-group "<name-of-existing-resource-group>" \
            --name "<name-of-existing-table-account>" \
            --query "id" \
            --output tsv \
    )
    
    az rest \
        --method "GET" \
        --url $resourceId/tableRoleDefinitions?api-version=2023-04-15
    ```

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. Create a new Bicep file to define your role definition. Name the file *data-plane-role-definition.bicep*. Add these `dataActions` to the definition:

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
      name: guid('table-role-definition', account.id)
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

1. Create a new Bicep parameters file named *`data-plane-role-definition.bicepparam`*. In this parameters file, assign the name of your existing Azure Cosmos DB for Table account to the `accountName` parameter.

    ```bicep
    using './data-plane-role-definition.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create). Specify the name of the Bicep template, parameters file, and Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters data-plane-role-definition.bicepparam \
        --template-file data-plane-role-definition.bicep
    ```

1. Review the output from the deployment. The output contains the unique identifier of the role definition in the `properties.outputs.definitionId.value` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    {
      "properties": {
        "outputs": {
          "definitionId": {
            "type": "String",
            "value": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-table-account/tableRoleDefinitions/dddddddd-9999-0000-1111-eeeeeeeeeeee"
          }
        }
      }
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-table-account/tableRoleDefinitions/dddddddd-9999-0000-1111-eeeeeeeeeeee`. This example uses fictitious data and your identifier would be distinct from this example. This is a subset of the typical JSON outputted from the deployment for clarity.

::: zone-end

::: zone pivot="azure-powershell"

1. Create or update your role definition using `Get-AzCosmosDBAccount` and `Invoke-AzRestMethod` together to issue an HTTP `PUT` request. Also, as part of this request, specify a unique GUID for your role definition. Finally, create a resource definition payload specifying the data actions listed here:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Can read account-level metadata |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Can perform any container-level data operations |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Can perform any operation on items with containers |

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-table-account>"
    }
    $resourceId = (
        Get-AzCosmosDBAccount @parameters |
            Select-Object -Property Id -First 1
    ).Id

    $payload = @{
      properties = @{
        roleName = "Azure Cosmos DB for Table Data Plane Owner"
        type = "CustomRole"
        assignableScopes = @(
          "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/sidandrews-rbac/providers/Microsoft.DocumentDB/databaseAccounts/sidandrews-rbac-table/"
        )
        permissions = @(
          @{
            dataActions = @(
              "Microsoft.DocumentDB/databaseAccounts/readMetadata",
              "Microsoft.DocumentDB/databaseAccounts/tables/*",
              "Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*"
            )
          }
        )
      }
    }

    $parameters = @{
      Path = "$resourceId/tableRoleDefinitions/d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4?api-version=2023-04-15"
      Method = "PUT"
      Payload = $payload | ConvertTo-Json -Depth 4
    }
    Invoke-AzRestMethod @parameters
    ```

    > [!NOTE]
    > In this example, the unique GUID specified was `d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4`. You can specify any unique GUID for your own role definition.

1. The output should return with a status code of **200**. Now, wait for the enqueued role definition deployment to finish. This task can take a few minutes.

    ```output
    StatusCode : 200
    ...
    ```

1. Finally, check the list of role definitions using `Invoke-AzRestMethod` again.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-table-account>"
    }
    $resourceId = (
        Get-AzCosmosDBAccount @parameters |
            Select-Object -Property Id -First 1
    ).Id
    
    $parameters = @{
      Path = "$resourceId/tableRoleDefinitions?api-version=2023-04-15"
      Method = "GET"
    }
    Invoke-AzRestMethod @parameters
    ```

::: zone-end

---

## Assign role to identity

Now, assign the newly defined role to an identity so that your applications can access data in Azure Cosmos DB for Table.

> [!IMPORTANT]
> This assignment task requires you to have the unique identifier of any identity you want to grant role-based access control permissions. If you do not have a unique identifier for an identity, follow the instructions in the [create managed identity](/entra/identity/managed-identities-azure-resources/how-to-configure-managed-identities) or [get signed-in identity](/cli/azure/ad/signed-in-user) guides.

::: zone pivot="azure-cli"

1. Use `az cosmosdb show` to get the unique identifier for your current account.

    ```azurecli-interactive
    az cosmosdb show \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-resource-group>" \
        --query "{id:id}"
    ```

1. Observe the output of the previous command. Record the value of the `id` property for this account as it is required to use in the next step.

    ```json
    {
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql`. This example uses fictitious data and your identifier would be distinct from this example.

1. Create a new JSON file named *role-assignment.json*. In the JSON file, add the unique identifier for your identity and unique identifier for the account resource.

    ```json
    {
      "properties": {
        "roleDefinitionId": "<account-resource-id>/tableRoleDefinitions/d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4",
        "scope": "<account-resource-id>",
        "principalId": "<id-of-existing-identity>"
      }
    }
    ```

    > [!NOTE]
    > In this example, the unique GUID specified was `d3d3d3d3-eeee-ffff-aaaa-b4b4b4b4b4b4`. You can use the unique GUID you used previously for your own role definition.

1. Now create or update a role assignment using `az cosmosdb show` and `az rest` together to issue an HTTP `PUT` request. As part of this request, specify a unique GUID for your role assignment.

    ```azurecli-interactive
    resourceId=$( \
        az cosmosdb show \
            --resource-group "<name-of-existing-resource-group>" \
            --name "<name-of-existing-table-account>" \
            --query "id" \
            --output tsv \
    )
    
    az rest \
        --method "PUT" \
        --url $resourceId/tableRoleAssignments/e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5?api-version=2023-04-15 \
        --body @role-assignment.json
    ```

    > [!NOTE]
    > In this example, the unique GUID specified was `e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5`. You can specify any unique GUID for your own role assignment.

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. Create another Bicep file to assign a role to an identity. Name this file *data-plane-role-assignment.bicep*.

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

1. Create a new Bicep parameters file named *`data-plane-role-assignment.bicepparam`*. In this parameters file; assign the name of your existing Azure Cosmos DB for Table account to the `accountName` parameter, the previously recorded role definition identifiers to the `roleDefinitionId` parameter, and the unique identifier for your identity to the `identityId` parameter.

    ```bicep
    using './data-plane-role-assignment.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    param roleDefinitionId = '<id-of-new-role-definition>'
    param identityId = '<id-of-existing-identity>'
    ```

1. Deploy this Bicep template using `az deployment group create`.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters data-plane-role-assignment.bicepparam \
        --template-file data-plane-role-assignment.bicep
    ```

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access using a managed identity.

::: zone-end

::: zone pivot="azure-powershell"

1. Use `Get-AzCosmosDBAccount to get the unique identifier for your current account.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-nosql-account>"
    }
    Get-AzCosmosDBAccount @parameters | Select -Property Id
    ```

1. Observe the output of the previous command. Record the value of the `Id` property for this account as it is required to use in the next step.

    ```output
    Id
    --    
    /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql
    ```

    > [!NOTE]
    > In this example, the `Id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql`. This example uses fictitious data and your identifier would be distinct from this example.

1. Now create or update a role assignment using `Get-AzCosmosDBAccount` and `Invoke-AzRestMethod` together to issue an HTTP `PUT` request. As part of this request, specify a unique GUID for your role assignment. Finally, create a resource assignment payload specifying the unique identifier for your identity.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-table-account>"
    }
    $resourceId = (
        Get-AzCosmosDBAccount @parameters |
            Select-Object -Property Id -First 1
    ).Id    

    $payload = @{
      properties = @{
        roleDefinitionId = "$resourceId/tableRoleDefinitions/00000000-0000-0000-0000-000000000002"
        scope = "$resourceId"
        principalId = "<id-of-existing-identity>"
      }
    }

    $parameters = @{
      Path = "$resourceId/tableRoleAssignments/e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5?api-version=2023-04-15"
      Method = "PUT"
      Payload = $payload | ConvertTo-Json -Depth 2
    }
    Invoke-AzRestMethod @parameters
    ```

    > [!NOTE]
    > In this example, the unique GUID specified was `e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5`. You can specify any unique GUID for your own role assignment.

::: zone-end

## Validate data plane access in code

Finally, validate that you correctly granted access using application code and the Azure SDK in your preferred programming language.

### [C#](#tab/csharp)

```csharp
using Azure.Identity;
using Azure.Data.Tables;

string endpoint = "<account-endpoint>";

DefaultAzureCredential credential = new();

TableServiceClient client = new(
    endpoint: new Uri(endpoint),
    tokenCredential: credential
);

TableClient table = client.GetTableClient(
    tableName: "<name-of-table>"
);

await table.GetEntityAsync<TableEntity>(
    partitionKey: "<partition-key>",
    rowKey: "<row-key>"
);
```

> [!IMPORTANT]
> This code sample uses the [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) and [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) libraries from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { TableServiceClient, TableClient } = require('@azure/data-tables');
const { DefaultAzureCredential } = require('@azure/identity');

const endpoint = '<account-endpoint>';

let credential = new DefaultAzureCredential();

let client = new TableServiceClient(endpoint, credential);

let table = new TableClient(endpoint, "<table-name>", credential);

await table.getEntity("<partition-key>", "<row-key>");
```

> [!IMPORTANT]
> This code sample uses the [`@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [TypeScript](#tab/typescript)

```typescript
import { TableServiceClient, TableClient } from '@azure/data-tables';
import { TokenCredential, DefaultAzureCredential } from '@azure/identity';

const endpoint: string = '<account-endpoint>';

let credential: TokenCredential = new DefaultAzureCredential();

let client: TableServiceClient = new TableServiceClient(endpoint, credential);

let table: TableClient = new TableClient(endpoint, "<table-name>", credential);

await table.getEntity("<partition-key>", "<row-key>");
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

table = client.get_table_client("<table-name>")

table.get_entity(
    row_key="<row-key>",
    partition_key="<partition-key>"
)
```

> [!IMPORTANT]
> This code sample uses the [`azure-data-tables`](https://pypi.org/project/azure-data-tables/) and [`azure-identity`](https://pypi.org/project/azure-identity/) packages from PyPI.

### [Go](#tab/go)

```go
import (
    "context"
    
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/data/aztables"
)

const endpoint = "<account-endpoint>"

func main() {
    credential, _ := azidentity.NewDefaultAzureCredential(nil)
    client, _ := aztables.NewServiceClient(endpoint, credential, nil)
    table := client.NewClient("<table-name>")
    
    _, err := table.GetEntity(context.TODO(), "<partition-key>", "<row-key>", nil)
    if err != nil {
        panic(err)
    }
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/data/aztables`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) and [`azure/azure-sdk-for-go/sdk/azidentity`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) packages from Go.

### [Java](#tab/java)

```java
import com.azure.data.tables.TableClient;
import com.azure.data.tables.TableServiceClient;
import com.azure.data.tables.TableServiceClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

public class Table{
    public static void main(String[] args){
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
            .build();
        
        TableServiceClient client = new TableServiceClientBuilder()
            .endpoint("<nosql-endpoint>")
            .credential(credential)
            .buildClient();

        TableClient table = client
            .getTableClient("<table-name>");

        table.getEntity("<partition-key>", "<row-key>");
    }
}
```

> [!IMPORTANT]
> This code samples uses the [`com.azure/azure-data-tables`](https://mvnrepository.com/artifact/com.azure/azure-data-tables) and [`com.azure/azure-identity`](https://mvnrepository.com/artifact/com.azure/azure-identity) packages from Maven.

---

> [!WARNING]
> If you are using a user-assigned managed identity, you will need to specify the unique identifier of the managed identity as part of creating the credentials object.
