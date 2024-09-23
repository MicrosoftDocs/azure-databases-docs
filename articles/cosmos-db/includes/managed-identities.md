---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 09/17/2024
ms.custom: subject-msia
zone_pivot_groups: azure-interface-portal-cli-powershell-bicep
---

Managed identities are one of many types of identity resources in Microsoft Entra ID for applications to use when connecting to services that support Microsoft Entra authentication. Managed identities can be used in lieu of traditional resource-owned credentials like keys. In Azure, managed identities provide a way for your applications to obtain a Microsoft Entra token to authenticate to Azure services without you needing to write a large amount of authentication code.

You can use Microsoft Entra to authenticate to Azure services including, but not limited to:

- Azure SQL
- Azure AI
- Azure Cosmos DB
- Azure Storage
- Azure Event Hubs
- Azure Container Registry

You can use managed identities to represent the principal that authenticates to an Azure service from other Azure services including, but not limited to:

- Azure Kubernetes Service
- Azure Container Apps
- Azure Virtual Machines
- Azure Functions
- Azure App Service
- Azure Spring Apps
- Azure Service Fabric

Managed identities enable multiple secure scenarios where various Azure services can connect to each other. Some examples include:

- Creating a system-assigned managed identity for an application in Azure Spring Apps to connect to and query an Azure SQL account
- Using a single user-assigned managed identity with both Azure Kubernetes Service and Azure Functions to issue requests to an Azure AI account
- Using a managed identity for an Azure Cosmos DB account to store keys in Azure Key Vault

For more information, see [managed identities for Azure resources](/entra/identity/managed-identities-azure-resources/overview).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

::: zone pivot="azure-interface-cli,azure-interface-bicep"

[!INCLUDE [Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-interface-portal"

::: zone-end

::: zone pivot="azure-interface-powershell"

[!INCLUDE [Azure PowerShell prerequisites](~/reusable-content/azure-powershell/azure-powershell-requirements-no-header.md)]

::: zone-end

## Create an Azure service with a system-assigned managed identity

Create a new Azure service with a system-assigned managed identity. This section creates an [Azure Container Instances](/azure/container-instances) resource.

::: zone pivot="azure-interface-cli"

1. Use [`az container create`](/cli/azure/container#az-container-create) to create a new container instance. Configure the account to use a system-assigned managed identity by using the `assign-identity` parameter.

    ```azurecli-interactive
    az container create \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-new-container>" \
        --image mcr.microsoft.com/dotnet/samples:aspnetapp-chiseled \
        --cpu 1 \
        --memory 2 \
        --assign-identity
    ```

1. Get the details for the system-assigned managed identity using [`az container show`](/cli/azure/container#az-container-show) and a JMESPath query.

    ```azurecli-interactive
    az container show \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-container>" \
        --query "identity"
    ```

1. Review the output from the command. It should include the unique identifiers for the identity and tenant.

    ```json
    {
      "principalId": "bbbbbbbb-1111-2222-3333-cccccccccccc",
      "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
      "type": "SystemAssigned",
      "userAssignedIdentities": null
    }
    ```

::: zone-end

::: zone pivot="azure-interface-bicep"

1. Create a new Bicep file to define a new container instance. Name the file *container-instance.bicep*. Set these properties for the container instance:

    | | Value |
    | --- | --- |
    | **`name`** | Use a parameter named `instanceName` |
    | **`location`** | Set to resource group's location |
    | **`identity.type`** | `SystemAssigned` |
    | **`properties.osType`** | `Linux` |
    | **`properties.containers[0].name`** | `aspnet-sample` |
    | **`properties.containers[0].properties.image`** | `mcr.microsoft.com/dotnet/samples:aspnetapp-chiseled` |
    | **`properties.containers[0].properties.resources.requests.cpu`** | `1` |
    | **`properties.containers[0].properties.resources.requests.memoryInGB`** | `2` |

    ```bicep
    metadata description = 'Create Azure Container Instance resource with system-assigned managed identity.'
    
    @description('Name of the Azure Container Instances resource.')
    param instanceName string
    
    resource instance 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
      name: instanceName
      location: resourceGroup().location
      identity: {
        type: 'SystemAssigned'
      }
      properties: {
        osType: 'Linux'
        containers: [
          {
            name: 'aspnet-sample'
            properties: {
              image: 'mcr.microsoft.com/dotnet/samples:aspnetapp-chiseled'
              resources: {
                requests: {
                  cpu: 1
                  memoryInGB: 2
                }
              }
            }
          }
        ]
      }
    }
    
    output systemAssignedIdentity object = instance.identity    
    ```

1. Create a new Bicep parameters file named *container-instance.bicepparam*. In this parameters file, create a unique name for your container instance using the `instanceName` parameter.

    ```bicep
    using './container-instance.bicep'
    
    param instanceName = '<name-of-new-container-instance>'
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create). Specify the name of the Bicep template, parameters file, and Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters "container-instance.bicepparam" \
        --template-file "container-instance.bicep"
    ```

1. Review the output from the deployment. The output contains the identity object from the container instance in the `properties.outputs.systemAssignedIdentity.value` property.

    ```json
    {
      "principalId": "bbbbbbbb-1111-2222-3333-cccccccccccc",
      "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
      "type": "SystemAssigned"
    }
    ```

::: zone-end

::: zone pivot="azure-interface-portal"

1. TODO

1. TODO

1. TODO

    :::image source="media/managed-identities/<todo>.png" lightbox="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

::: zone-end

::: zone pivot="azure-interface-powershell"

1. Create an object representing a container using [`New-AzContainerInstanceObject`](/powershell/module/az.containerinstance/new-azcontainerinstanceobject) and store it in a variable named `$container`. Then, use that container object to create a new container instance with [`New-AzContainerGroup`](/powershell/module/az.containerinstance/new-azcontainergroup). Configure the account to use a system-assigned managed identity by setting the `IdentityType` parameter to `SystemAssigned`.

    ```azurepowershell-interactive
    $parameters = @{
        Name = "aspnet-sample"
        Image = "mcr.microsoft.com/dotnet/samples:aspnetapp-chiseled"
        RequestCpu = 1 
        RequestMemoryInGb = 2
    }
    $container = New-AzContainerInstanceObject @parameters
    
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-new-container>"
        Container = $container
        OsType = "Linux"
        Location = "<azure-region>"
        IdentityType = "SystemAssigned"
    }
    New-AzContainerGroup @parameters
    ```

1. Get the details for the system-assigned managed identity using [`Get-AzContainerGroup`](/powershell/module/az.containerinstance/get-azcontainergroup) and `Format-List` selecting only the `Identity` property.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-container>"
    }
    Get-AzContainerGroup @parameters | Format-List Identity
    ```

1. Review the output from the command. It should include the unique identifiers for the identity and tenant.

    ```output
    Identity : {
                 "principalId": "bbbbbbbb-1111-2222-3333-cccccccccccc",
                 "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
                 "type": "SystemAssigned"
               }
    ```

::: zone-end

## Create a user-assigned managed identity

Create a user-assigned managed identity that can be used with one or more Azure services in a portable manner.

::: zone pivot="azure-interface-cli"

1. Use [`az identity create`](/cli/azure/identity#az-identity-create) to create a new user-assigned managed identity in your Azure resource group.

    ```azurecli-interactive
    az identity create \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-new-managed-identity>"
    ```

1. Get the list of user-assigned managed identities in your resource group using [`az identity list`](/cli/azure/identity#az-identity-list)

    ```azurecli-interactive
    az identity list \
        --resource-group "<name-of-existing-resource-group>"    
    ```

1. Review the output from the command. Record the value of the `id` field as this fully qualified resource identifier is used to assign the user-assigned managed identity to your Azure resource.

    ```json
    {
      "clientId": "11112222-bbbb-3333-cccc-4444dddd5555",
      "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned",
      "location": "<azure-location>",
      "name": "msdocs-identity-example-user-assigned",
      "principalId": "cccccccc-dddd-eeee-3333-444444444444",
      "resourceGroup": "msdocs-identity-example",
      "systemData": null,
      "tags": {},
      "tenantId": "aaaabbbb-0000-cccc-1111-dddd2222eeee",
      "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
    }
    ```

    > [!NOTE]
    > In this example, the `id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned`. This example uses fictituous data and your identifier would be distinct from this example.

::: zone-end

::: zone pivot="azure-interface-bicep"

1. Create a Bicep file to define a user-assigned managed identity and name the file *user-assigned-managed-identity.bicep*. Set these minimal properties:

    | | Value |
    | --- | --- |
    | **`name`** | Use an optional parameter named `identityName` and generate a unique default value |
    | **`location`** | Set to resource group's location |

    ```bicep
    metadata description = 'Create a user-assigned managed identity.'
    
    param identityName string = uniqueString(subscription().id, resourceGroup().id)
    
    resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
      name: identityName
      location: resourceGroup().location
    }
    
    output id string = identity.id
    output name string = identity.name
    ```

1. Deploy the Bicep template using `az deployment group create`. Specify the name of the Bicep template and Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --template-file "user-assigned-managed-identity.bicep"
    ```

1. Review the output from the deployment. The output contains the unique identifier of the managed identity in the `properties.outputs.name.value` property. Record this value as it is required to use when creating a new Azure resource later in this guide.

    ```json
    {
      "type": "String",
      "value": "msdocs-identity-example-user-assigned"
    }
    ```

    > [!NOTE]
    > In this example, the `name.value` would be `msdocs-identity-example-user-assigned`. This example uses fictituous data and your identifier would be distinct from this example.

::: zone-end

::: zone pivot="azure-interface-portal"

1. TODO

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

::: zone-end

::: zone pivot="azure-interface-powershell"

1. Create a new user-assigned managed identity using [`New-AzUserAssignedIdentity`](/powershell/module/az.managedserviceidentity/new-azuserassignedidentity) in your Azure resource group.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-new-managed-identity>"
        Location = "<azure-region>"
    }
    New-AzUserAssignedIdentity @parameters
    ```

1. Use [`Get-AzUserAssignedIdentity`](/powershell/module/az.managedserviceidentity/get-azuserassignedidentity) to get a list of user-assigned managed identities in your resource group.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
    }
    Get-AzUserAssignedIdentity @parameters | Format-List Name, Id
    ```

1. Review the output from the command. Record the value of the `Id` field as this fully qualified resource identifier is used to assign the user-assigned managed identity to your Azure resource.

    ```output
    Name : msdocs-identity-example-user-assigned
    Id   : /subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned
    ```

    > [!NOTE]
    > In this example, the `Id` value would be `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned`. This example uses fictituous data and your identifier would be distinct from this example.

::: zone-end

## Create an Azure service with a user-assigned managed identity

Assign the previously created user-assigned managed identity to a new Azure host service. This section creates an [Azure App Services](/azure/app-service) web app resource.

::: zone pivot="azure-interface-cli"

1. Create a new app service plan using [`az appservice plan create`](/cli/azure/appservice/plan#az-appservice-plan-create).

    ```azurecli-interactive
    az appservice plan create \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-new-plan>"
    ```

1. Assign the user-assigned managed identity to a new web app with [`az webapp create`](/cli/azure/webapp#az-webapp-create). Use the `id` field recorded earlier in this guide as the value of the `ssign-identity` parameter.

    ```azurecli-interactive
    az webapp create \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-web-app>" \
        --plan "<name-of-existing-plan>" \
        --assign-identity "<resource-id-recorded-earlier>"
    ```

1. Get the details for all identities assigned to this account using [`az webapp show`](/cli/azure/webapp#az-webapp-show) and a JMESPath query.

    ```azurecli-interactive
    az webapp show \
        --resource-group "<name-of-existing-resource-group>" \
        --name "<name-of-existing-account>" \
        --query "identity"   
    ```

1. Review the output from the command. It should include both the user-assigned managed identity.

    ```json
    {
      "principalId": null,
      "tenantId": null,
      "type": "UserAssigned",
      "userAssignedIdentities": {
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned": {
          "clientId": "11112222-bbbb-3333-cccc-4444dddd5555",
          "principalId": "cccccccc-dddd-eeee-3333-444444444444"
        }
      }
    }
    ```

::: zone-end

::: zone pivot="azure-interface-bicep"

1. Create another Bicep file named *app-service-web-app.bicep* and define an Azure App Service plan and web app. Set these properties for those resources:

    | | Resource | Value |
    | --- | --- |
    | **`name`** | Existing managed identity | Use a parameter named `identityName` |
    | **`name`** | App service plan | Use a parameter named `planName` |
    | **`location`** | App service plan | Set to resource group's location |
    | **`name`** | Web app | Use a parameter named `webAppName` |
    | **`location`** | Web app | Set to resource group's location |
    | **`identity.type`** | `UserAssigned` |
    | **`identity.userAssignedIdentities.{identity.id}`** | `{}` |
    | **`properties.serverFarmId`** | `plan.id` |

    ```bicep
    metadata description = 'Creates an Azure App Service plan and web app with a user-assigned managed identity.'
    
    @description('The name of the app service plan.')
    param planName string
    
    @description('The name of the web app.')
    param webAppName string
    
    @description('The name of the user-assigned managed identity.')
    param identityName string
    
    resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
      name: identityName
    }
    
    resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
      name: planName
      location: resourceGroup().location
    }
    
    resource webApp 'Microsoft.Web/sites@2023-12-01' = {
      name: webAppName
      location: resourceGroup().location
      identity: {
        type: 'UserAssigned'
        userAssignedIdentities: {
          '${identity.id}': {}
        }
      }
      properties: {
        serverFarmId: plan.id
      }
    }
    
    output userAssignedIdentity object = webApp.identity
    ```

1. Create a Bicep parameters file named *app-service-web-app.bicepparam*. In this parameters file, create a unique name for your web app and plan using the `planName` and `webAppName` parameters respectively. Then, provide the name of the user-assigned managed identity as the value of the `identityName` parameter.

    ```bicep
    using './app-service-web-app.bicep'
    
    param planName = '<name-of-new-app-service-plan>'
    param webAppName = '<name-of-new-web-app>'
    param identityName = '<name-of-existing-managed-identity>'
    ```

1. Deploy the Bicep template using `az deployment group create`. Specify the name of the Bicep template, parameters file, and Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<name-of-existing-resource-group>" \
        --parameters "app-service-web-app.bicepparam" \
        --template-file "app-service-web-app.bicep"
    ```

1. Review the output from the deployment. The output contains the identity object from the container instance in the `properties.outputs.userAssignedIdentity.value` property.

    ```json
    {
      "type": "UserAssigned",
      "userAssignedIdentities": {
        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned": {
          "clientId": "11112222-bbbb-3333-cccc-4444dddd5555",
          "principalId": "cccccccc-dddd-eeee-3333-444444444444"
        }
      }
    }
    ```

::: zone-end

::: zone pivot="azure-interface-portal"

1. TODO

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

1. TODO

    :::image source="media/managed-identities/<todo>.png" alt-text="Screenshot of [TODO].":::

::: zone-end

::: zone pivot="azure-interface-powershell"

1. Use [`New-AzWebApp`](/powershell/module/az.websites/new-azwebapp) to create a new Azure App Service web app.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-new-web-app>"
        Location = "<azure-region>"
    }
    New-AzWebApp @parameters
    ```

1. Patch the newly created web app to set the `identity.type` property to `UserAssigned` and add your existing user-assigned managed identity to the `identity.userAssignedIdentities` property. To accomplish this, first provide the `id` field recorded earlier in this guide as the value of the `identityId` shell variable. Then, construct a payload object and convert it to JSON. Finally, use [`Invoke-AzRestMethod`](/powershell/module/az.accounts/invoke-azrestmethod) with the `PATCH` HTTP verb to update the existing web app.

    ```azurepowershell-interactive
    $identityId = "<resource-id-recorded-earlier>"
    
    $payload = @{
        identity = @{
            type = "UserAssigned"
            userAssignedIdentities = @{
                "$identityId" = @{}
            }
        }
    } | ConvertTo-Json -Depth 3
    
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-web-app>"
        ResourceProviderName = 'Microsoft.Web'
        ResourceType = 'sites'
        ApiVersion = '2023-12-01'
        Method = 'PATCH'
        Payload = $payload
    }
    Invoke-AzRestMethod @parameters
    ```

1. Get the details for all identities assigned to the web app using [`Get-AzWebApp`](/powershell/module/az.websites/get-azwebapp), `Select-Object`, and `ConvertTo-Json` selecting only the `Identity` property.

    ```azurepowershell-interactive
    $parameters = @{
        ResourceGroupName = "<name-of-existing-resource-group>"
        Name = "<name-of-existing-web-app>"
    }
    Get-AzWebApp @parameters | Select-Object Identity | ConvertTo-Json -Depth 3
    ```

1. Review the output from the command. It should include the unique identifiers for the identity and tenant.

    ```output
    {
      "Identity": {
        "Type": "UserAssigned",
        "TenantId": null,
        "PrincipalId": null,
        "UserAssignedIdentities": {
          "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/msdocs-identity-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/msdocs-identity-example-user-assigned": {
            "PrincipalId": "cccccccc-dddd-eeee-3333-444444444444",
            "ClientId": "11112222-bbbb-3333-cccc-4444dddd5555"
          }
        }
      }
    }
    ```

::: zone-end
