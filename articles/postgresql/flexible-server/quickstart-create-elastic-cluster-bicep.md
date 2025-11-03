---
title: "Quickstart: Create elastic clusters with Bicep template"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL flexible server instance with elastic clusters by using a Bicep template.
author: jaredmeade
ms.author: jaredmeade
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
---

# Quickstart: Use a Bicep template to create an elastic cluster with Azure Database for PostgreSQL

Azure Database for PostgreSQL with elastic clusters is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud with a horizontal scale-out capability. You can use an Azure Resource Manager template (Bicep template) to create an elastic clusters instance.

Bicep is a domain-specific language that uses declarative syntax to deploy Azure resources. In a Bicep file, you define the infrastructure you want to deploy to Azure and then use that file throughout the development lifecycle to repeatedly deploy that infrastructure. Your resources are deployed in a consistent manner.

Bicep provides concise syntax, reliable type safety, and support for reusing code. Bicep offers an optimal authoring experience for your infrastructure-as-code solutions in Azure. To learn about Azure Bicep templates, see [Template deployment overview](/azure/azure-resource-manager/bicep/overview?tabs=bicep).

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Review the template

An Azure Database for PostgreSQL flexible server instance is the parent resource for a distributed database within a region. It provides the scope for management policies that apply to the cluster: firewall, users, roles, and configurations.

Create a _elastic-cluster-template.bicep_ file and copy the following script into it.

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

These resources are defined in the template:

- [Microsoft.DBforPostgreSQL/flexibleServers](/azure/templates/microsoft.dbforpostgresql/flexibleservers?tabs=json&pivots=deployment-language-bicep)

## Deploy the template

Select **Try it** from the following PowerShell code block to open Azure Cloud Shell. 

```azurecli-interactive

az login

$resourceGroupName = Read-Host -Prompt "Enter a name for the new resource group where the server will exist"

az deployment group create `
  --resource-group $resourceGroupName `
  --template-file ./elastic-cluster-template.bicep

```

## Review deployed resources

Follow these steps to verify if your Azure Database for PostgreSQL flexible server elastic cluster was created.

# [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), search for and select **Azure Database for PostgreSQL flexible servers**.
1. In the database list, select your new server to view the **Overview** page to manage your elastic cluster.

# [CLI](#tab/CLI)

You have to enter the name and the resource group of the new elastic cluster to view details about your Azure Database for PostgreSQL flexible server elastic cluster.

```azurecli-interactive

$resourceGroupName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL flexible server cluster exists"
$clusterName = Read-Host -Prompt "Enter your Azure Database for PostgreSQL flexible server elastic cluster name"
az resource show --resource-group $resourcegroupName --name $clusterName --resource-type "Microsoft.DBforPostgreSQL/flexibleServers"

```

---

## Next Steps
Keep this resource group and the elastic cluster if you want to use it to continue with the next suggested steps listed in the [Related content](#related-content) section. The next steps show you how to use elastic clusters with different application sharding models and designs.

## Clean up resources
When you are finished with your elastic cluster environment, you can delete your elastic cluster resource: 

To delete the elastic cluster:

# [Portal](#tab/azure-portal)

In the [portal](https://portal.azure.com), select the elastic cluster you want to delete.

1. From the Overview blade. select **Delete**.
2. Review your resource details, and acknowledge the delete request to confirm the deletion operation by checking the checkbox.
3. Press "Delete".

# [CLI](#tab/azure-cli)

```azurecli-interactive

$resourceGroupName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL flexible server exists"
$clusterName = Read-Host -Prompt "Enter your Azure Database for PostgreSQL flexible server elastic cluster name"
az resource delete --resource-type Microsoft.DBforPostgreSQL/flexibleServers `
--name $clusterName --resource-group $resourceGroupName

```

---

## Related content

- [Design multitenant database with elastic clusters](tutorial-multitenant-database.md).
