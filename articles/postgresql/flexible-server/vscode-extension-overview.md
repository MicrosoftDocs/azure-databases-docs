---
title: What is the PostgreSQL extension for Visual Studio Code? (Preview)
description: Overview of the PostgreSQL extension for VS Code.
author: jojohnso-msft
ms.author: jojohnso
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - build-2025
# customer intent: As a user, I want to understand what the PostgreSQL extension for VS Code is and how I can use it with Azure Database for PostgreSQL flexible server.
---
# Overview of the PostgreSQL Extension for Visual Studio Code

The PostgreSQL extension for Visual Studio Code, currently in public preview, is a feature-rich tool designed to simplify PostgreSQL database management and development. This extension empowers developers to connect to PostgreSQL databases, write and execute queries, and manage database objects without having to leave the Visual Studio Code environment. By introducing comprehensive functionality, intuitive UI design, and seamless integration with cloud platforms such as Azure Database for PostgreSQL, this extension revolutionizes the PostgreSQL development workflow.

## How to install the extension

To get started, you can install the PostgreSQL extension directly from the Extensions Marketplace in Visual Studio Code. Simply follow these steps:

1. Open the Extensions view in Visual Studio Code by clicking the Extensions icon in the Activity Bar or by using the "View: Extensions" command.
2. Search for "PostgreSQL" in the Extensions Marketplace.
3. Select the PostgreSQL extension and click "Install."

 :::image type="content" source="./media/devx-vscode-ext-overview/install-ext-1.png" alt-text="Screenshot showing the Marketplace installation page." lightbox="./media/devx-vscode-ext-overview/install-ext-1.png":::

Once installed, you'll see the PostgreSQL page represented by an elephant icon in the Visual Studio Code sidebar.

 :::image type="content" source="./media/devx-vscode-ext-overview/select-elephant-2.png" alt-text="Screenshot showing the PostgreSQL elephant icon selected." lightbox="./media/devx-vscode-ext-overview/select-elephant-2.png":::

## New features (Preview)

The PostgreSQL extension for Visual Studio Code brings an array of powerful new features aimed at enhancing productivity and streamlining development workflows. These preview features include:

### Connection Manager

The Connection Manager simplifies connecting to local and cloud-hosted PostgreSQL databases. Key functionalities include:

- Support for multiple connection profiles, allowing users to connect to and manage multiple PostgreSQL instances.
- Connection string parsing for seamless connectivity, whether you’re connecting to a local database or one deployed in the cloud.
- Integration with Azure Database for PostgreSQL for direct browsing and filtering of instances, along with Entra ID authentication for robust security.

 :::image type="content" source="./media/devx-vscode-ext-overview/connection-dialog-3.png" alt-text="Screenshot showing the connection dialog flow." lightbox="./media/devx-vscode-ext-overview/connection-dialog-3.png":::

### Object Explorer

The enhanced Object Explorer provides a hierarchical view of database objects, making it easier to browse and manage schemas, tables, views, functions, and more. Notable features include:

- Advanced filtering options to locate specific objects quickly.
- Capabilities to create, modify, and delete database objects like tables, views, and stored procedures.
- Visualization of database schemas and relationships for streamlined navigation.

  :::image type="content" source="./media/devx-vscode-ext-overview/object-explorer-4.png" alt-text="Screenshot showing the object explorer." lightbox="./media/devx-vscode-ext-overview/object-explorer-4.png":::

### Query Editor

The Query Editor improves the query drafting and execution experience with:

- Context-aware IntelliSense for auto-completion of SQL keywords, table names, and functions.
- Syntax highlighting and auto-formatting for better query readability.
- Query history tracking, allowing users to reuse previously executed queries.

  :::image type="content" source="./media/devx-vscode-ext-overview/query-editor-5.png" alt-text="Screenshot showing the query editor." lightbox="./media/devx-vscode-ext-overview/query-editor-5.png":::

### Results Viewer

The Results Viewer enables users to interact with query results through features such as:

- Exporting results to CSV, JSON, or Excel formats.
- Search, filter, and sort options to analyze data efficiently.
- Persistent data views to maintain context while navigating between tabs.

 :::image type="content" source="./media/devx-vscode-ext-overview/results-viewer-6.png" alt-text="Screenshot showing the results viewer." lightbox="./media/devx-vscode-ext-overview/results-viewer-6.png":::

### GitHub Copilot integration

This extension integrates with GitHub Copilot to offer AI-driven assistance tailored to PostgreSQL development. With commands like "@pgsql," developers can query their database, optimize schema, and even request Copilot to execute specific SQL operations. This feature enhances productivity by providing contextual guidance and actionable insights.

:::image type="content" source="./media/devx-vscode-ext-overview/ghc-chat-7.png" alt-text="Screenshot showing the pgsql github chat agent experience." lightbox="./media/devx-vscode-ext-overview/ghc-chat-7.png":::

## Supported operating systems

The PostgreSQL extension is compatible with the following operating systems:

- Windows
- macOS
- Linux

Including support for a variety of Linux distributions such as Ubuntu, Fedora, and Red Hat Enterprise Linux.

## Feedback and Support

The PostgreSQL extension for Visual Studio Code is continually evolving based on user feedback. Developers are encouraged to share their insights and report issues through the built-in feedback tool in VS Code. This can be completed via the VS Code Help menu or the PGSQL Command Palette:

- **Help > Report Issue**

:::image type="content" source="./media/devx-vscode-ext-overview/help-8.png" alt-text="Screenshot showing the VS Code help menu." lightbox="./media/devx-vscode-ext-overview/help-8.png":::

- To submit feedback via the Command Palette, press `Ctrl + Shift + P` to open the Command Palette, then type `PGSQL: Give Feedback`.

:::image type="content" source="./media/devx-vscode-ext-overview/give-feedback-9.png" alt-text="Screenshot showing the give feedback command in the VS Code Command Palette for the PostgreSQL extension." lightbox="./media/devx-vscode-ext-overview/give-feedback-9.png":::

## Related content

- [Azure Database for PostgreSQL documentation](overview.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-postgresql)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- [MSSQL extension for Visual Studio Code?](/sql/tools/visual-studio-code-extensions/mssql/mssql-extension-visual-studio-code)
