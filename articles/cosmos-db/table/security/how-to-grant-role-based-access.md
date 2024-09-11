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

## Get the account's unique identifier

TODO

1. TODO

## Create role-based access control definition

TODO

1. TODO

1. TODO. Name file *rbac-definition.bicep*.

    ```bicep
    metadata description = 'Create RBAC definition for data plane access to Azure Cosmos DB for Table.'
    
    @description('Name of the Azure Cosmos DB for Table account.')
    param accountName string
    
    @description('Name of the role definition.')
    param roleDefinitionName string
    
    @description('Description of the role definition.')
    param roleDefinitionDescription string
    
    resource account 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' existing = {
      name: accountName
    }
    
    resource definition 'Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions@2023-04-15' = {
      name: guid('nosql-role-definition', account.id)
      parent: account
      properties: {
        roleName: roleDefinitionName
        description: roleDefinitionDescription
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

1. TODO. Name file *`rbac-definition.bicepparam`*.

    ```bicep
    using './rbac-definition.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    param roleDefinitionName = 'API for Table Data Plane Owner'
    param roleDefinitionDescription = 'Grants permission to read metadata and perform all actions on tables, containers, and entities.'
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create).

    ```azurecli-interactive
    az deployment group create `
        --resource-group "<name-of-existing-resource-group>" `
        --parameters rbac-definition.bicepparam `
        --template-file rbac-definition.bicep
    ```

1. Review the output from the deployment

    ```json
    {
      "properties": {
        "outputs": {
          "definitionId": {
            "type": "String",
            "value": "<id-of-new-role-definition>"
          }
        }
      }
    }
    ```

    > [!NOTE]
    > This is a subset of the typical JSON outputted from the deployment for clarity.

## Assign role-based access control permission

TODO

1. TODO

1. TODO. Name file *rbac-assignment.bicep*.

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

1. TODO. Name file *`rbac-assignment.bicepparam`*.

    ```bicep
    using './rbac-assignment.bicep'
    
    param accountName = '<name-of-existing-table-account>'
    param roleDefinitionId = '<id-of-new-role-definition>'
    param identityId = '<id-of-existing-identity>'
    ```

1. TODO. [`az deployment group create`](/cli/azure/group/deployment#az-group-deployment-create).

    ```azurecli-interactive
    az deployment group create `
        --resource-group "<name-of-existing-resource-group>" `
        --parameters rbac-assignment.bicepparam `
        --template-file rbac-assignment.bicep
    ```

1. Repeat these steps to grant access to the account from other identities.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access using a managed identity.

## Next step

> [!div class="nextstepaction"]
> [Data actions reference](reference-data-actions.md)
