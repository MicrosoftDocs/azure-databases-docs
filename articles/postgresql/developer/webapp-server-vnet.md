---
title: "Article: Create Azure App Service Web App in Same Virtual Network"
description: Quickstart guide to create an Azure Database for PostgreSQL flexible server instance with a web app in the same virtual network.
author: agapovm
ms.author: maximagapov
ms.reviewer: maghan
ms.date: 01/08/2026
ms.service: azure-database-postgresql
ms.topic: article
ms.custom:
  - mvc
  - devx-track-azurecli
  - sfi-ropc-blocked
ms.devlang: azurecli
---

# Create an Azure Database for PostgreSQL with a web app in a virtual network

This article shows you how to create an Azure App Service Web app with Azure Database for PostgreSQL flexible server inside a [Virtual network](/azure/virtual-network/virtual-networks-overview).

In this article, you learn how to:
> [!div class="checklist"]
> - Create an Azure Database for PostgreSQL flexible server instance in a virtual network
> - Create a web app
> - Add the web app to the virtual network
> - Connect to Azure Database for PostgreSQL flexible server from the web app

## Prerequisites

- If you don't have an Azure subscription, create a [free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) account before you begin.
- [Install Azure CLI](/cli/azure/install-azure-cli) version 2.0 or later locally (or use [Azure Cloud Shell](https://azure.microsoft.com/get-started/azure-portal/cloud-shell/) which has CLI preinstalled). To see the version installed, run the `az --version` command.
- Sign in to your account by using the [az login](/cli/azure/authenticate-azure-cli) command. Note the **id** property from the command output for the corresponding subscription name.

  ```azurecli-interactive
  az login
  ```
- If you have multiple subscriptions, choose the appropriate subscription for billing the resource. Select the specific subscription ID under your account by using the [az account set](/cli/azure/account) command.

  ```azurecli-interactive
  az account set --subscription <subscription ID>
  ```

## Create a flexible server instance

in a new virtual network

Create a private Azure Database for PostgreSQL flexible server instance inside a virtual network (VNET) using the following command:

```azurecli-interactive
az postgres flexible-server create --resource-group demoresourcegroup --name demoserverpostgres --vnet demoappvnet --location westus2
```
This command performs the following actions, which might take a few minutes:

- Create the resource group if it doesn't already exist.
- Generates a server name if it's not provided.
- Creates a virtual network and subnet for the Azure Database for PostgreSQL flexible server instance.
- Creates admin username and password for your server if not provided.
- Creates an empty database called **postgres**.

Here's the sample output.

```json
Creating Resource Group 'demoresourcegroup'...
Creating new Vnet "demoappvnet" in resource group "demoresourcegroup"
Creating new Subnet "Subnetdemoserverpostgres" in resource group "demoresourcegroup"
Creating a private dns zone demoserverpostgres.private.postgres.database.azure.com in resource group "demoresourcegroup"
Creating PostgreSQL Server 'demoserverpostgres' in group 'demoresourcegroup'...
Your server 'demoserverpostgres' is using sku 'Standard_D2s_v3' (Paid Tier). Please refer to https://aka.ms/postgres-pricing for pricing details
Creating PostgreSQL database 'flexibleserverdb'...
Make a note of your password. If you forget, you would have to reset your password with "az postgres flexible-server update -n demoserverpostgres -g demoresourcegroup -p <new-password>".
Try using 'az postgres flexible-server connect' command to test out connection.
{
  "connectionString": "postgresql://generated-username:generated-password@demoserverpostgres.postgres.database.azure.com/postgres?sslmode=require",
  "host": "demoserverpostgres.postgres.database.azure.com",
  "id": "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/demoresourcegroup/providers/Microsoft.DBforPostgreSQL/flexibleServers/demoserverpostgres",
  "location": "East US",
  "password": "generated-password",
  "resourceGroup": "demoresourcegroup",
  "skuname": "Standard_D2s_v3",
  "subnetId": "/subscriptions/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/resourceGroups/demoresourcegroup/providers/Microsoft.Network/virtualNetworks/demoappvnet/subnets/Subnetdemoserverpostgres",
  "username": "generated-username",
  "version": "12"
}
```

## Create a web app

In this section, you create an app host in an App Service app, connect this app to the Azure Database for PostgreSQL flexible server database, and then deploy your code to that host. Make sure you're in the repository root of your application code in the terminal. The Basic Plan doesn't support VNET integration. Use Standard or Premium.

Create an App Service app (the host process) by using the `az webapp up` command.

```azurecli-interactive
az webapp up --resource-group demoresourcegroup --location westus2 --plan testappserviceplan --sku P2V2 --name mywebapp
```

> [!NOTE]  
> - For the _--location_ argument, use the same location as you did for the database in the previous section.
> - Replace \<app-name\> with a unique name across all Azure. Allowed characters for \<app-name\> are A-Z, 0-9, and -. A good pattern is to use a combination of your company name and an app identifier.

This command performs the following actions, which might take a few minutes:

- Creates the resource group if it doesn't already exist. (In this command, you use the same resource group in which you created the database earlier.)
- Creates the App Service app if it doesn't exist.
- Enables default logging for the app, if not already enabled.
- Uploads the repository by using ZIP deployment with build automation enabled.

### Create subnet for web app

Before enabling VNET integration, you need a subnet that's delegated to App Service Web App. Before creating the subnet, view the database subnet address to avoid using the same address prefix for the web app subnet.

```azurecli-interactive
az network vnet show --resource-group demoresourcegroup -n demoappvnet
```

Run the following command to create a new subnet in the same virtual network as the Azure Database for PostgreSQL flexible server instance. **Update the address prefix to avoid conflict with the Azure Database for PostgreSQL flexible server subnet.**

```azurecli-interactive
az network vnet subnet create --resource-group demoresourcegroup --vnet-name demoappvnet --name webappsubnet  --address-prefixes 10.0.1.0/24  --delegations Microsoft.Web/serverFarms
```

## Add the web app to the virtual network

Use the [az webapp vnet-integration](/cli/azure/webapp/vnet-integration) command to add a regional virtual network integration to a web app.

```azurecli-interactive
az webapp vnet-integration add --resource-group demoresourcegroup -n  mywebapp --vnet demoappvnet --subnet webappsubnet
```

## Configure environment variables to connect the database

After deploying the code to App Service, connect the app to the Azure Database for PostgreSQL flexible server instance in Azure. The app code expects to find database information in many environment variables. To set environment variables in App Service, use the [az webapp config appsettings set](/cli/azure/webapp/config/appsettings#az-webapp-config-appsettings-set) command.

```azurecli-interactive
az webapp config appsettings set  --name mywebapp --settings DBHOST="<postgres-server-name>.postgres.database.azure.com" DBNAME="postgres" DBUSER="<username>" DBPASS="<password>"
```
- Replace **postgres-server-name**, **username**, and **password** with the values for the newly created Azure Database for PostgreSQL flexible server instance.

- Replace **\<username\>** and **\<password\>** with the credentials that the command also generated for you.
- The resource group and app name come from the cached values in the .azure/config file.
- The command creates settings named **DBHOST**, **DBNAME**, **DBUSER**, and **DBPASS**. If your application code uses different names for the database information, use those names for the app settings as mentioned in the code.

Configure the web app to allow all outbound connections from within the virtual network.

```azurecli-interactive
az webapp config set --name mywebapp --resource-group demoresourcegroup --generic-configurations '{"vnetRouteAllEnabled": true}'
```

## Clean up resources

Clean up all resources you created in the article by using the following command. This command deletes all the resources in this resource group.

```azurecli-interactive
az group delete -n demoresourcegroup
```

## Related content

- [Map an existing custom DNS name to Azure App Service](/azure/app-service/app-service-web-tutorial-custom-domain)
