---
title: PostgreSQL Extension for VS Code Quickstart (Preview)
description: Quickstart guide for the PostgreSQL extension for VS Code.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what Semantic Operators are available in the azure_ai extension for Azure Database for PostgreSQL flexible server.
---

# Quickstart: Connect and query a database with the PostgreSQL extension for Visual Studio Code

## Overview

The PostgreSQL extension for Visual Studio Code is a powerful tool designed to streamline the development and management of PostgreSQL databases. This guide will walk you through connecting to a PostgreSQL database and executing queries within the Visual Studio Code environment.

## Prerequisites

- Visual Studio Code installed on your machine.
- PostgreSQL database installed locally or hosted in the cloud.
- PostgreSQL extension installed in Visual Studio Code.
- GitHub Copilot and GitHub Copilot Chat extension installed (optional, for enhanced PostgreSQL GitHub Copilot Chat agent experience).
- Azure account for connecting to cloud-hosted databases (optional).

## Install the PostgreSQL extension

To install the PostgreSQL extension:

1. Open Visual Studio Code and navigate to the Extensions view by clicking on the Extensions icon in the Activity Bar or using the "View: Extensions" command.
2. Search for "PostgreSQL" in the Extensions Marketplace.
3. Select the PostgreSQL extension authored by Microsoft and click "Install."
 
  :::image type="content" source="./media/quickstart-vscode-extension/install-ext-1.png" alt-text="Screenshot of PostgreSQL extension for VS Code showing the install screen." lightbox="./media/quickstart-vscode-extension/install-ext-1.png":::

Once installed, the PostgreSQL page, represented by an elephant icon, will appear in the Visual Studio Code sidebar.

## Add a connection to PostgreSQL

### Connecting to a local or remote database

1. Click on the elephant icon on the sidebar to open the PostgreSQL extension page.
2. Click on the "+ Add Connection" button.
3. Enter your connection details manually or use the connection string format:
   ```plaintext
   psql -h <server>.postgres.database.azure.com -p 5432 -U
   ```
4. If using Azure, sign in to your Azure account and browse for the database instance. Filter by subscription, resource group, server, and database name.

### Authentication

The extension supports two authentication methods:

- **Username/Password**: Enter your database credentials directly into the connection fields.
- **Entra ID Authentication**: For Azure-hosted databases, add your Entra ID account.

  :::image type="content" source="./media/quickstart-vscode-extension/connect-server-1.png" alt-text="Screenshot of PostgreSQL extension for VS Code connection dialog." lightbox="./media/quickstart-vscode-extension/connect-server-1.png":::

## Test and Save the connection

1. Click on "Test Connection" to verify that your connection details are correct.
2. Upon successful testing, the test box will display a checkmark.
3. Click "Connect" to establish the connection.
4. Your connection will automatically be saved and appear in the Connections window.

## Explore database objects

The Object Explorer provides a hierarchical view of your database objects:

- Expand the database item to view schemas, tables, views, functions, and stored procedures.
- Right-click on the database and you will see options to:
  - Launch a New Query
  - Chat with this database (starts the pgsql chat experience)
  - Connect with PSQL to launch a psql terminal connection
- Right-click on a table and select “Select Top 1000” to view its data. The query will open in the Query Editor, and the results will appear in the Results Viewer tab.

  :::image type="content" source="./media/quickstart-vscode-extension/new-query-2.png" alt-text="Screenshot of PostgreSQL extension for VS Code showing the option to launch a new query." lightbox="./media/quickstart-vscode-extension/new-query-2.png":::

## Execute queries

Use the Query Editor to draft and execute SQL queries:

- Take advantage of context-aware IntelliSense for auto-completion of SQL keywords and object names.
- Syntax highlighting and auto-formatting ensure better readability and accuracy.
- Access previously executed queries via the Query History pane.

## Review query results

The Results Viewer offers advanced features to interact with your query results:

- Export results to CSV, JSON, or Excel formats for further analysis.
- Use search, filter, and sort options to refine your data.
- Persistent data views maintain context while switching between tabs.

## Use GitHub Copilot for advanced assistance

### Enable Copilot integration

1. Ensure the GitHub Copilot and Copilot Chat extensions are installed.
2. Sign in to your GitHub account and enable the "@pgsql" Copilot Chat agent in the extension settings.

### Interactive database prompts

1. Right-click on a database and choose “Chat with this database” to interact with Copilot.
2. Write prompts like “@pgsql tell me about the tables in the HR schema” to receive detailed insights.

  :::image type="content" source="./media/quickstart-vscode-extension/ghc-chat-7.png" alt-text="Screenshot of PostgreSQL extension for VS Code GitHub copilot chat." lightbox="./media/quickstart-vscode-extension/ghc-chat-7.png":::


## Connect to an Azure Database for PostgreSQL Flexible Server instance with VS Code from the Azure Portal

### Prerequisites

Before proceeding, ensure the following prerequisites are met:

- Visual Studio Code is installed on your machine.
- The PostgreSQL extension by Microsoft is installed and enabled in VS Code.
- Your client IP address is allowed in the firewall settings of your Azure PostgreSQL Flexible Server.

### Steps to connect

#### Navigate to the Azure Portal

- Log in to the Azure Portal and locate your Azure Database for PostgreSQL Flexible Server instance. 
- Go to the Overview blade of your server instance.

#### Select "Connect with VS Code"

- On the Overview page, click the prominent **Connect with VS Code** button. 
- A side pane will appear listing the requirements to connect using VS Code.

  :::image type="content" source="./media/quickstart-vscode-extension/portal-connect-1.png" alt-text="Screenshot of Azure Portal showing an Azure Database for PostgreSQL instance with the Connect with VS Code button." lightbox="./media/quickstart-vscode-extension/portal-connect-1.png":::

#### Confirm requirements

- In the side pane, confirm that all prerequisites (VS Code and PostgreSQL extension) are satisfied by selecting the appropriate checkboxes. 
- If needed, download Visual Studio Code and the extension using the links provided in the side pane. 
- Optionally, fill out connection parameters such as the default database name, authentication method, and connection pooling.
 
  :::image type="content" source="./media/quickstart-vscode-extension/portal-connect-2.png" alt-text="Screenshot of Azure Portal showing an Azure Database for PostgreSQL instance with the Connect with VS Code panel. The open in Visual Studio Code button is highlighted.." lightbox="./media/quickstart-vscode-extension/portal-connect-2.png":::

#### Click "Open in Visual Studio Code"

- Click the **Open in Visual Studio Code** button in the side pane. 
- A “Retry Opening in Visual Studio Code” button will appear in the side pane in case Visual Studio Code and the extension is taking more than 40 seconds to open.

#### Launch Visual Studio Code

- If VS Code is already installed and running, the PostgreSQL extension’s connection dialog box will launch automatically. 
- If VS Code is installed but not open, it will launch within approximately 40 seconds, followed by the connection dialog box.

#### Auto-fill connection details

- The connection dialog box in the PostgreSQL extension will open with the Server Name field automatically populated with your server endpoint.

  :::image type="content" source="./media/quickstart-vscode-extension/portal-connect-3.png" alt-text="Screenshot of the PostgreSQL extension for VS Code Connection Dialog with the server name details prepopulated." lightbox="./media/quickstart-vscode-extension/portal-connect-3.png":::

#### Provide authentication details

Select your preferred authentication method:
- **Password Authentication**: Enter your username and password manually.
- **Entra Authentication**: Enter your Azure account credentials.

Specify other connection details such as Profile Name, Database Name (optional), Server Group, and Port Number.

#### Save and Connect

Click the **Save & Connect** button to establish the connection. Once connected, expand the server in the Object Explorer tree to view databases, schemas, and tables, or use the built-in query tool to manage your database objects.

#### Troubleshooting

If you encounter issues during the connection process:
- Verify that VS Code and the PostgreSQL extension are installed and enabled.
- Ensure your client IP address is allowed in the firewall settings of your Azure PostgreSQL Flexible Server.
- If prerequisites are not met, the side pane will provide feedback and steps to resolve the issue, including retrying the connection.


## Submit PostgreSQL extension feedback from Visual Studio Code

For bugs, feature requests, and issues please use the built-in feedback tool in Visual Studio Code. This can be completed via the VS Code Help menu or the PGSQL Command Palette:

- **Help > Report Issue**

  :::image type="content" source="./media/quickstart-vscode-extension/report-issue-3.png" alt-text="Screenshot of PostgreSQL extension for VS Code showing the report issue menu." lightbox="./media/quickstart-vscode-extension/report-issue-3.png":::
 
- To submit feedback via the Command Palette, press `Ctrl + Shift + P` to open the Command Palette, then type `PGSQL: Give Feedback`.

  :::image type="content" source="./media/quickstart-vscode-extension/give-feedback-4.png" alt-text="Screenshot of PostgreSQL extension for VS Code showing the give feedback menu." lightbox="./media/quickstart-vscode-extension/give-feedback-4.png":::


## Related content

- [Azure Database for PostgreSQL documentation](overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)