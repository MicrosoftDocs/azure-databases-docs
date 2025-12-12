---
title: Visualize Data using Power BI
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to visualize Azure Cosmos DB data using Power BI. Import JSON, create insightful reports, and gain actionable insights.
author: jilmal
ms.author: jmaldonado
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 12/05/2025
ms.custom: build-2023
ai-usage: ai-assisted
applies-to:
  - ✅ NoSQL
---

# Visualize Azure Cosmos DB for NoSQL data using Power BI

Learn how to connect Azure Cosmos DB data to Power BI Desktop, and create insightful reports for actionable business insights.

[!INCLUDE[SynapseLinkRetirement](includes/appliesto-synapse-link-retirement.md)]

## Connecting

Connect to Azure Cosmos DB from Power BI Desktop by using one of these options:

- Use [Mirroring in Microsoft Fabric](/fabric/database/mirrored-database/azure-cosmos-db?context=/azure/cosmos-db/context/context) to replicate Azure Cosmos DB data into Fabric OneLake. When you make changes to your database, the updates are sent to Fabric OneLake quickly. This process doesn't slow down your main database or use extra resources. Power BI reports access data directly from OneLake using DirectLake mode. With the enhanced Copilot features in Power BI within Fabric, tap into generative AI to gain key business insights.

- Use [Azure Synapse Link](../synapse-link.md) to build Power BI reports with no performance or cost effect on your transactional workloads, and no extract-transform-load (ETL) pipelines. You can either use [DirectQuery](/power-bi/connect-data/service-dataset-modes-understand#directquery-mode) or [import](/power-bi/connect-data/service-dataset-modes-understand#import-mode) mode. With [DirectQuery](/power-bi/connect-data/service-dataset-modes-understand#directquery-mode), you can build dashboards/reports    using live data from your Azure Cosmos DB accounts, without importing or copying the data into Power BI.

- Connect Power BI Desktop to Azure Cosmos DB account with the Azure Cosmos DB connector for Power BI. This option is only available in import mode and consumes request units (RUs) allocated for your transactional workloads.

> [!NOTE]
> Publish reports created in Power BI Desktop to PowerBI.com. Direct extraction of Azure Cosmos DB data can't be performed from PowerBI.com.

## Prerequisites

Before you follow the instructions in this Power BI tutorial, make sure you have access to these resources:

- [Download the latest version of Power BI Desktop](https://powerbi.microsoft.com/desktop)

- [Create an Azure Cosmos DB database account](quickstart-portal.md) and add data to your Azure Cosmos DB containers.

To share your reports in PowerBI.com, you need an account in PowerBI.com. To learn more about Power BI and Power BI Pro, see [https://powerbi.microsoft.com/pricing](https://powerbi.microsoft.com/pricing).

## Building BI reports using Mirroring in Microsoft Fabric

Enable mirroring on your existing Azure Cosmos DB containers to build BI reports or dashboards on this data in near real time.
For instructions to get started with Fabric and mirroring, see [mirroring tutorial for Azure Cosmos DB](/fabric/database/mirrored-database/azure-cosmos-db-tutorial?context=/azure/cosmos-db/context/context).

## Building BI reports using Azure Synapse Link

You can enable Azure Synapse Link on your existing Azure Cosmos DB containers and build BI reports on this data, in just a few select using Azure Cosmos DB portal. Power BI connects to Azure Cosmos DB using Direct Query mode, letting you query live Azure Cosmos DB data without impacting transactional workloads.

To build a Power BI report/dashboard:

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your Azure Cosmos DB account.

1. From the Integrations section, open the Power BI pane and select Get started.

   > [!NOTE]
   > This option is currently available only for API for NoSQL accounts. You can create T-SQL views directly in Synapse serverless SQL pools and build BI dashboards for Azure Cosmos DB for MongoDB. For more information, see [Use Power BI and serverless Synapse SQL pool to analyze Azure Cosmos DB data with Synapse](../synapse-link-power-bi.md).

1. From the Enable Azure Synapse Link tab, you can enable Azure Synapse Link on your account from Enable Azure Synapse Link for this account section. If Azure Synapse Link is already enabled for your account, you can't see this tab. This step is a prerequisite to start enabling Azure Synapse Link on your containers.

   > [!NOTE]
   > Enabling Azure Synapse Link has cost implications. For more information, see [Azure Synapse Link pricing](../synapse-link.md#pricing).

1. Next from the Enable Azure Synapse Link for your containers section, choose the required containers to enable Azure Synapse Link.

   - If you already enabled Azure Synapse Link on some containers, you see the checkbox next to the container name is selected. You might optionally deselect them, based on the data you'd like to visualize in Power BI.

   - If Azure Synapse Link isn't enabled, you can enable this feature on your existing containers. If enabling Azure Synapse Link is in progress on any of the containers, the data from those containers isn't included. You should come back to this tab later and import data when the containers are enabled.

   :::image type="content" source="media/powerbi-visualize/synapse-link-progress-existing-containers.png" alt-text="Screenshot that shows progress of Azure Synapse Link enabled on existing containers." border="true" lightbox="media/powerbi-visualize/synapse-link-progress-existing-containers.png":::

1. Depending on the amount of data in your containers, it might take a while to enable Azure Synapse Link. To learn more, see [enable Azure Synapse Link on existing containers](../configure-synapse-link.md#update-analytical-ttl) article.

   You can check the progress in the portal as shown in the following screen. Containers are enabled with Azure Synapse Link when the progress reaches 100%.

   :::image type="content" source="media/powerbi-visualize/synapse-link-existing-containers-registration-complete.png" alt-text="Screenshot that shows Azure Synapse Link successfully enabled on the selected containers." border="true" lightbox="media/powerbi-visualize/synapse-link-existing-containers-registration-complete.png":::

1. From the Select workspace tab, choose the Azure Synapse Analytics workspace and select Next. This step automatically creates T-SQL views in Synapse Analytics, for the containers selected earlier. For more information on T-SQL views required to connect your Azure Cosmos DB to Power BI, see [Prepare views](/azure/synapse-analytics/sql/tutorial-connect-power-bi-desktop#3-prepare-view) article.

   > [!NOTE]
   > Your Azure Cosmos DB container proprieties are represented as columns in T-SQL views, including deep nested JSON data. This representation is a quick start for your BI dashboards. These views are available in your Synapse workspace/database; you can also use these exact same views in Synapse Workspace for data exploration, data science, or data engineering. Advanced scenarios might demand more complex views or fine tuning of these views, for better performance. For more information. see [best practices for Azure Synapse Link when using Synapse serverless SQL pools](/azure/synapse-analytics/sql/resources-self-help-sql-on-demand#azure-cosmos-db-performance-issues) article.

1. Choose an existing workspace or create a new one. To select an existing workspace, provide the Subscription, Workspace, and the Database details. Azure portal uses your Microsoft Entra credentials to automatically connect to your Synapse workspace and create T-SQL views. Make sure you have "Synapse administrator" permissions to this workspace.

   :::image type="content" source="media/powerbi-visualize/synapse-create-views.png" alt-text="Screenshot that shows how to connect to Azure Synapse Link workspace and create views." border="true" lightbox="media/powerbi-visualize/synapse-create-views.png":::

1. Next, select Download .pbids to download the Power BI data source file. Open the downloaded file. It contains the required connection information and opens Power BI desktop.

   :::image type="content" source="media/powerbi-visualize/download-powerbi-desktop-files.png" alt-text="Screenshot that shows how to download the Power BI desktop files in .pbids format." border="true" lightbox="media/powerbi-visualize/download-powerbi-desktop-files.png":::

1. You can now connect to Azure Cosmos DB data from Power BI desktop. A list of T-SQL views corresponding to the data in each container are displayed.

   For example, the following screen shows vehicle fleet data. You can load this data for further analysis or transform it before loading.

   :::image type="content" source="media/powerbi-visualize/powerbi-desktop-select-view.png" alt-text="Screenshot that shows T-SQL views corresponding to the data in each container." border="true" lightbox="media/powerbi-visualize/powerbi-desktop-select-view.png":::

1. You can now start building the report using Azure Cosmos DB's analytical data. Any changes to your data aren't reflected in the report, as soon as the data is replicated to analytical store, which typically happens in a couple of minutes.


## Building BI reports using Power BI connector

Connecting to Azure Cosmos DB with the Power BI connector is currently supported for Azure Cosmos DB for NoSQL and API for Gremlin accounts only.

1. Run Power BI Desktop.

1. You can Get Data, see Recent Sources, or Open Other Reports directly from the welcome screen. Close the screen by selecting the "X" option. The Report view of Power BI Desktop is displayed.

   :::image type="content" source="media/powerbi-visualize/power_bi_connector_pbireportview.png" alt-text="Screenshot of Power BI Desktop Report View - Power BI connector.":::

1. Select the Home ribbon, then select on Get Data. The Get Data window should appear.

1. Select on Azure, select Azure Cosmos DB (Beta), and then select Connect.

   :::image type="content" source="media/powerbi-visualize/power_bi_connector_pbigetdata.png" alt-text="Screenshot of Power BI Desktop Get Data - Power BI connector.":::

1. On the Preview Connector page, select Continue. The Azure Cosmos DB window appears.

1. Specify the Azure Cosmos DB account endpoint URL you would like to retrieve the data from, and then select OK. To use your own account, you can retrieve the URL from the URI box in the Keys section of the Azure portal. Optionally you can provide the database name, collection name or use the navigator to select the database and collection to identify where the data comes from.

1. If you're connecting to this endpoint for the first time, you're prompted for the account credentials.

1. When the account is successfully connected, the Navigator pane appears. The Navigator shows a list of databases under the account.

1. Select and expand on the database where the data for the report comes from. Now, select a collection that contains the data to retrieve.

    The Preview pane shows a list of Record items. A Document is represented as a Record type in Power BI. Similarly, a nested JSON block inside a document is also a Record. To view the properties documents as columns, select on the grey button with two arrows in opposite directions that symbolize the expansion of the record.

1. Power BI Desktop Report view is where you can start creating reports to visualize data. Create reports by dragging and dropping fields into the Report canvas.

1. There are two ways to refresh data: unplanned and scheduled. Select **Refresh Now** to refresh the data. Check Power BI documentation for more information about the scheduled refresh option.

## Known issues and limitations

- For partitioned Azure Cosmos DB containers, a SQL query with an aggregate function is passed to Azure Cosmos DB if the query contains a filter (`WHERE` clause) on the partition key. If the aggregate query doesn't include a filter on the partition key, the connector performs the aggregation.

- The connector doesn't pass an aggregate function when it follows `TOP` or `LIMIT`.

- Azure Cosmos DB processes the TOP operation at the end when processing a query. For example, in the following query, TOP is applied in the subquery, while the aggregate function is applied on top of that result set:

  ```nosql
  SELECT COUNT(1) FROM (SELECT TOP 4 - FROM EMP) E
  ```

- If `DISTINCT` is included in an aggregate function, the connector doesn't pass the aggregate function to Azure Cosmos DB. `DISTINCT` in an aggregate function isn't supported Azure Cosmos DB for NoSQL.

- For the `SUM` aggregate function, Azure Cosmos DB returns undefined if any arguments in SUM are string, boolean, or null. If there are null values, the connector passes the query to Azure Cosmos DB to replace null values with zero during the SUM calculation.

- For the `AVG` aggregate function, Azure Cosmos DB returns undefined as result set if any of the arguments in SUM are string, boolean, or null. The connector exposes a connection property to disable passing down the AVG aggregate function to Azure Cosmos DB in case this default Azure Cosmos DB behavior needs to be overridden. When `AVG` pass down is disabled, it isn't passed down to Azure Cosmos DB, and the connector handles performing the AVG aggregation operation itself. For more information, go to "Enable `AVERAGE` function Pass down" in Advanced options.

- Azure Cosmos DB containers with large partition keys aren't supported in the connector.

- Aggregation pass down is disabled for the following syntax due to server limitations:

  - The query isn't filtering on a partition key or when the partition key filter uses the `OR` operator with another predicate at the top level in the `WHERE` clause.

  - The query has one or more partition keys appear in an `IS NOT NULL` clause in the `WHERE` clause.

- The V2 connector doesn't support complex data types like arrays, objects, and hierarchical structures. Use the [Fabric Mirroring for Azure Cosmos DB](/fabric/database/mirrored-database/azure-cosmos-db) feature for those scenarios.

- The V2 connector uses sampling of the first 1,000 documents to come up with the inferred schema. This approach isn't recommended for schema evolution scenarios where only some documents are updated. As an example, a newly added property to one document in a container with thousands of documents might not be included in the inferred schema. We recommend the [Fabric Mirroring for Azure Cosmos DB](/fabric/database/mirrored-database/azure-cosmos-db) feature for those scenarios.

- The V2 connector doesn't support nonstring values in object properties.

- Filter pass down is disabled for the following syntax because of server limitations:

  - When the query containing one or more aggregate columns is referenced in the `WHERE` clause

## Related content

- Learn more about Power BI in [Get started with Power BI](https://powerbi.microsoft.com/documentation/powerbi-service-get-started/).
- Learn more about Azure Cosmos DB on the [Azure Cosmos DB documentation landing page](../index.yml).
