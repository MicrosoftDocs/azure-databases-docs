---
title: What Is the PostgreSQL Extension for Visual Studio Code?
description: Overview of the PostgreSQL extension for Visual Studio Code.
author: swarathmika
ms.author: skakivaya
ms.reviewer: maghan
ms.date: 01/09/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: overview
ms.custom:
  - ignite-2025
ai-usage: ai-assisted
# customer intent: As a user, I want to understand what the PostgreSQL extension for VS Code is and how I can use it with an Azure Database for PostgreSQL flexible server instance.
---

# What is the PostgreSQL extension for Visual Studio Code?

The PostgreSQL extension for Visual Studio Code is a feature-rich tool designed to simplify PostgreSQL database management and development. This extension empowers developers to connect to PostgreSQL databases, write and execute queries, and manage database objects without leaving the Visual Studio Code environment. This extension revolutionizes the PostgreSQL development workflow by introducing comprehensive functionality, intuitive UI design, and seamless integration with cloud platforms such as Azure Database for PostgreSQL.

## How to install the extension

You can install the PostgreSQL extension directly from the Extensions Marketplace in Visual Studio Code. Follow these steps:

1. Open the Extensions view in Visual Studio Code by selecting the Extensions icon in the Activity Bar or by using the **View: Extensions** command.
1. Search for *PostgreSQL* in the Extensions Marketplace.
1. Select the **PostgreSQL** extension and select **Install**.

When you install the extension, an elephant icon appears to represent the PostgreSQL page in the Visual Studio Code sidebar.

## Features

The PostgreSQL extension for Visual Studio Code brings an array of powerful new features to enhance productivity and streamline development workflows.

### Connection Manager

The Connection Manager simplifies connecting to local and cloud-hosted PostgreSQL databases. Key functionalities include:

- Support for multiple connection profiles, so you can connect to and manage multiple PostgreSQL instances.
- Connection string parsing for seamless connectivity, whether you're connecting to a local database or one deployed in the cloud.
- Integration with Azure Database for PostgreSQL for direct browsing and filtering of instances, along with Microsoft Entra ID authentication for robust security.

### Object Explorer

The enhanced Object Explorer provides a hierarchical view of database objects, making it easier to browse and manage schemas, tables, views, and functions. Notable features include:

- Advanced filtering options to quickly locate specific objects.
- Capabilities to create, modify, and delete database objects like tables, views, and stored procedures.
- Visualization of database schemas and relationships for streamlined navigation.

### Query Editor

The Query Editor improves the query drafting and execution experience with:

- Context-aware IntelliSense for autocompletion of SQL keywords, table names, and functions.
- Syntax highlighting and autoformatting for better query readability.
- Query history tracking, so you can reuse previously executed queries.

### Results Viewer

The Results Viewer enables you to interact with query results through features such as:

- Exporting results to CSV, JSON, or Excel formats.
- Search, filter, and sort options to analyze data efficiently.
- Persistent data views to maintain context while navigating between tabs.

### GitHub Copilot integration

This extension integrates with GitHub Copilot to offer AI-driven assistance tailored to PostgreSQL development. With commands like `@pgsql`, you can query your database, optimize your schema, and even request Copilot to execute specific SQL operations. This feature enhances productivity by providing contextual guidance and actionable insights.

### Apache AGE Graph Visualization

Run Apache AGE Cypher queries and explore the results as an interactive node-edge graph. The extension automatically detects graph query results and renders them in a visual explorer with per-node callouts, zoom and pan controls, export support, and theme-aware styling.

To render results in the graph visualizer, your queries must meet the following requirements:

- **Return full objects, not scalar properties** - The graph visualizer needs complete vertex and edge objects. Queries that extract scalar properties (`RETURN p.name, p.title`) return plain text values and won't render in the visualizer. Instead of returning properties, return the full objects and name the relationship variable:

  ```sql
  SELECT * FROM cypher('my_graph', $$
      MATCH (a:Product)-[r:BOUGHT_TOGETHER]->(b:Product)
      RETURN a, r, b
  $$) AS (a agtype, r agtype, b agtype);
  ```

- **Set `disp_label` for meaningful node text** - Without `disp_label`, nodes display internal IDs. Set this property so the visualizer shows useful labels:

  ```sql
  SELECT * FROM cypher('my_graph', $$
      MATCH (a:Product)-[r:BOUGHT_TOGETHER]->(b:Product)
      SET a.disp_label = a.title
      SET b.disp_label = b.title
      RETURN a, r, b
  $$) AS (a agtype, r agtype, b agtype);
  ```

- **Match output columns to returned objects** - The wrapper `AS (...)` clause must have one column per returned object. For multi-hop queries, include every intermediate node and edge:

  ```sql
  SELECT * FROM cypher('my_graph', $$
      MATCH (a:Product)-[r1:BOUGHT_TOGETHER]->(mid:Product)-[r2:BOUGHT_TOGETHER]->(b:Product)
      RETURN a, r1, mid, r2, b
  $$) AS (a agtype, r1 agtype, mid agtype, r2 agtype, b agtype);
  ```

## Supported operating systems

The PostgreSQL extension works with the following operating systems:

- Windows
- macOS
- Linux

The extension supports various Linux distributions, including Ubuntu, Fedora, and Red Hat Enterprise Linux.

## Feedback and support

For bugs, feature requests, and issues, use the built-in feedback tool in Visual Studio Code. You can complete this feedback through the Visual Studio Code Help menu or the PGSQL command palette.

- Help menu
  - Go to **Help > Report Issue**

- Command palette
  - Open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Report Issue`

## Related content

- [Quickstart: Connect and query a database with the PostgreSQL extension for Visual Studio Code](vs-code-connect.md)
- [Quickstart: Configure GitHub Copilot for PostgreSQL extension in Visual Studio Code](vs-code-github-copilot.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
