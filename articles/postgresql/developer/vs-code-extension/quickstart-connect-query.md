---
title: "Quickstart: Connect and query PostgreSQL"
description: "Learn how to connect to a PostgreSQL database and run your first query using the PostgreSQL extension for Visual Studio Code."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/14/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: quickstart
---


# Quickstart: Connect and query PostgreSQL

In this quickstart, you use the PostgreSQL extension for Visual Studio Code to connect to a PostgreSQL server, create a table, insert rows, and run a query — all from inside VS Code.

## What you'll learn

- Open the connection dialog and connect to a PostgreSQL server
- Create a database and a table with the query editor
- Insert and query data
- View results in the **Results** panel

## Prerequisites

Before you begin, make sure you have the following:

- [Visual Studio Code](https://code.visualstudio.com/) installed.
- The [PostgreSQL extension for Visual Studio Code](pgsql-extension-overview.md) installed from the Extensions Marketplace.
- Access to a running PostgreSQL server. You can use a local installation, a [Docker container](https://hub.docker.com/_/postgres), or any on-premises or cloud-provided PostgreSQL instance.

## Connect to a server

1. Open the **PostgreSQL** view by pressing **Ctrl+Alt+D** (Windows/Linux) or **Cmd+Alt+D** (macOS), or select the PostgreSQL icon in the Activity Bar.

1. Hover over the **Connections** section header and select **Add New Connection** (the **+** icon). The connection dialog opens with the **Parameters** tab selected.

   :::image type="content" source="./media/screenshots/vscode/connection-dialog/default.png" alt-text="Connection dialog with Parameters tab visible" lightbox="./media/screenshots/vscode/connection-dialog/default.png":::

1. Fill in the connection fields for your PostgreSQL server:

   | Field | Example value | Description |
   |---|---|---|
   | **Server name** | `localhost` | The hostname or IP address of the server. |
   | **Authentication Type** | **Password** | Choose **Password**, **Entra Auth**, **AWS IAM (RDS/Aurora)**, or **None**. |
   | **User name** | `postgres` | Your PostgreSQL login. |
   | **Password** | *(your password)* | The password for the account. |
   | **Database name** | `postgres` | The database to connect to. |
   | **Connection Name** | `Local dev server` | An optional display name for this connection. |

   > [!TIP]
   > Select **Save Password** to store the password securely in the VS Code credential store so you aren't prompted on every connection. For Microsoft Entra ID authentication, AWS IAM authentication, or other identity setup, see [Connections and identity](connections.md).

1. Select **Save & Connect**.

   The server appears in Object Explorer with a green status indicator when the connection succeeds.

## Create a database

1. Right-click on your server node in Object Explorer and select **New Query**. A query editor opens that is connected to the server.

1. Paste the following statement and press **Ctrl+Shift+E** (Windows/Linux) or **Cmd+Shift+E** (macOS) to run it:

   ```sql
   CREATE DATABASE tutorialdb;
   ```

1. Right-click the server node in Object Explorer and select **Refresh** to see the new **tutorialdb** database in the tree.

## Create a table

1. Change the database context to **tutorialdb**. Use the database dropdown in the query editor toolbar, or run `pgsql.changeDatabase` from the Command Palette (**Change PostgreSQL Database**) and select **tutorialdb**.

1. Paste the following statement into the query editor and run it with **Ctrl+Shift+E** / **Cmd+Shift+E**:

   ```sql
   CREATE TABLE customers (
       id SERIAL PRIMARY KEY,
       name VARCHAR(50) NOT NULL,
       email VARCHAR(50) NOT NULL,
       city VARCHAR(50)
   );
   ```

   The **Messages** panel confirms the statement completed successfully.

## Insert data

Replace the contents of the query editor with the following statement and run it:

```sql
INSERT INTO customers (name, email, city)
VALUES
    ('Alice Johnson', 'alice@example.com', 'Seattle'),
    ('Bob Smith', 'bob@example.com', 'Portland'),
    ('Carol Williams', 'carol@example.com', 'San Francisco');
```

The **Messages** panel confirms that three rows were inserted.

## Query the data

Replace the contents of the query editor with the following statement and run it:

```sql
SELECT * FROM customers;
```

The **Results** panel displays the three rows you inserted.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/results-grid/default.png" alt-text="Results panel showing query output rows" lightbox="./media/screenshots/vscode/results-grid/default.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/results-grid/default.png" alt-text="Results panel showing query output rows" lightbox="./media/screenshots/cursor/results-grid/default.png":::

---

## Verify the result

To confirm the data is persisted, run a filtered query:

```sql
SELECT name, city
FROM customers
WHERE city = 'Seattle';
```

The **Results** panel returns one row for **Alice Johnson** in **Seattle**.

## Troubleshoot connection issues

If you can't connect to the server, check the following common causes:

- **Connection refused** — Verify that PostgreSQL is running and listening on the expected host and port. For local servers, confirm the service is started.
- **Password authentication failed** — Double-check the **User name** and **Password** values. Review the server's `pg_hba.conf` file to confirm the authentication method allows your connection.
- **SSL errors** — Configure SSL settings in the advanced connection options. For details, see [Connections and identity — SSL and TLS](connections.md#ssl-and-tls).

## Related content

- [Connections and identity](connections.md)
- [Query editor and IntelliSense](query-editor-intellisense.md)
- [Object Explorer](object-explorer.md)
