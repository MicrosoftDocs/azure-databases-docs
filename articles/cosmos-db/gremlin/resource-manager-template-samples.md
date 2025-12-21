---
title: Resource Manager templates for Azure Cosmos DB for Gremlin
description: Use Azure Resource Manager templates to create and configure Azure Cosmos DB for Gremlin.
author: manishmsfte
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.custom: devx-track-arm-template
ms.topic: how-to
ms.date: 10/14/2020
ms.author: mansha
---

# Manage Azure Cosmos DB for Gremlin resources using Azure Resource Manager templates

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

In this article, you learn how to use Azure Resource Manager templates to help deploy and manage your Azure Cosmos DB accounts, databases, and graphs.

This article has examples for API for Gremlin accounts only, to find examples for other API type accounts see: use Azure Resource Manager templates with Azure Cosmos DB's API for [Cassandra](../cassandra/templates-samples.md), [NoSQL](../samples-resource-manager-templates.md), [MongoDB](../mongodb/resource-manager-template-samples.md), [Table](../table/resource-manager-templates.md) articles.

> [!IMPORTANT]
>
> * Account names are limited to 44 characters, all lowercase.
> * To change the throughput values, redeploy the template with updated RU/s.
> * When you add or remove locations to an Azure Cosmos DB account, you can't simultaneously modify other properties. These operations must be done separately.

To create any of the Azure Cosmos DB resources below, copy the following example template into a new json file. You can optionally create a parameters json file to use when deploying multiple instances of the same resource with different names and values. There are many ways to deploy Azure Resource Manager templates including, [Azure portal](/azure/azure-resource-manager/templates/deploy-portal), [Azure CLI](/azure/azure-resource-manager/templates/deploy-cli), [Azure PowerShell](/azure/azure-resource-manager/templates/deploy-powershell) and [GitHub](/azure/azure-resource-manager/templates/deploy-to-azure-button).

<a id="create-autoscale"></a>

## Azure Cosmos DB account for Gremlin with autoscale provisioned throughput

This template will create an Azure Cosmos DB account for API for Gremlin with a database and graph with autoscale throughput. This template is also available for one-click deploy from Azure Quickstart Templates Gallery.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/template-deployments/deploy-to-azure-button.svg" alt-text="Button to deploy the Resource Manager template to Azure." border="false" link="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.documentdb%2Fcosmosdb-gremlin-autoscale%2Fazuredeploy.json":::

:::code language="json" source="~/quickstart-templates/quickstarts/microsoft.documentdb/cosmosdb-gremlin-autoscale/azuredeploy.json":::
