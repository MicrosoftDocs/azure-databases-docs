---
title: Copy Activity in Azure Data Factory and Azure Synapse Analytics
description: Guide to use copy activity in Azure Data Factory and Azure Synapse Analytics for Azure Database for PostgreSQL
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/22/2025
ms.service: azure-database-postgresql
ms.subservice: data-movement
ms.topic: how-to
---

# Copy activity in Azure Data Factory and Azure Synapse Analytics

With a Linked Service, you can connect to your instance of Azure Database for PostgreSQL flexible server and use it within Azure Data Factory and Synapse Analytics activities.

The Copy Activity supports **Copy Command**, **Bulk Insert**, and **Upsert**. For more information, see [Copy and transform data in Azure Database for PostgreSQL using Azure Data Factory or Synapse Analytics](/azure/data-factory/connector-azure-database-for-postgresql?tabs=data-factory).

The next section has a step-by-step guide on how to manually create a copy activity and how to create a pipeline.

## Prerequisites

- An Azure Database for PostgreSQL flexible server instance. For more information, see [Create an Azure Database for PostgreSQL](/azure/postgresql/flexible-server/quickstart-create-server).
- (Optional) An Azure integration runtime [created within a managed virtual network](/azure/data-factory/managed-virtual-network-private-endpoint).
- An Azure Data Factory Linked Service [connected to Azure Database for PostgreSQL](../integration/how-to-connect-data-factory-private-endpoint.md).
- An [Azure Data Factory Dataset](/azure/data-factory/concepts-datasets-linked-services?tabs=data-factory) with your Azure Database for PostgreSQL.

## Create a data copy activity via the portal

1. In [Azure Data Factory Studio](https://adf.azure.com), select the **Author** hub. Hover over the **Pipelines** section, select **...** at the left, and select **New pipeline** to create a new pipeline.

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/go-to-author.png" alt-text="Screenshot that shows where to select author in Azure Data Factory.":::

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/create-a-new-pipeline.png" alt-text="Screenshot that shows where to select new pipeline.":::

1. Under **Move and transform**, drag and drop the **Copy data** activity into the pipeline.

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/create-copy-activity.png" alt-text="Screenshot that shows where to select Copy data." lightbox="media/how-to-data-factory-copy-activity-azure/create-copy-activity.png":::

1. At the **General** tab, give a name to your pipeline.

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/give-a-name.png" alt-text="Screenshot that shows where to give a name to the pipeline at the general tab." lightbox="media/how-to-data-factory-copy-activity-azure/give-a-name.png":::

1. At the **Source** tab, select or create a **Source dataset**. In this example, select an Azure Database for PostgreSQL table.

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/select-source-dataset.png" alt-text="Screenshot that shows where to select or create a source dataset at the source tab." lightbox="media/how-to-data-factory-copy-activity-azure/select-source-dataset.png":::

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/source-datasource-selected.png" alt-text="Screenshot that shows a source dataset selected." lightbox="media/how-to-data-factory-copy-activity-azure/source-datasource-selected.png":::

1. At the **Sink** tab, select or create an Azure Database for PostgreSQL dataset as **Sink dataset**, and choose the **Write method**. For more information, see [Azure Copy Activity and Write Method](/azure/data-factory/connector-azure-database-for-postgresql?tabs=data-factory).

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/select-sink-datasource.png" alt-text="Screenshot that shows where to select or create a sink datasource at sink tab." lightbox="media/how-to-data-factory-copy-activity-azure/select-sink-datasource.png":::

1. Select between **Copy command**, **Bulk insert**, and **Upsert** for the **Write method**.

   #### [Copy Command](#tab/copy-command)

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/copy-command.png" alt-text="Screenshot that shows an example of copy command selected." lightbox="media/how-to-data-factory-copy-activity-azure/copy-command.png":::

   #### [Bulk Insert](#tab/bulk-insert)

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/bulk-insert.png" alt-text="Screenshot that shows of bulk insert selected." lightbox="media/how-to-data-factory-copy-activity-azure/bulk-insert.png":::

   #### [Upsert](#tab/upsert)

   Optionally, provide the key columns. In this example, select **New** and add the two primary key columns of this sink dataset.

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/providing-all-key-columns.png" alt-text="Screenshot that shows an example in providing all key columns." lightbox="media/how-to-data-factory-copy-activity-azure/providing-all-key-columns.png":::

1. If a custom mapping is required, configure your mapping in the **Mapping** tab.
1. Validate your pipeline.
1. Select **Debug** to run the pipeline manually.
1. Set up a [trigger for your pipeline](/azure/data-factory/concepts-pipeline-execution-triggers).

For JSON payload examples, see [Azure Database for PostgreSQL as sink](/azure/data-factory/connector-azure-database-for-postgresql?tabs=data-factory#azure-database-for-postgresql-as-sink).

## Key columns behavior on upsert

When you upsert data with the Azure Database for PostgreSQL connector, you can specify optional fields called **Key Columns**.

:::image type="content" source="media/how-to-data-factory-copy-activity-azure/select-optional-key-columns.png" alt-text="Screenshot that shows optional key columns." lightbox="media/how-to-data-factory-copy-activity-azure/select-optional-key-columns.png":::
There are three acceptable ways to use the **Key Columns**:
1. Select **New** and add all the primary key columns of the sink datasource table

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/providing-all-key-columns.png" alt-text="Screenshot that shows an example with all key columns." lightbox="media/how-to-data-factory-copy-activity-azure/providing-all-key-columns.png":::

1. Select **New** and add one or more unique columns of the sink datasource table
1. Leave the **Key columns** empty. In this case, the connector finds the primary key columns and uses them as **Key columns**

   :::image type="content" source="media/how-to-data-factory-copy-activity-azure/empty-key-columns.png" alt-text="Screenshot that shows an example with no key columns selected." lightbox="media/how-to-data-factory-copy-activity-azure/empty-key-columns.png":::

## Related content

- [Script activity in Azure Data Factory](how-to-data-factory-script-activity-azure.md)
- [How to connect to Azure Data Factory private endpoint](../integration/how-to-connect-data-factory-private-endpoint.md)
- [Networking with Private Link in Azure Database for PostgreSQL](../network/concepts-networking-private-link.md)
