---
title: What Is the PostgreSQL Extension for Visual Studio Code?
description: Overview of the PostgreSQL extension for Visual Studio Code.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 06/24/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: overview
ms.custom:
  - build-2025
ai-usage: ai-assisted
# customer intent: As a user, I want to understand what the PostgreSQL extension for VS Code is and how I can use it with an Azure Database for PostgreSQL flexible server instance.
---

# What is the PostgreSQL extension for Visual Studio Code preview?

Currently in public preview, the PostgreSQL extension for Visual Studio Code is a feature-rich tool designed to simplify PostgreSQL database management and development. This extension empowers developers to connect to PostgreSQL databases, write and execute queries, and manage database objects without leaving the Visual Studio Code environment. This extension revolutionizes the PostgreSQL development workflow by introducing comprehensive functionality, intuitive UI design, and seamless integration with cloud platforms such as Azure Database for PostgreSQL.

## How to install the extension

You can install the PostgreSQL extension directly from the Extensions Marketplace in Visual Studio Code to get started. Follow these steps:

1. Open the Extensions view in Visual Studio Code by selecting the Extensions icon in the Activity Bar or by using the **View: Extensions** command.
1. Search for *PostgreSQL* in the Extensions Marketplace.
1. Select the **PostgreSQL** extension and select **Install**.

Once installed, an elephant icon appears to represent the PostgreSQL page in the Visual Studio Code sidebar.

## New features in preview

The PostgreSQL extension for Visual Studio Code brings an array of powerful new features to enhance productivity and streamline development workflows. These preview features include:

### Connection Manager

The Connection Manager simplifies connecting to local and cloud-hosted PostgreSQL databases. Key functionalities include:

- Support for multiple connection profiles, allowing users to connect to and manage multiple PostgreSQL instances.
- Connection string parsing for seamless connectivity, whether you're connecting to a local database or one deployed in the cloud.
- Integration with Azure Database for PostgreSQL for direct browsing and filtering of instances, along with Microsoft Entra ID authentication for robust security.

### Object Explorer

The enhanced Object Explorer provides a hierarchical view of database objects, making browsing and managing schemas, tables, views, functions, and easier. Notable features include:

- Advanced filtering options to locate specific objects quickly.
- Capabilities to create, modify, and delete database objects like tables, views, and stored procedures.
- Visualization of database schemas and relationships for streamlined navigation.

### Query Editor

The Query Editor improves the query drafting and execution experience with:

- Context-aware IntelliSense for autocompletion of SQL keywords, table names, and functions.
- Syntax highlighting and autoformatting for better query readability.
- Query history tracking, allowing users to reuse previously executed queries.

### Results Viewer

The Results Viewer enables users to interact with query results through features such as:

- Exporting results to CSV, JSON, or Excel formats.
- Search, filter, and sort options to analyze data efficiently.
- Persistent data views to maintain context while navigating between tabs.

### GitHub Copilot integration

This extension integrates with GitHub Copilot to offer AI-driven assistance tailored to PostgreSQL development. With commands like `@pgsql`, developers can query their database, optimize schema, and even request Copilot to execute specific SQL operations. This feature enhances productivity by providing contextual guidance and actionable insights.

## Supported operating systems

The PostgreSQL extension is compatible with the following operating systems:

- Windows
- macOS
- Linux

Including support for various Linux distributions such as Ubuntu, Fedora, and Red Hat Enterprise Linux.

## Limitations and considerations

The PostgreSQL extension for Visual Studio Code is currently in preview, and there are some limitations and considerations to keep in mind:

- ARM64 not currently supported

## Feedback and support

For bugs, feature requests, and issues, use the built-in feedback tool in Visual Studio Code. You can complete this via the VS Code Help menu or the PGSQL command palette.

- Help menu
    - Go to **Help > Report Issue**

- Command palette
    - Open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Report Issue`

## Related content

- [Quickstart: Connect and query a database with the PostgreSQL extension for Visual Studio Code preview](quickstart-connect.md)
- [Quickstart: Configure GitHub Copilot for PostgreSQL extension in Visual Studio Code preview](quickstart-github-copilot.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)