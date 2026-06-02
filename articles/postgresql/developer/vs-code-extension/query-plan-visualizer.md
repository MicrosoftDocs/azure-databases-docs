---
title: "Query plan visualizer"
description: "Generate, import, and inspect PostgreSQL EXPLAIN plans in Tree, Table, Icicle, and Source views."
author: mmcfarland
ms.author: mmcfarland
ms.date: 05/11/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
---


# Query plan visualizer

Use the query plan visualizer in the PostgreSQL extension to inspect PostgreSQL `EXPLAIN` output without leaving your editor. You can generate a plan from the query editor or the Query Results panel, or open existing JSON or TEXT plan output from the editor. The visualizer runs the same way in **Visual Studio Code** and **Cursor**.

## Prerequisites

- [PostgreSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) installed.
- An active connection to a PostgreSQL server if you want to generate a live plan from the query editor or the Query Results panel.
- Optional AI assistant if you want AI-assisted analysis: install [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) in Visual Studio Code, or use the built-in AI in Cursor.
- Optional `EXPLAIN` output already open in the editor if you want to import a saved plan without connecting to a database.

## Choose how to open a plan

Use the entry point that matches your workflow:

- **Query editor**: Select **Visualize Query Plan** in the editor toolbar. If you do not select text first, the extension uses the current editor contents.
- **Query Results panel**: Run a query, then select **Visualize Query Plan** in the Query Results toolbar to inspect the query that produced that result set.
- **Imported plan**: Open any editor tab that contains PostgreSQL plan output, then run **PGSQL: Visualize Query Plan from Editor** from the **Command Palette**.

## Generate a plan from a live query

1. Open the SQL file you want to inspect in the query editor.
2. Connect to the target database.
3. Select the statement you want to analyze. If you leave the selection empty, the extension uses the current editor contents.
4. Select **Visualize Query Plan** in the editor toolbar. You can also run the query first and then select **Visualize Query Plan** in the **Query Results** panel.
5. In **Configure Query Plan**, choose the format and options you want, and then press Enter.
6. Review the plan in the visualizer.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/query-plan/default.png" alt-text="Query plan tree view in Visual Studio Code" lightbox="./media/screenshots/vscode/query-plan/default.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/query-plan/default.png" alt-text="Query plan tree view in Cursor" lightbox="./media/screenshots/cursor/query-plan/default.png":::

---

### Configure query plan options

The **Configure Query Plan** picker lets you choose the output format and the `EXPLAIN` options to run.

| Option | What it changes |
|---|---|
| **JSON** | Returns structured plan output that works best across the visual views. |
| **TEXT** | Returns PostgreSQL's plain-text `EXPLAIN` output and preserves that source in **Source View**. |
| **ANALYZE** | Executes the query and includes actual run-time statistics. |
| **BUFFERS** | Adds buffer usage statistics. Selecting it automatically enables **ANALYZE**. |
| **TIMING** | Adds actual timing data. Selecting it automatically enables **ANALYZE**. |
| **WAL** | Adds WAL usage statistics. Selecting it automatically enables **ANALYZE**. |
| **VERBOSE** | Adds extra output details such as schema and column information. |
| **COSTS** | Includes estimated startup and total cost values. |
| **SETTINGS** | Includes planner settings that differ from defaults. |

> [!CAUTION]
> `EXPLAIN ANALYZE` runs the query. If the statement modifies data, such as `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`, the extension shows a confirmation prompt before it continues.

## Open a saved plan from the editor

1. Open an editor tab that contains PostgreSQL `EXPLAIN` output in JSON or TEXT form.
2. Open the **Command Palette** (**Ctrl+Shift+P**).
3. Run **PGSQL: Visualize Query Plan from Editor**.
4. Review the imported plan in the visualizer.

This workflow does not require an active database connection. The command reads the current editor contents, so you can use it with copied plan output, saved `.json` or `.txt` files, or plan text pasted into a scratch editor.

## Switch between views

Use the view selector in the toolbar to move between **Tree View**, **Icicle View**, **Table View**, and **Source View**.

### Tree View

**Tree View** opens by default. Use it when you want a node-by-node diagram of the execution plan.

- Use the zoom controls to zoom in, zoom out, reset the view, or fit the plan to the window.
- Use the options panel to change the layout direction and the color metric that highlights expensive or unusual nodes.
- Select a node to open the details panel.
- Right-click a node to jump to another view or analyze that node with the AI assistant.

### Table View

Use **Table View** when you want to sort, search, and compare many nodes at once.

- The plan is flattened into a sortable table rather than a collapsible tree.
- The search box appears only in **Table View**.
- Search matches node type, relation name, index name, alias, filter text, and subplan name.
- Use the preset chooser to focus on **Performance**, **Estimates**, **Efficiency**, or **I/O**, or customize the visible metric columns.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/query-plan/table-view.png" alt-text="Query plan table view with tabular node data" lightbox="./media/screenshots/vscode/query-plan/table-view.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/query-plan/table-view.png" alt-text="Query plan table view with tabular node data" lightbox="./media/screenshots/cursor/query-plan/table-view.png":::

---

### Icicle View

Use **Icicle View** when you want a full-width visual summary of where cost, time, or buffer usage is concentrated.

- **Icicle View** is a separate view, not a pane inside **Tree View**.
- Use the options panel to switch presets, change the width metric, change the color metric, and switch between self and total scope where supported.
- Hover over a block to inspect its metrics, or right-click a block to open details or move to another view.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/query-plan/icicle-view.png" alt-text="Icicle view comparing cost, time, and buffer usage concentration" lightbox="./media/screenshots/vscode/query-plan/icicle-view.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/query-plan/icicle-view.png" alt-text="Icicle view comparing cost, time, and buffer usage concentration" lightbox="./media/screenshots/cursor/query-plan/icicle-view.png":::

---

### Source View

Use **Source View** when you want the original plan output.

- Select **Options** to switch between **Tree** and **Text** mode.
- The panel shows whether the imported or generated source is **JSON** or **TEXT**.
- **Expand All** and **Collapse All** appear in the toolbar only while **Source View** is active.
- In **Text** mode, the plan opens in a read-only editor. In **Tree** mode, you can inspect the parsed structure as a collapsible tree.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/query-plan/source-view.png" alt-text="Source view showing original plan output" lightbox="./media/screenshots/vscode/query-plan/source-view.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/query-plan/source-view.png" alt-text="Source view showing original plan output" lightbox="./media/screenshots/cursor/query-plan/source-view.png":::

---

Select **Copy Plan** at any time to copy the current plan source to the clipboard. JSON plans are copied in formatted form, and TEXT plans are copied as their original source.

## Inspect plan nodes

Select a node in **Tree View**, **Table View**, or **Icicle View** to open the details panel.

- **General** shows the node type, key metrics, and plan-specific analysis details.
- **I/O** appears when the plan includes buffer data.
- **Conditions** appears when the node exposes filters, join conditions, or similar predicates.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="./media/screenshots/vscode/query-plan/node-details.png" alt-text="Plan node details panel with metrics, I/O, and predicate tabs" lightbox="./media/screenshots/vscode/query-plan/node-details.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="./media/screenshots/cursor/query-plan/node-details.png" alt-text="Plan node details panel with metrics, I/O, and predicate tabs" lightbox="./media/screenshots/cursor/query-plan/node-details.png":::

---

Use this panel to compare estimated versus actual work, inspect buffer-heavy nodes, and confirm which predicates are driving the plan.

## Analyze plans with the AI assistant

Use the AI assistant when you want the extension to open an analysis chat with the current plan as context.

### Analyze the full plan

1. Open the plan in the visualizer.
2. Select **Analyze with Copilot** (or **Analyze with AI** in Cursor).
3. Choose whether to include your SQL query text with the analysis.
4. Review the new chat session that opens in Agent mode.

If the plan came from **PGSQL: Visualize Query Plan from Editor** and there is no useful SQL text yet, the extension can prompt you to enter the query first so the AI has better context.

### Analyze one node

1. Right-click the node you want to inspect.
2. Select **Analyze this node with Copilot** (or **Analyze this node with AI** in Cursor).
3. Review the new Agent mode chat session for node-specific analysis.

### Control whether SQL text is included

The `pgsql.copilot.autoAttachQuery` setting controls how the extension handles SQL text when it launches AI analysis:

- **Ask whether to include SQL each time**
- **Always include SQL without prompting**
- **Never include SQL**

When you choose to include or exclude SQL from the prompt, the extension can also offer to remember that choice for future sessions.

### Use the query plan tool in Agent mode

The visualizer caches the current plan and exposes it to the AI assistant through the `pgsql_query_plan` tool, or the MCP equivalent on supported hosts. That tool supports these actions:

| Action | Use it for |
|---|---|
| `get_summary` | Get a plan-wide summary before drilling into details. |
| `get_node` | Inspect one node by ID. |
| `get_subtree` | Inspect a node together with its descendants. |
| `list_nodes` | Find nodes by type or minimum cost. |

If you want the AI to start from the active query instead of the visualizer, use **Analyze Query Performance** from the editor's **AI Query Actions** submenu. Use the visualizer when you want to inspect the plan yourself first and then hand that exact plan to the AI.

## Tips for performance analysis

- Use **ANALYZE** when it is safe to run the statement. Estimates alone can hide bad row-count assumptions.
- Compare estimated and actual row counts to spot stale statistics or filter selectivity problems.
- Switch to **Table View** when the plan is large and you need search or side-by-side metric comparisons.
- Switch to **Source View** when you need the raw plan for an issue, code review, or discussion with teammates.

## Related content

- [Query editor and IntelliSense](query-editor-intellisense.md)
- [Copilot integration](copilot-integration.md)
- [Agent mode](copilot/agent-mode.md)
- [Commands reference](reference/commands.md)
- [Settings reference](reference/settings.md)
