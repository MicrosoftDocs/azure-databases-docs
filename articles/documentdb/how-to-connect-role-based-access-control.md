---
title: Connect using role-based access control and Microsoft Entra ID
description: Configure Microsoft Entra ID–based role-based access control (role-based access control) and connect to your Azure DocumentDB cluster using Microsoft Entra ID tokens.
author: seesharprun
ms.author: sidandrews
ms.topic: how-to
ms.date: 02/04/2026
ms.devlang: python
defaultDevLang: python
dev_langs:
  - python
  - typescript
  - csharp
zone_pivot_groups: azure-interface-portal-rest-bicep-terraform
ai-usage: ai-generated
---

# Connect to Azure DocumentDB using role-based access control and Microsoft Entra ID

Azure DocumentDB supports Microsoft Entra ID alongside native DocumentDB authentication. Each cluster is created with native authentication enabled and one built-in administrative user.

Role-based access control provides a centralized mechanism to assign and enforce permissions through Microsoft Entra ID, ensuring that only authorized identities can perform operations on your clusters. This approach simplifies governance, supports least-privilege principles, and makes auditing straightforward—helping organizations maintain operational integrity and compliance as deployments grow. Managing access in Azure DocumentDB involves two distinct levels: 

- **Azure role-based access** for managing the cluster as an Azure resource (such as reading metadata, managing firewall rules, and configuring private endpoints)
- **DocumentDB** access for reading and writing data within databases and collections on the cluster.

Enable Microsoft Entra ID to allow Microsoft Entra principals (users, service principals, or managed identities) to authenticate to the cluster. Microsoft Entra ID authentication is implemented using OpenID Connect (OIDC). Clients present an Entra-issued OIDC access token to the MongoDB driver. A cluster must have native authentication enabled; the supported configurations are native-only or Microsoft Entra ID authentication only or native and Microsoft Entra ID authentication.

> [!NOTE]
> You can enable or change authentication methods on a cluster at any time after provisioning. Changing authentication methods does **not** require a cluster restart and is nondisruptive. When a cluster is created, native DocumentDB authentication must be enabled. You can disable native authentication after the cluster is finished provisioning.

Benefits of using Microsoft Entra ID for authentication include:

- Uniform identity and sign-in across Azure services.
- Centralized management of credentials, password policies, and rotation.
- Support for passwordless and multifactor authentication methods from Microsoft Entra ID.
- Token-based authentication for applications, eliminating stored passwords.

When Microsoft Entra ID authentication is enabled, you can register one or more Microsoft Entra principals as administrative or nonadministrative users on the cluster. Registered principals become Azure resources under `Microsoft.DocumentDB/mongoClusters/users` and are replicated into the database; mapping these principals to MongoDB database roles grants the corresponding database privileges. This form of authentication supports multiple principal types including; human users, service principals (apps), user-assigned and system-assigned managed identities.

> [!NOTE]
> You can configure multiple Microsoft Entra ID identities and types of identities as administrators for a cluster at the same time. Microsoft Entra ID identity types include, but aren't limited to:
>
> - Human identities
> - User-assigned managed identities
> - System-assigned managed identities
> - Workload identities
>
> All identity types can be administrators simultaneously.
>

Administrative users have full privileges to manage the cluster and its data. Nonadministrative users can be added for ongoing production tasks that don't require administrative privileges. Nonadministrative users typically hold restricted roles, such as read-only or read-write access to specific databases, but lack the ability to perform cluster-wide administrative actions.

Review the following considerations before you use this feature:
    
- Authentication methods on the primary cluster and on the replica cluster are [managed independently](cross-region-replication.md).
- Microsoft Entra principals are persistent in the cluster metadata. If a principal is deleted from Microsoft Entra ID, the corresponding cluster user remains but can no longer obtain new tokens. Existing tokens remain valid until they expire (typically up to 90 minutes *from the issuance of the token*).
- To immediately revoke access, remove the principal from the cluster (delete the `users/<principal-id>` resource) and drop any associated database roles; database administrators must handle transfer of ownership or cleanup for deleted principals.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- One or more existing identities in Microsoft Entra ID.

::: zone pivot="rest-api,azure-resource-manager-bicep,azure-terraform"

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-portal"

::: zone-end

::: zone pivot="azure-terraform"

- [Terraform 1.2.0](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli) or later.

::: zone-end

## Manage Azure role-based access control

Azure role-based access control refers to the ability to manage resources for an Azure service without managing data. For example, role-based access for Azure DocumentDB clusters could include the ability to:

- Read all account and resource metadata
- Read and regenerate connection strings
- Manage databases and collections
- Modify account properties

Azure DocumentDB supports Azure role-based access control for `mongoCluster` resource type. The following [actions](/azure/role-based-access-control/role-definitions#actions) for `mongoCluster` resource type are available in Azure role-based access control for individual assignments and [custom role-based access control role creation](/azure/role-based-access-control/custom-roles):

| | Description |
| --- | --- |
| **`Microsoft.DocumentDB/mongoClusters/read`** | Reads a `mongoCluster` resource or list all `mongoCluster` resources. |
| **`Microsoft.DocumentDB/mongoClusters/write`** | Create or Update the properties or tags of the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/delete`** | Deletes the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/PrivateEndpointConnectionsApproval/action`** | Manage a private endpoint connection of `mongoCluster` resource |
| **`Microsoft.DocumentDB/mongoClusters/listConnectionStrings/action`** | List connection strings for a given `mongoCluster` resource |
| **`Microsoft.DocumentDB/mongoClusters/firewallRules/read`** | Reads a firewall rule or lists all firewall rules for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/firewallRules/write`** | Create or Update a firewall rule on a specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/firewallRules/delete`** | Deletes an existing firewall rule for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/read`** | Reads a private endpoint connection proxy for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/write`** | Create or Update a private endpoint connection proxy on a specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/delete`** | Deletes an existing private endpoint connection proxy for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnectionProxies/validate/action`** | Validates private endpoint connection proxy for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/read`** | Reads a private endpoint connection or lists all private endpoint connection for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/write`** | Create or Update a private endpoint connection on a specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateEndpointConnections/delete`** | Deletes an existing private endpoint connection for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/privateLinkResources/read`** | Reads a private link resource or lists all private link resource for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/users/read`** | Reads a user or lists all users for the specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/users/write`** | Create or Update a user on a specified `mongoCluster` resource. |
| **`Microsoft.DocumentDB/mongoClusters/users/delete`** | Deletes an existing user for the specified `mongoCluster` resource. |

::: zone pivot="rest-api"

1. Open a new terminal.

1. Sign in to Azure CLI.

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
      "Name": "Azure DocumentDB RBAC Owner",
      "IsCustom": true,
      "Description": "Can perform all Azure role-based access control actions for Azure DocumentDB clusters.",
      "Actions": [
        "Microsoft.DocumentDb/mongoClusters/*"
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
      "description": "Can perform all Azure role-based access control actions for Azure DocumentDB clusters.",
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1",
      "name": "e4e4e4e4-ffff-aaaa-bbbb-c5c5c5c5c5c5",
      "permissions": [
        {
          "actions": [
            "Microsoft.DocumentDb/*"
          ]
        }
      ],
      "roleName": "Azure DocumentDB RBAC Owner",
      "roleType": "CustomRole"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.Authorization/roleDefinitions/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1`. This example uses fictitious data and your identifier would be distinct from this example. This example is a subset of the typical JSON outputted from the deployment for clarity.

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. Open a new terminal.

1. Sign in to Azure CLI.

1. Create a new Bicep file to define your role definition. Name the file *control-plane-role-definition.bicep*. Add these `actions` to the definition:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDb/mongoClusters/*`** | Enables all possible actions. |

    ```bicep
    metadata description = 'Create RBAC definition for Azure role-based access control access to Azure DocumentDB.'

    @description('Name of the role definition.')
    param roleDefinitionName string = 'Azure DocumentDB RBAC Owner'

    @description('Description of the role definition.')
    param roleDefinitionDescription string = 'Can perform all Azure role-based access control actions for Azure DocumentDB clusters.'

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
              'Microsoft.DocumentDb/mongoClusters/*'
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
    metadata description = 'Assign RBAC role for Azure role-based access control access to Azure DocumentDB.'

    @description('Id of the role definition to assign to the targeted principal in the context of the cluster.')
    param roleDefinitionId string

    @description('Id of the identity/principal to assign this role in the context of the cluster.')
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

::: zone-end

::: zone pivot="azure-portal"

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Enter *Resource group* in the global search bar.

1. Within **Services**, select **Resource groups**.

1. In the **Resource groups** pane, select your existing resource group.

1. Within the pane for the resource group, select **Access control (IAM)** in the service menu.

1. In the **Access control (IAM)** pane, select **Add**. Then select **Add custom role**.

1. Within the **Basics** pane, configure the following options, and then select **Next**:

    | | Value |
    | --- | --- |
    | **Custom role name** | `Azure DocumentDB RBAC Owner` |
    | **Description** | `Can perform all Azure role-based access control actions for Azure DocumentDB clusters.` |
    | **Baseline permissions** | **Start from scratch** |

1. In the **Permissions** pane, select **Add permissions**. Then, search for `DocumentDB` in the permissions dialog. Finally, select the **Microsoft.DocumentDB/mongoClusters** option.

1. In the permissions dialog, select all **Actions** for `Microsoft.DocumentDB/mongoClusters`. Then, select **Add** to return to the **Permissions* pane.

1. Back in the **Permissions** pane, observe the list of permissions. Then, select **Review + create**.

1. In the **Review + create** pane, review the specified options for the new role definition. Finally, select **Create**.

1. Wait for the portal to finish creating the role definition.

1. In the **Access control (IAM)** pane, select **Add** and then **Add role assignment**.

1. In the **Role** pane, search for `Azure DocumentDB` and then select the **Azure DocumentDB RBAC Owner** role created earlier in this guide. Then, select **Next**.

    > [!TIP]
    > You can optionally filter the list of roles to only include custom roles.

1. In the **Members** pane, select the **Select members** option. In the members dialog, select the identity you wish to grant this level of access for your Azure DocumentDB clusters and then use the **Select** option to confirm your choice.

1. Back in the **Members** pane, review the selected member\[s\] and then select **Review + assign**.

1. In the **Review + assign** pane, review the specified options for the new role assignment. Finally, select **Review + assign**.

1. Wait for the portal to finish creating the role assignment.

::: zone-end

::: zone pivot="azure-terraform"

1. Open a new terminal.

1. Sign in to Azure CLI.

1. Check your target Azure subscription.

    ```azurecli-interactive
    az account show
    ```

1. Create a new Terraform file to define your role definition. Name the file *control-plane-role-definition.`tf`*. Add these `actions` to the definition:

    | | Description |
    | --- | --- |
    | **`Microsoft.DocumentDb/mongoClusters/*`** | Enables all possible actions. |

    ```terraform
    variable "role_definition_name" {
      type        = string
      description = "Name of the role definition."
      default     = "Azure DocumentDB RBAC Owner"
    }

    variable "role_definition_description" {
      type        = string
      description = "Description of the role definition."
      default     = "Can perform all Azure role-based access control actions for Azure DocumentDB clusters."
    }

    terraform {
      required_providers {
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }

    provider "azurerm" {
      features {}
    }

    data "azurerm_client_config" "current" {}

    data "azurerm_resource_group" "existing" {
      name = "<name-of-existing-resource-group>"
    }

    resource "azurerm_role_definition" "control_plane" {
      name               = var.role_definition_name
      scope              = data.azurerm_resource_group.existing.id
      description        = var.role_definition_description

      permissions {
        actions = [
          "Microsoft.DocumentDb/mongoClusters/*"
        ]
      }

      assignable_scopes = [
        data.azurerm_resource_group.existing.id
      ]
    }

    output "definition_id" {
      value = azurerm_role_definition.control_plane.id
    }
    ```

1. Initialize the Terraform deployment.

    ```azurecli-interactive
    terraform init --upgrade
    ```

1. Create an execution plan for the role definition and save it to a file named *role-definition.tfplan*.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --out "role-definition.tfplan"
    ```

1. Apply the execution plan to deploy the role definition to Azure.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "role-definition.tfplan"
    ```

1. Review the output from the deployment. The output contains the unique identifier of the role definition in the `definition_id` property. Record this value as it is required to use in the assignment step later in this guide.

1. Create a new Terraform file to define your role assignment. Name the file *control-plane-role-assignment.`tf`*.

    ```terraform
    variable "role_definition_id" {
      type        = string
      description = "Id of the role definition to assign to the targeted principal in the context of the cluster."
    }

    variable "identity_id" {
      type        = string
      description = "Id of the identity/principal to assign this role in the context of the cluster."
    }

    terraform {
      required_providers {
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }

    provider "azurerm" {
      features {}
    }

    data "azurerm_resource_group" "existing" {
      name = "<name-of-existing-resource-group>"
    }

    resource "azurerm_role_assignment" "control_plane" {
      scope              = data.azurerm_resource_group.existing.id
      role_definition_id = var.role_definition_id
      principal_id       = var.identity_id
    }
    ```

1. Create a new Terraform variables file named *control-plane-role-assignment.tfvars*. In this variables file; assign the previously recorded role definition identifiers to the `role_definition_id` variable, and the unique identifier for your identity to the `identity_id` variable.

    ```terraform
    role_definition_id = "<id-of-new-role-definition>"
    identity_id        = "<id-of-existing-identity>"
    ```

1. Initialize and apply this Terraform configuration.

    ```azurecli-interactive
    terraform init --upgrade
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --var-file="control-plane-role-assignment.tfvars" --out "role-assignment.tfplan"
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "role-assignment.tfplan"
    ```

::: zone-end

## Enable Microsoft Entra ID authentication

When you create an Azure DocumentDB cluster, the cluster is configured to solely use native authentication by default. To enable authentication using Microsoft Entra ID, turn on the Microsoft Entra ID authentication method and add Microsoft Entra ID identities to the cluster.

::: zone pivot="rest-api"

1. Get the details for the currently logged-in account using [`az ad signed-in-user`](/cli/azure/ad/signed-in-user#az-ad-signed-in-user-show).

    ```azurecli-interactive
    az ad signed-in-user show
    ```

1. The command outputs a JSON response containing various fields.

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Kai Carter",
      "givenName": "Kai",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<kai@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Carter",
      "userPrincipalName": "<kai@adventure-works.com>"
    }
    ```

    > [!TIP]
    > Record the value of the `id` field. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources. If you're using a managed identity instead, you can obtain the `id` for that managed identity by using the [`az identity show`](/cli/azure/identity#az-identity-show) command.

1. Enable Microsoft Entra ID authentication on the cluster by updating the cluster resource to include `MicrosoftEntraID` in the `authConfig.allowedModes` array:

    ```azurecli-interactive
    az resource patch \
        --resource-group "<resource-group>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties '{"authConfig":{"allowedModes":["MicrosoftEntraID","NativeAuth"]}}' \
        --latest-include-preview
    ```

    > [!NOTE]
    > Replace `<resource-group>` and `<cluster-name>` with your values.

1. Verify the change was applied by reading the `authConfig` property on the cluster using [`az resource show`](/cli/azure/resource#az-resource-show).

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

    > [!NOTE]
    > The output should include the `allowedModes` list. If Microsoft Entra ID was enabled successfully, the array contains both `NativeAuth` and `MicrosoftEntraID`.

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. (Optional) Get the unique identifier for the Microsoft Entra principal you plan to register on the cluster. You can obtain it with the Azure CLI using one of the following commands:

    - **Current signed-in identity**
    
      ```azurecli-interactive
      az ad signed-in-user show      
      ```

    - **Another human identity using friendly name**
    
      ```azurecli-interactive
      az ad user show \
        --id "<user-alias-and-domain>"
      ```

    - **Service principal using app identifier**
    
      ```azurecli-interactive
      az ad sp show \
        --id "<application-id>"
      ```

    - **Managed identity using resource group and name**
    
      ```azurecli-interactive
      az identity show \
        --resource-group "<resource-group>" \
        --name "<managed-identity-name>"      
      ```

1. Create a small Bicep template that updates the cluster `authConfig` to include Microsoft Entra ID (save as `enable-entra-id.bicep`):

    ```bicep
    param clusterName string
    param location string = resourceGroup().location

    resource cluster 'Microsoft.DocumentDB/mongoClusters@2025-09-01' = {
      name: clusterName
      location: location
      properties: {
        authConfig: {
          allowedModes: [
            'MicrosoftEntraID'
            'NativeAuth'
          ]
        }
      }
    }
    ```

1. Deploy the template to update the cluster:

    ```azurecli
    az deployment group create \
        --resource-group "<resource-group>" \
        --template-file enable-entra-id.bicep \
        --parameters clusterName="<cluster-name>"
    ```

1. Verify the `authConfig` property on the cluster by using [`az resource show`](/cli/azure/resource#az-resource-show).

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

    > [!NOTE]
    > The output should include the `allowedModes` list. If Microsoft Entra ID was enabled successfully, the array contains both `NativeAuth` and `MicrosoftEntraID`.

::: zone-end

::: zone pivot="azure-portal"

1. On the **Home** pane of the Azure portal, locate and select the **Microsoft Entra ID** option.

    :::image source="media/how-to-connect-role-based-access-control/home-entra-id-option.png" lightbox="media/how-to-connect-role-based-access-control/home-entra-id-option-full.png" alt-text="Screenshot of the Microsoft Entra ID option in the 'Home' page of the Azure portal.":::

    > [!TIP]
    > If this option isn't listed, select **More services** and then search for **Microsoft Entra ID** using the search term **"Entra"**.

1. Within the **Overview** pane for the Microsoft Entra ID tenant, select **Users** inside the **Manage** section of the service menu.

    :::image source="media/how-to-connect-role-based-access-control/users-option-service-menu.png" alt-text="Screenshot of the 'Users' option in the service menu for the Microsoft Entra ID tenant.":::

1. In the list of users, select the identity (user) that you want to get more details about.

    :::image source="media/how-to-connect-role-based-access-control/users-list.png" alt-text="Screenshot of the list of users for a Microsoft Entra ID tenant with an example user highlighted.":::

    > [!NOTE]
    > This screenshot illustrates an example user named *"Kai Carter"* with a principal of `kai@adventure-works.com`.

1. On the details pane for the specific user, observe the value of the **Object ID** property.

    :::image source="media/how-to-connect-role-based-access-control/user-details.png" alt-text="Screenshot of a user's details pane with the 'Object ID' highlighted.":::

    > [!TIP]
    > Record the value of the **Object ID** property. In this example, that value would be `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`. This value can then be used in various scripts to grant your current account role-based access control permissions to Azure resources. The steps are similar if you're using a managed identity.

1. Navigate to the existing Azure DocumentDB cluster resource.

1. In the cluster menu, under **Settings**, select **Authentication**.

1. In the **Authentication methods** section, select **Native DocumentDB and Microsoft Entra ID** to enable Microsoft Entra ID authentication alongside native authentication.

1. Select **Save** to persist the change.

1. The **Authentication methods** section should now list both **NativeAuth** and **MicrosoftEntraID** as enabled methods.

::: zone-end

::: zone pivot="azure-terraform"

1. (Optional) Get the unique identifier for the Microsoft Entra principal you plan to register on the cluster. You can obtain it with the Azure CLI using one of the following commands:

    - **Current signed-in identity**
    
      ```azurecli-interactive
      az ad signed-in-user show      
      ```

    - **Another human identity using friendly name**
    
      ```azurecli-interactive
      az ad user show \
        --id "<user-alias-and-domain>"
      ```

    - **Service principal using app identifier**
    
      ```azurecli-interactive
      az ad sp show \
        --id "<application-id>"
      ```

    - **Managed identity using resource group and name**
    
      ```azurecli-interactive
      az identity show \
        --resource-group "<resource-group>" \
        --name "<managed-identity-name>"      
      ```

1. Create a Terraform configuration file to enable Microsoft Entra ID authentication on your existing cluster. Save the file as *enable-entra-id.`tf`*:

    ```terraform
    variable "cluster_name" {
      type        = string
      description = "Name of the existing cluster"
    }

    variable "resource_group_name" {
      type        = string
      description = "Name of the existing resource group"
    }

    terraform {
      required_providers {
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }

    provider "azurerm" {
      features {}
    }

    data "azurerm_resource_group" "existing" {
      name = var.resource_group_name
    }

    data "azurerm_mongo_cluster" "existing" {
      name                = var.cluster_name
      resource_group_name = data.azurerm_resource_group.existing.name
    }

    resource "azurerm_mongo_cluster" "enable_entra" {
      name                   = data.azurerm_mongo_cluster.existing.name
      resource_group_name    = data.azurerm_resource_group.existing.name
      location               = data.azurerm_mongo_cluster.existing.location
      administrator_username = data.azurerm_mongo_cluster.existing.administrator_username
      administrator_password = data.azurerm_mongo_cluster.existing.administrator_password
      shard_count            = data.azurerm_mongo_cluster.existing.shard_count
      compute_tier           = data.azurerm_mongo_cluster.existing.compute_tier
      high_availability_mode = data.azurerm_mongo_cluster.existing.high_availability_mode
      storage_size_in_gb     = data.azurerm_mongo_cluster.existing.storage_size_in_gb
      version                = data.azurerm_mongo_cluster.existing.version
      
      # Enable both Microsoft Entra ID and Native authentication
      authentication_enabled = true
    }
    ```

    > [!TIP]
    > For more information on options using the `azurerm_mongo_cluster` resource, see [`azurerm` provider documentation in Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mongo_cluster#arguments-reference).

1. Create a variables file named *enable-entra-id.tfvars* with your cluster details:

    ```terraform
    cluster_name        = "<cluster-name>"
    resource_group_name = "<resource-group>"
    ```

1. Initialize and apply the Terraform configuration to enable Microsoft Entra ID authentication:

    ```azurecli-interactive
    terraform init --upgrade
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --var-file="enable-entra-id.tfvars" --out "enable-entra.tfplan"
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "enable-entra.tfplan"
    ```

1. Verify the `authConfig` property on the cluster by using [`az resource show`](/cli/azure/resource#az-resource-show).

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

    > [!NOTE]
    > The output should include the `allowedModes` list. If Microsoft Entra ID was enabled successfully, the array contains both `NativeAuth` and `MicrosoftEntraID`.

::: zone-end

## Manage DocumentDB administrative Microsoft Entra ID identities and native users

When Microsoft Entra ID authentication is enabled on an Azure DocumentDB cluster, you can add one or more Microsoft Entra ID principals as *administrator users* to that cluster. The Microsoft Entra ID administrator can be a Microsoft Entra ID user, a service principal, or a managed identity. Multiple Microsoft Entra ID administrators can be configured at any time.

Administrative Entra ID users are created as Azure entities under `Microsoft.DocumentDB/mongoClusters/users` and are replicated to the database.

Additionally, one or more nonadministrative Microsoft Entra ID users can be added to a cluster at any time once Microsoft Entra ID authentication is enabled. Nonadministrative users are often used for ongoing production tasks that don't require administrative privileges.

For Azure DocumentDB, this access is granted by registering Microsoft Entra principals on the cluster and mapping them to MongoDB database roles (for example, `readWrite` on a database or `root` on the `admin` database). Registered principals are created as Azure resources of type `Microsoft.DocumentDB/mongoClusters/users` whose names take the form `<cluster-name>/users/<principal-id>`.

Administrative users have full privileges to manage the cluster and its data, including complete user management capabilities. Nonadministrative users can be granted either read-write or read-only permissions on the cluster through specific MongoDB database roles. The **readWriteAnyDatabase** and **clusterAdmin** roles together grant full read-write permissions on the cluster, including privileges for database management and database operations. The **readAnyDatabase** role is used to grant read-only permissions on the cluster. You can't assign **readWriteAnyDatabase** and **clusterAdmin** roles separately - they must be granted together for full read-write access.

Nonadministrative (secondary) users and security principals are granted limited user management permissions on the cluster, as described in the following table:

| Security provider | Role | CreateUser | DeleteUser | UpdateUser | ListUser |
| --- | --- | --- | --- | --- | --- | 
| Microsoft Entra ID | Read-write (readWriteAnyDatabase, clusterAdmin) | :x: | :x: | :x: | :heavy_check_mark: | 
| Microsoft Entra ID | Read-only (readAnyDatabase) | :x: | :x: | :x: | :heavy_check_mark: | 
| Native DocumentDB | Read-write (readWriteAnyDatabase, clusterAdmin) | :x: | :x: | Only to change their own password | :heavy_check_mark: |
| Native DocumentDB | Read-only (readAnyDatabase) | :x: | :x: | Only to change their own password | :heavy_check_mark: |

::: zone pivot="rest-api"

1. Get the unique identifier (object ID) of the Microsoft Entra principal you want to grant access to using one of the following commands:

    - **Current signed-in identity**
    
      ```azurecli-interactive
      az ad signed-in-user show      
      ```

    - **Another human identity using friendly name**
    
      ```azurecli-interactive
      az ad user show \
        --id "<user-alias-and-domain>"
      ```

    - **Service principal using app identifier**
    
      ```azurecli-interactive
      az ad sp show \
        --id "<application-id>"
      ```

    - **Managed identity using resource group and name**
    
      ```azurecli-interactive
      az identity show \
        --resource-group "<resource-group>" \
        --name "<managed-identity-name>"      
      ```

1. Register the principal on the cluster and map it to MongoDB database roles. The following example registers a principal as a `readWrite` user on the `sales` database:

    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --location "<cluster-region>" \
        --properties '{"identityProvider":{"type":"MicrosoftEntraID","properties":{"principalType":"User"}},"roles":[{"db":"sales","role":"readWrite"}]}' \
        --latest-include-preview
    ```

    - Replace `principalType` with `servicePrincipal` for app/service principals or `ManagedIdentity` for managed identities.
    - To grant administrative privileges, use `{"db":"admin","role":"root"}` in the `roles` array.

1. List all registered principals and their mapped roles (cluster-level view):

    ```azurecli-interactive
    az rest \
        --method "GET" \
        --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users?api-version=2025-09-01"
    ```

    - The response contains an array of user resources, each with `identityProvider` metadata and a `roles` array showing mapped database roles.

1. Get details for a specific registered principal (replace `<principal-id>`):

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```

1. Remove a registered principal (revoke data-plane access):

    ```azurecli-interactive
    az resource delete \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. Create a Bicep file (for example `register-principal.bicep`) to register the principal and map database roles:

    ```bicep
    param clusterName string
    param principalId string
    param location string = resourceGroup().location
    param principalType string = 'User'
    param roles array = [
      {
        db: 'sales'
        role: 'readWrite'
      }
    ]

    resource user 'Microsoft.DocumentDB/mongoClusters/users@2025-09-01' = {
      name: '${clusterName}/users/${principalId}'
      location: location
      properties: {
        identityProvider: {
          type: 'Microsoft.EntraID'
          properties: {
            principalType: principalType
          }
        }
        roles: roles
      }
    }
    ```

1. Deploy the Bicep template to register the principal:

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<resource-group>" \
        --template-file register-principal.bicep \
        --parameters clusterName="<cluster-name>" principalId="<principal-id>"
    ```

1. List all registered principals for the cluster using the REST API (useful after Bicep deployment):

    ```azurecli-interactive
    az rest \
        --method GET \
        --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users?api-version=2025-09-01"
    ```

1. Get details for a specific registered principal created by Bicep (replace `<principal-id>`):

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```

1. Remove the principal by deleting the resource (or deploy a template without the user resource):

    ```azurecli-interactive
    az resource delete \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```

::: zone-end

::: zone pivot="azure-portal"

1. Open the target Azure DocumentDB cluster in the Azure portal.

1. Under **Settings**, select **Authentication**.

1. In the **Microsoft Entra ID authentication** section, the portal lists the registered Microsoft Entra principals by object ID. Use this view to:

    - Scan the list for expected object identifiers.
    - Inspect the details for a single principal by selecting a listed entry (or use the portal's search feature).
    - Use the **Remove** action next to an entry to immediately revoke that principal's data-plane access.

1. To get friendly names for object identifiers shown in the portal list, use the **Users** page within the **Microsoft Entra ID** section. Then, search by object ID or friendly name.

::: zone-end

::: zone pivot="azure-terraform"

1. Get the unique identifier (object ID) of the Microsoft Entra principal you want to grant access to using one of the following commands:

    - **Current signed-in identity**
    
      ```azurecli-interactive
      az ad signed-in-user show      
      ```

    - **Another human identity using friendly name**
    
      ```azurecli-interactive
      az ad user show \
        --id "<user-alias-and-domain>"
      ```

    - **Service principal using app identifier**
    
      ```azurecli-interactive
      az ad sp show \
        --id "<application-id>"
      ```

    - **Managed identity using resource group and name**
    
      ```azurecli-interactive
      az identity show \
        --resource-group "<resource-group>" \
        --name "<managed-identity-name>"      
      ```

1. Create a Terraform file (for example `register-principal.tf`) to register the principal and map database roles using the AzAPI provider:

    ```terraform
    variable "cluster_name" {
      type        = string
      description = "Name of the existing cluster"
    }

    variable "resource_group_name" {
      type        = string
      description = "Name of the existing resource group"
    }

    variable "principal_id" {
      type        = string
      description = "Object ID of the Microsoft Entra principal"
    }

    variable "principal_type" {
      type        = string
      description = "Type of principal: User, ServicePrincipal, or ManagedIdentity"
      default     = "User"
    }

    variable "roles" {
      type = list(object({
        db   = string
        role = string
      }))
      description = "Database roles to assign"
      default = [
        {
          db   = "sales"
          role = "readWrite"
        }
      ]
    }

    terraform {
      required_providers {
        azapi = {
          source  = "azure/azapi"
          version = "~> 2.0"
        }
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }

    provider "azurerm" {
      features {}
    }

    provider "azapi" {}

    data "azurerm_resource_group" "existing" {
      name = var.resource_group_name
    }

    data "azurerm_mongo_cluster" "existing" {
      name                = var.cluster_name
      resource_group_name = var.resource_group_name
    }

    resource "azapi_resource" "mongo_cluster_user" {
      type      = "Microsoft.DocumentDB/mongoClusters/users@2025-09-01"
      name      = var.principal_id
      parent_id = data.azurerm_mongo_cluster.existing.id
      location  = data.azurerm_resource_group.existing.location

      body = {
        properties = {
          identityProvider = {
            type = "MicrosoftEntraID"
            properties = {
              principalType = var.principal_type
            }
          }
          roles = var.roles
        }
      }
    }
    ```

    > [!TIP]
    > For more information on the AzAPI provider, see [Azure AzAPI Provider documentation](https://registry.terraform.io/providers/Azure/azapi/latest/docs). 
    > - Replace `principalType` with `servicePrincipal` for app/service principals or `ManagedIdentity` for managed identities.
    > - To grant administrative privileges, use `{"db":"admin","role":"root"}` in the `roles` array.

1. Create a variables file named `register-principal.tfvars`:

    ```terraform
    cluster_name        = "<cluster-name>"
    resource_group_name = "<resource-group>"
    principal_id        = "<principal-id>"
    principal_type      = "User"
    roles = [
      {
        db   = "sales"
        role = "readWrite"
      }
    ]
    ```

1. Initialize and apply the Terraform configuration to register the principal:

    ```azurecli-interactive
    terraform init --upgrade
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --var-file="register-principal.tfvars" --out "register-principal.tfplan"
    ```

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "register-principal.tfplan"
    ```

1. List all registered principals for the cluster using the REST API (useful after Terraform deployment):

    ```azurecli-interactive
    az rest \
        --method GET \
        --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users?api-version=2025-09-01"
    ```

1. Get details for a specific registered principal created by Terraform (replace `<principal-id>`):

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group>" \
        --name "<cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --latest-include-preview
    ```

1. Remove the principal by destroying the Terraform resource:

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform destroy --var-file="register-principal.tfvars"
    ```

::: zone-end

> [!NOTE]
> An Azure DocumentDB cluster is created with one built-in administrative native DocumentDB user. You can [add more native administrative DocumentDB users](secondary-users.md) after cluster provisioning is completed. Microsoft Entra ID administrative users added to the cluster are going to be in addition to native administrative DocumentDB users defined on the same cluster. All administrative Microsoft Entra ID identities are replicated to the database.
>
> Nonadministrative Microsoft Entra ID identities are created in the database. When you list nonadministrative users in the database, the list contains all administrative and nonadministrative Microsoft Entra ID identities and all [secondary (nonadministrative) native DocumentDB users](secondary-users.md).
>

## Get cluster credentials

You can connect to the cluster using either a connection URI or a custom settings object from the driver for your preferred language. In either option, the **scheme** must be set to `mongodb+srv` to connect to the cluster. The **host** is at either the `*.global.mongocluster.cosmos.azure.com` or `*.mongocluster.cosmos.azure.com` domain depending on whether you're using [the current cluster or global read-write endpoint](./how-to-cluster-replica.md#use-connection-strings). The `+srv` scheme and the `*.global.*` host ensures that your client is dynamically connected to the appropriate writable cluster in a multi-cluster configuration even if [a region swap operation occurs](./cross-region-replication.md#replica-cluster-promotion). In a single-cluster configuration, you can use either connection string indiscriminately.

The `tls` setting must also be enabled. The remaining recommended settings are best practice configuration settings.

| Option | Value |
| --- | --- |
| **`scheme`** | `mongodb+srv` |
| **`host`** | `<cluster-name>.global.mongocluster.cosmos.azure.com` or `<cluster-name>.mongocluster.cosmos.azure.com` |
| **`tls`** | `true` |
| **`authMechanism`** | `MONGODB-OIDC` |
| **`retrywrites`** | `false` |
| **`maxIdleTimeMS`** | `120000` |

::: zone pivot="rest-api,azure-resource-manager-bicep,azure-terraform"

> [!IMPORTANT]
> Use the [Azure portal](how-to-connect-role-based-access-control.md?pivots=azure-portal#get-cluster-credentials) to get the connection string.

::: zone-end

::: zone pivot="azure-portal"

1. Navigate to the Azure DocumentDB cluster.

1. Select the **Connection strings** navigation menu option.

1. Copy or record the value from the **Connection string** field.

    > [!TIP]
    > Microsoft Entra ID connection strings are in the **Microsoft Entra ID** section.

::: zone-end

## Connect using Microsoft Entra ID in Visual Studio Code

Use Visual Studio Code with the [DocumentDB extension](https://github.com/microsoft/vscode-documentdb) to connect to your Azure DocumentDB cluster using a Microsoft Entra ID identity.

> [!IMPORTANT]
> When you authenticate to an Azure DocumentDB cluster using Microsoft Entra ID in Visual Studio Code with DocumentDB extension, `shell` functionality isn't supported. If you need to use MongoDB shell with Microsoft Entra ID authentication, use [MongoDB Shell directly on a client machine](#connect-using-microsoft-entra-id-in-mongodb-compass-or-mongodb-shell).

1. Open Visual Studio Code.

1. Navigate the **DocumentDB** extension in the side bar.

1. In the **Connections** section, select **+ New Connection...**.

1. In the connection type dialog, select **Connection String**.

1. Use the following connection string:

     ```
     mongodb+srv://<client-id>@<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000
     ```

1. Wait for the automatic prompt to use Microsoft Entra ID authentication. Enter the appropriate credentials for your identity type.

    > [!NOTE]
    > For example, if you're signing in using your own identity (a human identity), use the passwordless authentication experience.

1. Wait for the connection to finalize. A new DocumentDB entry is then added to the **Connections** section for the cluster.

## Connect using Microsoft Entra ID in MongoDB Compass or MongoDB Shell

Connect to your Azure DocumentDB cluster using a Microsoft Entra ID identity directly with the [MongoDB Compass](https://www.mongodb.com/products/tools/compass) application.

1. Set up an execution environment for connecting to the Azure DocumentDB cluster by creating an Azure compute resource, like an Azure Virtual Machine.

1. Create either a system-assigned managed identity or a [user-assigned managed identity](/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal), and associate it with the virtual machine.

   :::image source="media/how-to-connect-role-based-access-control/assign-managed-identity.png" alt-text="Screenshot to assign managed identity on the Azure portal.":::

1. Register the managed identity in the Azure DocumentDB Cluster.

   :::image source="media/how-to-configure-entra-authentication/open-side-panel-to-add-entra-id-users.png" alt-text="Screenshot to register managed identity on the Azure DocumentDB Cluster.":::

1. Start the [MongoDB Compass](https://www.mongodb.com/products/tools/compass) application or [Mongo shell](https://www.mongodb.com/try/download/shell) in terminal.

1. Within MongoDB Compass, Select **+** in the **Connections** menu to add a new connection. While using the shell, get the **name** of your Azure DocumentDB cluster and the **client ID** for the target identity.

   :::image source="media/how-to-connect-role-based-access-control/review-client-id.png" alt-text="Screenshot to review clientid needed for constructing the Entra connection string from portal on the Azure DocumentDB.":::

1. Enter the following credential into the **URI** input box.

     ```
     mongodb+srv://<client-id>@<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=MONGODB-OIDC&retrywrites=false&maxIdleTimeMS=120000&authMechanismProperties=ENVIRONMENT:azure,TOKEN_RESOURCE:https://ossrdbms-aad.database.windows.net
     ```

1. Open the **Advanced Connection Options** dialog.

1. In the **General** section, select `mongodb+srv` for the **Connection String Scheme**.

1. Navigate to the **Authentication** section and ensure that the **OIDC** option is selected.

1. Navigate to the **OIDC Options** section and then ensure that the **Consider Target Endpoint Trusted** option is also selected.

1. Select **Save & Connect**.

## Manage DocumentDB secondary (nonadministrative) Microsoft Entra ID identities

Sign in to the cluster with an administrative Microsoft Entra ID identity to perform management operations for nonadministrative Microsoft Entra ID identities.

> [!NOTE]
> All management commands for nonadministrative users are supported for `securityPrincipal` and `user` principal types.
>
> Nonadministrative users aren't registered in the Azure portal.
>

1. Sign in to the cluster using an administrative Microsoft Entra ID identity and using a tool like [MongoDB Shell](#connect-using-microsoft-entra-id-in-mongodb-compass-or-mongodb-shell).

1. Add a nonadministrative Microsoft Entra ID identity with **read-write** permissions on the cluster using the `createUser` command:
    
    ```mongo
    db.runCommand(
      {
        createUser: "<entra-id-unique-identifier>",
        roles: [
          { role: "clusterAdmin", db: "admin" },
          { role: "readWriteAnyDatabase", db: "admin" }
        ],
        customData: { "IdentityProvider": { "type": "MicrosoftEntraID", "properties": { "principalType": "user" } } }
      }
    )
    ```

1. Add a nonadministrative Microsoft Entra ID identity with **read-only** permissions on the cluster with `createUser` and a different set of roles.

    ```mongo
    db.runCommand(
      {
        createUser: "<entra-id-unique-identifier>",
        roles: [
          { role: "readAnyDatabase", db: "admin" }
        ],
        customData: { "IdentityProvider": { "type": "MicrosoftEntraID", "properties": { "principalType": "user" } } }
      }
    )
    ```

1. Remove a nonadministrative Microsoft Entra ID identity from the cluster with the `dropUser` command.

    ```mongo
    db.runCommand(
      {
        dropUser: "<entra-id-unique-identifier>"
      }
    )
    ```

1. List all Microsoft Entra ID and native DocumentDB users on the cluster using `userInfo`.

    ```mongo
    db.runCommand(
      {
        usersInfo: 1
      }
    )
    ```

    > [!NOTE]
    > All Microsoft Entra ID and native DocumentDB administrative users are replicated to the database. Because of this replication, the list of users include all administrative and nonadministrative Microsoft Entra ID and native DocumentDB users on the cluster.

## Connect using Microsoft Entra ID in code

Validate that you correctly granted access using application code and the appropriate client library for your preferred language.

```python
class AzureIdentityTokenCallback(OIDCCallback):
    def __init__(self, credential):
        self.credential = credential

    def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
        token = self.credential.get_token(
            "https://ossrdbms-aad.database.windows.net/.default").token
        return OIDCCallbackResult(access_token=token)

clusterName = "<cluster-name>"

credential = DefaultAzureCredential()
authProperties = {"OIDC_CALLBACK": AzureIdentityTokenCallback(credential)}

client = MongoClient(
  f"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/",
  connectTimeoutMS=120000,
  tls=True,
  retryWrites=True,
  authMechanism="MONGODB-OIDC",
  authMechanismProperties=authProperties
)
```

```typescript
const AzureIdentityTokenCallback = async (params: OIDCCallbackParams, credential: TokenCredential): Promise<OIDCResponse> => {
  const tokenResponse: AccessToken | null = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
  return {
      accessToken: tokenResponse?.token || '',
      expiresInSeconds: (tokenResponse?.expiresOnTimestamp || 0) - Math.floor(Date.now() / 1000)
  };
};

const clusterName: string = '<cluster-name>';

const credential: TokenCredential = new DefaultAzureCredential();

const client = new MongoClient(
    `mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
    connectTimeoutMS: 120000,
    tls: true,
    retryWrites: true,
    authMechanism: 'MONGODB-OIDC',
    authMechanismProperties: {
        OIDC_CALLBACK: (params: OIDCCallbackParams) => AzureIdentityTokenCallback(params, credential),
        ALLOWED_HOSTS: ['*.azure.com']
    }
  }
);
```

```csharp
string tenantId = "<microsoft-entra-tenant-id>";
string clusterName = "<cluster-name>";

DefaultAzureCredential credential = new();
AzureIdentityTokenHandler tokenHandler = new(credential, tenantId);

MongoUrl url = MongoUrl.Create($"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/");
MongoClientSettings settings = MongoClientSettings.FromUrl(url);
settings.UseTls = true;
settings.RetryWrites = false;
settings.MaxConnectionIdleTime = TimeSpan.FromMinutes(2);
settings.Credential = MongoCredential.CreateOidcCredential(tokenHandler);
settings.Freeze();

MongoClient client = new(settings);

internal sealed class AzureIdentityTokenHandler(
    TokenCredential credential,
    string tenantId
) : IOidcCallback
{
    private readonly string[] scopes = ["https://ossrdbms-aad.database.windows.net/.default"];

    public OidcAccessToken GetOidcAccessToken(OidcCallbackParameters parameters, CancellationToken cancellationToken)
    {
        AccessToken token = credential.GetToken(
            new TokenRequestContext(scopes, tenantId: tenantId),
            cancellationToken
        );

        return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
    }

    public async Task<OidcAccessToken> GetOidcAccessTokenAsync(OidcCallbackParameters parameters, CancellationToken cancellationToken)
    {
        AccessToken token = await credential.GetTokenAsync(
            new TokenRequestContext(scopes, parentRequestId: null, tenantId: tenantId),
            cancellationToken
        );

        return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
    }
}
```

## Related content

- [Limitations of Microsoft Entra ID in Azure DocumentDB](./limitations.md#authentication-and-access-control-role-based-access-control)
- [Connect to Azure DocumentDB using a console application](how-to-build-dotnet-console-app.md)
