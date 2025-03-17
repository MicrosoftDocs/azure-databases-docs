---
title: "Quickstart: Create with Bicep"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL flexible server instance by using Bicep.
author: mumian
ms.author: jgao
ms.reviewer: maghan
ms.date: 02/28/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - devx-track-bicep
---

# Quickstart: Use a Bicep file to create an Azure Database for PostgreSQL flexible server instance

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this quickstart, you learn how to use a Bicep file to create an Azure Database for PostgreSQL Flexible Server instance.

Azure Database for PostgreSQL Flexible Server is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud. You can use Bicep to provision an Azure Database for PostgreSQL Flexible Server instance to deploy multiple servers or multiple databases on a server.

[!INCLUDE [About Bicep](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-bicep-introduction.md)]

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/free/).

## Review the Bicep

An Azure Database for PostgreSQL Flexible Server instance is the parent resource for one or more databases within a region. It provides the scope for management policies that apply to its databases: login, firewall, users, roles, and configurations.

Create a _main.bicep_ file and copy the following Bicep into it.

```bicep
param administratorLogin string

@secure()
param administratorLoginPassword string
param location string = resourceGroup().location
param serverName string
param serverEdition string = 'GeneralPurpose'
param skuSizeGB int = 128
param dbInstanceType string = 'Standard_D4ds_v4'
param haMode string = 'ZoneRedundant'
param availabilityZone string = '1'
param version string = '12'
param virtualNetworkExternalId string = ''
param subnetName string = ''
param privateDnsZoneArmResourceId string = ''

resource serverName_resource 'Microsoft.DBforPostgreSQL/flexibleServers@2021-06-01' = {
  name: serverName
  location: location
  sku: {
    name: dbInstanceType
    tier: serverEdition
  }
  properties: {
    version: version
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    network: {
      delegatedSubnetResourceId: (empty(virtualNetworkExternalId) ? json('null') : json('\'${virtualNetworkExternalId}/subnets/${subnetName}\''))
      privateDnsZoneArmResourceId: (empty(virtualNetworkExternalId) ? json('null') : privateDnsZoneArmResourceId)
    }
    highAvailability: {
      mode: haMode
    }
    storage: {
      storageSizeGB: skuSizeGB
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    availabilityZone: availabilityZone
  }
}
```

These resources are defined in the Bicep file:

- [Microsoft.DBforPostgreSQL/flexibleServers](/azure/templates/microsoft.dbforpostgresql/flexibleservers?tabs=bicep)

## Deploy the Bicep file

Use Azure CLI or Azure PowerShell to deploy the Bicep file.

# [CLI](#tab/CLI)

```azurecli-interactive
az group create --name exampleRG --location centralus
az deployment group create --resource-group exampleRG --template-file main.bicep
```

# [PowerShell](#tab/PowerShell)

```azurepowershell-interactive
New-AzResourceGroup -Name "exampleRG" -Location "centralus"
New-AzResourceGroupDeployment -ResourceGroupName exampleRG  -TemplateFile "./main.bicep"
```

---

You're prompted to enter these values:

- **serverName**: enter a unique name that identifies your Azure Database for PostgreSQL Flexible Server instance. For example, `mydemoserver-pg`. The domain name `postgres.database.azure.com` is appended to the server name you provide. The server can contain only lowercase letters, numbers, and the hyphen (-) character. It must contain at least 3 through 63 characters.
- **administratorLogin**: enter your own login account to use when you connect to the server. For example, `myadmin`. The admin login name can't be `azure_superuser`, `azure_pg_admin`, `admin`, `administrator`, `root`, `guest`, or `public`. It can't start with `pg_`.
- **administratorLoginPassword**: enter a new password for the server admin account. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

## Review deployed resources

Use the Azure portal, Azure CLI, or Azure PowerShell to validate the deployment and review the deployed resources.

# [CLI](#tab/CLI)

```azurecli-interactive
az resource list --resource-group exampleRG
```

# [PowerShell](#tab/PowerShell)

```azurepowershell-interactive
Get-AzResource -ResourceGroupName exampleRG
```

---

## Clean up resources

Keep this resource group, server, and single database if you want to go to the [Related content](#related-content). The reference shows you how to connect and query your database using different methods.

To delete the resource group:

# [CLI](#tab/CLI)

```azurecli-interactive
az group delete --name exampleRG
```

# [PowerShell](#tab/PowerShell)

```azurepowershell-interactive
Remove-AzResourceGroup -Name exampleRG
```

---

## Related content

- [Connect and query overview for Azure Database for PostgreSQL flexible server](how-to-connect-query-guide.md).
