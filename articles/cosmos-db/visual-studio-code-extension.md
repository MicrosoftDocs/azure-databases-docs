---
title: Use Visual Studio Code to Connect and Manage Resources
description: Learn how to connect to Azure Cosmos DB for NoSQL by using Visual Studio Code.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 10/14/2025
ai-usage: ai-assisted
zone_pivot_groups: azure-cosmos-db-apis-nosql-mongodb
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
applies-to:
  - ✅ NoSQL
  - ✅ MongoDB
---

# Use Visual Studio Code to connect and query Azure Cosmos DB instances

[Visual Studio Code](https://code.visualstudio.com/docs) is a versatile code editor for Linux, macOS, and Windows, supporting numerous extensions. This quickstart shows you how to connect to Azure Cosmos DB for NoSQL and Azure Cosmos DB for MongoDB using Visual Studio Code. It covers performing core database operations, including querying, inserting, updating, and deleting data.

::: zone pivot="api-nosql"

## Prerequisites

- An Azure Cosmos DB for NoSQL account configured with a database and container. Use any of these quickstarts here to set up a resource:
    - [Portal](quickstart-portal.md)
    - [Azure CLI](quickstart-template-bicep.md)

## Install extension

To connect and manage data in Azure Cosmos DB within Visual Studio, first install the **Azure Databases** extension.

1. Open Visual Studio Code.
1. Access the **Extensions** pane by selecting **View > Extensions**  or using the shortcut **Ctrl + Shift + X** on Windows and **Command + Shift + X** on macOS.
1. In the search bar, type [DocumentDB for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) and select the extension. Then, select **Install**.
1. After installation, reload Visual Studio Code if prompted.

### Connecting to an Azure Cosmos DB for NoSQL

1. In Visual Studio Code, go to the **Azure** pane (select the **Azure** icon in the Activity Bar).

1. Sign in to your Azure Cosmos DB for NoSQL account via Microsoft Entra ID:

    > [!NOTE]
    > Use Microsoft Entra ID role-based access control when accessing your Azure Cosmos DB resources.

1. Once you're signed in, in the Azure tree view, find your Azure Subscription and drill down to Azure Cosmos DB.

1. Select an existing account or right-click to create a new resource.

## Query and display your data

The following steps use the Query Editor to execute a query and view the results of the query:

1. In the menu for your collection, right-click on the collection to open the Query Editor in Preview.

     :::image type="content" source="media/visual-studio-code-extension/open-query-editor.png" lightbox="media/visual-studio-code-extension/open-query-editor.png" alt-text="Screenshot of the query editor in Visual Studio Code.":::

1. Run the query provided in the query editor to display your data in **Table View**:

    :::image type="content" source="media/visual-studio-code-extension/view-query-editor-results.png" lightbox="media/visual-studio-code-extension/view-query-editor-results.png" alt-text="Screenshot of the query editor results in Visual Studio Code.":::

1. Explore your data in other supported views:

    - **JSON View**: See the raw data structure.

        :::image type="content" source="media/visual-studio-code-extension/view-json-view.png" lightbox="media/visual-studio-code-extension/view-json-view.png" alt-text="Screenshot of the query editor results in json view.":::

    - **Tree View**: Easily explore nested data.

        :::image type="content" source="media/visual-studio-code-extension/view-tree-view.png" lightbox="media/visual-studio-code-extension/view-tree-view.png" alt-text="Screenshot of the query editor results in tree view.":::

## View query and index metrics

Within the query editor, view more query and index metrics to better help optimize your query performance.

1. Select the **Stats** tab next to the query **Results**.
    :::image type="content" source="media/visual-studio-code-extension/view-query-stats.png" lightbox="media/visual-studio-code-extension/view-query-stats.png" alt-text="Screenshot of the query stats in Visual Studio Code.":::

1. For more information on the metric definitions, see the [query metrics documentation](query-metrics.md).

## Insert, Edit, and Delete documents

- **Real-time document editing**: Add, view, edit, and delete documents instantly, with changes reflected in real-time.

- **Import from JSON**: Load your data quickly from JSON files.
    :::image type="content" source="media/visual-studio-code-extension/edit-documents.png" lightbox="media/visual-studio-code-extension/edit-documents.png" alt-text="Screenshot of edit documents in Visual Studio Code.":::


## Export query results

- **Download results**: Download query results to CSV or JSON files.
   :::image type="content" source="media/visual-studio-code-extension/export-results.png" lightbox="media/visual-studio-code-extension/export-results.png" alt-text="Screenshot of export results in Visual Studio Code.":::

## Related content

- [Get started with the API for NoSQL](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)

::: zone-end

::: zone pivot="api-mongodb"

## Prerequisites

- An Azure Cosmos DB for NoSQL account configured with a database and container.
- MongoDB shell (mongosh) installed for command-line interactions (optional but recommended).

## Install extension

To connect and manage data in Azure Cosmos DB, you need to install the **Azure Databases** extension for Visual Studio Code.

1. Open Visual Studio Code.
1. Access the **Extensions** pane by selecting **View > Extensions** or using the shortcut **Ctrl + Shift + X** on Windows and **Command + Shift + X** on macOS.
1. In the search bar, type [DocumentDB for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) and select the extension. Then, select **Install**.
1. After installation, reload Visual Studio Code if prompted.

## Connecting to a MongoDB workload

Now, connect to the MongoDB workload in Azure Cosmos DB for MongoDB.

1. In the **Workspace** panel, expand the **MongoDB accounts** section.

1. Here, you can view all your MongoDB accounts. Connect to a new MongoDB account using your credentials.

    > [!NOTE]
    > All successfully connected MongoDB clusters will remain listed in the MongoDB accounts section, even after closing Visual Studio Code.

## Intuitive Data Management

Easily manage your databases within Visual Studio Code:

- **Create and Drop Databases/Collections**: Create or delete databases and collections using the context menu on your account, database, or collection in the resource panel.

- **Import from JSON**: Quickly import data from JSON files into your collection.
    - **Initiate Import**
        1. Right-click on the collection name in the resource view and select **Import Documents into Collection**.
        1. Alternatively, open the "Collection View" by clicking on the **Documents** entry of your collection, then select the **Import** button.
    - **Select JSON File**
        1. Browse to locate the *.json file containing your data.
        1. Confirm to start the import process.

- **Export Data**: Save collections or query results as JSON for backup or sharing.
    - **Initiate Export**:
        - **Option 1**
            1. Right-click on the collection name in the resource view and select **Export Documents from Collection** to export the entire collection.
        - **Option 2**
            1. Open the "Collection View" by clicking on the **Documents** entry of your collection, then select the **Export** button.
            1. Choose to export either the entire collection or the results of the current query.
    - **Specify Destination File**:
        1. Enter the name and location for the destination *.json file.
        1. Confirm export to start saving the data.

- **Real-Time Document Editing**: Instantly add, view, edit, and delete documents with real-time updates.
    - **Open Document Editing**:
        - Access document editing options directly within the "Collection View." These controls are conveniently located above the data view for easy access.
    - **Available Actions**:
        - **Add**: Create new documents within the collection.
        - **View**: View the content of the selected document.
        - **Edit**: Edit the content of selected documents.
        - **Delete**: Remove selected documents with changes reflected immediately.

:::image type="content" source="media/visual-studio-code-extension/vcore-vs-code-screenshot.png" alt-text="Screenshot of VS-code extension of an MongoDB instance." lightbox="media/visual-studio-code-extension/vcore-vs-code-screenshot.png":::

## Powerful Query Tools

Run and refine your queries seamlessly:

- **Instant Results**: Immediately view query results in your preferred format—Table, JSON, or Tree view.
    - Switch views easily using the **View** dropdown menu.

- **Execute Queries Directly**: Write and execute MongoDB queries with features like syntax highlighting and autocompletion.
    - To run your query, select the **Find Query** button or press `Ctrl/Cmd+Enter` in the query editor.

> [!NOTE]
> Currently, only find filter queries are supported, with expanded query capabilities coming soon.

## Flexible Data Views

Explore your data using multiple views for different perspectives:

- **JSON View**: See the raw JSON data structure.

  :::image type="content" source="media/visual-studio-code-extension/vcore-vs-code-json-view.png" alt-text="Screenshot of VS-code extension of an MongoDB instance in JSON view." lightbox="media/visual-studio-code-extension/vcore-vs-code-json-view.png":::

- **Tree View**: Navigate and explore nested data effortlessly.

  :::image type="content" source="media/visual-studio-code-extension/vcore-vs-code-tree-view.png" alt-text="Screenshot of VS-code extension of an MongoDB instance in Tree view." lightbox="media/visual-studio-code-extension/vcore-vs-code-tree-view.png":::

- **Table View**: Quickly scan data and drill down into nested documents.

    - **To drill down**: Find entries with the `{}` icon, which indicate embedded objects. Double-click to expand and view contents.

    - **To go back**: Return to previous levels using the navigation breadcrumbs below the Table View.

  :::image type="content" source="media/visual-studio-code-extension/vcore-vs-code-table-view.png" alt-text="Screenshot of VS-code extension of an MongoDB instance in Table view." lightbox="media/visual-studio-code-extension/vcore-vs-code-table-view.png":::

## Mongo Shell Integration

Command-line functionality is available:

- **Launch `mongosh`**: Execute advanced MongoDB commands directly from Visual Studio Code.

> [!NOTE]
> The MongoDB shell (`mongosh`) isn't included with the extension. It must be installed separately and configured manually.

## Cluster Management

Stay on top of your resources:

- **View Cluster Details**: Check your cluster’s tier, server version, and resource usage.

- **Manage Tags**: Organize your clusters with tags that sync with the Azure portal.

::: zone-end
