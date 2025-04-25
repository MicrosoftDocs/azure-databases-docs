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

With a Linked Service, you can connect to your instance of Azure Database for PostgreSQL flexible server and use it within Microsoft Fabric Data Factory activities.

The Copy Activity supports **Copy Command**, **Bulk Insert** and **Upsert**. [Learn More about Copy Activity in Azure Database for PostgreSQL using Microsoft Fabric Data Factory](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity)

The next section will have a step-by-step in how to manually create a copy activity and how to create a pipeline. 

### Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server)
- A Microsoft Fabric Data Factory [Data pipeline](/fabric/data-factory/pipeline-landing-page)

### Create a Copy Data Activity via Azure portal

1. In Microsoft Fabric, select your workspace and switch to **Data factory** and, select the **New item** button, and select **Data pipeline** and provide a name in the **New pipeline" popup to create a Data pipeline

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png" alt-text="Screenshot that shows where to select new pipeline." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-a-new-fabric-data-factory-pipeline.png":::

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png" alt-text="Screenshot showing the dialog to give the new pipeline a name." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/new-pipeline-name.png":::


1. Select  **Activities** menu and select **Copy data** and **Add to canvas** from the drop-down menu displayed

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-copy-activity.png" alt-text="Screenshot that shows where to select Copy data" lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/create-copy-activity.png":::

1. At the **General tab**, give a name to your pipeline

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/give-a-name.png" alt-text="Screenshot that shows where to give a name to the pipeline at the general tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/give-a-name.png":::


1. At the **Source tab**, select or create a **Source dataset**. In this specific example, we selected an Azure Database for PostgreSQL table

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-source-dataset.png" alt-text="Screenshot that shows where to select or create a source dataset at the source tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-source-dataset.png":::

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/source-datasource-selected.png" alt-text="Screenshot that shows a source dataset selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/source-datasource-selected.png":::

1. At the **Sink tab**, select or create an Azure Database for PostgreSQL dataset as **Sink dataset**, and  choose the **Write method**. [Learn More about Azure Copy Activity and Write Method](/azure/data-factory/connector-azure-database-for-postgresql?tabs=data-factory)

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-sink-datasource.png" alt-text="Screenshot that shows where to select or create a sink datasource at sink tab." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-sink-datasource.png":::

1. Select between **Copy command**, **Bulk insert** and **Upsert** for the **Write method**  
    
   #### [Copy Command](#tab/copy-command)
          
   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/copy-command.png"alt-text="Screenshot that shows an example of copy command selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/copy-command.png":::

   #### [Bulk Insert](#tab/bulk-insert)
      
   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/bulk-insert.png"alt-text="Screenshot that shows of bulk insert selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/bulk-insert.png":::

   #### [Upsert](#tab/upsert)
       
   You optionally can provide the key columns. In this example, **New** button was clicked and added the two primary key columns of this sink dataset
      
   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png"alt-text="Screenshot that shows an example in providing all key columns." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png":::
   

1. If a custom mapping is required, configure your mapping in the **Mapping tab**
1. Validate your pipeline
1. Select Debug, this runs the pipeline manually
1. Set up a [trigger for your pipeline](/azure/data-factory/concepts-pipeline-execution-triggers)

For the JSON payloads examples, go to [Azure Database for PostgreSQL as sink](/azure/data-factory/connector-azure-database-for-postgresql?tabs=data-factory#azure-database-for-postgresql-as-sink)

## Key Columns Behavior on Upsert

When upserting data using the Azure Database for PostgreSQL connector, you can specify optional fields called **Key Columns**.

:::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-optional-key-columns.png" alt-text="Screenshot that shows optional key columns." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/select-optional-key-columns.png":::
There are three acceptable ways to use the **Key Columns**:
1. Select **New** and add all the primary key columns of the sink datasource table

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png" alt-text="Screenshot that shows an example with all key columns." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/providing-all-key-columns.png":::

1. Select **New** and add one or more unique columns of the sink datasource table
1. Leave the **Key columns** empty. In this case, the connector finds the primary key columns and uses them as **Key columns**

   :::image type="content" source="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/empty-key-columns.png" alt-text="Screenshot that shows an example with no key columns selected." lightbox="./media/how-to-use-microsoft-fabric-data-factory-copy-activity/empty-key-columns.png":::


## Related content

- [Learn More about Copy Activity in Microsoft Fabric Data Factory Data Pipeline](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity).
- [Learn More about Azure Database for PostgreSQL Data Pipeline Connector in Microsoft Fabric Data Factory](/fabric/data-factory/connector-azure-database-for-postgresql-overview).
- [Learn More about Script Activity in Microsoft Fabric Data Factory Data Pipeline to work with Azure Database for PostgreSQL flexible server](how-to-use-microsoft-fabric-data-factory-script-activity.md).