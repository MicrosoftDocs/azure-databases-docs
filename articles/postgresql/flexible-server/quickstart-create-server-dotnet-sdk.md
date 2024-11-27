---
title: "Quickstart: Create with Azure libraries (SDK) for.NET"
description: This document is a QuickStart guide for Azure SDK library for .NET to create, update, and delete an Azure PostgreSQL Flexible Server Instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 11/08/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
---

# Quickstart: Use Azure (SDK) libraries in .NET to create, update, delete - Azure PostgreSQL Flexible Server Instance

Azure Database for PostgreSQL flexible server is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud. You can use .NET SDK to provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server.

The `Azure.ResourceManager.PostgreSql` library is part of the Azure SDK for .NET and provides functionality for managing PostgreSQL flexible servers in Azure. With this library, you can perform various operations related to PostgreSQL flexible servers, including but not limited to:

1. **Creating Azure PostgreSQL Flexible Servers**:\
   You can create new Flexible Servers instances with specified configurations such as location, SKU, storage, and version.

2. **Updating Azure PostgreSQL Flexible Servers**:\
   You can update existing PostgreSQL flexible servers, including changing configurations like administrator login, password, SKU, storage, and version.

3. **Deleting Azure PostgreSQL Flexible Servers**:\
   You can delete existing Azure PostgreSQL flexible server instances.

4. **Retrieving Azure PostgreSQL Flexible Server Information**:\
   You can retrieve details about existing PostgreSQL flexible servers, including their configurations, status, and other metadata.

5. **Managing Databases**:\
   You can create, update, delete, and retrieve databases within the Azure PostgreSQL flexible server instance.

6. **Managing Firewall Rules**:\
   You can create, update, delete, and retrieve firewall rules for an instance to control access.

7. **Managing Configuration Settings**:\
   You can manage configuration settings for an Azure PostgreSQL flexible server instance, including retrieving and updating server parameters.

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/free/).
Log in to your account using az cli. To know more details on az cli follow this [Link](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)

### 1. Open the Terminal
### 2. Run the login command
```bash
az login
```
### 3. Follow the instructions that appear:
It involves selecting an account which redirects you to the browser and then selecting a subscription ID/name on the command line.

## Install the required packages.

```bash
dotnet add package Azure.Identity
dotnet add package Azure.ResourceManager
dotnet add package Azure.ResourceManager.PostgreSql
```
If you are having any issues related to initial setup for .NET follow this guide [Link](https://learn.microsoft.com/dotnet/core/install/windows)
After installing these packages, ensure that each one them is listed in the .csproj file before you execute the build and run commands. [Learn more about .csproj file](https://learn.microsoft.com/aspnet/web-forms/overview/deployment/web-deployment-in-the-enterprise/understanding-the-project-file)

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
            string subscriptionId = "subscription-id";
            // Replace with your resource group name 
            string resourceGroupName = "resource-group-name"; 
            // Replace with a unique server name
            string serverName = "server-name"; 
            // Replace with your desired region
            string location = "region-name"; 
            // Create the resource identifier for the resource group
            ResourceIdentifier resourceGroupId = ResourceGroupResource.CreateResourceIdentifier(subscriptionId, resourceGroupName);
            ResourceGroupResource resourceGroup = await armClient.GetResourceGroupResource(resourceGroupId).GetAsync();
            // Prepare server data
            var serverData = new PostgreSqlFlexibleServerData(location)
            {   
                AdministratorLogin = "admin-username", 
                AdministratorLoginPassword = "admin-password", 
                Version = "pgVersion", 
                Storage  = new PostgreSqlFlexibleServerStorage() {StorageSizeInGB = 128},
                Sku  = new PostgreSqlFlexibleServerSku("Standard_B1ms", PostgreSqlFlexibleServerSkuTier.Burstable), 
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
This example demonstrates how to create a PostgreSQL flexible server using the `Azure.ResourceManager.PostgreSql` library. You can similarly use other methods provided by the library to manage your PostgreSQL flexible servers and related resources.

Replace the following parameters in the code with your data:

- **subscription-id**: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- **resource-group**: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- **server-name**: A unique name that identifies your Azure Database for PostgreSQL flexible server instance. The domain name `postgres.database.azure.com` is appended to the server name you provide. The server name must be at least three characters and at most 63 characters, and can only contain lowercase letters, numbers, and hyphens.
- **location**: The Azure region where you want to create your Azure Database for PostgreSQL flexible server instance. It defines the geographical location where your server and its data reside. Choose a region close to your users for reduced latency. The location should be specified in the format of Azure region short names, like `westus2`, `east us`, or `north europe`.
- **admin-username**: The primary administrator username for the PostgreSQL server. 
- **admin-password**: A password for the primary administrator for the server. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).
- **SKU** : We use PostgreSqlFlexibleServerSku() constructor and in that we have to pass compute type and compute tier which is either Burstable, GeneralPurpose tier.
You can also customize storage size to your desired usage.
- **pgVersion** : The PostgreSQL server can be created with any of the following versions: 11, 12, 13, 14, 15, or 16.

## Authentication
> [!NOTE]  
> The DefaultAzureCredential class will try to authenticate using various methods, such as environment variables, managed identities, or the Azure CLI.  
> Make sure you have one of these methods set up. You can find more information on authentication in the [Azure SDK documentation](https://learn.microsoft.com/dotnet/api/overview/azure/identity-readme?view=azure-dotnet).


## Run the file
### Everytime you make any change in the .cs file do not forget to build and then run the file:
Run the .cs file with the below commands
```bash
dotnet build
dotnet run
```
> [!NOTE]
> Running this code will initiate the instance creation process, which may take a few minutes to complete.
## Review deployed resources
You can review the deployed flexible server instance through Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources.
## Update server data

Firstly, create a `UpdateServerData.cs` file. 
Using Azure PostgreSQL Flexible server .NET SDK you can also update server data like version, admin username, password etc. using 'CreateOrUpdateAsync' method. The 'CreateOrUpdateAsync' method either creates a new instance if there is no instance with same name, or updates the existing instance with the new server data if it does exist.

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
            string subscriptionId = "subscription-id";
            // Replace with your resource group name 
            string resourceGroupName = "resource-group-name"; 
            // Replace with a unique server name
            string serverName = "server-name"; 
            // Replace with your desired region
            string location = "region-name"; 
            // Create the resource identifier for the resource group
            ResourceIdentifier resourceGroupId = ResourceGroupResource.CreateResourceIdentifier(subscriptionId, resourceGroupName);
            ResourceGroupResource resourceGroup = await armClient.GetResourceGroupResource(resourceGroupId).GetAsync();
            // Prepare server data
            var serverData = new PostgreSqlFlexibleServerData(location)
            {
              
                Version = "16", // Updating version from lower version to a higher version
              
            };
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
Run the file and review the changes made in the resource with the 'UpdateServerData.cs' file.
## Clean up resources
You can clean up the created flexible server instances by following the steps mentioned in the 'Delete Instance' section:

## Delete Instance

You can delete the flexible server instance with the Azure SDK for .NET. Create a `DeleteServer.cs` file and add the following code.

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


            // Replace with your subscription ID
            string subscriptionId = "subscription-id";
            // Replace with your resource group name 
            string resourceGroupName = "resource-group-name"; 
            // Replace with a unique server name
            string serverName = "server-name"; 
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
- **server-name**: The name of the Azure database flexible server instance that you created before

You can also delete the resource group created through the Portal, CLI or PowerShell. Follow steps mentioned in CLI and PowerShell section if you want to delete it using CLI or PowerShell.

## CLI

```azurecli
az group delete --name <resource_group>
```

## PowerShell

```azurepowershell
Remove-AzResourceGroup -Name <resource_group>
```

---

## Related content

- [Create an Azure Database for PostgreSQL - Portal](quickstart-create-server-portal.md)
- [Create an Azure Database for PostgreSQL - Azure CLI](quickstart-create-server-cli.md)
- [Create an Azure Database for PostgreSQL - ARM template](quickstart-create-server-arm-template.md)
- [Create an Azure Database for PostgreSQL - Bicep](quickstart-create-server-bicep.md)
