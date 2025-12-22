---
title: Connect with Power BI
description: This article shows how to build Power BI reports from data on your Azure Database for PostgreSQL flexible server instance.
author: techieari
ms.author: arianap
ms.reviewer: maghan
ms.date: 09/18/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom: sfi-image-nochange
---

# Quickstart: Import data from Azure Database for PostgreSQL  in Power BI

In this Quickstart, you learn how to connect to an Azure Database for PostgreSQL flexible server instance with Power BI Desktop. With Power BI Desktop, you can visually explore your data through a free-form drag-and-drop canvas, a broad range of modern data visualizations, and an easy-to-use report authoring experience. You can import directly from the tables or import from a SELECT query. This article applies to Power BI Desktop only. Currently, Power Query online or Power BI Service is **not supported**.

## Prerequisites

- Install [Power BI desktop](https://aka.ms/pbidesktopstore).

## Connect with Power BI desktop from Azure portal

Get the connection information needed to connect to the Azure Database for PostgreSQL flexible server instance. You need the fully qualified server name and sign in credentials.

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you've created (such as **mydemoserverpbi**).
1. Select the server name.
1. From the server's **Overview** panel, Select **Power BI** setting from the left-hand menu.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-1.png" alt-text="Screenshot of viewing Power BI in Azure portal to connect to the database.":::

1. Select a database from the dropdown, for example *postgres* and then select **Get started**.
1. Download the Power BI desktop file *mydemoserverpbi_postgres.pbids*.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-2.png" alt-text="Screenshot of downloading Power BI file for the database.":::

1. Open the file in Power BI desktop.
1. Switch to **Database** tab to provide the username and password for your database server.

   > [!NOTE]
   > Windows authentication is not supported for Azure Database for PostgreSQL flexible server instances.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-3.png" alt-text="Screenshot of entering credentials to connect with Azure Database for PostgreSQL flexible server instance database.":::

1. In **Navigator**, select the data you require, then either load or transform the data.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-4.png" alt-text="Screenshot of navigator to view Azure Database for PostgreSQL flexible server instance tables.":::

## Connect to Azure Database for PostgreSQL  database from Power BI Desktop

You can connect to an Azure Database for PostgreSQL flexible server instance with Power BI desktop directly without the use of Azure portal.

### Get the Azure Database for PostgreSQL connection information

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you've created (such as **mydemoserverpbi**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.
1. Go to **Databases** page to find the database you want to connect to. Power BI desktop supports adding a connection to a single database and hence providing a database name is required for importing data.

### Add Azure Database for PostgreSQL connection in Power BI desktop

1. Select the **PostgreSQL database** option in the connector selection.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-5.png" alt-text="Screenshot of adding a postgresql connection in Power BI.":::

1. In the **PostgreSQL database** dialog, provide the name of the server and database.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-6.png" alt-text="Screeshot of Signing in to Power BI.":::

1. Select the **Database** authentication type and input your Azure Database for PostgreSQL flexible server instance credentials in the **User name** and **Password** boxes. Make sure to select the level to apply your credentials to.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-3.png" alt-text="Screenshot of entering credentials to connect with Azure Database for PostgreSQL flexible server instance database.":::

1. Once you're done, select **OK**.

1. In **Navigator**, select the data you require, then either load or transform the data.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-4.png" alt-text="Screenshot of navigator to view Azure Database for PostgreSQL flexible server instance tables.":::

## Connect to Azure Database for PostgreSQL  database from Power Query Online

To make the connection, take the following steps:

1. Select the **PostgreSQL database** option in the connector selection.

1. In the **PostgreSQL database** dialog, provide the name of the server and database.

    :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-7.png" alt-text="Screenshot of PostgreSQL connection with power query online.":::

   > [!NOTE]  
   > Data gateway is not needed for Azure Database for PostgreSQL flexible server instances.

1. Select the **Basic** authentication kind and input your Azure Database for PostgreSQL flexible server instance credentials in the **Username** and **Password** boxes.

1. If your connection isn't encrypted, clear **Use Encrypted Connection**.

1. Select **Next** to connect to the database.

1. In **Navigator**, select the data you require, then select **Transform data** to transform the data in Power Query Editor.

## Connect using advanced options

Power Query Desktop provides a set of advanced options that you can add to your query if needed.

   :::image type="content" source="./media/connect-with-power-bi-desktop/connector-power-bi-ap-8.png" alt-text="Screenshot of PostgreSQL advanced options.":::

The following table lists all of the advanced options you can set in Power Query Desktop.

| Advanced option | Description |
| --- | --- |
| Command timeout in minutes | If your connection lasts longer than 10 minutes (the default timeout), you can enter another value in minutes to keep the connection open longer. This option is only available in Power Query Desktop. |
| SQL statement | For information, go to [Import data from a database using native database query](/power-query/native-database-query). |
| Include relationship columns | If checked, includes columns that might have relationships to other tables. If this box is cleared, you won't see those columns. |
| Navigate using full hierarchy | If checked, the navigator displays the complete hierarchy of tables in the database you're connecting to. If cleared, the navigator displays only the tables whose columns and rows contain data. |

Once you've selected the advanced options you require, select **OK** in Power Query Desktop to connect to your PostgreSQL database.

## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](../configure-maintain/how-to-manage-server-portal.md).
- [Build visuals with Power BI Desktop](/power-bi/fundamentals/desktop-what-is-desktop).
- [Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL](../connectivity/connect-python.md).
- [Quickstart: Use Java and JDBC with Azure Database for PostgreSQL](../connectivity/connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data in Azure Database for PostgreSQL](../connectivity/connect-csharp.md).
- [Quickstart: Use Go language to connect and query data in Azure Database for PostgreSQL](../connectivity/connect-go.md).
- [Quickstart: Use PHP to connect and query data in Azure Database for PostgreSQL](../connectivity/connect-php.md).
- [Quickstart: Connect and query with Azure CLI with Azure Database for PostgreSQL](../connectivity/connect-azure-cli.md).
