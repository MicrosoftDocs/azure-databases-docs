---
title: Connect Using Visual Studio Code
description: Learn how to connect to Azure DocumentDB using Visual Studio Code with the DocumentDB extension. Perform database operations like querying, inserting, updating, and deleting data.
author: seesharprun
ms.author: sidandrews
ms.topic: how-to
ms.date: 10/14/2025
ms.custom:
  - sfi-image-nochange
  - sfi-ropc-nochange
ai-usage: ai-assisted
---

# Connect to Azure DocumentDB using the DocumentDB extension for Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/docs) is a versatile code editor for Linux, macOS, and Windows, supporting numerous extensions. This quickstart shows you how to connect to an Azure DocumentDB cluster using the [DocumentDB](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) extension in Visual Studio Code. It covers performing core database operations, including querying, inserting, updating, and deleting data.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- MongoDB Shell. For more information, see [install MongoDB shell](https://www.mongodb.com/try/download/shell)

- Firewall rules that allow your client to connect to the cluster. For more information, see [configure firewall](how-to-configure-firewall.md).

## Install the extension

Start by installing the **DocumentDB** extension in Visual Studio Code. This extension is used to connect to both Azure DocumentDB and native DocumentDB clusters.

1. Open **Visual Studio Code**.

1. Navigate to the **Extensions** view by selecting the corresponding icon in the Activity Bar, or use the `Ctrl+Shift+X` keyboard shortcut.

1. Search for the term `DocumentDB` and locate the **DocumentDB for VS Code** extension.

1. Select the **Install** button for the extension.

    > [!TIP]
    > You can also select the **Install** button in the extension's details view.

1. Wait for the installation to complete. Reload Visual Studio Code if prompted.

## Connect to cluster

Now, connect to your existing cluster using Service Discovery. Azure Service Discovery can find DocumentDB instances either running on Azure Virtual Machines or Azure DocumentDB. At this step, use Service Discovery to find your existing Azure DocumentDB cluster.

1. Navigate to the **DocumentDB** extension by selecting the corresponding icon in the Activity Bar.

1. In the **DocumentDB Connections** pane, select **+ New Connection...**.

1. In the first dialog, select **Service Discovery**.

1. In the next dialog, select **Azure DocumentDB - Azure Service Discovery**.

1. Select your Azure subscription.

    > [!IMPORTANT]
    > If you aren't signed in to any Azure subscriptions, you're prompted at this point to manage the subscriptions associated with Visual Studio Code. You must at least have one associated subscription to proceed with the next steps.

1. Select your existing Azure DocumentDB cluster to connect to the cluster.

    > [!TIP]
    > In many corporate environments, developer machine IP addresses are hidden due to a VPN or other corporate network settings. In these cases, you can temporarily allow access to all IP addresses by adding the `0.0.0.0` - `255.255.255.255` IP address range as a firewall rule. Use this firewall rule only temporarily as a part of connection testing and development. For more information, see [configure firewall](how-to-configure-firewall.md#grant-access-from-your-ip-address).

1. Observe the new node in the **DocumentDB Connections** pane for your existing cluster.

## Manage cluster resources

First, use the extension to manage databases and collections within the cluster.

1. In the **DocumentDB Connections** pane, expand the node for your cluster.

1. Select **+ Create Database...**.

1. Enter a unique name for your new database. For example, you can use the name **store**.

1. Expand the database node, and then select **+ Create Collection...**.

1. Enter a unique name for your new collection. For example, you can use the name **products**.

1. Open the context menu for the database node. Then, select **Create Collection...** again.

1. Enter another unique name for the second new collection. For example, use the name **employees**.

1. Open the context menu for one of the collection nodes. Then, select **Delete Collection...**.

    > [!TIP]
    > Alternatively, use the context menu for a database node to delete the corresponding database.

## Migrate and modify documents

Next, use the built-in tools to edit an existing document, import multiple documents, or export documents as JSON files.

1. In Visual Studio Code, create a new JSON file with a unique name. For example, use the name *inventory.json*.

1. Enter the following six products into the JSON file as an array.

    | | Name | Category | Quantity | Price | Sale |
    | --- | --- | --- | --- | --- | --- |
    | **`00000000-0000-0000-0000-000000004001`** | `Raiot Jacket` | `gear-paddle-safety-gear` | 909 | 42.00 | ❌ No |
    | **`00000000-0000-0000-0000-000000004007`** | `Xenmon Mountain Bike` | `gear-cycle-mountain-bikes` | 12 | 1399.00 | ✅ Yes |
    | **`00000000-0000-0000-0000-000000004018`** | `Windry Mittens` | `apparel-accessories-gloves-and-mittens` | 121 | 35 | ❌ No |
    | **`00000000-0000-0000-0000-000000004025`** | `Metix Sleeping Bag` | `gear-camp-sleeping-bags` | 118 | 150.00 | ✅ Yes |
    | **`00000000-0000-0000-0000-000000004058`** | `Complete Camp Cookware Set` | `gear-camp-cookware` | 170 | 88.00 | ✅ Yes |
    | **`00000000-0000-0000-0000-000000004318*`** | `Niborio Tent` | `gear-camp-tents` | 140 | 420 | ✅ Yes |

    ```json
    [
      {
        "_id": "00000000-0000-0000-0000-000000004001",
        "name": "Raiot Jacket",
        "category": "gear-paddle-safety-gear",
        "quantity": 909,
        "price": 42.00,
        "sale": false
      },
      {
        "_id": "00000000-0000-0000-0000-000000004007",
        "name": "Xenmon Mountain Bike",
        "category": "gear-cycle-mountain-bikes",
        "quantity": 12,
        "price": 1399.00,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004018",
        "name": "Windry Mittens",
        "category": "apparel-accessories-gloves-and-mittens",
        "quantity": 121,
        "price": 35.00,
        "sale": false
      },
      {
        "_id": "00000000-0000-0000-0000-000000004025",
        "name": "Metix Sleeping Bag",
        "category": "gear-camp-sleeping-bags",
        "quantity": 118,
        "price": 150.00,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004058",
        "name": "Complete Camp Cookware Set",
        "category": "gear-camp-cookware",
        "quantity": 170,
        "price": 88.00,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004318",
        "name": "Niborio Tent",
        "category": "gear-camp-tents",
        "quantity": 140,
        "price": 420.00,
        "sale": true
      }
    ]
    ```

1. **Save** the modified file.

1. Open the context menu for one of the collections in your cluster. Then, select **Import Documents into Collection...**.

1. Wait for the import process to complete.

1. Expand the collections node and select **Documents**.

1. Observe the newly imported documents in your collection.

1. Select one of the documents. Then, select the **Edit** icon in the menu of the **Documents** view.

1. Update the value of the `price` property for the document. For example, update the price of the **`Windry Mittens`** product from `35.00` to `45.00`.

    ```json
    {
      "_id": "00000000-0000-0000-0000-000000004018",
      "name": "Windry Mittens",
      "category": "apparel-accessories-gloves-and-mittens",
      "quantity": 121,
      "price": 45.00,
      "sale": false
    }
    ```

1. Select **Save** to persist the changes to the document.

1. Open the context menu again for the same collection. Now, select **Export Documents from Collection...**.

1. Give the newly exported JSON file a unique name. For example, name the file *inventory-modified.json*.

1. Open the new JSON file in the Visual Studio Code editor. Observe the documents represented in the JSON array.

    ```json
    [
      {
        "_id": "00000000-0000-0000-0000-000000004001",
        "name": "Raiot Jacket",
        "category": "gear-paddle-safety-gear",
        "quantity": 909,
        "price": 42,
        "sale": false
      },
      {
        "_id": "00000000-0000-0000-0000-000000004007",
        "name": "Xenmon Mountain Bike",
        "category": "gear-cycle-mountain-bikes",
        "quantity": 12,
        "price": 1399,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004025",
        "name": "Metix Sleeping Bag",
        "category": "gear-camp-sleeping-bags",
        "quantity": 118,
        "price": 150,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004058",
        "name": "Complete Camp Cookware Set",
        "category": "gear-camp-cookware",
        "quantity": 170,
        "price": 88,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004318",
        "name": "Niborio Tent",
        "category": "gear-camp-tents",
        "quantity": 140,
        "price": 420,
        "sale": true
      },
      {
        "_id": "00000000-0000-0000-0000-000000004018",
        "name": "Windry Mittens",
        "category": "apparel-accessories-gloves-and-mittens",
        "quantity": 121,
        "price": 45,
        "sale": false
      }
    ]
    ```

    > [!NOTE]
    > Numeric precision might vary between the imported and exported documents. This variation is because JavaScript Object Notation (JSON) and Binary JSON (BSON) use different data types for numbers.

## Query and visualize data

Use the `find` filter to perform queries against your data using the MongoDB Query Language (MQL) and output the results in JSON. Then, contextualize the data using the extension as tabular information or a tree view.

1. In the **Documents** view, update the query from the default `{  }` value to the following query:

    ```mongo
    {
      "sale": true,
      "price": {
        "$gt": 100
      }
    }
    ```

1. Select **Find Query**.

1. Observe the three documents that match the query in the results.

  | | Name | Category | Quantity | Price | Sale |
  | --- | --- | --- | --- | --- | --- |
  | **`00000000-0000-0000-0000-000000004007`** | `Xenmon Mountain Bike` | `gear-cycle-mountain-bikes` | 12 | 1399.00 | ✅ Yes |
  | **`00000000-0000-0000-0000-000000004025`** | `Metix Sleeping Bag` | `gear-camp-sleeping-bags` | 118 | 150.00 | ✅ Yes |
  | **`00000000-0000-0000-0000-000000004318*`** | `Niborio Tent` | `gear-camp-tents` | 140 | 420 | ✅ Yes |

1. In the results pane, open the drop-down list for the view and select **JSON View** to observe the results as separate JSON documents.

    ```json
    {
      "_id": "00000000-0000-0000-0000-000000004007",
      "name": "Xenmon Mountain Bike",
      "category": "gear-cycle-mountain-bikes",
      "quantity": 12,
      "price": 1399,
      "sale": true
    }
    ```
    
    ```json
    {
      "_id": "00000000-0000-0000-0000-000000004025",
      "name": "Metix Sleeping Bag",
      "category": "gear-camp-sleeping-bags",
      "quantity": 118,
      "price": 150,
      "sale": true
    }
    ```
    
    ```json
    {
      "_id": "00000000-0000-0000-0000-000000004318",
      "name": "Niborio Tent",
      "category": "gear-camp-tents",
      "quantity": 140,
      "price": 420,
      "sale": true
    }
    ```

1. Finally, select **Tree View** to review the results in a hierarchical format.

    - `00000000-0000-0000-0000-000000004007` - Document
    
      - `gear-cycle-mountain-bikes` - String
      
      - `Xenmon Mountain Bike` - String
      
      - `1399` - Double
      
      - `12` - Double
      
      - `true` - Boolean

    - `00000000-0000-0000-0000-000000004025` - Document
    
      - `gear-camp-sleeping-bags` - String
    
      - `Metix Sleeping Bag` - String
    
      - `150` - Double
    
      - `118` - Double
    
      - `true` - Boolean
    
    - `00000000-0000-0000-0000-000000004318` - Document
    
      - `gear-camp-tents` - String
    
      - `Niborio Tent` - String
    
      - `420` - Double
    
      - `140` - Double
    
      - `true` - Boolean

## Launch MongoDB Shell

Now, launch the MongoDB Shell (`mongosh`) with the extension connected directly to your cluster. Use the same syntax and commands you would typically use with the shell.

1. Open the context menu for the cluster. Next, select **Launch Shell**.

1. The shell launches in the default terminal for Visual Studio Code.

1. After you're successfully authenticated, observe the warning that appears.

    ```output
    ------
       Warning: Non-Genuine MongoDB Detected
       This server or service appears to be an emulation of MongoDB rather than an official MongoDB product.
    ------
    ```

    > [!TIP]
    > You can safely ignore this warning. This warning is generated because the connection string contains `cosmos.azure`. Azure DocumentDB is a native Azure platform as a service (PaaS) offering.

## Perform test queries

[!INCLUDE[Section - Connect test queries](includes/section-connect-test-queries.md)]

## Use MongoDB scrapbooks

Finally, open a scrapbook to run MQL commands directly against a collection in a manner similar to the shell.

1. Open the context menu for the collection and then select **DocumentDB Scrapbook > New DocumentDB Scrapbook**.

1. Enter the following MongoDB Query Language (MQL) commands to find products that are on sale, have a price between 100 and 1000, and a quantity greater than 50. The results only include the name, price, and quantity fields, and are sorted by price in descending order.

    ```mongo
    db.products.aggregate([
      {
        $match: {
          sale: true,
          price: { $gte: 100, $lte: 1000 },
          quantity: { $gt: 50 }
        }
      },
      {
        $project: {
          _id: 0,
          name: 1,
          price: 1,
          quantity: 1
        }
      },
      {
        $sort: { price: -1 }
      }
    ])
    ```

1. Select **Run All** to run the entire contents of the scrapbook against your current cluster.

1. Observe the output from the command.

    ```json
    [
      {
        "name": "Niborio Tent",
        "quantity": 140,
        "price": 420
      },
      {
        "name": "Metix Sleeping Bag",
        "quantity": 118,
        "price": 150
      }
    ]
    ```    

1. **Save** the scrapbook using a unique filename with the *\*.vscode-documentdb-scrapbook* extension.

## Related content

- [Connect to Azure DocumentDB using Azure Cloud Shell](how-to-connect-cloud-shell.md)
- [Connect to Azure DocumentDB using MongoDB Shell](how-to-connect-mongo-shell.md)
- [Configure the firewall for an Azure DocumentDB cluster](how-to-configure-firewall.md)
