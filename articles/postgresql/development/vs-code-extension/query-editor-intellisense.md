---
title: Query Editor and IntelliSense
titleSuffix: PostgreSQL extension for Visual Studio Code
description: Write and execute PostgreSQL queries with IntelliSense, view results in the results grid, export data, and use code snippets in the PostgreSQL extension for Visual Studio Code.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to write, run, and refine PostgreSQL queries with IntelliSense and results tools, so that I can develop SQL efficiently in Visual Studio Code.
---

# Query editor and IntelliSense

The PostgreSQL extension for Visual Studio Code provides a query editor with IntelliSense completions, keyboard-driven query execution, a results grid with export options, and built-in code snippets. You write SQL in a standard VS Code editor tab and run it against any connected PostgreSQL server without leaving the IDE.

## Prerequisites

- [PostgreSQL extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) installed.
- An active connection to a PostgreSQL server. For setup steps, see [Quickstart: Connect and query PostgreSQL](quickstart-connect-query.md).

## Open a query editor

You can open a new query editor in several ways:

- In the **Connections** tree, right-click a database node and select **New Query**.
- Run `PGSQL: New Query` from the Command Palette (**Ctrl+Shift+P**).
- Open or create any file with a `.sql` extension.

The query editor uses the VS Code text editor with the SQL language mode. When you connect the editor to a server, the extension activates IntelliSense and enables query execution commands.

### Connect and disconnect

To associate a query editor with a database connection:

| Action | Windows / Linux | macOS |
| --- | --- | --- |
| Connect | **Ctrl+Shift+C** | **Cmd+Shift+C** |
| Disconnect | **Ctrl+Shift+D** | **Cmd+Shift+D** |

You can also run `PGSQL: Connect` or `PGSQL: Disconnect` from the Command Palette.

### Change the database context

The active database for query execution appears in the VS Code status bar. To switch to a different database:

1. Select the database name in the status bar, or run `PGSQL: Change PostgreSQL Database` from the Command Palette.
1. Select the target database from the picker.

The new database context applies to all subsequent query executions in that editor.

### Connection status lens

When `pgsql.showConnectionStatusLens` is `true` (the default), the editor displays a code lens at the top of the file that shows the current connection status. Select the lens to connect or change databases.

## IntelliSense

IntelliSense provides context-aware auto-completions as you type SQL in the query editor. The extension analyzes your connected database schema to suggest tables, columns, functions, and keywords.

IntelliSense activates automatically as you type, or you can trigger it manually with **Ctrl+Space** (**Cmd+Space** on macOS). The following completion types are available:

| Completion type | Description |
| --- | --- |
| Keyword | SQL keywords such as `SELECT`, `FROM`, `WHERE` |
| Table / View | Tables and views in the current database |
| Column | Columns for tables referenced in the query |
| Function | Built-in and user-defined functions |
| Schema | Available schemas in the database |
| Join suggestion | `JOIN` clauses based on foreign key relationships |

When you type `JOIN` after a table reference, IntelliSense suggests related tables and fills in the join condition based on foreign key relationships.

### Configure IntelliSense

Enable or disable IntelliSense with the `pgsql.intelliSense.enableIntelliSense` setting. IntelliSense is enabled by default.

### Refresh the IntelliSense cache

If you change your database schema (for example, by adding tables or columns) and IntelliSense doesn't reflect those changes, refresh the cache:

1. Open the Command Palette (**Ctrl+Shift+P**).
1. Run `PGSQL: Refresh IntelliSense Cache`.

Use this command after schema migrations, DDL changes, or changes made outside the current editor session.

## Run queries

The extension provides multiple ways to run SQL queries against your connected database.

### Execute a query

Use **Execute PostgreSQL Query** to run SQL in the editor. If you select specific text, only the selected text runs. If nothing is selected, the entire contents of the editor run.

| Action | Windows / Linux | macOS |
| --- | --- | --- |
| Execute PostgreSQL Query | **Ctrl+Shift+E** or **Shift+Enter** | **Cmd+Shift+E** or **Shift+Enter** |
| Execute Current PostgreSQL Statement | **Ctrl+Shift+Enter** | **Ctrl+Shift+Enter** |

**Execute Current PostgreSQL Statement** runs only the SQL statement at the current cursor position. Use this command when you have multiple statements in the editor and want to run one without selecting it.

### Cancel a query

To stop a long-running query, run `PGSQL: Cancel PostgreSQL Query` from the Command Palette. The status bar shows execution progress while a query is running.

## PostgreSQL Query Results panel

After you run a query, results appear in the **PostgreSQL Query Results** panel below the editor. The panel has up to three tabs depending on the query type.

### Results tab

The **Results** tab displays the results grid. When a query returns multiple result sets, each set appears in its own grid within the tab.

The results grid provides these features for exploring data:

- **Sort**: Right-click a column header and select **Sort Ascending** or **Sort Descending**. Select **Clear Sort** to remove the sort.
- **Filter**: Right-click a column header and select **Show Filter** to narrow down displayed rows.
- **Resize columns**: Drag column borders to adjust width, or enable `pgsql.resultsGrid.autoSizeColumns` (on by default) to auto-size columns based on visible content.
- **Row numbering**: Row numbers appear on the left side of the grid.
- **Search**: Use the search field in the results toolbar to find values in the grid.

Joined queries and wider result sets use the same grid experience, so you can sort, filter, and scan related columns without leaving the editor.

#### Copy data

Right-click in the results grid to access copy options:

| Option | Description |
| --- | --- |
| **Select All** | Select all rows in the result set |
| **Copy** | Copy selected cells to the clipboard |
| **Copy with Headers** | Copy selected cells with column headers |
| **Copy Headers** | Copy only the column headers |

You can also use these results-pane keyboard shortcuts (configurable through the `pgsql.shortcuts` setting):

| Action | Default shortcut |
| --- | --- |
| Copy selection | **Ctrl+C** |
| Select all | **Ctrl+A** |
| Toggle results pane | **Ctrl+Alt+R** |
| Toggle messages pane | **Ctrl+Alt+Y** |
| Focus results grid | **Ctrl+Alt+G** |
| Previous result grid | **Ctrl+Up** |
| Next result grid | **Ctrl+Down** |

> [!TIP]  
> Set `pgsql.copyIncludeHeaders` to `true` to include column headers every time you copy. Set `pgsql.copyRemoveNewLine` to `false` to preserve newline characters in copied cells.

#### Save results

Export query results by selecting a save button in the results toolbar:

| Button | Format |
| --- | --- |
| **Save as CSV** | Comma-separated values (.csv) |
| **Save as JSON** | JavaScript Object Notation (.json) |
| **Save as Excel** | Microsoft Excel workbook (.xlsx) |

Customize CSV export behavior with these settings:

| Setting | Description | Default |
| --- | --- | --- |
| `pgsql.saveAsCsv.delimiter` | Column delimiter character | `,` |
| `pgsql.saveAsCsv.lineSeparator` | Line separator | System default |
| `pgsql.saveAsCsv.textIdentifier` | Character for enclosing text fields | `"` |
| `pgsql.saveAsCsv.encoding` | File encoding | `utf-8` |
| `pgsql.saveAsCsv.includeHeaders` | Include column headers | `true` |

#### Open results in a separate tab

For large result sets, open the results in a dedicated editor tab for more space. Select **Open in New Tab** in the results toolbar, or set `pgsql.openQueryResultsInTabByDefault` to `true` in your settings to always open results in a separate tab.

### Messages tab

The **Messages** tab shows query execution information including status messages, row counts, and execution time. Each message includes a timestamp.

The messages pane opens by default alongside the results grid. To change this behavior, set `pgsql.messagesDefaultOpen` to `false`.

> [!TIP]  
> Set `pgsql.showBatchTime` to `true` to display execution time for individual batches.

### Query Plan tab

When you run an `EXPLAIN` or `EXPLAIN ANALYZE` query, a **Query Plan** tab appears alongside **Results** and **Messages**. Select this tab to open the built-in execution plan visualizer, or select the **Visualize Query Plan** button in the PostgreSQL Query Results panel toolbar.

You can also run **Visualize Query Plan (PostgreSQL)** from the Command Palette to visualize the plan for the current query.

For detailed information about the execution plan visualizer, see [Query plan visualizer](query-plan-visualizer.md).

### Graph view for Apache AGE queries

When a query returns graph-oriented results from Apache AGE, the extension detects `cypher()` function calls and Apache AGE patterns (`agtype`, `ag_catalog`) and opens the result batch in a graph view instead of the standard grid.

- **Switch views**: Select **Switch to Graph** in the results toolbar to switch from the grid to the graph view, or **Switch to Table** to return to the grid.
- **Inspect elements**: Select nodes or edges in the graph to view their labels and properties in the **Properties** panel.
- **Navigate**: Use the graph toolbar buttons: **Zoom In**, **Zoom Out**, **Zoom to Fit**, and **Reset**.
- **Export**: Select **Save as PNG** in the graph toolbar to export the graph as an image.

> [!NOTE]  
> If the query doesn't return graphable data, the extension keeps the standard grid view.

## Code snippets

The extension includes built-in PostgreSQL code snippets that help you scaffold common SQL patterns. Type a snippet prefix in the editor and press **Tab** to expand the snippet. Tab through placeholders within the expanded snippet to fill in values.

### Available snippets

| Prefix | Description |
| --- | --- |
| `pgCreateTable` | Create a basic table with a primary key |
| `pgDropDatabase` | Drop an existing PostgreSQL database |
| `pgDropTable` | Remove a table |
| `pgInsertData` | Insert a row into a table |
| `pgSelectAll` | Simple `SELECT *` query |
| `pgUpdateRows` | Update data in a table |
| `pgDeleteRows` | Delete data from a table |
| `pgCreateIndex` | Create an index on a specified column |
| `pgCreateUser` | Create a new role or user |
| `pgGrantPrivileges` | Grant privileges on a table to a user |
| `pgCTE` | Common Table Expression (CTE) example |
| `pgLeftJoin` | `LEFT JOIN` query example |
| `pgExplainAnalyze` | `EXPLAIN ANALYZE` query for performance details |
| `pgListTables` | List all tables in a specific schema |

> [!TIP]  
> Type `pg` in the editor and browse the IntelliSense suggestions to see all available snippets.

## Query history

The **Query History** view in the PostgreSQL Activity Bar panel automatically captures the queries you run, so you can revisit and reuse them later.

### Manage query history

| Action | How to |
| --- | --- |
| Open a query | Select an entry in the **Query History** view to load it into a new editor |
| Run a query | Right-click an entry and select **Run Query** |
| Copy a query | Right-click an entry and select **Copy Query** |
| Delete an entry | Right-click an entry and select **Delete** |
| Clear all | Select the **Clear All Query History** button in the view toolbar |
| Browse in Command Palette | Run `PGSQL: Open Query History in Command Palette` |

### Control history capture

Use the **Query History** view toolbar to start or pause capture:

- **Start Query History Capture**: Resume recording executed queries.
- **Pause Query History Capture**: Stop recording.

Configure history behavior with these settings:

| Setting | Description | Default |
| --- | --- | --- |
| `pgsql.enableQueryHistoryFeature` | Enable the Query History feature | `true` |
| `pgsql.enableQueryHistoryCapture` | Automatically capture executed queries | `true` |
| `pgsql.queryHistoryLimit` | Maximum number of stored history entries | `20` |

## Related content

- [Quickstart: Connect and query PostgreSQL](quickstart-connect-query.md)
- [Query plan visualizer](query-plan-visualizer.md)
- [Object explorer](object-explorer.md)
- [Settings reference](reference/settings.md)
