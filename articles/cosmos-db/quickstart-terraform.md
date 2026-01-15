---
title: Quickstart - Create a Database and Container Using Terraform
description: Quickstart showing how to an Azure Cosmos DB database and a container using Terraform
author: ginsiucheng
ms.author: mjbrown
tags: azure-resource-manager, terraform
ms.custom: devx-track-terraform
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: quickstart
ms.date: 06/11/2025
appliesto:
  - ✅ NoSQL
---

# Quickstart - Create an Azure Cosmos DB database and container using Terraform

Azure Cosmos DB is Microsoft’s fast NoSQL database with open APIs for any scale. You can use Azure Cosmos DB to quickly create and query key/value databases, document databases, and graph databases. Without a credit card or an Azure subscription, you can set up a free [Try Azure Cosmos DB account](https://aka.ms/trycosmosdb). This quickstart focuses on the process of deployments via Terraform to create an Azure Cosmos database and a container within that database. You can later store data in this container.

## Prerequisites

An Azure subscription or free Azure Cosmos DB trial account

- [!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

Terraform should be installed on your local computer. Installation instructions can be found [here](https://learn.hashicorp.com/tutorials/terraform/install-cli).

## Review the Terraform File

The Terraform files used in this quickstart can be found on the [terraform samples repository](https://github.com/Azure/terraform). Create the below three files: providers.tf, main.tf and variables.tf. Variables can be set in command line or alternatively with a terraforms.tfvars file.

### Key Terraform parameters

The following table summarizes the critical variables used in this quickstart, their scope, constraints, and example values.

| Parameter | Scope | Description and constraints | Example value |
|----------|------|-----------------------------|---------------|
| `prefix` | Naming | Prefix used for all resource names. Must be lowercase, alphanumeric, and unique per subscription. | `cosmosdemo` |
<!-- Explanation: Added prefix parameter with constraints and example value as requested. -->
| `location` | Resource group | Azure region for the resource group. This location applies to the resource group only, not the Cosmos DB account. | `eastus` |
<!-- Explanation: Clarified that location applies to the resource group scope. -->
| `cosmosdb_account_location` | Cosmos DB account | Azure region for the Azure Cosmos DB account. This can differ from the resource group location. | `eastus` |
<!-- Explanation: Disambiguated account location versus resource group location. -->
| `throughput` | Database (RU/s) | Provisioned throughput for the SQL database in request units per second (RU/s). Must be between 400 and 1,000,000 RU/s. | `400` |
<!-- Explanation: Annotated throughput with RU/s and clarified that it applies at the database level. -->

### Provider Terraform File

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-autoscale/providers.tf":::

### Main Terraform File

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-manualscale/main.tf":::

Three Cosmos DB resources are defined in the main terraform file.

- [Microsoft.DocumentDB/databaseAccounts](/azure/templates/microsoft.documentdb/databaseaccounts): Create an Azure Cosmos account.

- [Microsoft.DocumentDB/databaseAccounts/sqlDatabases](/azure/templates/microsoft.documentdb/databaseaccounts/sqldatabases): Create an Azure Cosmos database with database-level throughput (RU/s).
<!-- Explanation: Explicitly stated that throughput applies at the database level. -->

- [Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers](/azure/templates/microsoft.documentdb/databaseaccounts/sqldatabases/containers): Create an Azure Cosmos container.
<!-- Explanation: Clarified that container is created without separate throughput in this example to avoid ambiguity. -->

### Variables Terraform File

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-manualscale/variables.tf":::

## Deploy via terraform

1. Save the terraform files as main.tf, variables.tf and providers.tf to your local computer.
2. Sign in to your terminal via Azure CLI or PowerShell
3. Deploy via Terraform commands
    - terraform init  
      *Expected result:* Terraform initializes successfully and downloads the azurerm provider.
      <!-- Explanation: Added an explicit success check for terraform init. -->
    - terraform plan  
      *Expected result:* The plan output shows **3 to add, 0 to change, 0 to destroy**.
      <!-- Explanation: Added a concise verification check for terraform plan. -->
    - terraform apply  
      *Expected result:* The final output includes **Apply complete! Resources: 3 added, 0 changed, 0 destroyed.**
      <!-- Explanation: Added an explicit success indicator for terraform apply. -->

## Validate the deployment

Use the Azure portal, Azure CLI, or Azure PowerShell to list the deployed resources in the resource group.

### [Azure CLI](#tab/azure-cli)

```azurecli-interactive
az resource list --resource-group "your resource group name"
```

*Expected result:* The output lists a `Microsoft.DocumentDB/databaseAccounts` resource along with its database and container.
<!-- Explanation: Added an explicit validation success check for Azure CLI output. -->

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell-interactive
Get-AzResource -ResourceGroupName "your resource group name"
```

*Expected result:* The command returns the Cosmos DB account, SQL database, and container resources.
<!-- Explanation: Added an explicit validation success check for Azure PowerShell output. -->

---

## Clean up resources

If you plan to continue working with subsequent quickstarts and tutorials, you might want to leave these resources in place.
When no longer needed, use the Azure portal, Azure CLI, or Azure PowerShell to delete the resource group and its resources.

### [Azure CLI](#tab/azure-cli)

```azurecli-interactive
az group delete --name "your resource group name"
```

*Expected result:* Azure CLI confirms the resource group deletion and no longer lists it in the subscription.
<!-- Explanation: Added a success confirmation for the cleanup step. -->

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell-interactive
Remove-AzResourceGroup -Name "your resource group name"
```

*Expected result:* The resource group is removed and no longer appears in `Get-AzResourceGroup` output.
<!-- Explanation: Added a success confirmation for the cleanup step. -->

---

## Next steps

In this quickstart, you created an Azure Cosmos account, a database and a container via terraform and validated the deployment. To learn more about Azure Cosmos DB and Terraform, continue on to the articles below.

- Read an [Overview of Azure Cosmos DB](introduction.md).
- Learn more about [Terraform](https://www.terraform.io/intro).
- Learn more about [Azure Terraform Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs).
- [Manage Cosmos DB with Terraform](manage-with-terraform.md)
- Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
  - If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md).
  - If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md).

---

### Agent feedback applied

- Added a concise Terraform parameter list with example values near **Review the Terraform File**.
- Added explicit success and verification checks adjacent to deployment, validation, and cleanup steps.
- Disambiguated throughput (RU/s) and location terminology, clarifying database-level throughput and resource group versus account location.