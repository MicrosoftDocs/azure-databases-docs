---
title: Use Studio 3T to connect
description: Connect to an Azure DocumentDB account by using the Studio 3T community tool to query data.
author: gahl-levy
ms.author: gahllevy
ms.topic: how-to
ms.date: 08/28/2023
ms.custom:
  - sfi-image-nochange
# customer intent: As a database owner, I want to use Studio 3T so that I can connect to and query my collections.
---

# Use Studio 3T to connect to Azure DocumentDB

Studio 3T is a professional GUI that offers IDE and client tools for MongoDB. It's a popular community tool to speed up MongoDB development with a straightforward user interface.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- The [Studio 3T](https://robomongo.org/) community tool.

## Connect by using Studio 3T

To add your Azure DocumentDB cluster to the Studio 3T Connection Manager, perform the following steps:

1. Retrieve the connection information for your Azure DocumentDB instance by using [these instructions](quickstart-portal.md#get-cluster-credentials).

    :::image type="content" source="./media/connect-using-robomongo/connection-string.png" alt-text="Screenshot of the pane for connection strings.":::

1. Run the **Studio 3T** application.

1. Under **File**, select the **Connect** button to manage your connections. Then, in the **Connection Manager** dialog, select **New Connection**.

1. In the **New Connection** dialog, select the first option and paste your connection string. Then select **Next**.

    :::image type="content" source="./media/connect-using-robomongo/new-connection.png" alt-text="Screenshot of the dialog for entering  connection credentials in Studio 3T.":::

1. On the **Server** tab, enter a name for **Connection name** and double-check your connection credentials.

    :::image type="content" source="./media/connect-using-robomongo/connection-configuration.png" alt-text="Screenshot of server connection information in Studio 3T for a new connection.":::

1. On the **SSL** tab, select **Use SSL protocol to connect**.

    :::image type="content" source="./media/connect-using-robomongo/connection-ssl.png" alt-text="Screenshot of SSL details in Studio 3T for a new connection.":::

1. Select **Test Connection** to verify that you can connect, and then select **Save**.

## Next step

> [!div class="nextstepaction"]
> [Migration options](migration-options.md)
