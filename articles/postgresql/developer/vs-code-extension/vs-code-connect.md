---
title: "Quickstart: PostgreSQL Extension for Visual Studio Code"
description: Quickstart guide for the PostgreSQL extension for Visual Studio Code.
author: swarathmika
ms.author: skakivaya
ms.reviewer: maghan
ms.date: 01/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: quickstart
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - ignite-2025
# customer intent: As a user, I want to understand what Semantic Operators are available in the azure_ai extension for an Azure Database for PostgreSQL flexible server instance.
---

# Quickstart: Connect and query a database with the PostgreSQL extension for Visual Studio Code

The PostgreSQL extension for Visual Studio Code is a powerful tool designed to streamline the development and management of PostgreSQL databases. This guide walks you through connecting to a PostgreSQL database and executing queries within the Visual Studio Code environment.

## Prerequisites

Before you begin, verify you have the proper tools and resources downloaded and installed.

These tools and resources help you follow along with this article and make the most of the GitHub Copilot integration for the PostgreSQL extension in Visual Studio Code.

- [Visual Studio Code](https://code.visualstudio.com/) installed on your machine.
- PostgreSQL database installed locally or hosted in the [cloud](../../flexible-server/quickstart-create-server.md).
- [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) installed in Visual Studio Code.
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) installed.
- [Azure account](../../flexible-server/how-to-deploy-on-azure-free-account.md) for connecting to cloud-hosted databases (optional).

## Install the PostgreSQL extension

To install the PostgreSQL extension:

1. Open Visual Studio Code and go to the Extensions view by selecting the Extensions icon in the Activity Bar or by using the **View: Extensions** command.
1. Search for *PostgreSQL* in the Extensions Marketplace.
1. Select the **PostgreSQL** extension authored by Microsoft and select **Install**.

When the extension is installed, the PostgreSQL page, represented by an elephant icon, appears in the Visual Studio Code sidebar.

## Add a connection to PostgreSQL

Whether hosted locally or on a remote server, connecting to a PostgreSQL database is a fundamental step in managing and interacting with your data. This process involves providing the necessary connection details, such as the server address, port, and authentication credentials, to establish a secure link between your client application and the database. With the PostgreSQL extension for Visual Studio Code, you can seamlessly connect to your database and use powerful tools to query, manage, and explore your data efficiently.

1. Select the elephant icon on the sidebar to open the PostgreSQL extension page.

1. Select the **Add Connection** button.

1. Enter your connection details manually or use the connection string format:

   ```bash
     psql -h <server>.postgres.database.azure.com -p 5432 -U
   ```

1. If using Azure, sign in to your Azure account and browse for the database instance. Filter by subscription, resource group, server, and database name.

### Authentication

The extension supports two authentication methods:

- **Username/Password**: Enter your database credentials directly into the connection fields.
- **Microsoft Entra ID Authentication**: Add your Microsoft Entra ID account for Azure-hosted databases.

:::image type="content" source="media/vs-code-connect/connect-server-1.png" alt-text="Screenshot of PostgreSQL extension for Visual Studio Code connection dialog.":::

## Test and save the connection

1. Select **Test Connection** to verify your connection details.
1. Upon successful testing, the test box displays a checkmark.
1. Select **Connect** to establish the connection.
1. Your connection automatically saves and appears in the Connections window.

## Explore database objects

The Object Explorer provides a hierarchical view of your database objects:

- Expand the database item to view schemas, tables, views, functions, and stored procedures.
- Right-click on the database to see options to:
  - Launch a New Query
  - Chat with this database (starts the pgsql chat experience)
  - Connect with PSQL to launch a psql terminal connection
- Right-click on a table and select **Select Top 1000** to view its data. The query opens in the Query Editor, and the results appear in the Results Viewer tab.

## Execute queries

Use the Query Editor to draft and execute SQL queries:

- Take advantage of context-aware IntelliSense to autocomplete SQL keywords and object names.
- Use syntax highlighting and autoformatting for better readability and accuracy.
- Access previously executed queries via the Query History pane.

## Review query results

The Results Viewer offers advanced features to interact with your query results:

- Export results to CSV, JSON, or Excel formats for further analysis.
- Use search, filter, and sort options to refine your data.
- Persistent data views maintain context while switching between tabs.

## Use GitHub Copilot for advanced assistance

The GitHub Copilot integration enhances your PostgreSQL development experience by providing AI-powered code suggestions, query optimization tips, and interactive database assistance. This feature helps you streamline your workflow, reduce development time, and gain deeper insights into your database operations. This section guides you through the steps to activate and use Copilot within the PostgreSQL extension for Visual Studio Code.

Ensure the GitHub Copilot and Copilot Chat extensions are installed.

Sign in to your GitHub account and enable the `@pgsql` Copilot Chat agent in the extension settings.

### Interactive database prompts

Right-click on a database and select **Chat with this database** to interact with Copilot.

Write prompts like the following example to receive detailed insights and suggestions.

```copilot-prompt
@pgsql tell me about the tables in the HR schema
```

For more information, see [Configure GitHub Copilot](vs-code-github-copilot.md).

## Connect to Azure Database for PostgreSQL with Visual Studio Code

Connect to an Azure Database for PostgreSQL flexible server instance by using Visual Studio Code by following these steps:

1. Sign in to the Azure portal and locate your Azure Database for PostgreSQL flexible server instance.
1. Go to the **Overview** page of your server instance.

### Connect with Visual Studio Code

The "Connect with Visual Studio Code" option in the Azure portal simplifies connecting to your Azure Database for PostgreSQL flexible server instance. This feature streamlines the setup by guiding you through the necessary prerequisites and automatically configuring connection details. By using this integration, you can quickly establish a connection and manage your database directly within the Visual Studio Code environment.

- Select the prominent **Connect with Visual Studio Code** button on the **Overview** page.
- A side pane appears that lists the requirements to connect by using Visual Studio Code.

:::image type="content" source="media/vs-code-connect/portal-connect-1.png" alt-text="Screenshot of Azure portal showing an Azure Database for PostgreSQL instance with the Connect with Visual Studio Code button.":::

### Confirm requirements

- In the side pane, confirm that all prerequisites (Visual Studio Code and PostgreSQL extension) are satisfied by selecting the appropriate checkboxes.
- If needed, download Visual Studio Code and the extension by using the links in the side pane.
- Optionally, fill out connection parameters such as the default database name, authentication method, and connection pooling.

  :::image type="content" source="media/vs-code-connect/portal-connect-2.png" alt-text="Screenshot of Azure portal showing an Azure Database for PostgreSQL instance with the Connect with Visual Studio Code panel. The open in Visual Studio Code button is highlighted.":::

### Open in Visual Studio Code

- Select the **Open in Visual Studio Code** button in the side pane.
- If Visual Studio Code and the extension take more than 40 seconds to open, a **Retry Opening in Visual Studio Code** button appears in the side pane.

### Launch Visual Studio Code

- If Visual Studio Code is installed and running, the PostgreSQL extension's connection dialog box launches automatically.
- If Visual Studio Code is installed but not open, it launches within approximately 40 seconds, followed by the connection dialog box.

### Autofill connection details

The connection dialog box in the PostgreSQL extension opens, and the **Server Name** field automatically fills in your server endpoint.

:::image type="content" source="media/vs-code-connect/portal-connect-3.png" alt-text="Screenshot of the PostgreSQL extension for Visual Studio Code Connection Dialog with the server name details prepopulated." lightbox="media/vs-code-connect/portal-connect-3.png":::

### Provide authentication details

Select your preferred authentication method:
- **Password Authentication**: Enter your username and password manually.
- **Entra Authentication**: Enter your Azure account credentials.

Specify other connection details such as **Profile Name**, **Database Name** (optional), **Server Group**, and **Port Number**.

### Save and connect

Select the **Save & Connect** button to establish the connection. Once connected, expand the server in the Object Explorer tree to view databases, schemas, and tables, or use the built-in query tool to manage your database objects.

### Troubleshoot

If you encounter issues during the connection process:

- Verify that Visual Studio Code and the PostgreSQL extension are installed and enabled.

- Ensure the IP address is allowed in the firewall settings of your Azure Database for PostgreSQL.

- If you don't meet the prerequisites, the side pane provides feedback and steps to resolve the issue, including retrying the connection.

## Feedback and support

For bugs, feature requests, and issues, use the built-in feedback tool in Visual Studio Code. You can complete this feedback process through the Visual Studio Code Help menu or the PGSQL command palette.

- Help menu
  - Go to **Help > Report Issue**

- Command palette
  - Open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Report Issue`

## Related content

- [What is the PostgreSQL extension for Visual Studio Code?](vs-code-overview.md)
- [Quickstart: Configure GitHub Copilot for PostgreSQL extension in Visual Studio Code](vs-code-github-copilot.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
