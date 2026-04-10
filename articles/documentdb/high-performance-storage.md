---
title: Premium SSD v2 - High Performance Storage
description: Learn how to use Premium SSD v2 high performance storage in Azure DocumentDB for higher IOPS and bandwidth.
author: suvishodcitus
ms.author: suvishod
ms.topic: feature-guide
ms.date: 04/13/2026
ms.custom:
  - references_regions
zone_pivot_groups: azure-interface-portal-rest-bicep-terraform
ai-usage: ai-assisted
---

# High performance storage in Azure DocumentDB

Azure DocumentDB high uses **Premium SSD v2** disks to deliver high performance storage for I/O-intensive workloads by de-coupling storage capacity from IOPS and bandwidth.

With Premium SSD v2 storage on Azure DocumentDB, the maximum configurable IOPS and bandwidth settings are available by default. The capacity of the Compute tier determines the achievable IOPS and and bandwidth regardless of the size of the storage disk. 

Only the required storage capacity needs to be selected, while IOPS and bandwidth settings are auto configured at no added cost.

Previously, more IOPS meant scaling up storage capacity. For instance, a jump from 5,000 IOPS to 20,000 IOPS required scaling storage capacity from 1TB to 20TB, even in the absence of higher storage needs. With Premium SSD v2, 20,000 IOPS can be achieved on the same 1TB disk so long as the compute tier has the capacity. Larger Compute tiers can support up to 80,000 IOPS - a 4x increase over previous limits.  

## Guidance

The **maximum storage performance** for your Azure DocumentDB cluster depends on the combination of **compute tier** and **storage size** you select. Each combination determines the effective limits for **IOPS** and **throughput**. Start by choosing the storage size you need, then select a compute tier that provides the required Input/output operations per second (IOPS) and throughput for your workload. If you’re unsure about performance requirements:

- Begin with the compute tier that fully unlocks the storage performance for your selected size.

- Run workload benchmarks.

- Gradually reduce compute until you find the smallest tier that delivers your desired performance.

## IOPS and throughput caps

This table lists the highest achievable IOPS and bandwidth configurations per compute cluster tier. Premium SSD v2 disks, regardless of storage capacity, will be auto configured with the upper bound values tabulated below, at no added cost.

### `2` vCores (M30)

| Compute Tier | Max IOPS | Max bandwidth (MBps) |
| M30 (2 core) | 3,750 | 85 |
| M40 (4 core) | 6,400 | 145 |
| M50 (8 core) | 12,800 | 290 |
| M60 (16 core) | 25,600 | 600 |
| M80 (32 core) | 51,200 | 865 |
| M200 (64 core) | 80,000 | 1,200 |


## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

::: zone pivot="rest-api,azure-resource-manager-bicep"

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

::: zone-end

::: zone pivot="azure-portal"

::: zone-end

::: zone pivot="azure-terraform"

- [Terraform 1.2.0](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli) or later.

::: zone-end

## Create a cluster with high performance storage

Configure a cluster using **Premium SSD v2** (high performance) storage as part of the cluster creation step.

::: zone pivot="azure-portal"

1. Sign in to the **Azure portal** (<https://portal.azure.com>).

1. From the Azure portal menu or the **Home page**, select **Create a resource**.

1. On the **New** page, search for and select **Azure DocumentDB**.

    :::image type="content" source="media/high-performance-storage/select-azure-documentdb.png" alt-text="Screenshot of the Azure portal search feature to locate Azure DocumentDB.":::

1. On the **Create Azure DocumentDB cluster** page and within the **Basics** section, select the **Configure** option within the **Cluster tier** section.

    :::image type="content" source="media/high-performance-storage/select-configure-option.png" alt-text="Screenshot of the options available to configure an Azure DocumentDB cluster.":::

1. On the **Configure** page, choose the cluster tier and storage size as required. Select the storage type as **Premium SSD v2** to enable high-performance storage, then select Save to apply the changes.

    :::image type="content" source="media/high-performance-storage/enable-premium-storage.png" alt-text="Screenshot of the configuration option specific to premium SSD v2 disks in Azure DocumentDB.":::

1. Fill in the remaining details and then select **Review + create**.

1. Review the settings you provide, and then select **Create**. It takes a few minutes to create the cluster. Wait for the resource deployment is complete.

1. Finally, select **Go to resource** to navigate to the Azure DocumentDB cluster in the portal.

:::image type="content" source="media/high-performance-storage/go-to-resource.png" alt-text="Screenshot of the deployment completion step with an option to navigate to the new Azure DocumentDB cluster.":::

::: zone-end

::: zone pivot="azure-resource-manager-bicep"

1. Open a new terminal.

1. Sign in to Azure CLI.

1. Create a new Bicep file to define your role definition. Name the file *main.bicep*.

1. Add this template to the file's content. Replace the `<cluster-name>`, `<location>`, `<username>`, and `<password>` placeholders with appropriate values.

    ```bicep
    resource cluster 'Microsoft.DocumentDB/mongoClusters@2025-08-01-preview' = {
      name: '<cluster-name>'
      location: '<location>'
      properties: {
        administrator: {
          userName: '<username>'
          password: '<password>'
        }
        serverVersion: '8.0'
        storage: {
          sizeGb: 32
          type: 'PremiumSSDv2'
        }
        compute: {
          tier: 'M30'
        }
        sharding: {
          shardCount: 1
        }
        highAvailability: {
          targetMode: 'Disabled'
        }
      }
    }
    ```

1. Deploy the Bicep template using [`az deployment group create`](/cli/azure/deployment/group#az-deployment-group-create). Specify the name of the Bicep template and replace the `<resource-group>` placeholder with the name of your target Azure resource group.

    ```azurecli-interactive
    az deployment group create \
        --resource-group "<resource-group>" \
        --template-file main.bicep
    ```

1. Wait for the deployment to complete. Review the output from the deployment.

::: zone-end

::: zone pivot="azure-terraform"

1. Open a new terminal.

1. Sign in to Azure CLI.

1. Check your target Azure subscription.

    ```azurecli-interactive
    az account show
    ```

1. Define your cluster in a new Terraform file. Name the file *cluster.`tf`*.

1. Add this resource configuration to the file's content. Replace the `<cluster-name>`, `<resource-group>`, and `<location>` placeholders with appropriate values.

    ```terraform
    variable "admin_username" {
      type        = string
      description = "Administrator username for the cluster."
      sensitive   = true
    }
    
    variable "admin_password" {
      type        = string
      description = "Administrator password for the cluster."
      sensitive   = true
    }
    
    terraform {
      required_providers {
        azurerm = {
          source  = "hashicorp/azurerm"
          version = "~> 4.0"
        }
      }
    }
    
    provider "azurerm" {
      features {}
    }
    
    data "azurerm_resource_group" "existing" {
      name = "<resource-group>"
    }
    
    resource "azurerm_mongo_cluster" "cluster" {
      name                   = "<cluster-name>"
      resource_group_name    = data.azurerm_resource_group.existing.name
      location               = "<location>"
      administrator_username = var.admin_username
      administrator_password = var.admin_password
      shard_count            = "1"
      compute_tier           = "M30"
      high_availability_mode = "Disabled"
      storage_size_in_gb     = "32"
      storage_type           = "PremiumSSDv2"
      version                = "8.0"
    }
    ```

    > [!TIP]
    > For more information on options using the `azurerm_mongo_cluster` resource, see [`azurerm` provider documentation in Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mongo_cluster#arguments-reference).

1. Initialize the Terraform deployment.

    ```azurecli-interactive
    terraform init --upgrade
    ```

1. Create an execution plan and save it to a file named *cluster.tfplan*. Provide values when prompted for the `admin_username` and `admin_password` variables.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform plan --out "cluster.tfplan"
    ```

    > [!NOTE]
    > This command sets the `ARM_SUBSCRIPTION_ID` environment variable temporarily. This setting is required for the `azurerm` provider starting with version 4.0 For more information, see [subscription ID in `azurerm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.0.0/docs/guides/4.0-upgrade-guide#specifying-subscription-id-is-now-mandatory).

1. Apply the execution plan to deploy the cluster to Azure.

    ```azurecli-interactive
    ARM_SUBSCRIPTION_ID=$(az account show --query id --output tsv) terraform apply "cluster.tfplan"
    ```

1. Wait for the deployment to complete. Review the output from the deployment.

::: zone-end

::: zone pivot="rest-api"

1. Open a new terminal.

1. Sign in to Azure CLI.

1. Create a new JSON file named *cluster.json*.

1. Add this document to the file's content. Replace the `<location>`, `<username>`, and `<password>` placeholders with appropriate values.

    ```json
    {
      "location": "<location>",
      "properties": {
        "administrator": {
          "userName": "<username>",
          "password": "<password>"
        },
        "serverVersion": "8.0",
        "storage": {
          "sizeGb": 32,
          "type": "PremiumSSDv2"
        },
        "compute": {
          "tier": "M30"
        },
        "sharding": {
          "shardCount": 1
        },
        "highAvailability": {
          "targetMode": "Disabled"
        }
      }
    }
    ```

1. Use the `az rest` Azure CLI command to create a new cluster with the configuration specified in the JSON file. Specify the name of the JSON file as the `body` of the request and replace the following placeholders:

    | | Description |
    | --- | --- |
    | **`<subscription-id>`** | The unique identifier of your target Azure subscription |
    | **`<resource-group>`** | The name of your target Azure resource group |
    | **`<cluster-name>`** | The unique name of your new Azure DocumentDB cluster |

    ```azurecli-interactive
    az rest \
        --method "GET" \
        --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>/users?api-version=2025-08-01-preview" \
        --body @cluster.json
    ```

    > [!TIP]
    > Use `az account show` to get the unique identifier of your target Azure subscription. 

1. Wait for the deployment to complete. Review the output from the deployment.

::: zone-end

## Limitations of high performance storage

Here are limitations of the high performance storage feature:

- Customer-managed keys (CMK) aren't supported.

- Storage capacity settings on Premimum SSD v2 disks can be adjusted up to four times within a 24-hour period. For newly created disks, the limit is three adjustments during the first 24 hours. 
  
- Replication from Premium SSD to Premium SSD v2 is supported only for migration scenarios. Ongoing replication isn't supported because Premium SSD can't match the performance of Premium SSD v2 and may result in increased latency.

- Online migration from Premium SSD to Premium SSD v2 isn't currently supported. To upgrade from Premium SSD to Premium SSD V2, you can perform a point-in-time-restore to a new server using Premium SSD v2. Alternatively, you can create a read replica from a Premium SSD server to a Premium SSD v2 server and promote it after replication completes.

- If you perform any operation that requires disk hydration following error might occur. This error occurs because Premium SSD v2 disks don't support any operation while the disk is still hydrating.
  - Error message: Unable to complete the operation because the disk is still being hydrated. Retry after some time.
  - Operations that can trigger this behavior include:
      - Performing compute scaling, storage scaling, enabling high availability (HA) in quick succession.
      - This also includes service-triggered failovers to guarantee high availability.
      - Using PITR (point-in-time-restore) to create a new cluster and immediately enabling High Availability while the disk is still being hydrated.
  - As a best practice, space out these operations or complete them sequentially, allowing hydration to finish between actions.

## Related content

- [Compute and storage tiers in Azure DocumentDB](compute-storage.md)
- [Azure DocumentDB limitations](limitations.md)
