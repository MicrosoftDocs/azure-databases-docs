---
title: Power BI tutorial for Azure Cosmos DB
description: Use this Power BI tutorial to import JSON, create insightful reports, and visualize data using the Azure Cosmos DB.
author: Rodrigossz
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 09/09/2024
ms.author: rosouz
---

# Visualize Azure Cosmos DB data using Power BI
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This article describes the steps required to connect Azure Cosmos DB data to [Power BI](https://powerbi.microsoft.com/) Desktop. 

You can connect to Azure Cosmos DB from Power BI desktop by using one of these options:
* Use [Mirroring in Microsoft Fabric](/fabric/database/mirrored-database/azure-cosmos-db?context=/azure/cosmos-db/context/context) to replicate Azure Cosmos DB data into Fabric OneLake. 
  Any changes to your database are automatically synced to Fabric OneLake in near real-time, without affecting the performance of your source database or consuming Resource Units (RUs).

  Power BI reports can then access data directly from OneLake using DirectLake mode. With the enhanced Copilot features in Power BI within Fabric, you can tap into generative AI to gain key business insights.
  
* Use [Azure Synapse Link](../synapse-link.md) to build Power BI reports with no performance or cost impact to your transactional workloads, and no ETL pipelines.
   
   You can either use [DirectQuery](/power-bi/connect-data/service-dataset-modes-understand#directquery-mode) or [import](/power-bi/connect-data/service-dataset-modes-understand#import-mode) mode. With [DirectQuery](/power-bi/connect-data/service-dataset-modes-understand#directquery-mode), you can build dashboards/reports    using live data from your Azure Cosmos DB accounts, without importing or copying the data into Power BI.

* Connect Power BI Desktop to Azure Cosmos DB account with the Azure Cosmos DB connector for Power BI. This option is only available in import mode and will consume RUs allocated for your transactional workloads.

> [!NOTE]
>  Reports created in Power BI Desktop can be published to PowerBI.com. Direct extraction of Azure Cosmos DB data cannot be performed from PowerBI.com. 

## Prerequisites
Before following the instructions in this Power BI tutorial, ensure that you have access to the following resources:

* [Download the latest version of Power BI Desktop](https://powerbi.microsoft.com/desktop).

* [Create an Azure Cosmos DB database account](quickstart-portal.md) and add data to your Azure Cosmos DB containers.

To share your reports in PowerBI.com, you must have an account in PowerBI.com.  To learn more about Power BI and Power BI Pro, see [https://powerbi.microsoft.com/pricing](https://powerbi.microsoft.com/pricing).

## Let's get started
### Building BI reports using Mirroring in Microsoft Fabric

You can enable mirroring on your existing Azure Cosmos DB containers and build BI reports/dashboards on this data, in near real-time.
For instructions to get started with Fabric and mirroring, visit [mirroring tutorial for Azure Cosmos DB.](/fabric/database/mirrored-database/azure-cosmos-db-tutorial?context=/azure/cosmos-db/context/context)

### Building BI reports using Azure Synapse Link

You can enable Azure Synapse Link on your existing Azure Cosmos DB containers and build BI reports on this data, in just a few clicks using Azure Cosmos DB portal. Power BI will connect to Azure Cosmos DB using Direct Query mode, allowing you to query your live Azure Cosmos DB data, without impacting your transactional workloads. 

To build a Power BI report/dashboard: 

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your Azure Cosmos DB account.

1. From the **Integrations** section, open the **Power BI** pane and select **Get started**.

   > [!NOTE]
   > Currently, this option is only available for API for NoSQL accounts. You can create T-SQL views directly in Synapse serverless SQL pools and build BI dashboards for Azure Cosmos DB for MongoDB. See ["Use Power BI and serverless Synapse SQL pool to analyze Azure Cosmos DB data with Synapse"](../synapse-link-power-bi.md) for more information. 

1. From the **Enable Azure Synapse Link** tab, you can enable Synapse Link on your account from **Enable Azure Synapse link for this account** section. If Synapse Link is already enabled for your account, you won't see this tab. This step is a prerequisite to start enabling Synapse Link on your containers.

   > [!NOTE]
   > Enabling Azure Synapse Link has cost implications. See [Azure Synapse Link pricing](../synapse-link.md#pricing) section for more details.

1. Next from the **Enable Azure Synapse Link for your containers** section, choose the required containers to enable Synapse Link.

   * If you already enabled Synapse Link on some containers, you will see the checkbox next to the container name is selected. You may optionally deselect them, based on the data you'd like to visualize in Power BI.

   * If Synapse Link isn't enabled, you can enable this on your existing containers. 

     If enabling Synapse Link is in progress on any of the containers, the data from those containers won't be included. You should come back to this tab later and import data when the containers are enabled.

   :::image type="content" source="../media/integrated-power-bi-synapse-link/synapse-link-progress-existing-containers.png" alt-text="Progress of Synapse Link enabled on existing containers." border="true" lightbox="../media/integrated-power-bi-synapse-link/synapse-link-progress-existing-containers.png":::

1. Depending on the amount of data in your containers, it may take a while to enable Synapse Link. To learn more, see [enable Synapse Link on existing containers](../configure-synapse-link.md#update-analytical-ttl) article.  

   You can check the progress in the portal as shown in the following screen. **Containers are enabled with Synapse Link when the progress reaches 100%.**

   :::image type="content" source="../media/integrated-power-bi-synapse-link/synapse-link-existing-containers-registration-complete.png" alt-text="Synapse Link successfully enabled on the selected containers." border="true" lightbox="../media/integrated-power-bi-synapse-link/synapse-link-existing-containers-registration-complete.png":::

1. From the **Select workspace** tab, choose the Azure Synapse Analytics workspace and select **Next**. This step will automatically create T-SQL views in Synapse Analytics, for the containers selected earlier. For more information on T-SQL views required to connect your Azure Cosmos DB to Power BI, see [Prepare views](/azure/synapse-analytics/sql/tutorial-connect-power-bi-desktop#3---prepare-view) article.
   > [!NOTE]
   >  Your Azure Cosmos DB container proprieties will be represented as columns in T-SQL views, including deep nested JSON data. This is a quick start for your BI dashboards. These views will be available in your Synapse workspace/database; you can also use these exact same views in Synapse Workspace for data exploration, data science, data engineering, etc. Please note that advanced scenarios may demand more complex views or fine tuning of these views, for better performance. For more information. see [best practices for Synapse Link when using Synapse serverless SQL pools](/azure/synapse-analytics/sql/resources-self-help-sql-on-demand#azure-cosmos-db-performance-issues) article.
    
1. You can either choose an existing workspace or create a new one. To select an existing workspace, provide the **Subscription**, **Workspace**, and the **Database** details. Azure portal will use your Microsoft Entra credentials to automatically connect to your Synapse workspace and create T-SQL views. Make sure you have "Synapse administrator" permissions to this workspace.

   :::image type="content" source="../media/integrated-power-bi-synapse-link/synapse-create-views.png" alt-text="Connect to Synapse Link workspace and create views." border="true" lightbox="../media/integrated-power-bi-synapse-link/synapse-create-views.png":::

1. Next, select **Download .pbids** to download the Power BI data source file. Open the downloaded file. It contains the required connection information and opens Power BI desktop.

   :::image type="content" source="../media/integrated-power-bi-synapse-link/download-powerbi-desktop-files.png" alt-text="Download the Power BI desktop files in .pbids format." border="true" lightbox="../media/integrated-power-bi-synapse-link/download-powerbi-desktop-files.png":::

1. You can now connect to Azure Cosmos DB data from Power BI desktop. A list of T-SQL views corresponding to the data in each container are displayed.

   For example, the following screen shows vehicle fleet data. You can load this data for further analysis or transform it before loading.

   :::image type="content" source="../media/integrated-power-bi-synapse-link/powerbi-desktop-select-view.png" alt-text="T-SQL views corresponding to the data in each container." border="true" lightbox="../media/integrated-power-bi-synapse-link/powerbi-desktop-select-view.png":::

1. You can now start building the report using Azure Cosmos DB's analytical data. Any changes to your data will be reflected in the report, as soon as the data is replicated to analytical store, which typically happens in a couple of minutes.


### Building BI reports using Power BI connector
> [!NOTE]
> Connecting to Azure Cosmos DB with the Power BI connector is currently supported for Azure Cosmos DB for NoSQL and API for Gremlin accounts only.

1. Run Power BI Desktop.

2. You can **Get Data**, see **Recent Sources**, or **Open Other Reports** directly from the welcome screen. Select the "X" at the top right corner to close the screen. The **Report** view of Power BI Desktop is displayed.
   
   :::image type="content" source="./media/powerbi-visualize/power_bi_connector_pbireportview.png" alt-text="Power BI Desktop Report View - Power BI connector":::

3. Select the **Home** ribbon, then click on **Get Data**.  The **Get Data** window should appear.

4. Click on **Azure**, select **Azure Cosmos DB (Beta)**, and then click **Connect**. 

   :::image type="content" source="./media/powerbi-visualize/power_bi_connector_pbigetdata.png" alt-text="Power BI Desktop Get Data - Power BI connector":::

5. On the **Preview Connector** page, click **Continue**. The **Azure Cosmos DB** window appears.

6. Specify the Azure Cosmos DB account endpoint URL you would like to retrieve the data from as shown below, and then click **OK**. To use your own account, you can retrieve the URL from the URI box in the **Keys** blade of the Azure portal. Optionally you can provide the database name, collection name or use the navigator to select the database and collection to identify where the data comes from.
   
7. If you're connecting to this endpoint for the first time, you're prompted for the account key. For your own account, retrieve the key from the **Primary Key** box in the **Read-only Keys** blade of the Azure portal. Enter the appropriate key and then click **Connect**.
   
   We recommend that you use the read-only key when building reports. This prevents unnecessary exposure of the primary key to potential security risks. The read-only key is available from the **Keys** blade of the Azure portal. 
    
8. When the account is successfully connected, the **Navigator** pane appears. The **Navigator** shows a list of databases under the account.

9. Click and expand on the database where the data for the report comes from. Now, select a collection that contains the data to retrieve.
    
    The Preview pane shows a list of **Record** items.  A Document is represented as a **Record** type in Power BI. Similarly, a nested JSON block inside a document is also a **Record**. To view the properties documents as columns, click on the grey button with two arrows in opposite directions that symbolize the expansion of the record. It's located on the right of the container's name, in the same preview pane.

10. Power BI Desktop Report view is where you can start creating reports to visualize data.  You can create reports by dragging and dropping fields into the **Report** canvas.

11. There are two ways to refresh data: ad hoc and scheduled. Simply click **Refresh Now** to refresh the data. Check Power BI documentation for more information about the scheduled refresh option.

## Known issues and limitations

* For partitioned Cosmos DB containers, a SQL query with an aggregate function is passed down to Cosmos DB if the query also contains a filter (WHERE clause) on the Partition Key. If the aggregate query doesn't contain a filter on the Partition Key, the aggregation is performed by the connector.

* The connector doesn't pass down an aggregate function if it's called upon after TOP or LIMIT is applied. Cosmos DB processes the TOP operation at the end when processing a query. For example, in the following query, TOP is applied in the subquery, while the aggregate function is applied on top of that result set:

   SELECT COUNT(1) FROM (SELECT TOP 4 * FROM EMP) E

* If DISTINCT is provided in an aggregate function, the connector doesn't pass the aggregate function down to Cosmos DB if a DISTINCT clause is provided in an aggregate function. When present in an aggregate function, DISTINCT isn't supported by the Cosmos DB SQL API.

* For the SUM aggregate function, Cosmos DB returns undefined as the result set if any of the arguments in SUM are string, boolean, or null. However, if there are null values, the connector passes the query to Cosmos DB in such a way that it asks the data source to replace a null value with zero as part of the SUM calculation.

* For the AVG aggregate function, Cosmos DB returns undefined as result set if any of the arguments in SUM are string, boolean, or null. The connector exposes a connection property to disable passing down the AVG aggregate function to Cosmos DB in case this default Cosmos DB behavior needs to be overridden. When AVG passdown is disabled, it isn't passed down to Cosmos DB, and the connector handles performing the AVG aggregation operation itself. For more information, go to "Enable AVERAGE function Passdown" in Advanced options.

* Azure Cosmos DB Containers with large partition key aren't currently supported in the connector.

* Aggregation passdown is disabled for the following syntax due to server limitations:

  * When the query isn't filtering on a partition key or when the partition key filter uses the OR operator with another predicate at the top level in the WHERE clause.

  * When the query has one or more partition keys appear in an IS NOT NULL clause in the WHERE clause.

* The V2 connector doesn't support complex data types such as arrays, objects, and hierarchical structures. We recommend the [Fabric Mirroring for Azure Cosmos DB]([/articles/cosmos-db/analytics-and-business-intelligence-overview.md](/fabric/database/mirrored-database/azure-cosmos-db) feature for those scenarios.

* The V2 connector uses sampling of the first 1,000 documents to come up with the inferred schema. It's not recommended for schema evolution scenarios when only part of the documents are updated. As an example, a newly added property to one document in a container with thousands of documents may not be included in the inferred schema. We recommend the [Fabric Mirroring for Azure Cosmos DB](/fabric/database/mirrored-database/azure-cosmos-db) feature for those scenarios.

* Currently the V2 connector doesn't support non-string values in object properties.

* Filter passdown is disabled for the following syntax due to server limitations:

* When the query containing one or more aggregate columns is referenced in the WHERE clause.
                           
## Next steps
* To learn more about Power BI, see [Get started with Power BI](https://powerbi.microsoft.com/documentation/powerbi-service-get-started/).
* To learn more about Azure Cosmos DB, see the [Azure Cosmos DB documentation landing page](../index.yml).
