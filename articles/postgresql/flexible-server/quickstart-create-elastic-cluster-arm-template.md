---
title: "Quickstart: Create Elastic Cluster with ARM template"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL - Flexible Server with Elastic Cluster by using an ARM template.
author: mulander
ms.author: adamwolk
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
---

# Quickstart: Use an ARM template to create an Elastic Cluster with Azure Database for PostgreSQL - Flexible Server instance

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server with Elastic Cluster is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud with horizontal scale-out capability. You can use an Azure Resource Manager template (ARM template) to create an Elastic Cluster instance.

[!INCLUDE [About Azure Resource Manager](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-introduction.md)]

Azure Resource Manager is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account. You use management features, like access control, locks, and tags, to secure and organize your resources after deployment. To learn about Azure Resource Manager templates, see [Template deployment overview](/azure/azure-resource-manager/templates/overview).

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/free/).

## Review the template

An Azure Database for PostgreSQL flexible server instance is the parent resource for a distributed database within a region. It provides the scope for management policies that apply to the cluster: firewall, users, roles, and configurations.

Create a _postgres-flexible-server-template.json_ file and copy the following JSON script into it.

```json
{
  "$schema": "http://schema.management.azure.com/schemas/2014-04-01-preview/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "administratorLogin": {
      "type": "string"
    },
    "administratorLoginPassword": {
      "type": "securestring"
    },
    "location": {
      "type": "string",
      "defaultValue": "eastus"
    },
    "serverName": {
      "type": "string"
    },
    "serverEdition": {
      "type": "string",
      "defaultValue": "GeneralPurpose"
    },
    "storageSizeGB": {
      "type": "int",
      "defaultValue": 64
    },
    "haEnabled": {
      "type": "string",
      "defaultValue": "Disabled"
    },
    "availabilityZone": {
      "type": "string",
      "defaultValue": "1"
    },
    "standbyAvailabilityZone": {
      "type": "string",
      "defaultValue": ""
    },
    "backupRetentionDays": {
      "type": "int",
      "defaultValue": 7
    },
    "skuName": {
      "type": "string",
      "defaultValue": "Standard_D4ds_v5"
    },
    "clusterSize": {
      "type": "int",
      "defaultValue": 2
    },
    "guid": {
      "type": "string",
      "defaultValue": "[newGuid()]"
    },
    "firewallRules": {
      "type": "object",
      "defaultValue": {
        "rules": [
          {
            "name": "ClientIP",
            "startIPAddress": "131.107.1.255",
            "endIPAddress": "131.107.1.255"
          },
          {
            "name": "AllowAll",
            "startIPAddress": "0.0.0.0",
            "endIPAddress": "255.255.255.255"
          }
        ]
      }
    },
    "network": {
      "type": "object",
      "defaultValue": { "publicNetworkAccess": "Enabled" }
    }
  },
  "variables": {
    "firewallRules": "[parameters('firewallRules').rules]"
  },
  "resources": [
    {
      "apiVersion": "2024-05-01-privatepreview",
      "location": "[parameters('location')]",
      "name": "[parameters('serverName')]",
      "properties": {
        "createMode": "Default",
        "version": "16",
        "administratorLogin": "[parameters('administratorLogin')]",
        "administratorLoginPassword": "[parameters('administratorLoginPassword')]",
        "availabilityZone": "[parameters('availabilityZone')]",
        "Storage": {
          "StorageSizeGB": "[parameters('storageSizeGB')]",
          "Autogrow": "Disabled"
        },
        "Network": "[if(empty(parameters('network')), json('null'), parameters('network'))]",
        "Backup": {
          "backupRetentionDays": "[parameters('backupRetentionDays')]",
          "geoRedundantBackup": "Disabled"
        },
        "highAvailability": {
          "mode": "[parameters('haEnabled')]",
          "standbyAvailabilityZone": "[parameters('standbyAvailabilityZone')]"
        },
        "cluster": {
          "clusterSize": "[parameters('clusterSize')]"
        }
      },
      "sku": {
        "name": "[parameters('skuName')]",
        "tier": "[parameters('serverEdition')]"
      },
      "type": "Microsoft.DBforPostgreSQL/flexibleServers"
    },
    {
      "condition": "[greater(length(variables('firewallRules')), 0)]",
      "type": "Microsoft.Resources/deployments",
      "apiVersion": "2019-08-01",
      "name": "[concat('firewallRules-', parameters('guid'), '-', copyIndex())]",
      "copy": {
        "count": "[if(greater(length(variables('firewallRules')), 0), length(variables('firewallRules')), 1)]",
        "mode": "Serial",
        "name": "firewallRulesIterator"
      },
      "dependsOn": [
        "[concat('Microsoft.DBforPostgreSQL/flexibleServers/', parameters('serverName'))]"
      ],
      "properties": {
        "mode": "Incremental",
        "template": {
          "$schema": "http://schema.management.azure.com/schemas/2014-04-01-preview/deploymentTemplate.json#",
          "contentVersion": "1.0.0.0",
          "resources": [
            {
              "type": "Microsoft.DBforPostgreSQL/flexibleServers/firewallRules",
              "name": "[concat(parameters('serverName'),'/',variables('firewallRules')[copyIndex()].name)]",
              "apiVersion": "2024-05-01-privatepreview",
              "properties": {
                "StartIpAddress": "[variables('firewallRules')[copyIndex()].startIPAddress]",
                "EndIpAddress": "[variables('firewallRules')[copyIndex()].endIPAddress]"
              }
            }
          ]
        }
      }
    }
  ]
}
```

These resources are defined in the template:

- [Microsoft.DBforPostgreSQL/flexibleServers](/azure/templates/microsoft.dbforpostgresql/flexibleservers?tabs=json)

## Deploy the template

Select **Try it** from the following PowerShell code block to open Azure Cloud Shell. The clusterSize parameter defines how many nodes your Elastic Cluster has.

```azurepowershell-interactive
$serverName = Read-Host -Prompt "Enter a name for the new Azure Database for PostgreSQL flexible server instance"
$resourceGroupName = Read-Host -Prompt "Enter a name for the new resource group where the server will exist"
$location = Read-Host -Prompt "Enter an Azure region (for example, centralus) for the resource group"
$adminUser = Read-Host -Prompt "Enter the Azure Database for PostgreSQL flexible server instance's administrator account name"
$adminPassword = Read-Host -Prompt "Enter the administrator password" -AsSecureString
$clusterSize = Read-Host -Prompt "Enter the desired cluster size"

New-AzResourceGroup -Name $resourceGroupName -Location $location # Use this command when you need to create a new resource group for your deployment
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName -clusterSize $clusterSize`
    -TemplateFile "postgres-flexible-server-template.json" `
    -serverName $serverName `
    -administratorLogin $adminUser `
    -administratorLoginPassword $adminPassword

Read-Host -Prompt "Press [ENTER] to continue ..."
```

## Review deployed resources

Follow these steps to verify if your server was created in Azure.

# [Azure portal](#tab/portal)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

1. In the [Azure portal](https://portal.azure.com), search for and select **Azure Database for PostgreSQL Flexible Servers**.
1. In the database list, select your new server to view the **Overview** page to manage the server.

# [PowerShell](#tab/PowerShell)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You have to enter the name of the new server to view the details of your Azure Database for PostgreSQL flexible server instance.

```azurepowershell-interactive
$serverName = Read-Host -Prompt "Enter the name of your Azure Database for PostgreSQL server"
Get-AzResource -ResourceType "Microsoft.DBforPostgreSQL/flexibleServers" -Name $serverName | ft
Write-Host "Press [ENTER] to continue..."
```

# [CLI](#tab/CLI)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You have to enter the name and the resource group of the new server to view details about your Azure Database for PostgreSQL flexible server instance.

```azurecli-interactive
echo "Enter your Azure Database for PostgreSQL flexible server instance name:" &&
read serverName &&
echo "Enter the resource group where the Azure Database for PostgreSQL flexible server instance exists:" &&
read resourcegroupName &&
az resource show --resource-group $resourcegroupName --name $serverName --resource-type "Microsoft.DBforPostgreSQL/flexibleServers"
```

---

## Clean up resources

Keep this resource group and the Elastic Cluster just created if you want to use it to continue with the next suggested steps listed in the [Related content](#related-content) section. The next steps show you how to use Elastic Clusters with different application sharding models and designs.

To delete the resource group:

# [Portal](#tab/azure-portal)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In the [portal](https://portal.azure.com), select the resource group you want to delete.

1. Select **Delete resource group**.
1. To confirm the deletion, type the name of the resource group.

# [PowerShell](#tab/azure-powershell)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

```azurepowershell-interactive
$serverName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL Flexible Server exists:"
Remove-AzResourceGroup -Name $serverName
```

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

```azurecli-interactive
echo "Enter the resource group where the Azure Database for PostgreSQL Flexible Server exists:" &&
read resourcegroupName &&
az group delete --name $resourcegroupName
```

---

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Design multitenant database with Elastic Cluster](tutorial-multitenant-database.md).
