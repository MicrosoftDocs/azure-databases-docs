---
title: Connect using role-based access control and Microsoft Entra ID
description: Learn how to set up role-based access control for Azure Cosmos DB for NoSQL accounts and data. Enhance security for your applications with step-by-step guidance.
author: seesharprun
ms.author: sidandrews
ms.reviewer: skhera
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.devlang: python
ms.date: 09/10/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
defaultDevLang: python
dev_langs:
  - python
  - javascript
  - typescript
  - csharp
  - go
  - java
  - rust
appliesto:
  - ✅ NoSQL
#Customer Intent: As a developer, I want to connect to Azure Cosmos DB for NoSQL using role-based access control, so that I can securely manage access to my database resources.
---

# Connect to Azure Cosmos DB for NoSQL using role-based access control and Microsoft Entra ID

Role-based access control refers to a method to manage access to resources in Azure. This method is based on specific identities being assigned roles that manage what level of access they have to one or more resources. Role-based access control provides a flexible system of fine-grained access management that ensures identities only have the least privileged level of access they need to perform their task.

For more information, see [role-based access control](/azure/role-based-access-control/overview).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An existing Azure Cosmos DB for NoSQL account.

- One or more existing identities in Microsoft Entra ID.

::: zone pivot="azure-cli,azure-resource-manager-bicep"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-portal"

::: zone-end

::: zone pivot="azure-powershell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Disable key-based authentication

[!INCLUDE[Disable key-based authentication](includes/disable-key-based-authentication.md)]

## Validate that key-based authentication is disabled

To validate that key-based access is disabled, attempt to use the Azure SDK to connect to Azure Cosmos DB for NoSQL using a resource-owner password credential (ROPC). This attempt should fail. If necessary, code samples for common programming languages are provided here.

```csharp
using Microsoft.Azure.Cosmos;

string connectionString = "AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;";

CosmosClient client = new(connectionString);
```

```javascript
const { CosmosClient } = require('@azure/cosmos');

const connectionString = 'AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;';

const client = new CosmosClient(connectionString);
```

```typescript
import { CosmosClient } from '@azure/cosmos'

let connectionString: string = 'AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;';

const client: CosmosClient = new CosmosClient(connectionString);
```

```python
from azure.cosmos import CosmosClient

connection_string = "AccountEndpoint=<nosql-endpoint>;AccountKey=<key>;"

client = CosmosClient(connection_string)
```

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

```rust
use azure_data_cosmos::CosmosClient;

fn main() {
    let client = CosmosClient::new_with_access_key(
        "<account-endpoint>",
        "<account-key>",
        None,
    ).unwrap();

    let container = client.database_client("<database-name>").container_client("<container-name>");

    let response = container.read_item("<partition-key>", "<item-id>", None);
    tokio::runtime::Runtime::new().unwrap().block_on(response).unwrap();
}
```

## Grant control plane role-based access

[!INCLUDE[Grant control plane role-based access](includes/grant-control-plane-role-based-access.md)]

## Validate control plane role-based access in code

[!INCLUDE[Validate control plane role-based access](includes/validate-control-plane-role-based-access.md)]

## Grant data plane role-based access

Data plane access refers to the ability to read and write data within an Azure service without the ability to manage resources in the account. For example, Azure Cosmos DB data plane access could include the ability to:

- Read some account and resource metadata
- Create, read, update, patch, and delete items
- Execute NoSQL queries
- Read from a container's change feed
- Execute stored procedures
- Manage conflicts in the conflict feed

First, you must prepare a role definition with a list of `dataActions` to grant access to read, query, and manage data in Azure Cosmos DB for NoSQL. In this guide, you prepare a custom role. Then, assign the newly defined role to an identity so that your applications can access data in Azure Cosmos DB for NoSQL.

> [!IMPORTANT]
> Obtaining an existing data plane role definition requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
>
> Creating a new data plane role definition requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/write`
>
> Creating a new data plane role assignment requires these control plane permissions:
>
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/read`
> - `Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/write`
>

> [!WARNING]
> Azure Cosmos DB for NoSQL's native role-based access control doesn't support the `notDataActions` property. Any action that isn't specified as an allowed `dataAction` is excluded automatically.

::: zone pivot="azure-cli"

1. List all of the role definitions associated with your Azure Cosmos DB for NoSQL account using [`az cosmosdb sql role definition list`](/cli/azure/cosmosdb/sql/role/definition#az-cosmosdb-sql-role-definition-list). 

    ```azurecli-interactive
    az cosmosdb sql role definition list \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>"
    ```


1. Create a new JSON file named *role-definition.json*, which is used for the creation of the custom role. In this file, create a resource definition specifying the data actions listed here:

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
1. Review the output from the previous command. Locate the role definition you just created named **Azure Cosmos DB for NOSQL Data Plane Owner**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide as `--role-definition-id`

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
    > In this example, the `--role-definition-id` value would be `bbbbbbbb-1111-2222-3333-cccccccccccc`. This example uses fictitious data and your identifier would be distinct from this example.

1. Assign the new role using [`az cosmosdb sql role assignment create`](/cli/azure/cosmosdb/sql/role/assignment#az-cosmosdb-sql-role-assignment-create). Use the previously recorded role definition identifiers for the `--role-definition-id` argument, unique identifier for your identity for the `--principal-id` argument, and the data plane scope for the `--scope` argument. To grant access to the entire account, use `/` as the scope.

    ```azurecli-interactive
    az cosmosdb sql role assignment create \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>" \
        --role-definition-id "<id-of-new-role-definition>" \
        --principal-id "<id-of-existing-identity>" \
        --scope "/"
    ```

    > [!TIP]
    > If you're attempting to grant data plane role-based access control to your own identity, you can use this command to get the identity:
    >
    > ```azurecli-interactive
    > az ad signed-in-user show
    > ```
    >
    > For more information, see [`az ad signed-in-user`](/cli/azure/ad/signed-in-user).

    > [!TIP]
    > In Azure Cosmos DB's native implementation of role-based access control, **scope** refers to the granularity of resources within an account for which you want permission applied. At the highest level, you can scope a data plane role-based access control assignment to the entire account using the largest scope. This scope includes all databases and containers within the account:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/
    > ```
    >
    > Or, you can scope your data plane role assignment to a specific database:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>
    > ```
    >
    > Finally, you can scope the assignment to a single container, the most granular scope:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>/colls/<container-name>
    > ```
    >
    > In many cases, you can use the relative scope instead of the fully qualified scope. For example, you can use this relative scope to grant data plane role-based access control permissions to a specific database and container from an Azure CLI command:
    >
    > ```output
    > /dbs/<database-name>/colls/<container-name>
    > ```
    >
    > You can also grant universal access to all databases and containers using the relative scope:
    >
    > ```output
    > /
    > ```
    >

1. Use [`az cosmosdb sql role assignment list`](/cli/azure/cosmosdb/sql/role/assignment#az-cosmosdb-sql-role-assignment-list) to list all role assignments for your Azure Cosmos DB for NoSQL account. Review the output to ensure your role assignment was created.

    ```azurecli-interactive
    az cosmosdb sql role assignment list \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>"
    ```

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. List all of the role definitions associated with your Azure Cosmos DB for NoSQL account using [`az cosmosdb sql role definition list`](/cli/azure/cosmosdb/sql/role/definition#az-cosmosdb-sql-role-definition-list).

    ```azurecli-interactive
    az cosmosdb sql role definition list \
        --resource-group "<name-of-existing-resource-group>" \
        --account-name "<name-of-existing-nosql-account>"
    ```

1. Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

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

    > [!TIP]
    > In Azure Cosmos DB's native implementation of role-based access control, **scope** refers to the granularity of resources within an account for which you want permission applied. At the highest level, you can scope a data plane role-based access control assignment to the entire account using the largest scope. This scope includes all databases and containers within the account:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/
    > ```
    >
    > Or, you can scope your data plane role assignment to a specific database:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>
    > ```
    >
    > Finally, you can scope the assignment to a single container, the most granular scope:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>/colls/<container-name>
    > ```
    >
    > In many cases, you can use the relative scope instead of the fully qualified scope. For example, you can use this relative scope to grant data plane role-based access control permissions to a specific database and container from an Azure CLI command:
    >
    > ```output
    > /dbs/<database-name>/colls/<container-name>
    > ```
    >
    > You can also grant universal access to all databases and containers using the relative scope:
    >
    > ```output
    > /
    > ```
    >

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

1. Create a new Bicep file to define your role assignment. Name the file *data-plane-role-assignment.bicep*.

    ```bicep
    metadata description = 'Assign RBAC role for data plane access to Azure Cosmos DB for NoSQL.'
    
    @description('Name of the Azure Cosmos DB for NoSQL account.')
    param accountName string
    
    @description('Id of the role definition to assign to the targeted principal in the context of the account.')
    param roleDefinitionId string
    
    @description('Id of the identity/principal to assign this role in the context of the account.')
    param identityId string = deployer().objectId
    
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

    > [!TIP]
    > If you're attempting to grant data plane role-based access control to your own identity, you can omit the `identityId` parameter. The Bicep template then uses `deployer().objectId` to get the identity of the principal that deployed the template. For more information, see [`deployer`](/azure/azure-resource-manager/bicep/bicep-functions-deployment#deployer).

1. Deploy the Bicep template using `az deployment group create`.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters data-plane-role-assignment.bicepparam \
        --template-file data-plane-role-assignment.bicep
    ```

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity. You can also repeat these steps to allow applications to access resources using a managed identity.

::: zone-end

::: zone pivot="azure-powershell"

1. Use [`Get-AzCosmosDBSqlRoleDefinition`](/powershell/module/az.cosmosdb/get-azcosmosdbsqlroledefinition) to list all of the role definitions associated with your Azure Cosmos DB for NoSQL account.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
    }
    Get-AzCosmosDBSqlRoleDefinition @parameters
    ```

1. Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `Id` property. Record this value as it is required to use in the assignment step later in this guide.

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

    > [!TIP]
    > In Azure Cosmos DB's native implementation of role-based access control, **scope** refers to the granularity of resources within an account for which you want permission applied. At the highest level, you can scope a data plane role-based access control assignment to the entire account using the largest scope. This scope includes all databases and containers within the account:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/
    > ```
    >
    > Or, you can scope your data plane role assignment to a specific database:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>
    > ```
    >
    > Finally, you can scope the assignment to a single container, the most granular scope:
    >
    > ```output
    > /subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>/dbs/<database-name>/colls/<container-name>
    > ```
    >
    > In many cases, you can use the relative scope instead of the fully qualified scope. For example, you can use this relative scope to grant data plane role-based access control permissions to a specific database and container from an Azure CLI command:
    >
    > ```output
    > /dbs/<database-name>/colls/<container-name>
    > ```
    >
    > You can also grant universal access to all databases and containers using the relative scope:
    >
    > ```output
    > /
    > ```
    >

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

1. Use [`Get-AzCosmosDBAccount`](/powershell/module/az.cosmosdb/get-azcosmosdbaccount) to get the metadata for your current account.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-nosql-account>"
    }    
    Get-AzCosmosDBAccount @parameters | Select -Property Id
    ```

1. Use [`New-AzCosmosDBSqlRoleAssignment`](/powershell/module/az.cosmosdb/new-azcosmosdbsqlroleassignment) to assign the new role. Use the previously recorded role definition identifiers for the `RoleDefinitionId` parameter, unique identifier for your identity for the `PrincipalId` parameter, and the data plane scope for the `Scope` parameter. To grant access to the entire account, use `/` as the scope.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
        RoleDefinitionId = "<id-of-new-role-definition>"
        PrincipalId = "<id-of-existing-identity>"
        Scope = "/"
    }
    New-AzCosmosDBSqlRoleAssignment @parameters
    ```

    > [!TIP]
    > If you're attempting to grant data plane role-based access control to your own identity, you can use this command to get the identity:
    >
    > ```azurepowershell-interactive
    > Get-AzADUser -SignedIn | Format-List `
    >     -Property Id, DisplayName, Mail, UserPrincipalName
    > ```
    >
    > For more information, see [`Get-AzADUser`](/powershell/module/az.resources/get-azaduser).

1. List all role assignments for your Azure Cosmos DB for NoSQL account using [`Get-AzCosmosDBSqlRoleAssignment`](/powershell/module/az.cosmosdb/get-azcosmosdbsqlroleassignment). Review the output to ensure your role assignment was created.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        AccountName = "<name-of-existing-nosql-account>"
    }
    Get-AzCosmosDBSqlRoleAssignment @parameters
    ```

::: zone-end

::: zone pivot="azure-portal"

> [!WARNING]
> Managing data plane role-based access control isn't supported in the Azure portal.

::: zone-end

## Validate data plane role-based access in code

Validate that you correctly granted access using application code and the Azure SDK.

```csharp
using Azure.Core;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

string endpoint = "<account-endpoint>";

TokenCredential credential = new DefaultAzureCredential();

CosmosClient client = new(endpoint, credential);

Container container = client.GetContainer("<database-name>", "<container-name>");

await container.ReadItemAsync<dynamic>("<item-id>", new PartitionKey("<partition-key>"));
```

```javascript
const { CosmosClient } = require('@azure/cosmos');
const { DefaultAzureCredential } = require('@azure/identity');

const endpoint = '<account-endpoint>';

const credential = new DefaultAzureCredential();

const client = new CosmosClient({ endpoint, aadCredentials:credential});

const container = client.database('<database-name>').container('<container-name>');

await container.item('<item-id>', '<partition-key>').read<String>();
```

```typescript
import { Container, CosmosClient, CosmosClientOptions } from '@azure/cosmos'
import { TokenCredential, DefaultAzureCredential } from '@azure/identity'

let endpoint: string = '<account-endpoint>';

let credential: TokenCredential = new DefaultAzureCredential();

let options: CosmosClientOptions = {
  endpoint: endpoint,
  aadCredentials: credential
};

const client: CosmosClient = new CosmosClient(options);

const container: Container = client.database('<database-name>').container('<container-name>');

await container.item('<item-id>', '<partition-key>').read<String>();
```

```python
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

endpoint = "<account-endpoint>"

credential = DefaultAzureCredential()

client = CosmosClient(endpoint, credential=credential)

container = client.get_database_client("<database-name>").get_container_client("<container-name>")

container.read_item(
    item="<item-id>",
    partition_key="<partition-key>",
)
```

```go
import (
    "context"
    
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/data/azcosmos"
)

const endpoint = "<account-endpoint>"

func main() {
    credential, _ := azidentity.NewDefaultAzureCredential(nil)
    client, _ := azcosmos.NewClient(endpoint, credential, nil)
    
    database, _ := client.NewDatabase("<database-name>")
    container, _ := database.NewContainer("<container-name>")
    
    _, err := container.ReadItem(context.TODO(), azcosmos.NewPartitionKeyString("<partition-key>"), "<item-id>", nil)
    if err != nil {
        panic(err)
    }
}
```

```java
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.CosmosContainer;
import com.azure.cosmos.models.PartitionKey;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

public class NoSQL {
    public static void main(String[] args) {   
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
            .build();
            
        CosmosClient client = new CosmosClientBuilder()
            .endpoint("<account-endpoint>")
            .credential(credential)
            .buildClient();

        CosmosContainer container = client.getDatabase("<database-name>").getContainer("<container-name>");

        container.readItem("<item-id>", new PartitionKey("<partition-key>"), Object.class);
    }
}
```

```rust
use azure_data_cosmos::CosmosClient;
use azure_identity::DefaultAzureCredential;

fn main() {
    let credential = DefaultAzureCredential::new().unwrap();
    let client = CosmosClient::new("<account-endpoint>", credential, None).unwrap();

    let container = client.database_client("<database-name>").container_client("<container-name>");

    let response = container.read_item("<partition-key>", "<item-id>", None);
    tokio::runtime::Runtime::new().unwrap().block_on(response).unwrap();
}
```

## Related content

- [Secure your Azure Cosmos DB for NoSQL account](security.md)
- [Overview of Azure Cosmos DB for NoSQL](overview.md)
