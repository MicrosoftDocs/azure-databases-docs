---
title: "Agent mode"
description: "Use Agent mode in the PostgreSQL extension to let your AI assistant chain PostgreSQL tools across multi-step workflows in Visual Studio Code and Cursor."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/11/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: how-to
---


# Agent mode

Agent mode lets the AI assistant in your editor use PostgreSQL tools from the extension as part of a single multi-step conversation. Instead of only answering a question, the assistant can connect to a database, inspect schema, run queries, open scripts, and help you move through a workflow end to end.

Agent mode runs in both **Visual Studio Code** (with GitHub Copilot) and **Cursor** (with its built-in AI). The extension exposes the same PostgreSQL tool surface in both editors; only the chat panel that opens differs.

Use Agent mode when you want the AI to take structured actions, not just explain or draft SQL.

## Prerequisites

Before you start, make sure you have:

- The PostgreSQL extension installed.
- Copilot/AI features enabled in the extension (`pgsql.copilot.enable` is `true`).
- At least one database connection configured in the extension.
- An AI assistant available in your editor:
  - **Visual Studio Code** — GitHub Copilot or GitHub Copilot Chat installed and active.
  - **Cursor** — no extra installation; the built-in AI is used automatically.

## Start Agent mode

1. Connect to the target server or database in the PostgreSQL extension.
2. In **Object Explorer**, right-click the database you want to use.
3. Select **Connect AI**.
4. Continue the conversation in the chat panel that opens with the workflow you want to complete.
   - In **Visual Studio Code**, this is the GitHub Copilot Chat panel in Agent mode.
   - In **Cursor**, this is Cursor's native AI panel; the extension provides a brief MCP-oriented preamble so the assistant knows about the available PostgreSQL tools.

After the session starts, the AI can combine PostgreSQL tools behind the scenes as it works through your request.

## Choose the right access mode

The `pgsql.copilot.accessMode` setting controls how much database access Agent mode receives. The setting ID keeps its `pgsql.copilot.*` prefix for compatibility; the user-visible label is **Copilot access mode** in Visual Studio Code and **AI access mode** in Cursor.

| Mode | What the AI can do | Recommended use |
|---|---|---|
| `ro` | Read-only operations such as `SELECT`, `SHOW`, `EXPLAIN`, schema inspection, and analysis | Production systems or shared environments where you want investigation without changes |
| `rw` | Read operations plus data-modifying statements and DDL, with explicit confirmation before execution | Local development, disposable sandboxes, and controlled test environments |

> [!CAUTION]
> Use `ro` mode for production databases unless you intentionally want schema or data changes available through Agent mode.

## Understand the tool families

Agent mode can use multiple tool families depending on the workflow.

| Tool family | What it does | When you use it |
|---|---|---|
| Connection tools | List profiles, connect, disconnect, list databases | Start or switch context |
| Schema context tools | Fetch object definitions or visualize schema | Understand tables, views, functions, indexes, and relationships |
| Query tools | Run read queries, inspect query plans, open scripts | Investigate data, validate ideas, or review generated SQL |
| Modification tools | Run DDL or DML with confirmation | Apply controlled schema or data changes in `rw` mode |
| Data import tools | Describe CSV files and bulk-load them | Plan and execute CSV import workflows |

> [!TIP]
> In **Cursor**, the same tools are also surfaced through the MCP server registration. Cursor's native chat can call them directly without using the **Connect AI** entry point. See [MCP server](../mcp-server.md) for details.

## Use Agent mode for common workflows

### Explore an unfamiliar database

Ask the AI to connect to the database, list key objects, and summarize the schema areas that matter to your task.

Example:

> Connect to my development database, list the tables in the public schema, and tell me which ones look related to customers and orders.

### Investigate query performance

Ask the AI to combine schema context with query execution or plan inspection.

Example:

> Connect to the staging database, run this query in read-only mode, and explain which part of the execution plan is driving the cost.

### Load or reshape data

Use Agent mode when the workflow includes scripts or CSV-based operations.

Example:

> Review this CSV file, tell me what schema it implies, and prepare a safe import plan for the `sales.records` table.

### Move from draft to manual review

When you want a human review checkpoint before execution, ask the AI to open the generated SQL in the query editor instead of running it immediately.

## Know when to use Agent mode instead of @pgsql

Use [@pgsql chat participant](pgsql-chat.md) when you want a schema-aware answer or a query draft. The `@pgsql` participant is available in **Visual Studio Code** only.

Use Agent mode (available in both Visual Studio Code and Cursor) when you want the AI to:

- connect to the right database for you,
- chain multiple tools in one conversation,
- inspect results before the next step, or
- prepare a script or controlled modification workflow.

> [!NOTE]
> In **Cursor**, Agent mode is the primary path because the `@pgsql` chat participant isn't available there. The same tool surface is also reachable from Cursor's native chat through the MCP server.

## Troubleshoot Agent mode

### The AI cannot modify the database

Check `pgsql.copilot.accessMode` and confirm that the active connection is not resolved to `ro`.

### The tool you expect is unavailable

Make sure Copilot integration is enabled and that you started from a database with a valid PostgreSQL connection context.

### A connection request fails

Confirm the connection profile still exists, the credentials are available, and the extension can connect to the same database outside Agent mode.

### I want a simpler chat-first workflow

In **Visual Studio Code**, use [@pgsql chat participant](pgsql-chat.md) when you want explanation, query drafting, or schema questions without tool-driven automation. In **Cursor**, ask the same kinds of questions from the native chat — the extension's MCP tools are still discoverable, but the chat behaves more conversationally without an explicit Agent mode entry.

## Related content

- [Copilot integration](../copilot-integration.md)
- [@pgsql chat participant](pgsql-chat.md)
- [MCP server](../mcp-server.md)
- [Query plan visualizer](../query-plan-visualizer.md)
- [Copilot tools reference](../reference/copilot-tools.md)
- [Settings reference](../reference/settings.md)
