---
title: High Performance Storage (Preview)
description: Learn how to use Premium SSD v2 high performance storage in Azure DocumentDB for consistent low latency and predictable IOPS scaling. Configure storage for I/O-intensive workloads.
author: suvishodcitus
ms.author: suvishod
ms.topic: feature-guide
ms.date: 11/21/2025
ms.custom:
  - references_regions
zone_pivot_groups: azure-interface-portal-rest-bicep-terraform
ai-usage: ai-assisted
---

# High performance storage in Azure DocumentDB (preview)

Azure DocumentDB high performance storage uses **Premium SSD v2** to deliver consistent low latency and predictable IOPS for I/O-intensive workloads. This capability enables you to achieve performance scaling based on your compute and storage configurations, maximizing throughput and efficiency per vCore.

## Guidance

The **maximum storage performance** for your Azure DocumentDB cluster depends on the combination of **compute tier** and **storage size** you select. Each combination determines the effective limits for **IOPS** and **throughput**. Start by choosing the storage size you need, then select a compute tier that provides the required Input/output operations per second (IOPS) and throughput for your workload. If you’re unsure about performance requirements:

- Begin with the compute tier that fully unlocks the storage performance for your selected size.

- Run workload benchmarks.

- Gradually reduce compute until you find the smallest tier that delivers your desired performance.

## IOPS and throughput caps

This section lists the limits in IOPS and throughput for each tier of Azure DocumentDB:

For more information on tiers, see [compute and storage tiers](compute-storage.md).

### `2` vCores (M30)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 | 3,750 |
| **Max throughput (MB/s)** | 85 | 85 | 85 | 85 | 85 | 85 | 85 | 85 | 85 | 85 | 85 | 85 |

### `4` vCores (M40)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 | 6,400 |
| **Max throughput (MB/s)** | 145 | 145 | 145 | 145 | 145 | 145 | 145 | 145 | 145 | 145 | 145 | 145 |

### `8` vCores (M50)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 | 12,800 |
| **Max throughput (MB/s)** | 290 | 290 | 290 | 290 | 290 | 290 | 290 | 290 | 290 | 290 | 290 | 290 |

### `16` vCores (M60)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 16,000 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 | 25,600 |
| **Max throughput (MB/s)** | 600 | 600 | 600 | 600 | 600 | 600 | 600 | 600 | 600 | 600 | 600 | 600 |

### `32` vCores (M80)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 16,000 | 32,000 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 | 51,200 |
| **Max throughput (MB/s)** | 865 | 865 | 865 | 865 | 865 | 865 | 865 | 865 | 865 | 865 | 865 | 865 |

### `64` vCores (M200)

| Storage (GiB) | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Max IOPS** | 16,000 | 32,000 | 64,000 | 80,000 | 80,000 | 80,000 | 80,000 | 80,000 | 80,000 | 80,000 | 80,000 | 80,000 |
| **Max throughput (MB/s)** | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 | 1,200 |

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

1. On the **Configure** page, choose the cluster tier and storage size as required. Select the storage type as **Premium SSD v2** (preview) to enable high-performance storage, then select Save to apply the changes.

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
        azapi = {
          source = "azure/azapi"
          version = "~> 2.0"
        }
      }
    }
    
    provider "azapi" {
    }
    
    provider "azurerm" {
      features {}
    }
    
    data "azurerm_resource_group" "existing" {
        name = "<resource-group>"
    }

    resource "azapi_resource" "cluster" {
      schema_validation_enabled = false
      type = "Microsoft.DocumentDB/mongoClusters@2025-08-01-preview"
      name = "<cluster-name>"
      parent_id = data.azurerm_resource_group.existing.id
      location = "<location>"  
      body = {
        properties = {
          administrator = {
            userName = var.admin_username
            password = var.admin_password
          }
          serverVersion = "8.0"
          storage = {
            sizeGb = 32
            type = "PremiumSSDv2"
          }
          compute = {
            tier = "M30"
          }
          sharding = {
            shardCount = 1
          }
          highAvailability = {
            targetMode = "Disabled"
          }
        }
      }
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

- High availability (HA) isn't supported 

- Replica clusters aren't supported

- Customer-managed keys (CMK) aren't supported

- The Azure portal renders storage size but doesn't render effective IOPS/throughput

- High performance storage is available in a limited subset of Azure regions

## Considerations for high performance storage

Consider these things when using high performance storage in your Azure DocumentDB cluster:

- High performance storage can get the maximum performance for your selected compute/storage combination for the fixed price per 1 GiB of storage / month. For more information, see [Azure DocumentDB pricing](https://azure.microsoft.com/pricing/details/document-db/).

## Related content

- [Compute and storage tiers in Azure DocumentDB](compute-storage.md)
- [Azure DocumentDB limitations](limitations.md)
