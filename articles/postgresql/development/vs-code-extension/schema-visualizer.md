---
title: Schema Visualizer
titleSuffix: PostgreSQL extension for Visual Studio Code
description: Explore PostgreSQL table relationships in an interactive schema visualizer with filtering, refresh, and layout controls.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
# customer intent: As a user, I want to visualize PostgreSQL table relationships, so that I can understand schema structure before writing or changing SQL.
---

# Schema visualizer

The schema visualizer in the PostgreSQL extension opens a webview that maps tables and foreign key relationships for the database you already use in the extension. Use it to understand an unfamiliar schema, confirm how tables relate before you change them, or focus on one schema before you write SQL. The visualizer runs the same way in **Visual Studio Code** and **Cursor**.

## When to use the schema visualizer

Use the schema visualizer when you need to:

- get a relationship map for a database with many tables,
- focus on one schema without permanently hiding the rest of the database, or
- move from the **Connections** tree, the server dashboard, or an Agent mode tool workflow into a visual schema view.

> [!TIP]  
> Use the schema visualizer for structure and relationships. When you need object definitions, direct search, or script generation, use [Object explorer](object-explorer.md).

## Prerequisites

Before you open the schema visualizer, make sure you have:

- an active connection to the target PostgreSQL database, and
- an AI assistant available in your editor only if you want to open the visualizer from [Agent mode](copilot/agent-mode.md).

## Open the schema visualizer

### Open the full database map

1. In the **Connections** tree, right-click a database node.
1. Select **Visualize Schema**.
1. Wait for the **Visualize Schema** tab to open in the editor.

The visualizer opens a new editor tab and loads the tables, columns, and foreign key relationships for that database.

:::image type="content" source="schema-visualizer/cursor-editor-schema-visualizer-default.png" alt-text="Screenshot of the schema visualizer showing a database entity-relationship diagram." lightbox="schema-visualizer/cursor-editor-schema-visualizer-default.png":::

If you already work from [Server dashboard](server-dashboard.md), select **Visualize schema** in the toolbar and then choose the database you want to open.

### Focus on one schema

1. In the **Connections** tree, expand the database that contains the schema you want to inspect.
1. Right-click the schema node.
1. Select **Visualize Schema**.

The visualizer opens with that schema visible first and the other schemas hidden. Use this path when the full database diagram would be too dense to read on first load.

### Open from Agent mode

If you already work in [Agent mode](copilot/agent-mode.md), ask the AI assistant to visualize the connected database schema. The extension exposes the `pgsql_visualize_schema` tool for that workflow, so the AI can open the same schema visualizer without sending you back to the **Connections** tree first.

## Read the diagram

Each table appears as a node on the canvas. The node header shows the schema and table name, and the body lists the table's columns with their data types. Primary key columns include a key indicator so you can identify them quickly.

Relationship lines connect foreign key columns to the referenced columns on related tables. Follow those lines when you need to understand join paths, parent-child relationships, or cross-schema dependencies.

:::image type="content" source="schema-visualizer/cursor-editor-schema-visualizer-default.png" alt-text="Screenshot of the schema visualizer relationship map with table connections." lightbox="schema-visualizer/cursor-editor-schema-visualizer-default.png":::

> [!NOTE]  
> The schema visualizer focuses on table relationships. It shows tables and foreign key constraints only. For views, functions, sequences, and object definitions, use [Object explorer](object-explorer.md).

## Filter and compare schemas

When a database includes multiple schemas, the legend lists each schema with its own color and visibility control. Use the legend to reduce clutter and compare only the parts of the database that matter to the current task.

1. In the legend, find the schema you want to hide or restore.
1. Use the visibility button for that schema.
1. Review the updated diagram.

When you hide a schema, the remaining tables can still show colored indicators for hidden cross-schema relationships. That helps you keep important dependencies in view even when the related schema is temporarily hidden.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="schema-visualizer/default-schema-visualizer-schema-legend.png" alt-text="Screenshot of schema legend with per-schema visibility toggles." lightbox="schema-visualizer/default-schema-visualizer-schema-legend.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="schema-visualizer/cursor-editor-schema-visualizer-schema-legend.png" alt-text="Screenshot of schema legend with per-schema visibility toggles." lightbox="schema-visualizer/cursor-editor-schema-visualizer-schema-legend.png":::

---

## Work with large schemas

The schema visualizer includes navigation and layout controls so you can reframe the diagram as the visible tables change.

- **Pan**: Select and drag on an empty area of the canvas to move around the diagram.
- **Zoom**: Use the scroll wheel, trackpad pinch, or the **+** and **-** buttons in the controls overlay to zoom in and out.
- **Fit to view**: Select the fit-to-view button in the controls overlay to automatically zoom and center the diagram so all visible tables fit within the viewport.
- **Minimap**: For large schemas, use the minimap in the corner of the canvas to see your current viewport position relative to the full diagram.
- **Auto Layout**: Select **Auto Layout** to recalculate the layout for the visible tables.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="schema-visualizer/default-schema-visualizer-navigation-controls.png" alt-text="Screenshot of zoom and layout controls for the schema visualizer." lightbox="schema-visualizer/default-schema-visualizer-navigation-controls.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="schema-visualizer/cursor-editor-schema-visualizer-navigation-controls.png" alt-text="Screenshot of zoom and layout controls for the schema visualizer." lightbox="schema-visualizer/cursor-editor-schema-visualizer-navigation-controls.png":::

---

## Refresh after schema changes

The schema visualizer doesn't update automatically after you change the database. If you add or drop tables, columns, or foreign keys, select **Refresh** to reload the current schema model and redraw the relationship map.

## Related content

- [Common workflows](common-workflows.md)
- [Object explorer](object-explorer.md)
- [Server dashboard](server-dashboard.md)
- [Copilot integration](copilot-integration.md)
- [Agent mode](copilot/agent-mode.md)
