---
title: Enable Fleet Analytics (Preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Monitor and manage your usage and costs effectively by enabling fleet analytics for Azure Cosmos DB.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 05/07/2025
ai-usage: ai-assisted
zone_pivot_groups: azure-fleet-storage
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Enable fleet analytics in Azure Cosmos DB (preview)

[!INCLUDE[Preview](includes/notice-preview.md)]

:::zone pivot="fleet-storage-fabric"

In this guide, you enable Azure Cosmos DB fleet analytics for your Microsoft Fabric workspace.

:::zone-end

:::zone pivot="fleet-storage-data-lake"

In this guide, you enable Azure Cosmos DB fleet analytics for your Azure Data Lake Storage account.

:::zone-end

## Prerequisites

- An existing Azure Cosmos DB fleet

    - If you don't have an existing a fleet, [create a new fleet](how-to-create-fleet.md).
    
    - Fleet analytics only supports Azure Cosmos DB for NoSQL accounts that are configured with the fleet.

:::zone pivot="fleet-storage-fabric"

- An existing Microsoft Fabric workspace

    - The workspace must use **OneLake** as the default storage location.
    
    - The workspace must be backed by a **licensed or trial** Fabric capacity.

> [!NOTE]
> It is recommended to create a dedicated Fabric workspace for Fleet Analytics because the service principal associated with the feature requires Contributor access to the entire workspace.

:::zone-end

:::zone pivot="fleet-storage-data-lake"

- An existing Azure Storage account compatible with Azure Data Lake Storage (Gen2)

    - The **hierarchical namespace** feature must be enabled at account creation.

:::zone-end

## Enable fleet analytics

First, configure the resources required for fleet analytics.

:::zone pivot="fleet-storage-fabric"

1. Sign-in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the existing Azure Cosmos DB fleet.

1. On the page for the fleet, select **Fleet analytics** in the **Monitoring** section of the resource menu.

1. Then, select **Add destination**.

1. In the **Fleet analytics** dialog, select **Send to Fabric workspace**. Then, select your existing Fabric workspace, select an existing OneLake lakehouse, and then **save** the destination.

    :::image source="media/how-to-enable-fleet-analytics/fabric-destination-dialog.png" alt-text="Screenshot of the fleet analytics dialog for a Fabric workspace in the Azure portal.":::

1. Navigate to your Fabric workspace in the Microsoft Fabric portal.

1. In the **Manage** section of your workspace, add the principal for fleet analytics as the **Contributor** role by searching for the shared **Cosmos DB Fleet Analytics** service principal.

    :::image source="media/how-to-enable-fleet-analytics/fabric-access-control-configuration.png" alt-text="Screenshot of the workspace role-based access control configuration in the Fabric portal.":::

    > [!IMPORTANT]
    > Failure to complete this step results in data not being written to your destination Fabric workspace.

1. **Save** your changes.

:::zone-end

:::zone pivot="fleet-storage-data-lake"

1. Sign-in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the existing Azure Cosmos DB fleet.

1. On the page for the fleet, select **Fleet analytics** in the **Monitoring** section of the resource menu.

1. Then, select **Add destination**.

1. In the **Fleet analytics** dialog, select **Send to storage account**. Then, select your existing Azure Storage account, select an existing container, and then **save** the destination.

    :::image source="media/how-to-enable-fleet-analytics/storage-destination-dialog.png" alt-text="Screenshot of the fleet analytics dialog for an Azure Storage account in the Azure portal.":::

1. Navigate to your Azure Storage account. Then, navigate to the **Access Control (IAM)** page.

1. Select the **Add role assignment** menu option.

1. On the **Add role assignment** page, select the **Storage Blob Contributor** role to grant permissions to contribute blobs to the existing account.

1. Now, use the **+ Select members** option. In the dialog, search for and select the shared **Cosmos DB Fleet Analytics** service principal.

    :::image source="media/how-to-enable-fleet-analytics/storage-access-control-configuration.png" alt-text="Screenshot of the account role-based access control configuration in the Azure portal.":::

    > [!IMPORTANT]
    > Failure to complete this step results in data not being written to your destination Azure Storage account.


1. **Review + assign** your role assignment.

:::zone-end

## Query and visualize data

:::zone pivot="fleet-storage-fabric"

In a star schema design, retrieving detailed information typically requires joining fact tables with their related dimension tables, following standard best practices. This section walks through the steps to query and visualize data using Microsoft Fabric.

1. Open your Fabric workspace.

1. Navigate to your existing OneLake resource.

    :::image source="media/how-to-enable-fleet-analytics/existing-onelake-resource.png" alt-text="Screenshot of an existing OneLake resource within a Microsoft Fabric workspace.":::

1. In the SQL endpoint explorer, select any table and run a `SELECT TOP 100` query to quickly observe the data. This query can be found in the context menu.

    :::image source="media/how-to-enable-fleet-analytics/run-context-menu-query.png" alt-text="Screenshot of the context menu with the 'SELECT TOP 100' query option in the SQL endpoint explorer within the workspace.":::

    > [!TIP]
    > Alternatively, run the following query to view Account-level details:
    >
    > ```sql
    > SELECT TOP (100) [Timestamp],
    >     [ResourceId],
    >     [FleetId],
    >     [DefaultConsistencyLevel],
    >     [IsSynapseLinkEnabled],
    >     [IsFreeTierEnabled],
    >     [IsBurstEnabled],
    >     [BackupMode],
    >     [BackupStrategy],
    >     [BackupRedundancy],
    >     [BackupIntervalInMinutes],
    >     [BackupRetentionIntervalInHours],
    >     [TotalRUPerSecLimit],
    >     [APISettings],
    >     [AccountKeySettings],
    >     [LastDateAnyAccountKeyRotated]
    > FROM [FactAccountHourly]
    > ```
    >

1. Observe the results of the query. Notice that you only have a reference to the `ResourceId` field. Using just the results of this query, you can't determine the exact database or container for individual rows.

1. Run this sample query joining both the `DimResource` and `FactRequestHourly` tables to find your **top 100 most active accounts by transactions**.

    ```sql
    SELECT TOP 100
        DR.[SubscriptionId],
        DR.[AccountName],
        DR.[ResourceGroup],
        SUM(FRH.[TotalRequestCount]) AS sum_total_requests
    FROM 
        [FactRequestHourly] FRH
    JOIN 
        [DimResource] DR
        ON FRH.[ResourceId] = DR.[ResourceId]
    WHERE 
        FRH.[Timestamp] >= DATEADD(DAY, -7, GETDATE()) -- Filter for the last 7 days
        AND ResourceName IN ('Document', 'StoredProcedure') -- Filter for Dataplane Operations
    GROUP BY 
        DR.[AccountName],
        DR.[SubscriptionId],
        DR.[ResourceGroup]
    ORDER BY
    sum_total_requests DESC; -- Order by total requests in descending order
    ```

1. Run this query to find the **top 100 largest accounts by storage**.

    ```sql
    SELECT TOP 100
        DR.[SubscriptionId],
        DR.[AccountName],
        MAX(FRH.[MaxDataStorageInKB] / (1024.0 * 1024.0)) AS DataUsageInGB,
        MAX(FRH.[MaxIndexStorageInKB] / (1024.0 * 1024.0)) AS IndexUsageInGB,
        MAX(
            FRH.[MaxDataStorageInKB] / (1024.0 * 1024.0) + 
            FRH.[MaxIndexStorageInKB] / (1024.0 * 1024.0)
        ) AS StorageInGB
    FROM 
        [FactResourceUsageHourly] FRH
    JOIN 
        [DimResource] DR
        ON FRH.[ResourceId] = DR.[ResourceId]
    WHERE 
        FRH.[Timestamp] >= DATEADD(DAY, -1, GETDATE()) -- Filter for the last 1 day
    GROUP BY 
        DR.[AccountName],
        DR.[SubscriptionId]
    ORDER BY
        StorageInGB DESC; -- Order by total storage usage
    ```    

1. Now, create a view on the data by opening the context menu and selecting **Save as view**. Give the view a unique name and then select **Ok**.

    :::image source="media/how-to-enable-fleet-analytics/save-as-view.png" alt-text="Screenshot of the 'Save as view' context menu option for a SQL query in the workspace.":::

    :::image source="media/how-to-enable-fleet-analytics/set-view-name.png" alt-text="Screenshot of the dialog to specify the name of the new view in the workspace.":::

    > [!TIP]
    > Alternatively, create a view directly using this query:
    >
    > ```sql
    > CREATE VIEW [MostActiveCustomers]
    > AS
    > SELECT 
    >     a.ResourceId AS UsageResourceId,
    >     a.Timestamp,
    >     a.MeterId,
    >     a.FleetId,
    >     a.ConsumedUnits,
    >     b.ResourceId AS ResourceDetailId
    > FROM
    >     FactMeterUsageHourly a
    > INNER JOIN
    >     DimResource b ON a.ResourceId = b.ResourceId
    > ```
    >    

1. Navigate to the newly created view within the **Views** folder of your endpoint.

    :::image source="media/how-to-enable-fleet-analytics/navigate-view.png" alt-text="Screenshot of the 'Views' folder within the hierarchy of a SQL endpoint in the workspace.":::

1. Navigate to the view you recently created (or a query) and then select **Explorer this data (preview)** and then select **Visualize results**.

    :::image source="media/how-to-enable-fleet-analytics/explore-visualize-query.png" alt-text="Screenshot of the menu option to visualize an existing query in the workspace.":::

1. On the Power BI landing page, create relevant visuals for your scenario. For example, you can show the percentage of your Azure Cosmos DB workload with the **autoscale** feature enabled.

    :::image source="media/how-to-enable-fleet-analytics/powerbi-visualization.png" alt-text="Screenshot of the Power BI visualization dialog for a SQL query or view within the workspace.":::

:::zone-end

:::zone pivot="fleet-storage-data-lake"

This section walks through the steps to create and query a table or DataFrame loaded from data stored in Azure Storage (ADLS) or Azure Databricks. This section uses a Notebook connected to Apache Spark with Python and SQL cells.

1. First, define the Azure Storage account configuration targeting the

    ```python
    # Define storage configuration
    container_name = "<azure-storage-container-name>"
    account_name = "<azure-storage-account-name>"
    base_url = f"abfss://{container_name}@{account_name}.dfs.core.windows.net"
    source_path = f"{base_url}/FactResourceUsageHourly"
    ```

1. Create the data as a table. **Reload and refresh data** from an external source (Azure Storage - ADLS) by dropping and recreating the `fleet_data` table.

    ```python
    table_name = "fleet_data"
    
    # Drop the table if it exists
    spark.sql(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create the table
    spark.sql(f"""
        CREATE TABLE {table_name}
        USING delta
        LOCATION '{source_path}'
    """)
    ```

1. Query and render the results from the `fleet_data` table.

    ```python
    # Query and display the table
    df = spark.sql(f"SELECT * FROM {table_name}")
    display(df)
    ```

1. Define the full list of extra tables to be created for processing fleet analytics data.

    ```python
    # Table names and folder paths (assumed to match)
    tables = [
        "DimResource",
        "DimMeter",
        "FactResourceUsageHourly",
        "FactAccountHourly",
        "FactRequestHourly",
        "FactMeterUsageHourly"
    ]

    # Drop and recreate each table
    for table in tables:
        spark.sql(f"DROP TABLE IF EXISTS {table}")
        spark.sql(f"""
            CREATE TABLE {table}
            USING delta
            LOCATION '{base_url}/{table}'
        """)
    ```

1. Run a query using any of those tables. For example, this query finds your **top 100 most active accounts by transactions**.

    ```sql
    SELECT 
        DR.SubscriptionId,
        DR.AccountName,
        DR.ResourceGroup,
        SUM(FRH.TotalRequestCount) AS sum_total_requests
    FROM 
        FactRequestHourly FRH
    JOIN 
        DimResource DR
        ON FRH.ResourceId = DR.ResourceId
    WHERE 
        FRH.Timestamp >= DATE_SUB(CURRENT_DATE(), 7) -- Filter for the last 7 days
        AND FRH.ResourceName IN ('Document', 'StoredProcedure') -- Filter for Dataplane Operations
    GROUP BY 
        DR.AccountName,
        DR.SubscriptionId,
        DR.ResourceGroup
    ORDER BY
        sum_total_requests DESC
    LIMIT 100; -- Limit to top 100 results
    ```

1. Run this query to find the **top 100 largest accounts by storage**.

    ```sql
    SELECT 
        DR.SubscriptionId,
        DR.AccountName,
        MAX(FRH.MaxDataStorageInKB / (1024.0 * 1024.0)) AS DataUsageInGB,
        MAX(FRH.MaxIndexStorageInKB / (1024.0 * 1024.0)) AS IndexUsageInGB,
        MAX(
            FRH.MaxDataStorageInKB / (1024.0 * 1024.0) + 
            FRH.MaxIndexStorageInKB / (1024.0 * 1024.0)
        ) AS StorageInGB
    FROM 
        FactResourceUsageHourly FRH
    JOIN 
        DimResource DR
        ON FRH.ResourceId = DR.ResourceId
    WHERE 
        FRH.Timestamp >= DATE_SUB(CURRENT_DATE(), 1) -- Filter for the last 1 day
    GROUP BY 
        DR.AccountName,
        DR.SubscriptionId
    ORDER BY
        StorageInGB DESC
    LIMIT 100; -- Limit to top 100 results
    ```    

:::zone-end

## Related content

- [Fleet analytics overview](fleet-analytics.md)
- [FAQ](fleet-faq.yml#fleet-analytics)
- [Schema reference](fleet-analytics-schema-reference.md)
