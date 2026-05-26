---
title: What Is the PostgreSQL Extension for Visual Studio Code with Azure HorizonDB?
description: Overview of the PostgreSQL extension for Visual Studio Code with Azure HorizonDB.
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: overview
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2026
ai-usage: ai-assisted
---

# What is the PostgreSQL extension for Visual Studio Code?

The PostgreSQL extension for Visual Studio Code simplifies PostgreSQL database management and development. You can connect to PostgreSQL databases, write and execute queries, and manage database objects without leaving Visual Studio Code.

The extension integrates with Azure-managed PostgreSQL services, including:

- **Azure Database for PostgreSQL flexible server** - the general-purpose managed PostgreSQL service in Azure.
- **Azure HorizonDB** - a cloud-native PostgreSQL service built for tier-1 enterprise workloads. HorizonDB features a disaggregated storage/compute architecture, low-latency commits, fast failover, load-balanced read scale-out across readable HA replicas, and deep AI integration.

The same extension works against both services. Where behavior differs (for example, connection endpoints or supported authentication methods), it's called out in the sections that follow.

## How to install the extension

You can install the PostgreSQL extension directly from the Extensions Marketplace in Visual Studio Code. Follow these steps:

1. Open the Extensions view in Visual Studio Code by selecting the **Extensions** icon in the Activity Bar or by using the **View: Extensions** command.
1. Search for **PostgreSQL** in the Extensions Marketplace.
1. Select the **PostgreSQL** extension authored by Microsoft and select **Install**.

When you install the extension, an elephant icon appears to represent the PostgreSQL page in the Visual Studio Code sidebar.

## Features

The PostgreSQL extension for Visual Studio Code provides the following features for both Azure Database for PostgreSQL flexible server and Azure HorizonDB.

### Connection Manager

The Connection Manager simplifies connecting to local and cloud-hosted PostgreSQL databases. Key functionalities include:

- Support for multiple connection profiles, so you can connect to and manage multiple PostgreSQL instances side by side, including a mix of flexible server and HorizonDB clusters.
- Connection string parsing for seamless connectivity, whether you're connecting to a local database, an Azure Database for PostgreSQL flexible server instance, or an Azure HorizonDB cluster.
- Integration with Azure Database for PostgreSQL flexible server **and** Azure HorizonDB for direct browsing and filtering of instances by subscription, resource group, server/cluster, and database.
- Microsoft Entra ID authentication for Azure Database for PostgreSQL flexible server. (Azure HorizonDB currently supports PostgreSQL authentication.)

#### HorizonDB connection endpoints

Azure HorizonDB exposes two endpoints, which you can add as separate connection profiles in the extension:

- **Read/write endpoint** - Connects to the primary, which accepts both read and write transactions. Use this endpoint for application writes, schema changes, and any read workload that requires the latest committed data. The endpoint is listed on the cluster **Overview** page and on the **Replicas** page in the Azure portal.
- **Reader endpoint** - Automatically load-balances read-only connections across all readable HA replicas in the cluster. Use this endpoint for read scale-out workloads, reporting, and analytics. Up to four readable HA replicas are supported today (increasing to 8), each sized identically to the primary.

A typical pattern is to save two profiles in the Connection Manager - one pointed at the read/write endpoint and one pointed at the reader endpoint - and switch between them in the Object Explorer based on the task at hand.

### Object Explorer

The enhanced Object Explorer provides a hierarchical view of database objects, making it easier to browse and manage schemas, tables, views, and functions. Notable features include:

- Advanced filtering options to quickly locate specific objects.
- Capabilities to create, modify, and delete database objects like tables, views, and stored procedures.
- Visualization of database schemas and relationships for streamlined navigation.
- For HorizonDB, you can inspect the 55+ allow-listed extensions available on the cluster via the `pg_available_extensions` catalog view directly from the Query Editor.

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

### Schema Visualization

The Schema Visualizer gives you an interactive, diagram-based view of your database structure without writing any SQL. Right-click a database (or any object underneath it) in the Object Explorer and select **Visualize Schema** to launch the visualizer.

Key capabilities include:

- **Full table view** - Every table is rendered as a card showing its columns and data types.
- **Relationship lines** - Foreign key relationships between tables are drawn as connecting lines, so you can see at a glance how your data model fits together.
- **Schema-based organization** - Tables are grouped by their parent schema (for example, `public`, `hr`, `ecom`), making it easy to navigate large databases.
- **Show / hide by schema** - Toggle entire schemas on or off to focus only on the parts of the model you care about, and to keep diagrams readable on large databases.
- **Pan and zoom** - Navigate large diagrams with standard pan, zoom, and fit-to-screen controls.

Schema Visualization works against any connected database, including local PostgreSQL and Azure HorizonDB clusters.

### Apache AGE Graph Visualization

The Apache AGE Graph Visualizer lets you run Apache AGE Cypher queries and explore the results as an interactive node-edge graph. The extension automatically detects graph query results and renders them in a visual explorer with per-node callouts, zoom and pan controls, export support, and theme-aware styling.

The `age` extension is allow-listed by default on Azure HorizonDB, so graph workloads can run on a HorizonDB cluster without additional configuration. The same requirements apply when you author Cypher queries against flexible server or HorizonDB:

- **Return full objects, not scalar properties** - The graph visualizer needs complete vertex and edge objects. Queries that extract scalar properties (`RETURN p.name, p.title`) return plain text values and won't render in the visualizer. Instead, return the full objects and name the relationship variable:

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

### AI integration (Azure HorizonDB)

When connected to an Azure HorizonDB cluster, the extension gives you a first-class authoring surface for HorizonDB's AI capabilities, which are exposed as standard PostgreSQL extensions and functions:

- `pgvector` - Vector data type and similarity operators.
- `pg_diskann` - High-performance vector index with **Advanced Filtering**, which evaluates `WHERE` predicates during the vector graph traversal so filtered similarity queries return faster and more consistently.
- `azure_ai` - AI Functions such as `azure_ai.generate()`, `azure_ai.is_true()`, `azure_ai.extract()`, and `azure_openai.create_embeddings()`.
- **[AI Model Management (Gated Preview)](../../ai/ai-model-management.md)** - When enabled on the cluster, HorizonDB automatically provisions a default chat model (`gpt-5`) and a default embedding model (`text-embedding-3-small`) through Microsoft Foundry, installs and configures `azure_ai`, and wires the AI Functions to those managed models - no manual key handling required. Access requires [sign-up and approval](https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR6wWnvFyIUpElDcnO56BZqhUMFpKRERLVldQRDdKTTNWRVZJSklKWVRYMy4u). You can also register your own Microsoft Foundry deployments (Bring Your Own Model) and call them by alias from the same AI Functions.

You can author and run these AI workloads directly from the Query Editor, and the Results Viewer renders vector and JSONB output inline.

### GitHub Copilot integration

This extension integrates with GitHub Copilot to offer AI-driven assistance tailored to PostgreSQL development. With commands like `@pgsql`, you can query your database, optimize your schema, and request Copilot to execute specific SQL operations against either an Azure Database for PostgreSQL flexible server instance or an Azure HorizonDB cluster. Copilot picks up the live connection context - including extensions installed on the target - so suggestions on a HorizonDB connection are aware of `pgvector`, `pg_diskann`, `azure_ai`, and `age`.

## Supported operating systems

The PostgreSQL extension works with the following operating systems:

- Windows
- macOS
- Linux

The extension supports various Linux distributions, including Ubuntu, Fedora, and Red Hat Enterprise Linux.

## Feedback and support

For bugs, feature requests, and issues, use the built-in feedback tool in Visual Studio Code. You can complete this feedback through the Visual Studio Code Help menu or the PGSQL command palette.

- **Help menu**
  - Go to **Help > Report Issue**
- **Command palette**
  - Open the Command Palette with `Ctrl + Shift + P` and run: `PGSQL: Report Issue`

## Related content

- [Quickstart: PostgreSQL Extension for Visual Studio Code in Azure HorizonDB](vs-code-connect.md)
- [Quickstart: Configure GitHub Copilot for PostgreSQL extension in Visual Studio Code](vs-code-github-copilot.md)
- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
