---
title: "Quickstart: Create with Azure libraries (SDK) for Python"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL - Flexible Server instance using Azure libraries (SDK) for Python.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 11/07/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
---

# Quickstart: Use an Azure libraries (SDK) for dotnet to create an Azure Database for PostgreSQL - Flexible Server instance

In this quickstart, you learn how to use the [Azure libraries (SDK) for dotnet] to create, update, delete a Azure PostgreSQL flexible server instance.

Azure Database for PostgreSQL flexible server is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud. You can use Python SDK to provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server.

The `Azure.ResourceManager.PostgreSql` library is part of the Azure SDK for .NET and provides functionality for managing PostgreSQL flexible servers in Azure. With this library, you can perform various operations related to PostgreSQL flexible servers, including but not limited to:

1. **Creating PostgreSQL Flexible Servers**:
   - You can create new PostgreSQL flexible servers with specified configurations such as location, SKU, storage, and version.

2. **Updating PostgreSQL Flexible Servers**:
   - You can update existing PostgreSQL flexible servers, including changing configurations like administrator login, password, SKU, storage, and version.

3. **Deleting PostgreSQL Flexible Servers**:
   - You can delete existing PostgreSQL flexible servers.

4. **Retrieving PostgreSQL Flexible Server Information**:
   - You can retrieve details about existing PostgreSQL flexible servers, including their configurations, status, and other metadata.

5. **Managing Databases**:
   - You can create, update, delete, and retrieve databases within a PostgreSQL flexible server.

6. **Managing Firewall Rules**:
   - You can create, update, delete, and retrieve firewall rules for a PostgreSQL flexible server to control access.

7. **Managing Configuration Settings**:
   - You can manage configuration settings for a PostgreSQL flexible server, including retrieving and updating server parameters.



## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/free/).

Install the required packages.

```bash
dotnet add package Azure.Identity
dotnet add package Azure.ResourceManager
dotnet add package Azure.ResourceManager.PostgreSql
```
## Create the Server

Create a `CreateServer.cs` file and include the following code.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace CreatePostgreSqlFlexibleServer
{
    class Program   
    {  
        static async Task Main(string[] args)
        {

            TokenCredential credential = new DefaultAzureCredential();
            ArmClient armClient = new ArmClient(credential);
            // Replace with your subscription ID
            string subscriptionId = "your-subscription-id";
            // Replace with your resource group name 
            string resourceGroupName = "your-resource-group-name"; 
            // Replace with a unique server name
            string serverName = "your-server-name"; 
            // Replace with your desired region
            string location = "your-region-name"; 
            // Create the resource identifier for the resource group
            ResourceIdentifier resourceGroupId = ResourceGroupResource.CreateResourceIdentifier(subscriptionId, resourceGroupName);
            ResourceGroupResource resourceGroup = await armClient.GetResourceGroupResource(resourceGroupId).GetAsync();

            // Prepare server data
            var serverData = new PostgreSqlFlexibleServerData(location)
            {   
                AdministratorLogin = "admin-username", 
                AdministratorLoginPassword = "admin-password", 
                Version = <pgversion>, 
                Storage  = new PostgreSqlFlexibleServerStorage() {StorageSizeInGB = 128},
                Sku  = new PostgreSqlFlexibleServerSku("Standard_D4s_v3", PostgreSqlFlexibleServerSkuTier.GeneralPurpose), 
            };
            try
            {
            ArmOperation<PostgreSqlFlexibleServerResource> operation = await resourceGroup.GetPostgreSqlFlexibleServers().CreateOrUpdateAsync(Azure.WaitUntil.Completed, serverName, serverData);
            PostgreSqlFlexibleServerResource serverResource = operation.Value;
            Console.WriteLine($"PostgreSQL Flexible Server '{serverResource.Data.Name}' created successfully.");
            }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
        }
    }
}
```
The above example demonstrates how to create a PostgreSQL flexible server using the `Azure.ResourceManager.PostgreSql` library. You can similarly use other methods provided by the library to manage your PostgreSQL flexible servers and related resources.

Replace the following parameters in the code with your data:

- **subscription-id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource-group**: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **server-name**: A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide. The server name must be at least three characters and at most 63 characters, and can only contain lowercase letters, numbers, and hyphens.
- **location**: The Azure region where you want to create your Azure Database for PostgreSQL flexible server instance. It defines the geographical location where your server and its data reside. Choose a region close to your users for reduced latency. The location should be specified in the format of Azure region short names, like `westus2`, `east us`, or `north europe`.
- **admin-username**: The primary administrator username for the server. You can create additional users after the server has been created.
- **admin-password**: A password for the primary administrator for the server. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

You can also customize other parameters like storage size, engine version, etc.

> [!NOTE]  
> The DefaultAzureCredential class will try to authenticate using various methods, such as environment variables, managed identities, or the Azure CLI.  
> Make sure you have one of these methods set up. You can find more information on authentication in the [Azure SDK documentation](https://learn.microsoft.com/dotnet/api/overview/azure/identity-readme?view=azure-dotnet).

## Review deployed resources
You can review the deployed flexible server instance through Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources.


# [Dotnet SDK](#tab/DotnetSDK)

To check if the flexible server instance exists we can use the following code:

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace CreatePostgreSqlFlexibleServer
{
    class Program
    {
        static async Task Main(string[] args)
        {
            string subscriptionId = <subscription-id>; // Replace with your subscription ID
            string resourceGroupName = <resource-group-name>; // Replace with your resource group name
            string serverName = <server-name>; // Replace with a unique server name
            string location = <region-name>; // Replace with your desired region
            // Create the resource identifier for the resource group
            var credential = new DefaultAzureCredential();
            //Authenticate
            var armClient = new ArmClient(credential);
      

            //Used to fetch the flexible server instance from the specific resource group
            var postgresServerResourceId = PostgreSqlFlexibleServerResource.CreateResourceIdentifier(subscriptionId, resourceGroupName, serverName);
            var postgresServer = armClient.GetPostgreSqlFlexibleServerResource(postgresServerResourceId);

            if(postgresServerResourceId.ToString().Contains(serverName))
            {
                Console.WriteLine($"PostgreSQL Flexible Server '{serverName}' does not exist");
            }
            else
            {
                Console.WriteLine($"PostgreSQL Flexible Server '{serverName}' already exists");
            }
        
        }
        
        }
    }
```
## Update server data

Using Azure PostgreSQL Flexible server Dotnet SDK you can also update server data like version, admin username, password etc using 'CreateOrUpdateAsync' method. With that method it creates the instance if there exists no instance with the same name or if there exists an instance with same name it updates that instance with the new server data.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace CreatePostgreSqlFlexibleServer
{
    class Program
    {
        static async Task Main(string[] args)
        {

            TokenCredential credential = new DefaultAzureCredential();
            ArmClient armClient = new ArmClient(credential);
            string subscriptionId = <subscription-id>; // Replace with your subscription ID
            string resourceGroupName = <resource-group-name>; // Replace with your resource group name
            string serverName = <server-name>; // Replace with a unique server name
            string location = <region>; // Replace with your desired region
            // Create the resource identifier for the resource group
            ResourceIdentifier resourceGroupId = ResourceGroupResource.CreateResourceIdentifier(subscriptionId, resourceGroupName);
            ResourceGroupResource resourceGroup = await armClient.GetResourceGroupResource(resourceGroupId).GetAsync();

            // Prepare server data
            var serverData = new PostgreSqlFlexibleServerData(location)
            {
              
                Version = "16", // Updating version from lower version to a higher version
              
            };

            // Create the PostgreSQL flexible server
            try
            {
            ArmOperation<PostgreSqlFlexibleServerResource> operation = await resourceGroup.GetPostgreSqlFlexibleServers().CreateOrUpdateAsync(Azure.WaitUntil.Completed, serverName, serverData);
            PostgreSqlFlexibleServerResource serverResource = operation.Value;
            Console.WriteLine($"PostgreSQL Flexible Server '{serverResource.Data.Name}' updated successfully.");
            }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
        }
    }
}

```
## Delete Instance

You can also delete the flexible server instance with the Azure SDK for dotnet.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace CreatePostgreSqlFlexibleServer
{
    class Program
    {
        static async Task Main(string[] args)
        {

          //  TokenCredential credential = new DefaultAzureCredential();
           // ArmClient armClient = new ArmClient(credential);
            string subscriptionId = "5c5037e5-d3f1-4e7b-b3a9-f6bf94902b30"; // Replace with your subscription ID
            string resourceGroupName = "gkasar"; // Replace with your resource group name
            string serverName = "gkasarnetserver"; // Replace with a unique server name
            string location = "east us"; // Replace with your desired region
            // Create the resource identifier for the resource group
          // Authenticate
        var credential = new DefaultAzureCredential();
        var armClient = new ArmClient(credential);

      

            // Create the PostgreSQL flexible server
            try
            {
              // Get the PostgreSQL Flexible Server resource
        var postgresServerResourceId = PostgreSqlFlexibleServerResource.CreateResourceIdentifier(subscriptionId, resourceGroupName, serverName);
        var postgresServer = armClient.GetPostgreSqlFlexibleServerResource(postgresServerResourceId);

        // Delete the server
        await postgresServer.DeleteAsync(Azure.WaitUntil.Completed);

        Console.WriteLine($"PostgreSQL Flexible Server '{serverName}' deleted successfully.");
            }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
        }
    }
}
```
Replace the following parameters with your data:

- **subscription-id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource-group-name**: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **sever-name**: The name of the Azure database flexible server instance that you created before

# [CLI](#tab/CLI)

```azurecli
az group delete --name <resource_group>
```

# [PowerShell](#tab/PowerShell)

```azurepowershell
Remove-AzResourceGroup -Name <resource_group>
```

---

## Related content

- [Create an Azure Database for PostgreSQL - Portal](quickstart-create-server-python-sdk.md)
- [Create an Azure Database for PostgreSQL - Azure CLI](quickstart-create-server-cli.md)
- [Create an Azure Database for PostgreSQL - ARM template](quickstart-create-server-arm-template.md)
- [Create an Azure Database for PostgreSQL - Bicep](quickstart-create-server-bicep.md)
