---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/10/2025
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
---

Control plane access refers to the ability to manage resources for an Azure service without managing data. For example, Azure Cosmos DB control plane access could include the ability to:

- Read all account and resource metadata
- Read and regenerate account keys and connection strings
- Perform account backups and restore
- Start and track data transfer jobs
- Manage databases and containers
- Modify account properties

> [!IMPORTANT]
> In Azure Cosmos DB, you need control plane access to manage native data-plane role-based access control definitions and assignments. Since Azure Cosmos DB's data plane role-based access control mechanism is native, you need control plane access to create definitions and assignments and store them as resources within an Azure Cosmos DB account.

First, you must prepare a role definition with a list of `actions` to grant access to manage account resources in Azure Cosmos DB. In this guide, you prepare a built-in and custom role. Then, assign the newly defined role\[s\] to an identity so that your applications can access resources in Azure Cosmos DB.

::: zone pivot="azure-cli"

1. List all of the role definitions associated with your Azure Cosmos DB account using [`az role definition list`](/cli/azure/role/definition#az-role-definition-list). 

    ```azurecli-interactive
    az role definition list \
        --name "Cosmos DB Operator"
    ```

1. Review the output and locate the role definition named **Cosmos DB Operator**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    [
      {
        "assignableScopes": [
          "/"
        ],
        "description": "Lets you manage Azure Cosmos DB accounts, but not access data in them. Prevents access to account keys and connection strings.",
        "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/providers/Microsoft.Authorization/roleDefinitions/230815da-be43-4aae-9cb4-875f7bd000aa",
        "name": "230815da-be43-4aae-9cb4-875f7bd000aa",
        "permissions": [
          {
            "actions": [
              "Microsoft.DocumentDb/databaseAccounts/*",
              "Microsoft.Insights/alertRules/*",
              "Microsoft.Authorization/*/read",
              "Microsoft.ResourceHealth/availabilityStatuses/read",
              "Microsoft.Resources/deployments/*",
              "Microsoft.Resources/subscriptions/resourceGroups/read",
              "Microsoft.Support/*",
              "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/action"
            ],
            "condition": null,
            "conditionVersion": null,
            "dataActions": [],
            "notActions": [
              "Microsoft.DocumentDB/databaseAccounts/dataTransferJobs/*",
              "Microsoft.DocumentDB/databaseAccounts/readonlyKeys/*",
              "Microsoft.DocumentDB/databaseAccounts/regenerateKey/*",
              "Microsoft.DocumentDB/databaseAccounts/listKeys/*",
              "Microsoft.DocumentDB/databaseAccounts/listConnectionStrings/*",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/delete",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/write",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/delete",
              "Microsoft.DocumentDB/databaseAccounts/mongodbRoleDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/mongodbRoleDefinitions/delete",
              "Microsoft.DocumentDB/databaseAccounts/mongodbUserDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/mongodbUserDefinitions/delete"
            ],
            "notDataActions": []
          }
        ],
        "roleName": "Cosmos DB Operator",
        "roleType": "BuiltInRole",
        "type": "Microsoft.Authorization/roleDefinitions",
      }
    ]
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/providers/Microsoft.Authorization/roleDefinitions/230815da-be43-4aae-9cb4-875f7bd000aa`. This example uses fictitious data and your identifier would be distinct from this example. However, the identifier (`230815da-be43-4aae-9cb4-875f7bd000aa`) is globally unique across all role definitions in Azure.

1. Use [`az group show`](/cli/azure/group#az-group-show) to get the metadata for your current resource group.

    ```azurecli-interactive
    az group show \
        --name "<name-of-existing-resource-group>"
    ```

1. Observe the output of the previous command. Record the value of the `id` property for this resource group as it is required to use in the next step.

    ```json
    {
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example",
      "location": "westus",
      "name": "msdocs-identity-example",
      "type": "Microsoft.Resources/resourceGroups"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example`. This example uses fictitious data and your identifier would be distinct from this example. This string is a truncated example of the output.

1. Create a new JSON file named *role-definition.json*. In the file, create this resource definition specifying the values listed here. For the `AssignableScopes` list, add the `id` property of the resource group recorded in the previous step.

    ```json
    {
      "Name": "Azure Cosmos DB Control Plane Owner",
      "IsCustom": true,
      "Description": "Can perform all control plane actions for an Azure Cosmos DB account.",
      "Actions": [
        "Microsoft.DocumentDb/*"
      ],
      "AssignableScopes": [
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example"
      ]
    }
    ```

    > [!NOTE]
    > This example uses the `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example` value recorded from the previous step. Your actual resource identifier could be different.

1. Create a new role definition using [`az role definition create`](/cli/azure/role/definition#az-role-definition-create). Use the *role-definition.json* file as the input for the `--role-definition` argument.

    ```azurecli-interactive
    az role definition create \
        --role-definition role-definition.json
    ```

1. Review the output from the definition creation command. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    {
      "assignableScopes": [
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example"
      ],
      "description": "Can perform all control plane actions for an Azure Cosmos DB account.",
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1",
      "name": "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
      "permissions": [
        {
          "actions": [
            "Microsoft.DocumentDb/*"
          ]
        }
      ],
      "roleName": "Azure Cosmos DB Control Plane Owner",
      "roleType": "CustomRole"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`. This example uses fictitious data and your identifier would be distinct from this example. This example is a subset of the typical JSON outputted from the deployment for clarity.

1. Use `az group show` to get the metadata for your current resource group again.

    ```azurecli-interactive
    az group show \
        --name "<name-of-existing-resource-group>"
    ```

1. Observe the output of the previous command. Record the value of the `id` property for this resource group as it is required to use in the next step.

    ```json
    {
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example",
      "location": "westus",
      "name": "msdocs-identity-example",
      "type": "Microsoft.Resources/resourceGroups"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example`. This example uses fictitious data and your identifier would be distinct from this example. This string is a truncated example of the output.

1. Assign the new role using [`az role assignment create`](/cli/azure/role/assignment#az-role-assignment-create). Use your resource group's identifier for the `--scope` argument, the role's identifier for the `-role` argument, and the unique identifier for your identity to the `--assignee` argument.

    ```azurecli-interactive
    az role assignment create \
        --assignee "<your-principal-identifier>" \
        --role "subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1" \
        --scope "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example"
    ```

    > [!NOTE]
    > In this example command, the `scope` was set to the fictitious example `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example` from the previous step's example. Your resource group's identifier would be distinct from this example. The `role` was also set to the fictitious `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`. Again, your role identifier would be distinct.

1. Observe the output from the command. The output includes a unique identifier for the assignment in the `id` property.

    ```json
    {
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleAssignments/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1",
      "name": "ffffffff-5555-6666-7777-aaaaaaaaaaaa",
      "principalId": "aaaaaaaa-bbbb-cccc-1111-222222222222",
      "resourceGroup": "msdocs-identity-example",
      "roleDefinitionId": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1",
      "scope": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example",
      "type": "Microsoft.Authorization/roleAssignments"
    }
    ```

    > [!NOTE]
    > In this example, the `id` property is `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleAssignments/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`, which is another fictitious example.

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access to the data using a managed identity.

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. List all of the role definitions associated with your Azure Cosmos DB account using [`az role definition list`](/cli/azure/role/definition#az-role-definition-list). 

    ```azurecli-interactive
    az role definition list \
        --name "Cosmos DB Operator"
    ```

1. Review the output and locate the role definition named **Cosmos DB Operator**. The output contains the unique identifier of the role definition in the `id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    [
      {
        "assignableScopes": [
          "/"
        ],
        "description": "Lets you manage Azure Cosmos DB accounts, but not access data in them. Prevents access to account keys and connection strings.",
        "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/providers/Microsoft.Authorization/roleDefinitions/230815da-be43-4aae-9cb4-875f7bd000aa",
        "name": "230815da-be43-4aae-9cb4-875f7bd000aa",
        "permissions": [
          {
            "actions": [
              "Microsoft.DocumentDb/databaseAccounts/*",
              "Microsoft.Insights/alertRules/*",
              "Microsoft.Authorization/*/read",
              "Microsoft.ResourceHealth/availabilityStatuses/read",
              "Microsoft.Resources/deployments/*",
              "Microsoft.Resources/subscriptions/resourceGroups/read",
              "Microsoft.Support/*",
              "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/action"
            ],
            "condition": null,
            "conditionVersion": null,
            "dataActions": [],
            "notActions": [
              "Microsoft.DocumentDB/databaseAccounts/dataTransferJobs/*",
              "Microsoft.DocumentDB/databaseAccounts/readonlyKeys/*",
              "Microsoft.DocumentDB/databaseAccounts/regenerateKey/*",
              "Microsoft.DocumentDB/databaseAccounts/listKeys/*",
              "Microsoft.DocumentDB/databaseAccounts/listConnectionStrings/*",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions/delete",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/write",
              "Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments/delete",
              "Microsoft.DocumentDB/databaseAccounts/mongodbRoleDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/mongodbRoleDefinitions/delete",
              "Microsoft.DocumentDB/databaseAccounts/mongodbUserDefinitions/write",
              "Microsoft.DocumentDB/databaseAccounts/mongodbUserDefinitions/delete"
            ],
            "notDataActions": []
          }
        ],
        "roleName": "Cosmos DB Operator",
        "roleType": "BuiltInRole",
        "type": "Microsoft.Authorization/roleDefinitions",
      }
    ]
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/providers/Microsoft.Authorization/roleDefinitions/230815da-be43-4aae-9cb4-875f7bd000aa`. This example uses fictitious data and your identifier would be distinct from this example. However, the identifier (`230815da-be43-4aae-9cb4-875f7bd000aa`) is globally unique across all role definitions in Azure.

1. Create a new Bicep file to define your role definition. Name the file *control-plane-role-definition.bicep*. Add these `actions` to the definition:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDb/*`** | Enables all possible actions. |

    ```bicep
    metadata description = 'Create RBAC definition for control plane access to Azure Cosmos DB.'
    
    @description('Name of the role definition.')
    param roleDefinitionName string = 'Azure Cosmos DB Control Plane Owner'
    
    @description('Description of the role definition.')
    param roleDefinitionDescription string = 'Can perform all control plane actions for an Azure Cosmos DB account.'
    
    resource definition 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
      name: guid(subscription().id, resourceGroup().id, roleDefinitionName)
      scope: resourceGroup()
      properties: {
        roleName: roleDefinitionName
        description: roleDefinitionDescription
        type: 'CustomRole'
        permissions: [
          {
            actions: [
              'Microsoft.DocumentDb/*'
            ]
          }
        ]
        assignableScopes: [
          resourceGroup().id
        ]
      }
    }
    
    output definitionId string = definition.id
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create). Specify the name of the Bicep template and Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --template-file control-plane-role-definition.bicep
    ```

1. Review the output from the deployment. The output contains the unique identifier of the role definition in the `properties.outputs.definitionId.value` property. Record this value as it is required to use in the assignment step later in this guide.

    ```json
    {
      "properties": {
        "outputs": {
          "definitionId": {
            "type": "String",
            "value": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1"
          }
        }
      }
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`. This example uses fictitious data and your identifier would be distinct from this example. This example is a subset of the typical JSON outputted from the deployment for clarity.

1. Create a new Bicep file to define your role assignment. Name the file *control-plane-role-assignment.bicep*.

    ```bicep
    metadata description = 'Assign RBAC role for control plane access to Azure Cosmos DB.'
    
    @description('Id of the role definition to assign to the targeted principal in the context of the account.')
    param roleDefinitionId string
    
    @description('Id of the identity/principal to assign this role in the context of the account.')
    param identityId string
    
    resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
      name: guid(subscription().id, resourceGroup().id, roleDefinitionId, identityId)
      scope: resourceGroup()
      properties: {
        roleDefinitionId: roleDefinitionId
        principalId: identityId
      }
    }
    ```

1. Create a new Bicep parameters file named *control-plane-role-assignment.`bicepparam`*. In this parameters file; assign the previously recorded role definition identifiers to the `roleDefinitionId` parameter, and the unique identifier for your identity to the `identityId` parameter.

    ```bicep
    using './control-plane-role-assignment.bicep'
    
    param roleDefinitionId = '<id-of-new-role-definition>'
    param identityId = '<id-of-existing-identity>'
    ```

1. Deploy this Bicep template using `az deployment group create`.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters control-plane-role-assignment.bicepparam \
        --template-file control-plane-role-assignment.bicep
    ```

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access to the data using a managed identity.

::: zone-end

::: zone pivot="azure-portal"

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Enter *Resource group* in the global search bar.

    :::image source="media/grant-control-plane-role-based-access/global-search.png" lightbox="media/grant-control-plane-role-based-access/global-search-full.png" alt-text="Screenshot of the global search bar in the Azure portal.":::

1. Within **Services**, select **Resource groups**.

    :::image source="media/grant-control-plane-role-based-access/search-results.png" alt-text="Screenshot of the 'Resource groups' option selected in the search menu.":::

1. In the **Resource groups** pane, select your existing resource group.

    :::image source="media/grant-control-plane-role-based-access/resource-group.png" alt-text="Screenshot of an existing resource group in the list of resource groups for the subscription.":::

    > [!NOTE]
    > This example screenshot includes the `msdocs-identity-example` resource group. Your actual resource group name could be different.

1. Within the pane for the resource group, select **Access control (IAM)** in the service menu.

    :::image source="media/grant-control-plane-role-based-access/access-control-service-menu.png" alt-text="Screenshot of the 'Access Control (IAM)' option in the service menu for a resource group.":::

1. In the **Access control (IAM)** pane, select **Roles**.

    :::image source="media/grant-control-plane-role-based-access/access-control-roles-option.png" alt-text="Screenshot of the 'Roles' option in the 'Access Control (IAM)' pane.":::

1. In the **Roles** section, use the search phrase **Cosmos DB** and locate the **Cosmos DB Operator** role definition. Then, select the **View** option associated with that definition.

    :::image source="media/grant-control-plane-role-based-access/role-definitions-list.png" alt-text="Screenshot of a list of role definitions at the current assignable scope filtered to include only definitions with 'Cosmos DB' in the title.":::

1. In the **Cosmos DB Operator** role definition dialog, observe the actions assigned as part of this role definition.

    :::image source="media/grant-control-plane-role-based-access/role-definition-dialog.png" alt-text="Screenshot of the 'Cosmos DB Operator' dialog with details about the built-in role definition.":::

1. Close the **Cosmos DB Operator** role definition dialog.

1. Back in the **Access control (IAM)** pane, select **Add**. Then select **Add custom role**.

    :::image source="media/grant-control-plane-role-based-access/add-custom-role.png" alt-text="Screenshot of the 'Add custom role' option in the 'Access Control (IAM)' menu for the 'Add' option.":::

1. Within the **Basics** pane, configure the following options, and then select **Next**:

    | | Value |
    | --- | --- |
    | **Custom role name** | `Azure Cosmos DB Control Plane Owner` |
    | **Description** | `Can perform all control plane actions for an Azure Cosmos DB account.` |
    | **Baseline permissions** | **Start from scratch** |

    :::image source="media/grant-control-plane-role-based-access/role-basics-pane.png" alt-text="Screenshot of the 'Basics' pane for adding a custom role.":::

1. In the **Permissions** pane, select **Add permissions**. Then, search for `DocumentDB` in the permissions dialog. Finally, select the **Microsoft.DocumentDB** option.

    :::image source="media/grant-control-plane-role-based-access/role-permissions-pane.png" alt-text="Screenshot of the 'Permissions' pane for adding a custom role.":::

    :::image source="media/grant-control-plane-role-based-access/role-add-permissions-dialog.png" alt-text="Screenshot of the 'Add permissions' dialog filtered to permissions related to 'DocumentDB' for adding a custom role.":::

1. In the permissions dialog, select all **Actions** for `Microsoft.DocumentDB`. Then, select **Add** to return to the **Permissions* pane.

    :::image source="media/grant-control-plane-role-based-access/role-add-permissions-dialog-selections.png" alt-text="Screenshot of all permissions selected for 'DocumentDB' in a dialog for a custom role.":::

1. Back in the **Permissions** pane, observe the list of permissions. Then, select **Review + create**.

    :::image source="media/grant-control-plane-role-based-access/role-permissions-pane-filled.png" alt-text="Screenshot of the 'Permissions' pane with multiple permissions added to the list for a custom role.":::

1. In the **Review + create** pane, review the specified options for the new role definition. Finally, select **Create**.

    :::image source="media/grant-control-plane-role-based-access/role-review-create-pane.png" alt-text="Screenshot of the 'Review + create' pane for adding a custom role.":::

1. Wait for the portal to finish creating the role definition.

1. In the **Access control (IAM)** pane, select **Add** and then **Add role assignment**.

    :::image source="media/grant-control-plane-role-based-access/add-role-assignment.png" alt-text="Screenshot of the 'Add role assignment' option in the 'Access Control (IAM)' menu for the 'Add' option.":::

1. In the **Role** pane, search for `Azure Cosmos DB` and then select the **Azure Cosmos DB Control Plane Owner** role created earlier in this guide. Then, select **Next**.

    :::image source="media/grant-control-plane-role-based-access/assignment-role-pane.png" alt-text="Screenshot of the 'Role' pane for adding a role assignment.":::

    > [!TIP]
    > You can optionally filter the list of roles to only include custom roles.

1. In the **Members** pane, select the **Select members** option. In the members dialog, select the identity you wish to grant this level of access for your Azure Cosmos DB account and then use the **Select** option to confirm your choice.

    :::image source="media/grant-control-plane-role-based-access/assignment-members-pane.png" alt-text="Screenshot of the 'Members' pane for adding a role assignment.":::

    :::image source="media/grant-control-plane-role-based-access/assignment-select-members-dialog.png" alt-text="Screenshot of the identity selection dialog for adding a role assignment.":::

    > [!NOTE]
    > This screenshot illustrates an example user named *"Kai Carter"* with a principal of `kai@adventure-works.com`.

1. Back in the **Members** pane, review the selected member\[s\] and then select **Review + assign**.

    :::image source="media/grant-control-plane-role-based-access/assignment-select-members-dialog-selections.png" alt-text="Screenshot of the 'Members' pane with a selected identity for a role assignment.":::

1. In the **Review + assign** pane, review the specified options for the new role assignment. Finally, select **Review + assign**.

    :::image source="media/grant-control-plane-role-based-access/assignment-review-assign-pane.png" alt-text="Screenshot of the 'Review + create' pane for a role assignment.":::

1. Wait for the portal to finish creating the role assignment.

::: zone-end

::: zone pivot="azure-powershell"

1. Use [`Get-AzRoleDefinition`](/powershell/module/az.resources/get-azroledefinition) to list all of the role definitions associated with your Azure Cosmos DB account.

    ```azurepowershell-interactive
    $parameters = @{
        Name = "Cosmos DB Operator"
    }
    Get-AzRoleDefinition @parameters
    ```

1. Review the output and locate the role definition named **Cosmos DB Built-in Data Contributor**. The output contains the unique identifier of the role definition in the `Id` property. Record this value as it is required to use in the assignment step later in this guide.

    ```output
    Name             : Cosmos DB Operator
    Id               : 230815da-be43-4aae-9cb4-875f7bd000aa
    IsCustom         : False
    Description      : Lets you manage Azure Cosmos DB accounts, but not access data in them. Prevents access to account keys and connection strings.
    Actions          : {Microsoft.DocumentDb/databaseAccounts/*, Microsoft.Insights/alertRules/*, Microsoft.Authorization/*/read, Microsoft.ResourceHealth/availabilityStatuses/read…}
    NotActions       : {Microsoft.DocumentDB/databaseAccounts/dataTransferJobs/*, Microsoft.DocumentDB/databaseAccounts/readonlyKeys/*, Microsoft.DocumentDB/databaseAccounts/regenerateKey/*, Microsoft.DocumentDB/databaseAccounts/listKeys/*…}
    DataActions      : {}
    NotDataActions   : {}
    AssignableScopes : {/}
    ```

    > [!NOTE]
    > In this example, the `Id` value would be `230815da-be43-4aae-9cb4-875f7bd000aa`. The identifier is globally unique across all role definitions in Azure.

1. Use [`Get-AzResourceGroup`](/powershell/module/az.resources/get-azresourcegroup) to get the metadata for your current resource group.

    ```azurepowershell-interactive
    $parameters = @{
        Name = "<name-of-existing-resource-group>"
    }
    Get-AzResourceGroup @parameters
    ```

1. Observe the output of the previous command. Record the value of the `ResourceId` property for this resource group as it is required to use in the next step.

    ```output
    ResourceGroupName : msdocs-identity-example
    Location          : westus
    ProvisioningState : Succeeded
    ResourceId        : /subscriptions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1/resourcegroups/msdocs-identity-example
    ```

    > [!NOTE]
    > In this example, the `ResourceId` value would be `/subscriptions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1/resourcegroups/msdocs-identity-example`. This example uses fictitious data and your identifier would be distinct from this example. This string is a truncated example of the typical output.

1. First, import the [`Az.Resources`](/powershell/module/az.resources) module. Then, Create a new [`Microsoft.Azure.Commands.Resources.Models.Authorization.PSRoleDefinition`](/dotnet/api/microsoft.azure.commands.resources.models.authorization.psroledefinition) object. In the object, create this resource definition specifying the values listed here. For the `AssignableScopes` list, add the `ResourceId` property of the resource group recorded in the previous step. Finally, use the role definition object as the input for the `-Role` parameter of [`New-AzRoleDefinition`](/powershell/module/az.resources/new-azroledefinition).

    ```azurepowershell-interactive
    Import-Module Az.Resources

    $parameters = @{
        TypeName = "Microsoft.Azure.Commands.Resources.Models.Authorization.PSRoleDefinition"
        Property = @{
            Name = "Azure Cosmos DB Control Plane Owner"
            Description = "Can perform all control plane actions for an Azure Cosmos DB account."
            IsCustom = $true
            Actions = @(
                "Microsoft.DocumentDb/*"
            )
            AssignableScopes = @(
                "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example"
            )
        }
    }
    $role = New-Object @parameters
    
    New-AzRoleDefinition -Role $role
    ```

    > [!NOTE]
    > This example uses the `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example` value recorded from the previous step. Your actual resource identifier could be different.

1. Review the output from the definition creation command. The output contains the unique identifier of the role definition in the `Name` property. Record this value as it is required to use in the assignment step later in this guide.

    ```output
    Name             : Azure Cosmos DB Control Plane Owner
    Id               : e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5
    IsCustom         : True
    Description      : Can perform all control plane actions for an Azure Cosmos DB account.
    Actions          : {Microsoft.DocumentDb/*}
    AssignableScopes : {/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example}
    ```

    > [!NOTE]
    > In this example, the `Name` value would be `Azure Cosmos DB Control Plane Owner`. This example is a subset of the typical output of the deployment for clarity.

1. Assign the new role using [`New-AzRoleAssignment`](/powershell/module/az.resources/new-azroleassignment). Use the role's name for the `RoleDefinitionName` parameter and the unique identifier for your identity to the `ObjectId` parameter.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        ObjectId = "<your-principal-identifier>"
        RoleDefinitionName = "Azure Cosmos DB Control Plane Owner"
    }
    New-AzRoleAssignment @parameters
    ```

1. Observe the output from the command. The output includes a unique identifier for the assignment in the `RoleAssignmentId` property.

    ```output
    RoleAssignmentName : ffffffff-5555-6666-7777-aaaaaaaaaaaa
    RoleAssignmentId   : /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleAssignments/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1
    Scope              : /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example
    DisplayName        : Kai Carter
    SignInName         : <kai@adventure-works.com>
    RoleDefinitionName : Azure Cosmos DB Control Plane Owner
    RoleDefinitionId   : e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5
    ```

    > [!NOTE]
    > In this example, the `RoleAssignmentId` property is `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleAssignments/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`, which is another fictitious example. This example is a subset of the typical output of the deployment for clarity.

1. Repeat these steps to grant access to the account from any other identities you would like to use.

    > [!TIP]
    > You can repeat these steps for as many identities as you'd like. Typically, these steps are at least repeated to allow developers access to an account using their human identity and to allow applications access to the data using a managed identity.

::: zone-end

> [!IMPORTANT]
> Assigning a role definition requires you to already have the unique identifier of any identity you want to grant role-based access control permissions.
