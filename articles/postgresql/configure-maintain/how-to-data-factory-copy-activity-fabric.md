---
title: Create a Copy Activity in Microsoft Fabric Data Factory
description: Learn how to create a copy activity in Microsoft Fabric Data Factory for Azure Database for PostgreSQL.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 04/25/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
---

# Create a copy activity in Microsoft Fabric Data Factory

The copy activity in Microsoft Fabric Data Factory can help you connect to your Azure Database for PostgreSQL flexible server instance to perform data movement and transformation activities.

The copy activity supports *copy command*, *bulk insert*, and *upsert* as write methods. To learn more, see [Configure Azure Database for PostgreSQL in a copy activity](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity).

This article has step-by-step instructions on how to create a copy activity.

## Prerequisites

- An Azure Database for PostgreSQL flexible server instance. To learn more, go to [Create an Azure Database for PostgreSQL](/azure/postgresql/flexible-server/quickstart-create-server).
- A Microsoft Fabric Data Factory [data pipeline](/fabric/data-factory/pipeline-landing-page).

## Create a copy activity

1. In Microsoft Fabric, select your workspace, switch to **Data factory**, and then select the **New item** button.

1. On the **New item** pane, search for **pipeline** and select the **Data pipeline** tile.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/create-a-new-fabric-data-factory-pipeline.png" alt-text="Screenshot that shows selections for starting the process of creating a data pipeline." lightbox="./media/how-to-data-factory-copy-activity-fabric/create-a-new-fabric-data-factory-pipeline.png":::

1. In the **New pipeline** dialog, enter a name and then select the **Create** button to create a data pipeline.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/new-pipeline-name.png" alt-text="Screenshot that shows the dialog for naming a new pipeline." lightbox="./media/how-to-data-factory-copy-activity-fabric/new-pipeline-name.png":::

1. On the **Activities** menu, select **Copy data**, and then select **Add to canvas**.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/create-copy-activity.png" alt-text="Screenshot that shows selections for copying data and adding it to a canvas." lightbox="./media/how-to-data-factory-copy-activity-fabric/create-copy-activity.png":::

1. With the copy activity selected on the data pipeline canvas, on the **General** tab, enter a name for the activity.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/give-a-name.png" alt-text="Screenshot that shows where to enter a name for a copy activity on the General tab." lightbox="./media/how-to-data-factory-copy-activity-fabric/give-a-name.png":::

1. On the **Source** tab, select or create a source connection. [Learn more about connecting to your data by using the modern get-data experience for data pipelines](/fabric/data-factory/modern-get-data-experience-pipeline).

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/select-source-connection.png" alt-text="Screenshot that shows where to select or create a source connection on the Source tab." lightbox="./media/how-to-data-factory-copy-activity-fabric/select-source-connection.png":::

   The following example shows the selection of an Azure Database for PostgreSQL table as a source connection.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/source-datasource-selected.png" alt-text="Screenshot that shows a source connection selected." lightbox="./media/how-to-data-factory-copy-activity-fabric/source-datasource-selected.png":::

1. On the **Destination** tab, select or create an Azure Database for PostgreSQL connection.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/select-destination-datasource.png" alt-text="Screenshot that shows where to select or create a destination data source on the Destination tab." lightbox="./media/how-to-data-factory-copy-activity-fabric/select-destination-datasource.png":::

1. For **Write method**, select **Copy command**, **Bulk insert**, or **Upsert**.

   ### [Copy command](#tab/copy-command)

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/copy-command.png"alt-text="Screenshot that shows an example of copy command selected as the write method." lightbox="./media/how-to-data-factory-copy-activity-fabric/copy-command.png":::

   ### [Bulk insert](#tab/bulk-insert)

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/bulk-insert.png"alt-text="Screenshot that shows an example of bulk insert selected as the write method." lightbox="./media/how-to-data-factory-copy-activity-fabric/bulk-insert.png":::

   ### [Upsert](#tab/upsert)

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/upsert.png"     alt-text="Screenshot that shows an example of upsert selected as the write method." lightbox="./media/how-to-data-factory-copy-activity-fabric/upsert.png":::

1. If a custom mapping is required, configure your mapping on the **Mapping** tab.

1. Validate your pipeline.

1. Select the **Run** button, which runs the pipeline manually.

1. Set up a [trigger for your pipeline](/fabric/data-factory/pipeline-runs).

## Specify the behavior of key columns on upsert

When you upsert data by using the Azure Database for PostgreSQL connector, you need to specify fields called *key columns*. You specify them in the **Key columns** area of the **Destination** tab.

:::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/select-key-columns.png" alt-text="Screenshot that shows the area for key columns on the Destination tab." lightbox="./media/how-to-data-factory-copy-activity-fabric/select-key-columns.png":::

There are two acceptable ways to use key columns:

- Select **New** and add all the primary key columns of the table for the destination data source.

   :::image type="content" source="./media/how-to-data-factory-copy-activity-fabric/providing-all-key-columns.png" alt-text="Screenshot that shows an example with all key columns for a destination data source." lightbox="./media/how-to-data-factory-copy-activity-fabric/providing-all-key-columns.png":::

- Select **New** and add one or more unique columns of the table for the destination data source.

## Related content

- [Configure Azure Database for PostgreSQL in a copy activity](/fabric/data-factory/connector-azure-database-for-postgresql-copy-activity)
- [Azure Database for PostgreSQL connector overview](/fabric/data-factory/connector-azure-database-for-postgresql-overview)
- [Create a script activity in Microsoft Fabric Data Factory](how-to-data-factory-script-activity-fabric.md)
