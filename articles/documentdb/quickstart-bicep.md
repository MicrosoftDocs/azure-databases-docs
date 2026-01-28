---
title: |
  Quickstart: Deploy a Cluster Using Bicep
description: Learn how to deploy an Azure DocumentDB cluster using Bicep to store databases, collections, and documents. Follow this quickstart for step-by-step guidance.
author: gahl-levy
ms.author: gahllevy
ms.topic: quickstart
ms.date: 09/30/2025
ms.custom:
  - sfi-ropc-nochange
---

# Quickstart: Deploy an Azure DocumentDB cluster using Bicep

In this quickstart, you deploy a new Azure DocumentDB cluster using Bicep. This quickstart provides step-by-step instructions to help you get started quickly. This cluster contains all your MongoDB resources: databases, collections, and documents. It provides a unique endpoint for tools and software development kits (SDKs) to connect to Azure DocumentDB and perform operations.

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prerequisite-azure-subscription.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Configure environment

[!INCLUDE[Section - Configure Azure CLI environment](includes/section-azure-cli-environment.md)]

## Prepare the Bicep template

Create and configure a Bicep file to define the resources required for deploying an Azure DocumentDB cluster.

1. Create a new *main.bicep* file in your project directory.

1. Add this template to the file's content.

    ```bicep
    @description('Cluster name')
    @minLength(8)
    @maxLength(40)
    param clusterName string = 'msdocs-${uniqueString(resourceGroup().id)}'
    
    @description('Location for the cluster.')
    param location string = resourceGroup().location
    
    @description('Username for admin user')
    param adminUsername string
    
    @secure()
    @description('Password for admin user')
    @minLength(8)
    @maxLength(128)
    param adminPassword string
    
    resource cluster 'Microsoft.DocumentDB/mongoClusters@2025-09-01' = {
      name: clusterName
      location: location
      properties: {
        administrator: {
          userName: adminUsername
          password: adminPassword
        }
        serverVersion: '8.0'
        sharding: {
          shardCount: 1
        }
        storage: {
          sizeGb: 32
        }
        highAvailability: {
          targetMode: 'Disabled'
        }
        compute: {
          tier: 'M10'
        }
      }
    }
    
    resource firewallRules 'Microsoft.DocumentDB/mongoClusters/firewallRules@2025-09-01' = {
      parent: cluster
      name: 'AllowAllAzureServices'
      properties: {
        startIpAddress: '0.0.0.0'
        endIpAddress: '0.0.0.0'
      }
    }
    ```

    > [!TIP]
    > For more information on options using the `Microsoft.DocumentDB/mongoclusters` resource, see [`Microsoft.DocumentDB/mongoclusters` documentation](/azure/templates/microsoft.documentdb/mongoclusters).
    >

## Deploy the template

Deploy the template created in the previous step using an Azure Resource Manager deployment.

1. Use the [`az group create`](/cli/azure/group#az-group-create) command to create a new resource group in your subscription.

    ```azurecli
    az group create \
        --name "<resource-group-name>" \
        --location "<location>"
    ```

1. Use [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create) to deploy the bicep template. You're then prompted to enter a value for the `adminUsername` and `adminPassword` parameters.

    ```azurecli
    az deployment group create \
        --resource-group "<resource-group-name>" \
        --template-file 'main.bicep'
    ```

    > [!TIP]
    > Alternatively, use the ``--parameters`` option to pass in a parameters file with predefined values.
    >
    > ```azurecli
    > az deployment group create \
    >     --resource-group "<resource-group-name>" \
    >     --template-file 'main.bicep' \
    >     --parameters @main.parameters.json
    > ```
    >
    > This example JSON file injects `clusteradmin` and `P@ssw.rd` values for the `adminUsername` and `adminPassword` parameters respectively.
    >
    > ```json
    > {
    >   "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    >   "contentVersion": "1.0.0.0",
    >   "parameters": {
    >     "adminUsername": {
    >       "value": "clusteradmin"
    >     },
    >     "adminPassword": {
    >       "value": "P@ssw.rd"
    >     }
    >   }
    > }
    > ```
    >

1. Wait for the deployment operation to complete before moving on.

## Review deployed resources

[!INCLUDE[Section - Azure CLI list resources](includes/section-azure-cli-list-resources.md)]

## Clean up resources

When you're done with your Azure DocumentDB cluster, you can delete the Azure resources you created so you don't incur more charges.

1. Use [`az group delete`](/cli/azure/group#az-group-delete) to remove the resource group from your subscription.

    ```azurecli
    az group delete \
        --name "<resource-group-name>" \
        --yes \
        --no-wait
    ```
    
    > [!IMPORTANT]
    > Ensure you no longer need the resources before running this command, as it permanently deletes them.

## Related content

- [Connect from MongoDB Shell](how-to-connect-mongo-shell.md)
- [Connect from Azure Cloud Shell](how-to-connect-cloud-shell.md)
- [Migrate data to Azure DocumentDB](migration-options.md)
