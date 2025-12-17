---
title: Create a Fleet (Preview)
description: Create an Azure Cosmos DB fleet along with the corresponding fleetspace and fleetspace account resources.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 05/07/2025
ai-usage: ai-assisted
zone_pivot_groups: azure-interface-portal-cli-bicep
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Create an Azure Cosmos DB fleet 

This article provides step-by-step instructions for creating and managing fleets, fleetspaces, and fleetspace accounts. Follow the guidance here to set up and configure your Azure Cosmos DB fleet resources one-by-one. At the end of this guide, you have a fully configured fleet with a single fleetspace, throughput pooling, and a registered Azure Cosmos DB account as a fleetspace account.

For more information about fleets, see [fleets overview](fleet.md).

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prereq-azure-subscription.md)]

:::zone pivot="azure-cli,azure-resource-manager-bicep"

- Azure CLI

:::zone-end

:::zone pivot="azure-resource-manager-bicep"

- Bicep

:::zone-end

## Create a fleet

Set up your fleet by creating the fleet that eventually contains your fleetspace, and fleetspace account resources. A fleet is a high-level entity that organizes and manages multiple database accounts across different subscriptions and/or resource groups within fleetspaces. One fleet corresponds to one multitenant application. Specify a region and unique name for the fleet.

> [!NOTE]
> The region selected for your fleet resources doesn't affect or determine the locations/regions of any database accounts in the fleet.

:::zone pivot="azure-portal"

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Enter *Cosmos DB fleet* in the global search bar.

1. Within **Services**, select **Azure Cosmos DB Fleets**.

1. On the **Azure Cosmos DB Fleets** page, select **+ Create**.

1. Within the **Basics** pane, configure the following options, and then select **Review + create**:

    | | Value |
    | --- | --- |
    | **Subscription** | *Select your Azure subscription* |
    | **Resource group** | *Create a new resource group or select an existing resource group* |
    | **Fleet Name** | *Provide a globally unique name* |
    | **Region** | *Select a supported Azure region for your subscription* |

    :::image source="media/how-to-create-fleet/new-fleet.png" alt-text="Screenshot of the fleet creation overview page in the Azure portal.":::

1. On the **Review + create** pane, wait for validation of your fleet to finish successfully, and then select **Create**.

:::zone-end

:::zone pivot="azure-cli"

1. Create a fleet using `az resource create` and an empty (`{}`) JSON properties object:

    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<fleet-name>" \
        --resource-type "Microsoft.DocumentDB/fleets" \
        --location "<azure-region>" \
        --latest-include-preview \
        --properties "{}"
    ```

1. Optionally, perform common fleet management operations including:

    - Retrieving a specific fleet.

        ```azurecli-interactive
        az resource show \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>" \
            --resource-type "Microsoft.DocumentDB/fleets" \
            --latest-include-preview
        ```
        
    - Listing all fleets within a resource group.

        ```azurecli-interactive
        az resource list \
            --resource-group "<resource-group-name>" \
            --resource-type "Microsoft.DocumentDB/fleets"
        ```
        
    - Deleting a specific fleet.

        ```azurecli-interactive
        az resource delete \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>" \
            --resource-type "Microsoft.DocumentDB/fleets" \
            --latest-include-preview
        ```

:::zone-end

:::zone pivot="azure-resource-manager-bicep"

```bicep
resource fleet 'Microsoft.DocumentDB/fleets@2025-10-25' = {
  name: '<fleet-name>'
  location: '<azure-region>'
  properties: {}
}
```

:::zone-end

## Create a fleetspace

Before adding accounts to the fleet, you must create a fleetspace. A fleetspace is a logical grouping of database accounts within the fleet, where RU/s can optionally be shared among all resources in database accounts within the fleetspace​. Each database account within a fleet must be a part of a fleetspace. 

> [!NOTE]
> In this guide, throughput pooling is configured for the fleetspace. You can opt to not use throughput pooling. Throughput pooling is an optional configuration that allows account resources to share RU/s. This shared RU/s is on top of the dedicated RU/s that are already available for the resource.  
The pool minimum and maximum RU/s can be changed at any time. The service tier and data regions cannot be changed after fleetspace creation. 
>
> To configure throughput pooling for a fleetspace, specify the regions and the service tier that apply to all accounts within the fleetspace. If throughput pooling is configured, all accounts within the fleetspace must share the same regional and service tier configuration.  
>
> For more information, see [fleet pools](fleet-pools.md).
>

:::zone pivot="azure-portal"

1. Navigate to your existing fleet resource within the Azure portal.

1. Select the **Fleetspaces** option within the **Fleet resources** section of the resource menu.

1. Within the dialog, configure the following options, and then select **Ok**:

   | | Value |
   | --- | --- |
   | **Fleetspace name** | *Provide a unique name within your fleet* |
   | **Enable throughput pooling** | *Select the checkbox* |
   | **Select regions for accounts in throughput pool** | Select and **Add** a list of regions for accounts in the throughput pool |
   | **Select write-region type for accounts in throughput pool** | *Select either **Single-write region** (General purpose) or **Multi-write region** (Business critical)* |
   | **Throughput pool minimum RU/s** | *A whole number, not less than 100,000, and must be a multiple of 1,000* |
   | **Throughput pool maximum RU/s** | *A whole number, not less than 100,000, or less than* `throughputPoolConfiguration.minThroughput` *and must be a multiple of 1,000* |
   
   :::image source="media/how-to-create-fleet/new-fleetspace.png" alt-text="Screenshot of the fleetspace creation dialog in the Azure portal.":::

:::zone-end

:::zone pivot="azure-cli"

1. Create a fleetspace within your fleet using the following properties:

    | | Value |
    | --- | --- |
    | **`fleetspaceAPIKind`** | `NoSQL` |
    | **`throughputPoolConfiguration.minThroughput`** | *A whole number, not less than 100,000, and must be a multiple of 1,000* |
    | **`throughputPoolConfiguration.maxThroughput`** | *A whole number, not less than 100,000, or less than* `throughputPoolConfiguration.minThroughput` *and must be a multiple of 1,000* |
    | **`throughputPoolConfiguration.serviceTier`** | *Either* `GeneralPurpose` *or* `BusinessCritical` |
    | **`throughputPoolConfiguration.dataRegions`** | *List of regions for accounts in the throughput pool* |
    
    ```azurecli-interactive
    json=$(jq \
        --arg "locationName" "<azure-region>" \
        --arg "api" "NoSQL" \
        --arg "minRUs" 100000 \
        --arg "maxRUs" 100000 \
        --arg "tier" "GeneralPurpose" \
        --null-input \
        --compact-output \
        '{fleetspaceAPIKind:$api,serviceTier:$tier,dataRegions:[$locationName],throughputPoolConfiguration:{minThroughput:$minRUs,maxThroughput:$maxRUs}}' \
    )
    
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<fleet-name>/fleetspaces/<fleetspace-name>" \
        --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/" \
        --location "<azure-region>" \
        --latest-include-preview \
        --properties $json
    ```

    > [!TIP]
    > You can configure the `minThroughput`, `maxThroughput`, `writeRegionType`, and `dataRegions` properties to whatever is appropriate for your scenario.
    
1. Optionally, perform common fleetspace management operations including:

    - Retrieving a specific fleetspace within a fleet.

        ```azurecli-interactive
        az resource show \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>/fleetspaces/<fleetspace-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/" \
            --latest-include-preview
        ```
        
    - Listing all fleetspaces within a fleet.

        ```azurecli-interactive
        az resource list \
            --resource-group "<resource-group-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/"
        ```

    - Deleting a specific fleetspace within a fleet.

        ```azurecli-interactive
        az resource delete \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>/fleetspaces/<fleetspace-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/" \
            --latest-include-preview
        ```

:::zone-end

:::zone pivot="azure-resource-manager-bicep"

| | Value |
| --- | --- |
| **`fleetspaceAPIKind`** | `NoSQL` |
| **`throughputPoolConfiguration.minThroughput`** | *A whole number, not less than 100,000, and must be a multiple of 1,000* |
| **`throughputPoolConfiguration.maxThroughput`** | *A whole number, not less than 100,000, or less than* `throughputPoolConfiguration.minThroughput` *and must be a multiple of 1,000* |
| **`throughputPoolConfiguration.serviceTier`** | *Either* `GeneralPurpose` *or* `BusinessCritical` |
| **`throughputPoolConfiguration.dataRegions`** | *List of regions for accounts in the throughput pool* |

```bicep
resource fleetspace 'Microsoft.DocumentDB/fleets/fleetspaces@2025-10-15' = {
  name: '<fleetspace-name>'
  parent: fleet
  location: '<azure-region>'
  serviceTier: 'General Purpose''
  dataRegions:  [
        '<azure-region>'
      ]
  properties: {
    fleetspaceAPIKind: 'NoSQL'
    throughputPoolConfiguration: {
      minThroughput: 100000
      maxThroughput: 100000
    }
  }
}
```

> [!TIP]
> You can configure the `minThroughput`, `maxThroughput`, `writeRegionType`, and `dataRegions` properties to whatever is appropriate for your scenario.

:::zone-end

## Add accounts to a fleetspace

Once the fleetspace is created, add accounts either to the fleetspace itself. Accounts from any subscription/resource group can be added to the fleet. When pooling is configured for the fleetspace, these resources consume RU/s from the pool.

> [!IMPORTANT]
> You can't add accounts to your fleetspace that are already associated with an existing fleetspace.

:::zone pivot="azure-portal"

1. Select the **Database accounts** option within the **Fleet resources** section of the resource menu.

1. In the **Fleetspace** section, select an existing fleetspace.

    :::image source="media/how-to-create-fleet/select-fleetspace.png" alt-text="Screenshot of the option to select a fleetspace with the fleetspace account registration page in the Azure portal.":::

1. Then, enable the **Browse accounts to add to this fleetspace** option.

1. Select an existing Azure Cosmos DB for NoSQL account and then select **+ Add to fleetspace**.

    :::image source="media/how-to-create-fleet/add-fleetspace-account.png" alt-text="Screenshot of the page to register Azure Cosmos DB accounts with a fleetspace in the Azure portal.":::

:::zone-end

:::zone pivot="azure-cli"

1. Create a fleetspace account within your fleetspace using the following properties:

    | | Value |
    | --- | --- |
    | **`accountLocation`** | *Location for the Azure Cosmos DB account.* |
    | **`accountResourceIdentifier`** | *Fully qualified resource identifier for the target Azure Cosmos DB account.* |

    ```azurecli-interactive
    databaseResourceId=$(az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-resource-name>" \
        --resource-type "Microsoft.DocumentDB/databaseAccounts" \
        --query "id" \
        --output tsv \
    )
    
    json=$(jq \
        --arg "locationName" "<azure-region>" \
        --arg "accountResourceId" "$databaseResourceId" \
        --null-input \
        --compact-output \
        '{accountLocation:$locationName,accountResourceIdentifier:$accountResourceId}' \
    )
    
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<fleet-name>/fleetspaces/<fleetspace-name>/fleetspaceAccounts/<fleetspace-account-name>" \
        --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/fleetspaceAccounts/" \
        --location "<azure-region>" \
        --latest-include-preview \
        --properties $json
    ```


1. Optionally, perform common fleetspace management operations including:

    - Retrieving a specific fleetspace account within a fleetspace.

        ```azurecli-interactive
        az resource show \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>/fleetspaces/<fleetspace-name>/fleetspaceAccounts/<fleetspace-account-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/fleetspaceAccounts/" \
            --latest-include-preview
        ```
    
    - Listing fleetspace accounts within a fleetspace.

        ```azurecli-interactive
        az resource list \
            --resource-group "<resource-group-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/fleetspaceAccounts/"
        ```
    
    - Deleting a specific fleetspace account.    

        ```azurecli-interactive
        az resource delete \
            --resource-group "<resource-group-name>" \
            --name "<fleet-name>/fleetspaces/<fleetspace-name>/fleetspaceAccounts/<fleetspace-account-name>" \
            --resource-type "Microsoft.DocumentDB/fleets/fleetspaces/fleetspaceAccounts/" \
            --latest-include-preview
        ```

:::zone-end

:::zone pivot="azure-resource-manager-bicep"

| | Value |
| --- | --- |
| **`accountLocation`** | *Location for the Azure Cosmos DB account.* |
| **`accountResourceIdentifier`** | *Fully qualified resource identifier for the target Azure Cosmos DB account.* |

```bicep
resource account 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = {
  name: '<azure-cosmos-db-resource-name>'
}

resource fleetspaceAccount 'Microsoft.DocumentDB/fleets/fleetspaces/fleetspaceAccounts@2025-10-15' = {
  name: '<fleetspace-account-name>'
  parent: fleetspace
  location: '<azure-region>'
  properties: {
    accountLocation: '<azure-region>'
    accountResourceIdentifier: account.id
  }
}
```

:::zone-end

## Related content

- [Overview of fleets](fleet.md)
- [Fleet analytics](fleet-analytics.md)
- [Fleet pools](fleet-pools.md)
