---
title: "PostgreSQL extension for Visual Studio Code"
description: "Overview of the PostgreSQL extension for Visual Studio Code, providing database development tools for PostgreSQL."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/24/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: overview
---


# PostgreSQL extension for Visual Studio Code

The PostgreSQL extension for Visual Studio Code (`ms-ossdata.vscode-pgsql`) brings database development tools directly into your editor. You can connect to local, on-premises, or cloud-provided PostgreSQL servers, write queries with IntelliSense, explore database objects, visualize query plans and schemas, and manage Azure Database for PostgreSQL Flexible Server resources—all without leaving VS Code. The extension also integrates with AI assistants for AI-assisted query authoring, analysis, and agent-driven workflows.

> [!NOTE]
> The extension also runs in **Cursor**. PostgreSQL AI features are supported in both editors and follow each editor's native AI experience: Visual Studio Code includes the **@pgsql** chat participant alongside Agent mode and MCP server registration, while Cursor uses **Connect AI** (Agent mode) or MCP server registration.

## Get started

If you're new to the extension, start with one of these guides:

| Goal | Guide |
|---|---|
| Run your first query | [Quickstart: Connect and query](quickstart-connect-query.md) |
| Find the right article for your task | [Common workflows](common-workflows.md) |
| Configure identity, TLS, or saved profiles | [Connections and identity](connections.md) |

## Install the extension

1. Open Visual Studio Code.
1. Open the **Extensions** view (`Ctrl+Shift+X`, or `Cmd+Shift+X` on macOS).
1. Search for **postgresql**.
1. Select **PostgreSQL** by Microsoft and then select **Install**.

> [!TIP]
> After installation, a PostgreSQL icon appears in the **Activity Bar**. Select it to open the **PostgreSQL view**, where you manage connections and explore database objects.

## Key features

The following sections summarize each major feature area. Select the link at the end of each section for the full article.

### Connection dialog

The connection dialog connects you to local, on-premises, and cloud-provided PostgreSQL servers, with integrated authentication support for Microsoft Entra ID and AWS IAM (RDS/Aurora). Enter connection parameters individually, paste a connection string, or browse your Azure subscriptions to discover Azure Database for PostgreSQL Flexible Servers and Horizon Preview servers.

- **Three input modes** — individual parameters (host, port, database, username), connection string, or **Browse Azure**.
- **Saved and recent connections** — saved profiles appear in the **Connections** list for quick reuse; recently used connections are always available.
- **Server groups** — organize connections into named groups with color coding for easy identification in **Object Explorer**.

For details, see [Connections and identity](connections.md) and [Advanced connection options](advanced-connection-options.md).

### Object Explorer

**Object Explorer** provides a navigable tree view of your connected PostgreSQL servers. Expand servers, databases, and schemas to inspect tables, views, functions, sequences, types, extensions, roles, tablespaces, and event triggers.

- **Search** — find objects by name across all supported object types with the built-in search.
- **Scripting** — right-click any object to generate `SELECT`, `CREATE`, `ALTER`, `DROP`, or `EXECUTE` scripts that open in the query editor.
- **Deep refresh** — refresh any node to recursively update all expanded descendants, reflecting schema changes without disconnecting.

For details, see [Object Explorer](object-explorer.md).

### Query editor and IntelliSense

The query editor provides a rich editing surface for PostgreSQL SQL. IntelliSense offers context-aware completions for table names, column names, functions, schemas, keywords, and join clauses.

- **Run Query** and **Run Current Statement** — run the full editor contents or only the statement at the cursor.
- **Code snippets** — insert common SQL patterns such as `CREATE TABLE`, `INSERT`, and `SELECT`.
- **Query history** — access previously run queries from the Command Palette to rerun or modify them.

For details, see [Query editor and IntelliSense](query-editor-intellisense.md).

### Query results

Results appear in the **Query Results** panel below the editor. The results grid supports sorting, filtering, and column resizing.

- **Export** — save results to CSV, JSON, or Excel.
- **Chart visualization** — visualize results as line, bar, pie, or scatter charts.
- **Graph view** — Apache AGE graph-query results switch automatically to a node-and-edge view.
- **Messages tab** — review row counts, execution times, and server messages.

For details, see [Query editor and IntelliSense](query-editor-intellisense.md).

### Query plan visualizer

The **Query plan visualizer** presents `EXPLAIN` output in multiple interactive formats so you can identify performance bottlenecks.

- **Four views** — Tree View, Icicle View, Table View, and Source View.
- **Metrics** — inspect cost estimates, actual row counts, execution time, and buffer usage per node.
- **Import plans** — visualize saved plan files or editor content without a live database connection.
- **Copilot analysis** — select **Analyze with Copilot** (or **Analyze with AI** in Cursor) for an AI-generated explanation of the plan.

For details, see [Query plan visualizer](query-plan-visualizer.md).

### Schema visualizer

The **Schema visualizer** generates an interactive entity-relationship diagram. Tables appear as draggable nodes with columns listed inside, and foreign key relationships display as connecting edges.

- **Color-coded schemas** — each schema receives a distinct color for quick identification.
- **Legend toggle** — show or hide the schema legend to maximize diagram space.

For details, see [Schema visualizer](schema-visualizer.md).

### Server dashboard

The **Server dashboard** shows connection properties, server version, and SSL status for any connected server. For Azure Database for PostgreSQL Flexible Servers, it also displays Azure Monitor metrics. Investigation tabs let you drill into specific areas of server activity.

- **Overview** — monitor CPU, memory, storage, connections, IOPS, and other metrics grouped by category.
- **Queries** — view top SQL statements ranked by execution time, call count, or other metrics, with drill-down into individual query details.
- **Waits** — analyze wait events with a ranked table and over-time chart.
- **Sessions** — inspect active sessions, blocking trees, and lock activity.
- **Toolbar actions** — connect, disconnect, open a new query editor, launch the **Schema visualizer**, open an AI chat, or start Azure management actions from the dashboard toolbar.

For details, see [Server dashboard](server-dashboard.md).

### Azure server management

Manage Azure Database for PostgreSQL Flexible Server resources without leaving VS Code.

- **Start, stop, and restart** — control the server lifecycle from **Object Explorer** or the **Server dashboard**.
- **Firewall rules** — view and update network access rules.
- **Server parameters** — browse and modify server parameters.
- **Clone server** — duplicate an existing server configuration.

For details, see [Azure server management](azure-server-management.md).

### Server creation

Provision new PostgreSQL servers directly from VS Code.

- **Docker** — create a local PostgreSQL server in a Docker container for development and testing.
- **Azure Database for PostgreSQL Flexible Server** — walk through a guided setup that configures region, compute tier, storage, and authentication.
- **Azure HorizonDB** (Preview) — provision a cloud-native, highly scalable PostgreSQL cluster with configurable vCores and optional AI capabilities.

For details, see [Create a PostgreSQL server](create-server.md).

### Copilot integration

The extension integrates with AI assistants across chat, editor actions, and multi-step tool workflows.

- **@pgsql chat participant** — ask natural-language questions about your databases, generate queries, or get help with PostgreSQL concepts in the GitHub Copilot Chat panel. **Visual Studio Code only.** For details, see [@pgsql chat participant](copilot/pgsql-chat.md).
- **Editor actions** — right-click SQL in the editor to explain a query, rewrite it for optimization, or analyze its execution plan from the **AI Query Actions** submenu. Available in both Visual Studio Code and Cursor.
- **Agent mode** — the AI agent invokes PostgreSQL tools directly, combining AI reasoning with live database operations. Available in both Visual Studio Code and Cursor. For details, see [Agent mode](copilot/agent-mode.md).

For an overview of all AI capabilities, see [Copilot integration](copilot-integration.md).

### MCP server

The extension registers a Model Context Protocol (MCP) server that exposes PostgreSQL tools—connection management, schema exploration, query execution, and query plan visualization—to supported AI-enabled hosts. External AI tools can interact with your PostgreSQL connections programmatically through this registration.

For details, see [MCP server](mcp-server.md).

### psql terminal

Open a `psql` terminal session connected to any database in **Object Explorer**, or run `.sql` files through `psql` directly from the editor context menu. This gives you full access to native `psql` features such as `\` meta-commands, `COPY`, and interactive scripting.

For details, see [psql terminal](psql-terminal.md).

### Oracle to PostgreSQL migration

An AI-assisted migration workflow helps you convert Oracle database schemas and objects to PostgreSQL-compatible SQL.

- **Guided migration** — connect to an Oracle source, select objects to migrate, and review the converted output.
- **AI-assisted conversion** — A Microsoft Foundry model translates Oracle-specific syntax, data types, and procedural code to PostgreSQL equivalents.

For details, see [Oracle to PostgreSQL migration](oracle-migration.md).

## Supported operating systems

| Operating system | Architecture | Notes |
|---|---|---|
| Windows | x64, Arm64 | Arm64 requires Windows 11. |
| macOS | x64, Arm64 | — |
| Linux | x64, Arm64 | Requires `glibc` 2.35 or later. |

## Feedback and support

To report a bug or request a feature, file an issue on the [vscode-pgsql GitHub repository](https://github.com/microsoft/vscode-pgsql/issues).

## Related content

- [Quickstart: Connect and query](quickstart-connect-query.md)
- [Common workflows](common-workflows.md)
- [Connections and identity](connections.md)
- [Object Explorer](object-explorer.md)
- [Query editor and IntelliSense](query-editor-intellisense.md)
- [Query plan visualizer](query-plan-visualizer.md)
- [Schema visualizer](schema-visualizer.md)
- [Server dashboard](server-dashboard.md)
- [Azure server management](azure-server-management.md)
- [Create a PostgreSQL server](create-server.md)
- [Copilot integration](copilot-integration.md)
- [MCP server](mcp-server.md)
- [psql terminal](psql-terminal.md)
- [Oracle to PostgreSQL migration](oracle-migration.md)
- [Commands reference](reference/commands.md)
- [Settings reference](reference/settings.md)
- [Keyboard shortcuts reference](reference/keyboard-shortcuts.md)
