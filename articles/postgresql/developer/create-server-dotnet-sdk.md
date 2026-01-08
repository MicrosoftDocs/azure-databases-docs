---
title: "Quickstart: Create with Azure Libraries (SDK) For.NET"
description: This document is a QuickStart guide for Azure SDK library for .NET to create, update, and delete an Azure PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/08/2026
ms.service: azure-database-postgresql
ms.topic: quickstart
---

# Create an Azure Database for PostgreSQL instance using .NET SDK

In this quickstart, you learn how to use the Azure SDK libraries in .NET to create, update, and delete an Azure PostgreSQL flexible server instance. Azure Database for PostgreSQL is a managed service that allows you to run, manage, and scale highly available PostgreSQL databases in the cloud. Using the .NET SDK, you can provision an Azure Database for PostgreSQL flexible server instance, multiple servers, or multiple databases on a server.

## Prerequisites

- [An Azure account with an active subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md).
- [.NET framework](https://dotnet.microsoft.com/download) installed on your local machine.
- [Azure CLI](/cli/azure/install-azure-cli) installed on your local machine.

## Azure.ResourceManager.PostgreSql library

The `Azure.ResourceManager.PostgreSql` library is part of the Azure SDK for .NET and provides functionality for managing PostgreSQL flexible server instances in Azure. With this library, you can perform various operations related to PostgreSQL flexible server instances, including but not limited to:

1. **Creating Azure PostgreSQL flexible server instances**:\
   You can create new flexible server instances with specified configurations such as location, SKU, storage, and version.

1. **Updating Azure PostgreSQL flexible server instances**:\
   You can update existing PostgreSQL flexible server instances, including changing configurations like administrator login, password, SKU, storage, and version.

1. **Deleting Azure PostgreSQL flexible server instances**:\
   You can delete existing Azure PostgreSQL flexible server instances.

1. **Retrieving Azure PostgreSQL Information**:\
   You can retrieve details about existing PostgreSQL flexible server instances, including their configurations, status, and other metadata.

1. **Managing Databases**:\
   You can create, update, delete, and retrieve databases within the Azure PostgreSQL flexible server instance.

1. **Managing Firewall Rules**:\
   You can create, update, delete, and retrieve firewall rules for an instance to control access.

1. **Managing Configuration Settings**:\
   You can manage configuration settings for an Azure PostgreSQL flexible server instance, including retrieving and updating server parameters.

## Log in to Azure

Before using the Azure SDK for .NET to create, update, or delete an Azure Database for PostgreSQL flexible server instance, you must log in to your Azure account using the Azure CLI.

### Run the login command

Log in to your account using [az CLI](/cli/azure/authenticate-azure-cli-interactively)

```azurecli-interactive
az login
```

## Install required packages

Install the necessary packages using the following commands:

```bash
dotnet add package Azure.Identity
dotnet add package Azure.ResourceManager
dotnet add package Azure.ResourceManager.PostgreSql
```

After installing these packages, ensure that each em is listed in the `.csproj` file befoexecutingute the build and run commands.

To Learn more about the `.csproj` file, visit [Web Deployment](/aspnet/web-forms/overview/deployment/web-deployment-in-the-enterprise/understanding-the-project-file).

> [!NOTE]  
> If you are having issues related to initial setup for .NET, follow this [guide](/dotnet/core/install/windows).

## Create the project

Create a new .NET project by following the steps mentioned in this [link](/dotnet/core/tutorials/cli-templates-create-project-template)

### Create the Server

To create a PostgreSQL flexible server instance, create a file named `CreateServer.cs` with the following code.

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
              Storage = new PostgreSqlFlexibleServerStorage() { StorageSizeInGB = 128 },
              Sku = new PostgreSqlFlexibleServerSku("Standard_B1ms", PostgreSqlFlexibleServerSkuTier.Burstable),
           };
            try
            {
               ArmOperation<PostgreSqlFlexibleServerResource> operation = await resourceGroup.GetPostgreSqlFlexibleServers().CreateOrUpdateAsync(Azure.WaitUntil.Completed, serverName, serverData);
              PostgreSqlFlexibleServerResource serverResource = operation.Value;
              Console.WriteLine($"PostgreSQL flexible server '{serverResource.Data.Name}' created successfully.");
           }
            catch (Exception ex)
            {
               Console.WriteLine($"An error occurred: {ex.Message}");
            }
   }
  }
}
```

This example demonstrates creating a PostgreSQL flexible server instance using the Azure Resource Manager. PostgreSql library. You can similarly use other methods provided by the library to manage your PostgreSQL flexible server instances and related resources.

Replace the following parameters in the code with your data:

- `subscription-id`: Your Azure subscription ID.
- `resource-group-name`: The name of your resource group.
- `server-name`: A unique name for your PostgreSQL server.
- `location`: The Azure region for your server.
- `admin-username`: The administrator username.
- `admin-password`: The administrator password.
- `pgVersion`: The PostgreSQL version (for example, 11, 12, 13, 14, 15, or 16).

### Authentication

The `DefaultAzureCredential` class tries to authenticate using methods like environment variables, managed identities, or Azure CLI. Ensure you have one of these methods configured.

## Run the file

To run the file, you must build and execute the .cs file using the .NET CLI. This initiates the creation, update, or deletion process for the PostgreSQL instance as per the code.

Every time you make any change in the .cs file, don't forget to build and then run the file

Run the .cs file with the below commands

```bash
dotnet build
dotnet run
```

> [!NOTE]  
> Running this code will initiate the instance creation process, which might take a few minutes to complete.

## Review deployed resources

You can review the deployed flexible server instance through Azure portal, Azure CLI, Azure PowerShell, and various other tools to validate the deployment and review the deployed resources.

## Update server data

Create a `UpdateServerData.cs` file.

You can also update server data using the Azure PostgreSQL .NET SDK.

For example, you can update the version, admin username, password, etc., using the `CreateOrUpdateAsync` method.

The `CreateOrUpdateAsync` method either creates a new instance if there's no instance with the same name or updates the existing instance with the new server data if it does exist.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace UpdateServerData
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
            ResourceIdentifier resourceGroupId = ResourceGroupResource.CreateResourceIdentifier(subscriptionId, resourceGroupName);
            ResourceGroupResource resourceGroup = await armClient.GetResourceGroupResource(resourceGroupId).GetAsync();
            // Prepare server data
            var serverData = new PostgreSqlFlexibleServerData(location)
           {
              // Updating version from a lower version to a higher version
              Version = "16",
           };
            try
             {
               ArmOperation<PostgreSqlFlexibleServerResource> operation = await resourceGroup.GetPostgreSqlFlexibleServers().CreateOrUpdateAsync(Azure.WaitUntil.Completed, serverName, serverData);
               PostgreSqlFlexibleServerResource serverResource = operation.Value;
               Console.WriteLine($"PostgreSQL flexible server '{serverResource.Data.Name}' updated successfully.");
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

You can clean up the created flexible server instances by deleting the flexible server instance with the Azure SDK for .NET.

Create a `DeleteServer.cs` file and add the following code.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

namespace DeleteServer
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
            try
            {
                // Get the PostgreSQL flexible server resource
                var postgresServerResourceId = PostgreSqlFlexibleServerResource.CreateResourceIdentifier(subscriptionId, resourceGroupName, serverName);
                var postgresServer = armClient.GetPostgreSqlFlexibleServerResource(postgresServerResourceId);
                // Delete the server
                await postgresServer.DeleteAsync(Azure.WaitUntil.Completed);
                Console.WriteLine($"PostgreSQL flexible server '{serverName}' deleted successfully.");
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

- `subscription-id`: Your own [subscription ID](/azure/azure-portal/get-subscription-tenant-id#find-your-azure-subscription).
- `resource-group-name`: The name of the resource group you want to use. The script creates a new resource group if it doesn't exist.
- `server-name`: The name of the Azure database flexible server instance that you created.

You can also delete the resource group created through the Portal, CLI, or PowerShell. Follow the steps mentioned in the CLI and PowerShell section if you want to delete it using CLI or PowerShell.

Replace placeholders with your details and run the file.

Alternatively, you can remove the resource group using:
- **Azure CLI**: `az group delete --name <resource_group>`
- **PowerShell**: `Remove-AzResourceGroup -Name <resource_group>`
- **Azure portal**: Navigate to the resource group and delete it.

## Related content

- [Quickstart: Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md)
