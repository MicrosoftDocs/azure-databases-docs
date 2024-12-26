---
title: Use data plane role-based access control
titleSuffix: Azure Cosmos DB for NoSQL
description: Grant access to run queries, manage entities, and perform operations using role-based access control, Microsoft Entra, and Azure Cosmos DB for NoSQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/09/2024
zone_pivot_groups: azure-interface-cli-powershell-bicep
#Customer Intent: As a security user, I want to grant an identity data-plane access to Azure Cosmos DB for NoSQL, so that my developer team can use the SDK of their choice with minimal code change.
---

# Use data plane role-based access control with Azure Cosmos DB for NoSQL

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

:::image type="complex" source="media/how-to-grant-control-plane-role-based-access/map.svg" border="false" alt-text="Diagram of the current location ('Role-based access control') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, Network, and Reference. The 'Role-based access control' location is currently highlighted.
:::image-end:::

> [!Tip] 
> Visit our new **[Samples Gallery](https://aka.ms/AzureCosmosDB/Gallery)** for the latest samples for building new apps

This article walks through the steps to grant an identity access to manage data in an Azure Cosmos DB for NoSQL account.

> [!IMPORTANT]
> The steps in this article only cover data plane access to perform operations on individual items and run queries. To learn how to manage databases and containers for the control plane, see [grant control plane role-based access](how-to-grant-control-plane-role-based-access.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- An existing Azure Cosmos DB for NoSQL account.
- One or more existing identities in Microsoft Entra ID.

::: zone pivot="azure-interface-cli,azure-interface-bicep"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-shell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Prepare role definition

First, you must prepare a role definition with a list of `dataActions` to grant access to read, query, and manage data in Azure Cosmos DB for NoSQL.

### [Built-in definition](#tab/built-in-definition)

> [!IMPORTANT]
> Obtaining an existing data plane role definition requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
>
> For more information, see [grant control plane role-based access](how-to-grant-control-plane-role-based-access.md).

::: zone pivot="azure-interface-cli,azure-interface-bicep"

List all of the role definitions associated with your Azure Cosmos DB for NoSQL account using [`az cosmosdb sql role definition list`](/cli/azure/cosmosdb/sql/role/definition#az-cosmosdb-sql-role-definition-list). Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

```azurecli-interactive
az cosmosdb sql role definition list \
    --resource-group "<name-of-existing-resource-group>" \
    --account-name "<name-of-existing-nosql-account>"
```

```json
[
  ...,
  {
    "assignableScopes": [
      "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
    ],
    "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002",
    "name": "00000000-0000-0000-0000-000000000002",
    "permissions": [
      {
        "dataActions": [
          "Microsoft.DocumentDB/databaseAccounts/readMetadata",
          "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
          "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*"
        ],
        "notDataActions": []
      }
    ],
    "resourceGroup": "msdocs-identity-example",
    "roleName": "Cosmos DB Built-in Data Contributor",
    "type": "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions",
    "typePropertiesType": "BuiltInRole"
  }
  ...
]
```

> [!NOTE]
> In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002`. This example uses fictitious data and your identifier would be distinct from this example.

::: zone-end

::: zone pivot="azure-interface-shell"

Use [`Get-AzCosmosDBSqlRoleDefinition`](/powershell/module/az.cosmosdb/get-azcosmosdbsqlroledefinition) to list all of the role definitions associated with your Azure Cosmos DB for NoSQL account. Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `Id` property. Record this value as it is required to use in the assignment step later in this guide.

```azurepowershell-interactive
$parameters = @{
    ResourceGroupName = "<name-of-existing-resource-group>"
    AccountName = "<name-of-existing-nosql-account>"
}
Get-AzCosmosDBSqlRoleDefinition @parameters
```

```output
Id                         : /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002
RoleName                   : Cosmos DB Built-in Data Contributor
Type                       : BuiltInRole
AssignableScopes           : {/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccountsmsdocs-identity-example-nosql}
Permissions.DataActions    : {Microsoft.DocumentDB/databaseAccounts/readMetadata, Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*, Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*}
Permissions.NotDataActions : 
```

> [!NOTE]
> In this example, the `Id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002`. This example uses fictitious data and your identifier would be distinct from this example. However, the identifier (`00000000-0000-0000-0000-000000000002`) is unique across all role definitions in your account.

::: zone-end

### [Custom definition](#tab/custom-definition)

> [!IMPORTANT]
> Creating a new data plane role definition requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/write`
>
> For more information, see [grant control plane role-based access](how-to-grant-control-plane-role-based-access.md).

> [!WARNING]
> Azure Cosmos DB for NoSQL's native role-based access control doesn't support the `notDataActions` property. Any action that is not specified as an allowed `dataAction` is excluded automatically.

::: zone pivot="azure-interface-cli"

1. Create a new JSON file named *role-definition.json*. In this file, create a resource definition specifying the data actions listed here:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Can read account-level metadata |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Can perform any container-level data operations |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Can perform any operation on items with containers |

    ```json
    {
      "RoleName": "Azure Cosmos DB for NoSQL Data Plane Owner",
      "Type": "CustomRole",
      "AssignableScopes": [
        "/"
      ],
      "Permissions": [
        {
          "DataActions": [
            "Microsoft.DocumentDB/databaseAccounts/readMetadata",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*"
          ]
        }
      ]
    }
    ```

1. Next, use [`az cosmosdb sql role definition create`](/cli/azure/cosmosdb/sql/role/definition#az-cosmosdb-sql-role-definition-create) to create the role definition. Use the *role-definition.json* as the input for the `--body` argument.

    ```azurecli-interactive
    az cosmosdb sql role definition create \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>" \
        --body "@role-definition.json"
    ```  

1. Now, list all of the role definitions associated with your Azure Cosmos DB for NoSQL account using [`az cosmosdb sql role definition list`](/cli/azure/cosmosdb/sql/role/definition#az-cosmosdb-sql-role-definition-list).

    ```azurecli-interactive
    az cosmosdb sql role definition list \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>"
    ```

1. Review the output from the previous command. Locate the role definition you just created named **Azure Cosmos DB for NOSQL Data Plane Owner**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    {
      "assignableScopes": [
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
      ],
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/bbbbbbbb-1111-2222-3333-cccccccccccc",
      "name": "bbbbbbbb-1111-2222-3333-cccccccccccc",
      "permissions": [
        {
          "dataActions": [
            "Microsoft.DocumentDB/databaseAccounts/readMetadata",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*"
          ],
          "notDataActions": []
        }
      ],
      "resourceGroup": "msdocs-identity-example",
      "roleName": "Azure Cosmos DB for NoSQL Data Plane Owner",
      "type": "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions",
      "typePropertiesType": "CustomRole"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/bbbbbbbb-1111-2222-3333-cccccccccccc`. This example uses fictitious data and your identifier would be distinct from this example.

::: zone-end

::: zone pivot="azure-interface-bicep"

1. Create a new Bicep file to define your role definition. Name the file *data-plane-role-definition.bicep*. Add these `dataActions` to the definition:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Can read account-level metadata |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Can perform any container-level data operations |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Can perform any operation on items with containers |

    ```bicep
    metadata description = 'Create RBAC definition for data plane access to Azure Cosmos DB for NoSQL.'
    
    @description('Name of the Azure Cosmos DB for NoSQL account.')
    param accountName string
    
    @description('Name of the role definition.')
    param roleDefinitionName string = 'Azure Cosmos DB for NoSQL Data Plane Owner'
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' existing = {
      name: accountName
    }
    
    resource definition 'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions@2024-05-15' = {
      name: guid(account.id, roleDefinitionName)
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
              'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*'
              'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*'
            ]
          }
        ]
      }
    }
    
    output definitionId string = definition.id
    ```

1. Create a new Bicep parameters file named *data-plane-role-definition.`bicepparam`*. In this parameters file, assign the name of your existing Azure Cosmos DB for NoSQL account to the `accountName` parameter.

    ```bicep
    using './data-plane-role-definition.bicep'
    
    param accountName = '<name-of-existing-nosql-account>'
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create).

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters data-plane-role-definition.bicepparam \
        --template-file data-plane-role-definition.bicep
    ```

::: zone-end

::: zone pivot="azure-interface-shell"

1. Create a new role definition using [`New-AzCosmosDBSqlRoleDefinition`](/powershell/module/az.cosmosdb/new-azcosmosdbsqlroledefinition). For the `DataAction` parameter, specify the data actions listed here:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDB/databaseAccounts/readMetadata`** | Can read account-level metadata |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*`** | Can perform any container-level data operations |
    | **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*`** | Can perform any operation on items with containers |

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
        RoleName = "Azure Cosmos DB for NoSQL Data Plane Owner"
        Type = "CustomRole"
        AssignableScope = @(
            "/"
        )
        DataAction = @(
            "Microsoft.DocumentDB/databaseAccounts/readMetadata",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
            "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*"
        )
    }
    New-AzCosmosDBSqlRoleDefinition @parameters
    ```

1. Use [`Get-AzCosmosDBSqlRoleDefinition`](/powershell/module/az.cosmosdb/get-azcosmosdbsqlroledefinition) to list all of the role definitions associated with your Azure Cosmos DB for NoSQL account.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
    }
    Get-AzCosmosDBSqlRoleDefinition @parameters    
    ```

1. Review the output from the previous command. Locate the role definition you just created named **Azure Cosmos DB for NOSQL Data Plane Owner**. The output contains the unique identifier of the role definition in the `Id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```output
    Id                         : /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/bbbbbbbb-1111-2222-3333-cccccccccccc
    RoleName                   : Azure Cosmos DB for NoSQL Data Plane Owner
    Type                       : CustomRole
    AssignableScopes           : {/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql}
    Permissions.DataActions    : {Microsoft.DocumentDB/databaseAccounts/readMetadata, Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*, Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*}
    Permissions.NotDataActions :
    ```

    > [!NOTE]
    > In this example, the `Id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql/sqlRoleDefinitions/bbbbbbbb-1111-2222-3333-cccccccccccc`. This example uses fictitious data and your identifier would be distinct from this example.

::: zone-end

---

## Assign role to identity

Now, assign the newly defined role to an identity so that your applications can access data in Azure Cosmos DB for NoSQL.

> [!IMPORTANT]
> Creating a new data plane role assignment requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/write`
>
> For more information, see [grant control plane role-based access](how-to-grant-control-plane-role-based-access.md).

::: zone pivot="azure-interface-cli"

1. Use [`az cosmosdb show`](/cli/azure/cosmosdb#az-cosmosdb-show) to get the unique identifier for your current account.

    ```azurecli-interactive
    az cosmosdb show \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-nosql-account>" \
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

1. Assign the new role using [`az cosmosdb sql role assignment create`](/cli/azure/cosmosdb/sql/role/assignment#az-cosmosdb-sql-role-assignment-create). Use the previously recorded role definition identifiers to the `--role-definition-id` argument, and the unique identifier for your identity to the `--principal-id` argument. Finally, use your account's identifier for the `--scope` argument.

    ```azurecli-interactive
    az cosmosdb sql role assignment create \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>" \
        --role-definition-id "<id-of-new-role-definition>" \
        --principal-id "<id-of-existing-identity>" \
        --scope "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
    ```

1. Use [`az cosmosdb sql role assignment list`](/cli/azure/cosmosdb/sql/role/assignment#az-cosmosdb-sql-role-assignment-list) to list all role assignments for your Azure Cosmos DB for NoSQL account. Review the output to ensure your role assignment was created.

    ```azurecli-interactive
    az cosmosdb sql role assignment list \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>"
    ```

::: zone-end

::: zone pivot="azure-interface-bicep"

1. Create a new Bicep file to define your role assignment. Name the file *data-plane-role-assignment.bicep*.

    ```bicep
    metadata description = 'Assign RBAC role for data plane access to Azure Cosmos DB for NoSQL.'
    
    @description('Name of the Azure Cosmos DB for NoSQL account.')
    param accountName string
    
    @description('Id of the role definition to assign to the targeted principal in the context of the account.')
    param roleDefinitionId string
    
    @description('Id of the identity/principal to assign this role in the context of the account.')
    param identityId string
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' existing = {
      name: accountName
    }
    
    resource assignment 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-05-15' = {
      name: guid(roleDefinitionId, identityId, account.id)
      parent: account
      properties: {
        principalId: identityId
        roleDefinitionId: roleDefinitionId
        scope: account.id
      }
    }
    
    output assignmentId string = assignment.id
    ```

1. Create a new Bicep parameters file named *data-plane-role-assignment.`bicepparam`*. In this parameters file, assign the name of your existing Azure Cosmos DB for NoSQL account to the `accountName` parameter, the previously recorded role definition identifiers to the `roleDefinitionId` parameter, and the unique identifier for your identity to the `identityId` parameter.

    ```bicep
    using './data-plane-role-assignment.bicep'
    
    param accountName = '<name-of-existing-nosql-account>'
    param roleDefinitionId = '<id-of-new-role-definition>'
    param identityId = '<id-of-existing-identity>'
    ```

1. Deploy the Bicep template using `az deployment group create`.

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

::: zone pivot="azure-interface-shell"

1. Use [`Get-AzCosmosDBAccount`](/powershell/module/az.cosmosdb/get-azcosmosdbaccount) to get the metadata for your current account.

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

1. Use [`New-AzCosmosDBSqlRoleAssignment`](/powershell/module/az.cosmosdb/new-azcosmosdbsqlroleassignment) to assign the new role. Use the previously recorded role definition identifiers to the `RoleDefinitionId` parameter, and the unique identifier for your identity to the `PrincipalId` parameter. Finally, use your account's identifier for the `Scope` parameter.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
        RoleDefinitionId = "<id-of-new-role-definition>"
        PrincipalId = "<id-of-existing-identity>"
        Scope = "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/msdocs-identity-example/providers/Microsoft.DocumentDB/databaseAccounts/msdocs-identity-example-nosql"
    }    
    New-AzCosmosDBSqlRoleAssignment @parameters
    ```

1. List all role assignments for your Azure Cosmos DB for NoSQL account using [`Get-AzCosmosDBSqlRoleAssignment`](/powershell/module/az.cosmosdb/get-azcosmosdbsqlroleassignment). Review the output to ensure your role assignment was created.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
    }
    Get-AzCosmosDBSqlRoleAssignment @parameters
    ```

::: zone-end

## Validate data plane access in code

Finally, validate that you correctly granted access using application code and the Azure SDK in your preferred programming language.

### [C#](#tab/csharp)

```csharp
using Azure.Core;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

string endpoint = "<account-endpoint>";

TokenCredential credential = new DefaultAzureCredential();

CosmosClient client = new(endpoint, credential);
```

> [!IMPORTANT]
> This code sample uses the [`Microsoft.Azure.Cosmos`](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) and [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) libraries from NuGet.

### [JavaScript](#tab/javascript)

```javascript
const { CosmosClient } = require('@azure/cosmos');
const { DefaultAzureCredential } = require('@azure/identity');

const endpoint = '<account-endpoint>';

const credential = new DefaultAzureCredential();

const client = new CosmosClient({ endpoint, aadCredentials:credential})
```

> [!IMPORTANT]
> This code sample uses the [`@azure/cosmos`](https://www.npmjs.com/package/@azure/cosmos) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [TypeScript](#tab/typescript)

```typescript
import { CosmosClient, CosmosClientOptions } from '@azure/cosmos'
import { TokenCredential, DefaultAzureCredential } from '@azure/identity'

let endpoint: string = '<account-endpoint>';

let credential: TokenCredential = new DefaultAzureCredential();

let options: CosmosClientOptions = {
  endpoint: endpoint,
  aadCredentials: credential
};

const client: CosmosClient = new CosmosClient(options);
```

> [!IMPORTANT]
> This code sample uses the [`@azure/cosmos`](https://www.npmjs.com/package/@azure/cosmos) and [`@azure/identity`](https://www.npmjs.com/package/@azure/identity) packages from npm.

### [Python](#tab/python)

```python
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

endpoint = "<account-endpoint>"

credential = DefaultAzureCredential()

client = CosmosClient(endpoint, credential=credential)
```

> [!IMPORTANT]
> This code sample uses the [`azure-cosmos`](https://pypi.org/project/azure-cosmos/) and [`azure-identity`](https://pypi.org/project/azure-identity/) packages from PyPI.

### [Go](#tab/go)

```go
package main

import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos"
)

const endpoint = "<account-endpoint>"

func main() {
    credential, _ := azidentity.NewDefaultAzureCredential(nil)
    client, _ := azcosmos.NewClient(endpoint, credential, nil)
}
```

> [!IMPORTANT]
> This code sample uses the [`azure/azure-sdk-for-go/sdk/data/azcosmos`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos) [`azure/azure-sdk-for-go/azidentity`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) packages from Go.

### [Java](#tab/java)

```java
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

public class NoSQL{
    public static void main(String[] args){
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
            .build();
        
        CosmosClient client = new CosmosClientBuilder()
            .endpoint("<account-endpoint>")
            .credential(credential)
            .buildClient();
    }
}
```

> [!IMPORTANT]
> This code samples uses the [`com.azure/azure-cosmos`](https://mvnrepository.com/artifact/com.azure/azure-cosmos) and [`com.azure/azure-identity`](https://mvnrepository.com/artifact/com.azure/azure-identity) packages from Maven.

---
