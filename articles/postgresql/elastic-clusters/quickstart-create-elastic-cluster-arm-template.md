---
title: "Quickstart: Create elastic clusters with ARM template"
description: In this Quickstart, learn how to create an Azure Database for PostgreSQL flexible server instance with elastic clusters by using an ARM template.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: quickstart
---

# Quickstart: Use an ARM template to create an elastic cluster with Azure Database for PostgreSQL

Azure Database for PostgreSQL with elastic clusters is a managed service that you use to run, manage, and scale highly available PostgreSQL databases in the cloud with a horizontal scale-out capability. You can use an Azure Resource Manager template (ARM template) to create an elastic clusters instance.

[!INCLUDE [About Azure Resource Manager](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-introduction.md)]

Azure Resource Manager is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account. You use management features, like access control, locks, and tags, to secure and organize your resources after deployment. To learn about Azure Resource Manager templates, see [Template deployment overview](/azure/azure-resource-manager/templates/overview).

## Prerequisites

An Azure account with an active subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Review the template

An Azure Database for PostgreSQL flexible server instance is the parent resource for a distributed database within a region. It provides the scope for management policies that apply to the cluster: firewall, users, roles, and configurations.

Create a _elastic-cluster-template.json_ file and copy the following JSON script into it.

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
      "defaultValue": "canadacentral"
    },
    "clusterName": {
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
      "apiVersion": "2025-08-01",
      "location": "[parameters('location')]",
      "name": "[parameters('clusterName')]",
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
          "mode": "[parameters('haEnabled')]"
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
        "[concat('Microsoft.DBforPostgreSQL/flexibleServers/', parameters('clusterName'))]"
      ],
      "properties": {
        "mode": "Incremental",
        "template": {
          "$schema": "http://schema.management.azure.com/schemas/2014-04-01-preview/deploymentTemplate.json#",
          "contentVersion": "1.0.0.0",
          "resources": [
            {
              "type": "Microsoft.DBforPostgreSQL/flexibleServers/firewallRules",
              "name": "[concat(parameters('clusterName'),'/',variables('firewallRules')[copyIndex()].name)]",
              "apiVersion": "2025-08-01",
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

Select **Try it** from the following PowerShell code block to open Azure Cloud Shell.

```azurepowershell-interactive
$clusterName = Read-Host -Prompt "Enter a name for the new Azure Database for PostgreSQL flexible server elastic cluster instance"
$resourceGroupName = Read-Host -Prompt "Enter a name for the new resource group where the elastic cluster will exist"
$adminUser = Read-Host -Prompt "Enter the Azure Database for PostgreSQL flexible server elastic cluster instance's administrator account name"
$adminPassword = Read-Host -Prompt "Enter the administrator password" -AsSecureString
# New-AzResourceGroup -Name $resourceGroupName -Location <AZURE_LOCATION>  Use this command when you need to create a new resource group for your deployment
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
    -TemplateFile "elastic-cluster-template.json" `
    -clusterName $clusterName `
    -administratorLogin $adminUser `
    -administratorLoginPassword $adminPassword

Read-Host -Prompt "Press [ENTER] to continue ..."
```

## Review deployed resources

Follow these steps to verify if your Azure Database for PostgreSQL flexible server elastic cluster was created.

# [Azure portal](#tab/portal)

1. In the [Azure portal](https://portal.azure.com), search for and select **Azure Database for PostgreSQL flexible servers**.
1. In the database list, select your new server to view the **Overview** page to manage your elastic cluster.

# [PowerShell](#tab/PowerShell)

You have to enter the name of the new cluster to view the details of your Azure Database for PostgreSQL flexible server elastic cluster.

```azurepowershell-interactive
$clusterName = Read-Host -Prompt "Enter the name of your Azure Database for PostgreSQL elastic cluster"
Get-AzResource -ResourceType "Microsoft.DBforPostgreSQL/flexibleServers" -Name $clusterName | ft
Write-Host "Press [ENTER] to continue..."
```

# [CLI](#tab/CLI)

You have to enter the name and the resource group of your new elastic cluster to view details about your Azure Database for PostgreSQL flexible server elastic cluster instance.

```azurecli-interactive
echo "Enter your Azure Database for PostgreSQL flexible server elastic cluster name:" &&
read clusterName &&
echo "Enter the resource group where the Azure Database for PostgreSQL flexible server elastic cluster exists:" &&
read resourcegroupName &&
az resource show --resource-group $resourcegroupName --name $clusterName --resource-type "Microsoft.DBforPostgreSQL/flexibleServers"
```

---

## Next Steps
Keep this resource group and the elastic cluster if you want to use it to continue with the next suggested steps listed in the [Related content](#related-content) section. The next steps show you how to use elastic clusters with different application sharding models and designs.

## Clean up resources
When you are finished with your elastic cluster environment, you can delete your elastic cluster resource: 

To delete the elastic cluster:

# [Portal](#tab/azure-portal)

In the [portal](https://portal.azure.com), select the resource group you want to delete.

1. Select **Delete resource group**.
1. To confirm the deletion, type the name of the resource group.

# [PowerShell](#tab/azure-powershell)

```azurepowershell-interactive
$clusterName = Read-Host -Prompt "Enter the resource group where the Azure Database for PostgreSQL flexible server elastic cluster exists"
Remove-AzResourceGroup -Name $clusterName
```

# [CLI](#tab/azure-cli)

```azurecli-interactive
echo "Enter the resource group where the Azure Database for PostgreSQL flexible server elastic cluster exists:" &&
read resourcegroupName &&
az group delete --name $resourcegroupName
```

---

## Related content

- [Design multitenant database with elastic clusters](../configure-maintain/tutorial-multitenant-database.md).
