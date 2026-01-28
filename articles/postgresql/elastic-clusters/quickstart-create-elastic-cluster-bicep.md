---
title: "Quickstart: Create elastic clusters with Bicep template"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL flexible server instance with elastic clusters by using a Bicep template.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: elastic-clusters
ms.topic: quickstart
---

# Quickstart: Use a Bicep template to create an elastic cluster with Azure Database for PostgreSQL

Azure Database for PostgreSQL with elastic clusters is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud with a horizontal scale-out capability. You can use a Bicep template to provision your Azure Database for PostgreSQL flexible server elastic clusters instance.

[!INCLUDE [About Bicep](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-bicep-introduction.md)]

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Review the Bicep template

An Azure Database for PostgreSQL flexible server elastic cluster instance is the parent resource for a distributed database within a region. It provides the scope for management policies that apply to the cluster: firewall, users, roles, and configurations.

Create an `elastic-cluster-template.bicep` file and copy the following script into it.

```bicep
param administratorLogin string

@secure()
param administratorLoginPassword string

param clusterName string

param location string = 'canadacentral'

param clusterSize int = 2

param skuName string = 'Standard_D4ds_v5'
param serverEdition string = 'GeneralPurpose'

param storageSizeGB int = 64

param availabilityZone string = '1'

param backupRetentionDays int = 7

resource server 'Microsoft.DBforPostgreSQL/flexibleServers@2025-08-01' = {
  location: location
  name: clusterName
  properties: {
    createMode: 'Default'
    version: '17'
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    availabilityZone: availabilityZone
    Storage: {
      StorageSizeGB: storageSizeGB
      Autogrow: 'Disabled'
    }
    Network: {
      publicNetworkAccess: 'Enabled'
    }
    Backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    cluster: {
      clusterSize: clusterSize
    }
  }
  sku: {
    name: skuName
    tier: serverEdition
  }
}

param firewallRules object = {
  rules: [
    {
      name: 'AllowAll'
      startIPAddress: '0.0.0.0'
      endIPAddress: '255.255.255.255'
    }
  ]
}

// Create one child firewall rule per entry in firewallRules.rules
resource serverFirewallRules 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2025-08-01' = [
  for rule in firewallRules.rules: {
    name: rule.name
    parent: server
    properties: {
      startIpAddress: rule.startIPAddress
      endIpAddress: rule.endIPAddress
    }
  }
]
```

These resources are defined in the Bicep file:

- [Microsoft.DBforPostgreSQL/flexibleServers](/azure/templates/microsoft.dbforpostgresql/flexibleservers?tabs=bicep)

## Deploy the Bicep file

Use Azure CLI or Azure PowerShell to deploy the Bicep file.

```azurecli-interactive
az login

$resourceGroupName = Read-Host -Prompt "Enter a name for the resource group where the server will exist"

az deployment group create `
  --resource-group $resourceGroupName `
  --template-file ./elastic-cluster-template.bicep
```

You're prompted to enter these values:

- **clusterName**: enter a unique name that identifies your Azure Database for PostgreSQL flexible server elastic cluster instance. The domain name `postgres.database.azure.com` is appended to the cluster name you provide. The cluster name can contain only lowercase letters, numbers, and the hyphen (-) character. It must contain at least 3 through 63 characters.
- **administratorLogin**: enter your own authentication account to use when you connect to the server. For example, `clusterAdmin`. The admin authentication name can't be `azure_superuser`, `azure_pg_admin`, `admin`, `administrator`, `root`, `guest`, or `public`. It can't start with `pg_`.
- **administratorLoginPassword**: enter a new password for the server admin account. It must contain between 8 and 128 characters. Your password must contain characters from three of the following categories: English uppercase letters, English lowercase letters, numbers (0 through 9), and nonalphanumeric characters (!, $, #, %, etc.).

## Review deployed resources

Follow these steps to verify if your Azure Database for PostgreSQL flexible server elastic cluster was created.

#### [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), search for and select **Azure Database for PostgreSQL flexible servers**.
1. In the database list, select your new server to view the **Overview** page to manage your elastic cluster.

#### [CLI](#tab/CLI)

You have to enter the name and the resource group of the new elastic cluster to view details about your Azure Database for PostgreSQL flexible server elastic cluster.

```azurecli-interactive
$resourceGroupName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL flexible server cluster exists"
$clusterName = Read-Host -Prompt "Enter your Azure Database for PostgreSQL flexible server elastic cluster name"
az resource show --resource-group $resourcegroupName --name $clusterName --resource-type "Microsoft.DBforPostgreSQL/flexibleServers"
```

---

> [!NOTE]
> Keep this resource group and the elastic cluster if you want to use it to continue with the next suggested steps listed in the [Related content](#related-content) section. The next steps show you how to use elastic clusters with different application sharding models and designs.

## Clean up resources

When you're finished with your elastic cluster environment, delete your elastic cluster resource. 

To delete the elastic cluster, follow these steps:

#### [Portal](#tab/azure-portal)

In the [portal](https://portal.azure.com), select the elastic cluster you want to delete.

1. From the **Overview** page, select **Delete**.
1. Review your resource details, and acknowledge the delete request to confirm the deletion operation by checking the checkbox.
1. Select **Delete**.

#### [CLI](#tab/azure-cli)

```azurecli-interactive

$resourceGroupName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL flexible server exists"
$clusterName = Read-Host -Prompt "Enter your Azure Database for PostgreSQL flexible server elastic cluster name"
az resource delete --resource-type Microsoft.DBforPostgreSQL/flexibleServers `
--name $clusterName --resource-group $resourceGroupName

```

---

## Related content

- [Design multitenant database with elastic clusters](../configure-maintain/tutorial-multitenant-database.md).
