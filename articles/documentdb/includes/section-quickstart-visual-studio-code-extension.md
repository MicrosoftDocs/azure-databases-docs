---
ms.topic: include
ms.date: 10/14/2025
---

Use the **DocumentDB** extension in Visual Studio Code to perform core database operations, including querying, inserting, updating, and deleting data.

1. Open **Visual Studio Code**.

1. Navigate to the **Extensions** view and search for the term `DocumentDB`. Locate the **DocumentDB for VS Code** extension.

1. Select the **Install** button for the extension. Wait for the installation to complete. Reload Visual Studio Code if prompted.

1. Navigate to the **DocumentDB** extension by selecting the corresponding icon in the Activity Bar.

1. In the **DocumentDB Connections** pane, select **+ New Connection...**.

1. In the dialog, select **Service Discovery** and then **Azure DocumentDB - Azure Service Discovery**.

1. Select your Azure subscription and your newly created Azure DocumentDB cluster.

    > [!TIP]
    > In many corporate environments, developer machine IP addresses are hidden due to a VPN or other corporate network settings. In these cases, you can temporarily allow access to all IP addresses by adding the `0.0.0.0` - `255.255.255.255` IP address range as a firewall rule. Use this firewall rule only temporarily as a part of connection testing and development. For more information, see [configure firewall](../how-to-configure-firewall.md#grant-access-from-your-ip-address).

1. Back in the **DocumentDB Connections** pane, expand the node for your cluster and navigate to your existing document and collection nodes.

1. Open the context menu for the collection and then select **DocumentDB Scrapbook > New DocumentDB Scrapbook**.

1. Enter the following MongoDB Query Language (MQL) commands and then select **Run All**. Observe the output from the commands.

    ```mongo
    db.products.find({
      price: { $gt: 200 },
      sale: true
    })
    .sort({ price: -1 })
    .limit(3)
    ```
