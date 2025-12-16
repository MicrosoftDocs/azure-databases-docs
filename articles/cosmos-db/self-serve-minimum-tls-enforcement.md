---
title: Self-Serve Minimum TLS Version Enforcement
titleSuffix: Azure Cosmos DB
description: Learn how to use self-serve minimum TLS version enforcement for your Azure Cosmos DB account to improve your security posture.
author: sudhanshukhera
ms.author: skhera
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 07/23/2025
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Self-serve minimum TLS version enforcement in Azure Cosmos DB

This article discusses how to enforce a minimum version of the Transport Layer Security (TLS) protocol for your Cosmos DB account, using a self-service API.

## How minimum TLS version enforcement works in Azure Cosmos DB

The multitenant nature of Cosmos DB requires the service to meet the access and security needs of every user. To achieve this, Cosmos DB enforces minimum TLS protocols at the *application layer*, and not at lower layers in the network stack where TLS operates. This enforcement occurs on any authenticated request to a specific database account, according to the settings set on that account by the customer.

The *minimum service-wide accepted version is TLS 1.2*. This selection can be changed on a per-account basis, as discussed in the following section. 

## How to set the minimum TLS version for my Cosmos DB database account

Starting with version 2022-11-15 of the Azure Cosmos DB Resource Provider API, a new property is exposed for every Cosmos DB database account, called `minimalTlsVersion`. It accepts the following value:
- `Tls12` for setting the minimum version to TLS 1.2

The *default value for new accounts* is `Tls12`.

> [!IMPORTANT]
> **Starting August 31, 2025, all Cosmos DB database accounts must use Transport Layer Security (TLS) 1.2 or higher**, as [support for TLS 1.0 and 1.1 is retired](https://azure.microsoft.com/updates?id=update-retirement-tls1-0-tls1-1-versions-azure-services).
>
> Effective **March 31, 2025, support for TLS 1.3** is enabled for Azure Cosmos DB.

### Set minimum TLS protocol using the Azure portal

This self-serve feature is available in the Azure portal while creating and editing an account. Azure Cosmos DB accounts enforce the TLS 1.2 protocol. However, Azure Cosmos DB also supports the following TLS protocols depending on the API kind selected.

- **MongoDB:** TLS 1.2
- **Cassandra:** TLS 1.2
- **Table, SQL and Graph:** TLS 1.2

### Steps to set minimum TLS protocol while creating an account

If you're using an API Kind that only supports TLS 1.2, you'll notice in the **Networking** tab that the TLS protocol disabled.

:::image type="content" source="media/self-serve-minimum-tls-enforcement/tls-create-account.png" alt-text="Screenshot of API Kind that only supports TLS 1 point 2." lightbox="media/self-serve-minimum-tls-enforcement/tls-create-account.png":::

If you're using an API Kind that accepts multiple TLS protocols, then you can navigate to the **Networking** tab and the **Minimum Transport Layer Security Protocol** option is available. You can change the selected protocol by just clicking on the dropdown and selecting the desired protocol.

:::image type="content" source="media/self-serve-minimum-tls-enforcement/tls-select-account.png" alt-text="Screenshot of API Kind that accepts multiple TLS protocols." lightbox="media/self-serve-minimum-tls-enforcement/tls-select-account.png":::

After setting up your account, you can review in the **Review + create** tab, under **Networking**, that the selected TLS Protocol is set as you specified.

:::image type="content" source="media/self-serve-minimum-tls-enforcement/summary.png" alt-text="Screenshot of selected TLS Protocol is set as you specified.":::

### Steps to set the minimum TLS protocol while editing an account

1. Navigate to your Azure Cosmos DB account on the Azure portal.

1. Select **Networking** from the sidebar menu, then select the **Connectivity** tab.

1. You'll find the **Minimum Transport Layer Security Protocol** option. If you're using an API Kind that only supports TLS 1.2, you'll notice this option disabled. Otherwise, you can select the desired TLS Protocol by just clicking on it.

    :::image type="content" source="media/self-serve-minimum-tls-enforcement/edit.png" alt-text="Screenshot of minimum transport layer security protocol option.":::

1. Select **Save** once you changed the TLS protocol.

    :::image type="content" source="media/self-serve-minimum-tls-enforcement/save.png" alt-text="Screenshot of save after change.":::

1. Once it's saved, you'll receive a success notification. Still, this change can take up to 15 minutes to take effect after the configuration update is completed.

    :::image type="content" source="media/self-serve-minimum-tls-enforcement/notification-success.png" alt-text="Screenshot of success notification.":::

### Set via Azure CLI

To set using Azure CLI, use the command:

```azurecli-interactive
rg="myresourcegroup"
dbName="mycosmosdbaccount"
minimalTlsVersion="Tls12"
az cosmosdb update -n $dbName -g $rg --minimal-tls-version $minimalTlsVersion
```

### Set via Azure PowerShell

To set using Azure PowerShell, use the command:

```azurepowershell-interactive
$minimalTlsVersion = "Tls12"
Update-AzCosmosDBAccount -ResourceGroupName myresourcegroup -Name mycosmosdbaccount -MinimalTlsVersion $minimalTlsVersion
```

### Set via ARM template

To set this property using an ARM template, update your existing template or export a new template for your current deployment, then add `"minimalTlsVersion"` to the properties for the `databaseAccounts` resources, with the desired minimum TLS version value. The following example shows a basic Azure Resource Manager template with this property setting, using a parameter.

```json
{
    {
      "type": "Microsoft.DocumentDB/databaseAccounts",
      "name": "mycosmosdbaccount",
      "apiVersion": "2022-11-15",
      "location": "[parameters('location')]",
      "kind": "GlobalDocumentDB",
      "properties": {
        "consistencyPolicy": {
          "defaultConsistencyLevel": "[parameters('defaultConsistencyLevel')]",
          "maxStalenessPrefix": 1,
          "maxIntervalInSeconds": 5
        },
        "locations": [
          {
            "locationName": "[parameters('location')]",
            "failoverPriority": 0
          }
        ],
        "locations": "[variable('locations')]",
        "databaseAccountOfferType": "Standard",
        "minimalTlsVersion": "[parameters('minimalTlsVersion')]",
      }
    }
}
```

> [!IMPORTANT]
> Make sure you include the other properties for your account and child resources when redeploying with this property. Don't deploy this template as is or it will reset all of your account properties.

### For new accounts

You can create accounts with the `minimalTlsVersion` property set by using the preceding ARM template, or by using Azure CLI or Azure PowerShell:

```azurecli-interactive
az cosmosdb create --name <CosmosDBAccountName> \
  --resource-group <ResourceGroupName> \
  --kind GlobalDocumentDB \
  --locations regionName=<Region> \
  --minimal-tls-version "Tls12"
```

```azurepowershell-interactive
New-AzCosmosDBAccount `
  -ResourceGroupName "<YourResourceGroupName>" `
  -Name "<YourCosmosDBAccountName>" `
  -Location "<AzureRegion>" `
  -Kind GlobalDocumentDB `
  -EnableAutomaticFailover $true `
  -MinimalTlsVersion "Tls12"
```

## How to verify minimum TLS version enforcement

Because Cosmos DB enforces the minimum TLS version at the application layer, conventional TLS scanners that check whether handshakes are accepted by the service for a specific TLS version are unreliable to test enforcement in Cosmos DB. To verify enforcement, refer to the [official open-source cosmos-tls-scanner tool](https://github.com/Azure/cosmos-tls-scanner/).

You can also get the current value of the `minimalTlsVersion` property by using Azure CLI or Azure PowerShell.

### Get current value via Azure CLI

To get the current value of the property using Azure CLI, run the command:

```azurecli-interactive
subId=$(az account show --query id -o tsv)
rg="myresourcegroup"
dbName="mycosmosdbaccount"
az rest --uri "/subscriptions/$subId/resourceGroups/$rg/providers/Microsoft.DocumentDB/databaseAccounts/$dbName?api-version=2022-11-15" --method GET
```

### Get current value via Azure PowerShell

To get the current value of the property using Azure PowerShell, run the command:

```azurepowershell-interactive
Get-AzCosmosDBAccount -ResourceGroupName myresourcegroup -Name mycosmosdbaccount
```

## Related content

- [Prepare for upcoming TLS 1.3 support for Azure Cosmos DB](./tls-support.md)
- [Moving to TLS 1.2 for Azure Cosmos DB](https://aka.ms/tls12)
