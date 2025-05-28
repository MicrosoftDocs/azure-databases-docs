---
title: Using Copy Activity in Microsoft Fabric Data Factory
description: Guide to use Copy Activity in Microsoft Fabric Data Factory for Azure Database for PostgreSQL
author: KazimMir
ms.author: v-kmir
ms.reviewer: danyal.bukhari
ms.date: 04/25/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Copy Activity in Microsoft Fabric Data Factory

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

## Copy Activity

Copy activity in Microsoft Fabric Data Factory can help you connect to your instance of Azure Database for PostgreSQL flexible server to perform data movement and transformation activities.

The Copy Activity supports **Copy Command**, **Bulk Insert** and **Upsert**. [Learn More about Copy Activity in Azure Database for PostgreSQL using Microsoft Fabric Data Factory](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity)

The next section will have a step-by-step instructions on how to create a Copy Activity. 

### Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server)
- A Microsoft Fabric Data Factory [Data pipeline](/fabric/data-factory/pipeline-landing-page)

### Create a Copy Data Activity via Fabric portal

1. In Microsoft Fabric, select your workspace, switch to **Data factory** and select the **New item** button. Search and select the **Data pipeline** tile in the **New item** sidebar displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png" alt-text="Screenshot that shows where to select new pipeline." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png":::

1. Provide a name in the **New pipeline** popup and select the **Create** button to create a Data pipeline

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png" alt-text="Screenshot showing the dialog to give the new pipeline a name." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png":::


1. Select  **Activities** menu, select **Copy data**, and **Add to canvas** from the drop-down menu displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-copy-activity.png" alt-text="Screenshot that shows where to select Copy data" lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-copy-activity.png":::

1. With the Copy activity selected on the data pipeline canvas, in the **General tab**, give a name to your activity

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/give-a-name.png" alt-text="Screenshot that shows where to give a name to the pipeline at the general tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/give-a-name.png":::


1. At the **Source tab**, select or create a **Connection**. [Learn more](/fabric/data-factory/modern-get-data-experience-pipeline) about connecting to your data with the new modern get data experience for data pipelines

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-source-connection.png" alt-text="Screenshot that shows where to select or create a source connection at the source tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-source-connection.png":::

1. In this specific example, we selected an Azure Database for PostgreSQL table

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/source-datasource-selected.png" alt-text="Screenshot that shows a source connection selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/source-datasource-selected.png":::

1. At the **Destination tab**, select or create an Azure Database for PostgreSQL **Connection**, and  choose the **Write method**.

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-destination-datasource.png" alt-text="Screenshot that shows where to select or create a destination datasource at destination tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-destination-datasource.png":::

1. Select between **Copy command**, **Bulk insert** and **Upsert** for the **Write method**  
    
   #### [Copy Command](#tab/copy-command)
          
   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/copy-command.png"alt-text="Screenshot that shows an example of Copy command selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/copy-command.png":::

   #### [Bulk Insert](#tab/bulk-insert)
      
   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/bulk-insert.png"alt-text="Screenshot that shows of Bulk insert selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/bulk-insert.png":::

   #### [Upsert](#tab/upsert)

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/upsert.png"alt-text="Screenshot that shows of Upsert selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/upsert.png":::
   

1. If a custom mapping is required, configure your mapping in the **Mapping tab**
1. Validate your pipeline
1. Select Run button, this runs the pipeline manually
1. Set up a [trigger for your pipeline](/fabric/data-factory/pipeline-runs)

## Key Columns Behavior on Upsert

When upserting data using the Azure Database for PostgreSQL connector, you need to specify fields called **Key Columns**.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-key-columns.png" alt-text="Screenshot that shows key columns." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-key-columns.png":::
There are two acceptable ways to use the **Key Columns**:

1. Select **New** and add all the primary key columns of the destination datasource table

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png" alt-text="Screenshot that shows an example with all key columns." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png":::

1. Select **New** and add one or more unique columns of the destination datasource table


## Related content

- [Learn more about Copy Activity in Microsoft Fabric Data Factory Data Pipeline](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity).
- [Learn more about Azure Database for PostgreSQL Data Pipeline Connector in Microsoft Fabric Data Factory](/fabric/data-factory/connector-azure-database-for-postgresql-overview).
- [Learn more about Script Activity to work with Azure Database for PostgreSQL flexible server in Microsoft Fabric Data Factory Data Pipeline ](how-to-use-microsoft-fabric-data-factory-script-activity.md).