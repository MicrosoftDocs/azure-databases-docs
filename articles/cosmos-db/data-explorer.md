---
title: Use the Data Explorer to manage your data
titleSuffix: Azure Cosmos DB
description: Learn about the Azure Cosmos DB Data Explorer, a standalone web-based interface that allows you to view and manage the data stored in Azure Cosmos DB.
author: meredithmooreux
ms.author: merae
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 10/04/2024
# CustomerIntent: As a database developer, I want to access the Data Explorer so that I can observe my data and make queries against my data.
---

# Use the Azure Cosmos DB Data Explorer to manage your data

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

Azure Cosmos DB Data Explorer is a web-based interface that allows you to view and manage the data stored in Azure Cosmos DB.

The dedicated Azure Cosmos DB Data Explorer (<https://cosmos.azure.com>) has a few key advantages when compared to the Azure portal's Data Explorer experience, including:

- Full screen real-estate to browse data, run queries, and observe query results
- Ability to provide users without access to the Azure portal or an Azure subscription read or read-write capabilities over data in containers
- Ability to share query results with users who don't have an Azure subscription or Azure portal access

## Prerequisites

- An existing Azure Cosmos DB account.
  - If you don't have an Azure subscription, [Try Azure Cosmos DB free](https://cosmos.azure.com/try/).

## Access the Data Explorer directly using your Azure subscription

You can use access the Data Explorer directly and use your existing credentials to quickly get started with the tool.

1. Navigate to <https://cosmos.azure.com>.

1. Select **Sign In**. Sign in using your existing credentials that have access to the Azure Cosmos DB account.

1. Next, select your Azure subscription and target account from the **Select a Database Account** menu.

    ![Screenshot of the 'Select a Database Account' menu in the Data Explorer.](media/data-explorer/select-database-account.png)

## Access the Data Explorer from the Azure portal using your Azure subscription

If you're already comfortable with the Azure portal, you can navigate directly from the in-portal Data Explorer to the standalone Data Explorer.

1. Sign in to [Azure portal](https://portal.azure.com/).

1. Navigate to your existing Azure Cosmos DB account.

1. In the resource menu, select **Data Explorer**.

1. Next, select the **Open Full Screen** menu option.

    ![Screenshot of the Data Explorer page with the 'Open Full Screen' option highlighted.](media/data-explorer/open-full-screen.png)

1. In the **Open Full Screen** dialog, select **Open**.

## Configure request unit threshold

In the Data Explorer, you can configure a limit to the request units per second (RU/s) that queries use. Use this functionality to control the cost and performance in request units (RU) of your queries. This functionality can also cancel high-cost queries automatically.

1. Start in the explorer for the target Azure Cosmos DB account.

1. Select the **Settings** menu option.

    ![Screenshot of an Data Explorer page with the 'Open Settings' option highlighted.](media/data-explorer/open-settings.png)

1. In the **Settings** dialog, configure whether you want to **Enable RU threshold** and the actual **RU threshold** value.

    ![Screenshot of the individual settings to configure the request unit threshold.](media/data-explorer/configure-ru-threshold.png)

    > [!TIP]
    > The RU threshold is enabled automatically with a default value of **5,000** RUs.

## Use with Microsoft Entra authentication

You can use Microsoft Entra-based authentication within the explorer by enabling it via configuration. For more information about role-based access control, see the [security guide](security.yml).

1. Start in the explorer for the target Azure Cosmos DB account.

1. Select the **Settings** menu option.

1. In the **Settings** dialog, configure whether you want to **`Enable Entra ID (RBAC)`** using one of three possible values:

    | | Description |
    | --- | --- |
    | **Automatic (default)** | Role-based access control (RBAC) is automatically used if key-based authentication is disabled for your account. Otherwise, Data Explorer uses key-based authentication for data requests. |
    | **True** | Role-based access control is always used for data requests. If role-based access control isn't configured correctly for the account or identity, then the requests fail. |
    | **False** | Key-based authentication is always used for data requests. If key-based authentication is disabled, then the requests fail. |

    ![Screenshot of the Microsoft Entra ID role-based access control setting and three potential values.](media/data-explorer/enable-entra-auth.png)

    > [!NOTE]
    > Changing this setting to an option that uses key-based authentication could trigger a request to retrieve the primary key on behalf of the identity that is signed in.

1. Now, select the **Login for Entra ID RBAC** option in the command bar of the explorer.

    > [!TIP]
    > This step is not necessary when using the Azure Cosmos DB Data Explorer (<https://cosmos.azure.com>). The Azure Cosmos DB Data Explorer also supports the option to manually set the value of the **`Enable Entra ID (RBAC)`** to `True` using the <https://cosmos.azure.com?feature.enableAadDataPlane=true> URL.

## Known issues

Here are a few currently known issues:

- Browsing items that contain a UUID isn't supported in Data Explorer. This limitation doesn't affect loading containers, only viewing individual items or queries that include these items. To view and manage these items, users should continue to use the same tooling/SDKs that was originally used to create these items.

- HTTP 401 errors could occur due to insufficient role-based access control permissions for your Microsoft Entra ID account. This condition can be true particularly if the account has a custom role. Any custom roles must have the `Microsoft.DocumentDB/databaseAccounts/listKeys/*` action included to use the Data Explorer.

## Next step

> [!div class="nextstepaction"]
> [Getting started with queries](nosql/query/getting-started.md)
