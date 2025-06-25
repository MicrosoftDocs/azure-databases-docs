---
title: Connect With Power BI
description: This article shows how to build Power BI reports from data on Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom: sfi-image-nochange
---

# Quickstart: Import data from Azure Database for MySQL - Flexible Server in Power BI

> [!NOTE]  
> This article applies to Power BI Desktop only. Currently Power Query online or Power BI Service is **not supported**.

With Power BI Desktop you can visually explore your data through a free-form drag-and-drop canvas, a broad range of modern data visualizations, and an easy-to-use report authoring experiences. You can import directly from the tables or import from a SELECT query. In this quickstart, you learn how to connect with Azure Database for MySQL Flexible Server with Power BI Desktop.

## Prerequisites

1. Install [Power BI desktop](https://aka.ms/pbidesktopstore).
1. If you connect with MySQL database for the first time in Power BI, you need to install the Oracle [MySQL Connector/NET](https://dev.mysql.com/downloads/connector/net/) package.
1. Skip the steps below if MySQL server has SSL disabled. If SSL is enabled, then follow the steps below to install the certificate.
   1. Download the [SSL public certificate](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem).
   1. Install the SSL certificate in Trusted Root certification authorities store by following these steps:
      1. Start **certmgr.msc** Management Console on your Windows system.
      1. Right-click **Trusted Root Certification Authorities** and select **Import**.
      1. Follow the prompts in the wizard to import the root certificate (for example, DigiCertGlobalRootCA.crt.pem) and select OK.

## Connect with Power BI desktop from Azure portal

Get the connection information needed to connect to the Azure Database for MySQL Flexible Server instance. You need the fully qualified server name and sign in credentials.

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you've created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, Select **Power BI** setting from the left-hand menu.

   :::image type="content" source="media/connect-with-powerbi-desktop/use-azure-db-for-mysql-with-power-bi-desktop.png" alt-text="Screenshot of viewing Power BI in Azure portal to connect to the database." lightbox="media/connect-with-powerbi-desktop/use-azure-db-for-mysql-with-power-bi-desktop.png":::

1. Select a database from the dropdown list, for example *contactsdb* and then select **Get started**.
1. Download the Power BI desktop file *contactsdb.pbids*.

   :::image type="content" source="media/connect-with-powerbi-desktop/download-powerbi-desktop-file-for-database.png" alt-text="Screenshot of downloading Power BI file for the database." lightbox="media/connect-with-powerbi-desktop/download-powerbi-desktop-file-for-database.png":::

1. Open the file in Power BI desktop.
1. Switch to **Database** tab to provide the username and password for your database server. **Note Windows authentication is not supported for Azure Database for MySQL Flexible Server.**

   :::image type="content" source="media/connect-with-powerbi-desktop/enter-credentials.png" alt-text="Screenshot of entering credentials to connect with Azure Database for MySQL Flexible Server database." lightbox="media/connect-with-powerbi-desktop/enter-credentials.png":::

1. In **Navigator**, select the data you require, then either load or transform the data.

   :::image type="content" source="media/connect-with-powerbi-desktop/navigator.png" alt-text="Screenshot of navigator to view MySQL tables." lightbox="media/connect-with-powerbi-desktop/navigator.png":::

## Connect to MySQL database from Power BI Desktop

You can connect to Azure Database for MySQL Flexible Server with Power BI desktop directly without using the Azure portal.

### Get the MySQL connection information

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the Azure Database for MySQL Flexible Server instance you've created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.
1. Go to **Databases** page to find the database you want to connect to. Power BI desktop supports adding a connection to a single database and hence providing a database name is required for importing data.

### Add MySQL connection in Power BI desktop

1. Select the **MySQL database** option in the connector selection.

   :::image type="content" source="media/connect-with-powerbi-desktop/add-mysql-connection.png" alt-text="Screenshot of adding a mysql connection in Power BI." lightbox="media/connect-with-powerbi-desktop/add-mysql-connection.png":::

1. In the **MySQL database** dialog, provide the name of the Azure Database for MySQL Flexible Server instance and database.

   :::image type="content" source="media/connect-with-powerbi-desktop/signin.png" alt-text="Screenshot of signing into Power BI Desktop." lightbox="media/connect-with-powerbi-desktop/signin.png":::

1. Select the **Database** authentication type and input your MySQL credentials in the **User name** and **Password** boxes. Make sure to select the level to apply your credentials to.

   :::image type="content" source="media/connect-with-powerbi-desktop/enter-credentials.png" alt-text="Screenshot of entering credentials to connect with MySQL database." lightbox="media/connect-with-powerbi-desktop/enter-credentials.png":::

1. Once you're done, select **OK**.

1. In **Navigator**, select the data you require, then either load or transform the data.

   :::image type="content" source="media/connect-with-powerbi-desktop/navigator.png" alt-text="Screenshot of navigator to view MySQL tables." lightbox="media/connect-with-powerbi-desktop/navigator.png":::

## Connect to MySQL database from Power Query Online

A data gateway is required to use MySQL with Power BI query online. See [how to deploy a data gateway for MySQL](/power-bi/connect-data/service-gateway-deployment-guidance). Once data gateway is setup, take the following steps to add a new connection:

1. Select the **MySQL database** option in the connector selection.

1. In the **MySQL database** dialog, provide the name of the server and database.

    :::image type="content" source="media/connect-with-powerbi-desktop/power-query-service-signin.png" alt-text="Screenshot of MySQL connection with power query online." lightbox="media/connect-with-powerbi-desktop/power-query-service-signin.png":::

1. Select the **Basic** authentication kind and input your MySQL credentials in the **Username** and **Password** boxes.

1. If your connection isn't encrypted, clear **Use Encrypted Connection**.

1. Select **Next** to connect to the database.

1. In **Navigator**, select the data you require, then select **Transform data** to transform the data in Power Query Editor.

## Connect using advanced options

Power Query Desktop provides a set of advanced options that you can add to your query if needed. The following table lists all of the advanced options you can set in Power Query Desktop.

| Advanced option | Description |
| --- | --- |
| Command timeout in minutes | If your connection lasts longer than 10 minutes (the default timeout), you can enter another value in minutes to keep the connection open longer. This option is only available in Power Query Desktop. |
| SQL statement | For information, go to [Import data from a database using native database query](/power-query/native-database-query). |
| Include relationship columns | If checked, includes columns that might have relationships to other tables. If this box is cleared, you can't see those columns. |
| Navigate using full hierarchy | If checked, the navigator displays the complete hierarchy of tables in the database you're connecting to. If cleared, the navigator displays only the tables whose columns and rows contain data. |

Once you've selected the advanced options you require, select **OK** in Power Query Desktop to connect to your MySQL database.

## Next step

> [!div class="nextstepaction"]
> [Build visuals with Power BI Desktop](/power-bi/fundamentals/desktop-what-is-desktop)
