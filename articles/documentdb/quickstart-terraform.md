---
title: |
  Quickstart: Deploy a Cluster Using Terraform
description: Learn how to deploy an Azure DocumentDB cluster using Terraform to store databases, collections, and documents. Follow this quickstart for step-by-step guidance.
author: gahl-levy
ms.author: gahllevy
ms.topic: quickstart
ms.date: 09/30/2025
ms.custom:
  - sfi-ropc-nochange
---

# Quickstart: Deploy an Azure DocumentDB cluster using Terraform

In this quickstart, you deploy a new Azure DocumentDB cluster using Terraform. This quickstart provides step-by-step instructions to help you get started quickly. This cluster contains all your MongoDB resources: databases, collections, and documents. It provides a unique endpoint for tools and software development kits (SDKs) to connect to Azure DocumentDB and perform operations.

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prerequisite-azure-subscription.md)]

- [Terraform 1.2.0](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli) or later.

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Configure environment

[!INCLUDE[Section - Configure Azure CLI environment](includes/section-azure-cli-environment.md)]

## Prepare the Terraform configuration

Create and configure a Terraform file to define the resources required for deploying an Azure DocumentDB cluster.

1. Create a new *main.tf* file in your project directory.

1. Add this configuration to the file's content.

    ```terraform
    variable "admin_username" {
      type = string
      description = "Username for default administrator account"
    }
    
    variable "admin_password" {
      type = string
      description = "Password for default administrator account"
      sensitive = true
    }
    
    terraform {
      required_providers {
        azurerm = {
          source = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }
    
    provider "azurerm" {
      features { }
    }
    
    resource "azurerm_resource_group" "resource_group" {
      name     = "example-resource-group"
      location = "West US"
    }
    
    resource "azurerm_mongo_cluster" "cluster" {
      name                   = "example-mongo-cluster"
      resource_group_name    = azurerm_resource_group.resource_group.name
      location               = azurerm_resource_group.resource_group.location
      administrator_username = var.admin_username
      administrator_password = var.admin_password
      shard_count            = "1"
      compute_tier           = "M10"
      high_availability_mode = "Disabled"
      storage_size_in_gb     = "32"
      version                = "8.0"
    }
    ```
    
    > [!TIP]
    > For more information on options using the `azurerm_mongo_cluster` resource, see [`azurerm` provider documentation in Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mongo_cluster#arguments-reference).

## Deploy the configuration

Deploy the configuration file created in the previous step using an execution plan.

1. Initialize the Terraform deployment with Terraform CLI.

    ```azurecli-interactive
    terraform init --upgrade
    ```

1. Create an execution plan, and save it to a file named *main.tfplan*. Provide values when prompted for the `admin_username` and `admin_password` variables.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --out "main.tfplan"
    ```

    > [!NOTE]
    > This command sets the `ARM_SUBSCRIPTION_ID` environment variable temporarily. This setting is required for the `azurerm` provider starting with version 4.0 For more information, see [subscription ID in `azurerm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.0.0/docs/guides/4.0-upgrade-guide#specifying-subscription-id-is-now-mandatory).

1. Apply the execution plan to deploy resources to Azure.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "main.tfplan"
    ```

1. Wait for the deployment operation to complete before moving on.

## Review deployed resources

[!INCLUDE[Section - Azure CLI list resources](includes/section-azure-cli-list-resources.md)]

## Clean up resources

Remove all the resources defined in your Terraform configuration.

1. Destroy your resources managed by Terraform using the `destroy` command.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform destroy
    ```

    > [!TIP]
    > Alternatively, use [`az group delete`](/cli/azure/group#az-group-delete) to remove the resource group from your subscription:
    >
    > ```azurecli
    > az group delete \
    >     --name "<resource-group-name>" \
    >     --yes \
    >     --no-wait
    > ```
    >

    > [!IMPORTANT]
    > Ensure you no longer need the resources before running this command, as it permanently deletes them.

1. Confirm any relevant prompts to proceed with the deletion.

## Related content

- [Connect from MongoDB shell](how-to-connect-mongo-shell.md)
- [Connect from Azure cloud shell](how-to-connect-cloud-shell.md)
- [Migrate data to Azure DocumentDB](migration-options.md)
