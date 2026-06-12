---
title: Copilot Integration
titleSuffix: PostgreSQL extension for Visual Studio Code
description: "Use GitHub Copilot (or Cursor's built-in AI) with the PostgreSQL extension: chat with @pgsql, analyze queries, explore schemas, and use Agent mode."
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
# customer intent: As a user, I want to understand the PostgreSQL extension's AI integration options, so that I can choose the right Copilot, Agent mode, or MCP workflow.
---

# Copilot integration

The PostgreSQL extension integrates with AI assistants through three surfaces: the **@pgsql** chat participant (Visual Studio Code only), **Agent mode** tools, and a **PostgreSQL Tools MCP Server Provider**. This page helps you choose the right entry point and understand the shared configuration that applies across all three.

The extension runs in both **Visual Studio Code** (with GitHub Copilot) and **Cursor** (with its built-in AI). Most features work the same way in both editors; the small number of editor-specific behaviors are called out throughout this article.

## Prerequisites

Before you use any AI-assisted feature, make sure the following requirements are met:

- The PostgreSQL extension is installed and you have at least one database connection configured.
- An AI assistant is available in your editor:
  - **Visual Studio Code**: install **GitHub Copilot** or **GitHub Copilot Chat** and sign in with an active subscription.
  - **Cursor**: no extra installation; the built-in AI is used automatically.

> [!NOTE]  
> Copilot features are enabled by default (`pgsql.copilot.enable` is `true`). When you set this to `false`, the **@pgsql** chat participant (Visual Studio Code only), **AI Query Actions** editor submenu, Agent mode tools, and the MCP server provider are all hidden.

> [!TIP]  
> AI assistance works best when you already have an active database connection. If you haven't connected yet, start with [Connections and identity](connections.md).

## Choose the right entry point

| If you want to... | Start here | Availability | Learn more |
| --- | --- | --- | --- |
| Ask a schema-aware question about your database | **@pgsql** chat participant | Visual Studio Code only | [@pgsql chat participant](copilot/postgresql-chat-participant.md) |
| Start Agent mode with a specific database already in scope | **Connect AI** from a database node in the **Connections** tree | Visual Studio Code and Cursor | [Agent mode](copilot/agent-mode.md) |
| Explain, rewrite, or analyze SQL from the editor | **AI Query Actions** submenu in the editor context menu | Visual Studio Code and Cursor | [Editor actions](#use-editor-actions-for-query-focused-help) |
| Automate a multi-step database task | **Connect AI** on a database node to start Agent mode | Visual Studio Code and Cursor | [Agent mode](copilot/agent-mode.md) |
| Expose PostgreSQL tools to MCP-compatible hosts | **PostgreSQL Tools MCP Server Provider** | Visual Studio Code and Cursor | [MCP server](mcp-server.md) |

## Use @pgsql for schema-aware chat

> [!NOTE]  
> The **@pgsql** chat participant is registered only in **Visual Studio Code**, where it plugs into GitHub Copilot Chat. In **Cursor**, use **Connect AI** from a database node in the **Connections** tree to start Agent mode with the same schema context, or rely on the MCP server in Cursor's native chat surface.

The extension registers an **@pgsql** chat participant (ID: `vscode-postgresql.chat-agent`) for schema-aware conversations in GitHub Copilot Chat. Type `@pgsql` followed by your question, and the participant answers using live schema context from your connected database.

To start a tool-driven workflow with a database already in scope, right-click a database node in the **Connections** tree and select **Connect AI**.

For end-user guidance, example prompts, and troubleshooting, continue to [@pgsql chat participant](copilot/postgresql-chat-participant.md).

## Use editor actions for query-focused help

When you have SQL open in the query editor, right-click to find the **AI Query Actions** submenu. It contains the following actions:

| Action | Description |
| --- | --- |
| **Explain Query** | Returns a plain-language explanation of what the query does. |
| **Rewrite Query** | Suggests an alternative version of the query while preserving the intended result. |
| **Analyze Query Performance** | Runs `EXPLAIN ANALYZE` against the connected database, then sends the execution plan to the AI for analysis. |

You can also select **Ask AI about this Query** from the editor toolbar to open a chat conversation grounded in the current editor contents.

To reset remembered query-inclusion choices for plan analysis, run **Clear query inclusion preferences for AI analysis** from the Command Palette.

## Use Agent mode for tool-driven workflows

Agent mode gives the AI assistant access to PostgreSQL tools so it can connect, inspect schema, run queries, open scripts, and work through multi-step tasks in one conversation. Right-click a database node in the **Connections** tree and select **Connect AI** to start an Agent mode session.

For tool families, example workflows, and troubleshooting, continue to [Agent mode](copilot/agent-mode.md).

## Use the MCP server in supported hosts

The extension registers a **PostgreSQL Tools MCP Server Provider** (ID: `pgsql-tools-mcp-server-provider`) that exposes the same PostgreSQL tool surface through the Model Context Protocol. MCP-compatible hosts can discover and invoke these tools without using the built-in chat workflows.

For supported hosts, automatic registration behavior, and the tool families exposed through MCP, continue to [MCP server](mcp-server.md).

## Configure access mode

The `pgsql.copilot.accessMode` setting controls how much database access the AI assistant receives across Agent mode and MCP tools. The default is **Read/Write** (`rw`).

| Setting value | UI label | What the AI assistant can do |
| --- | --- | --- |
| `ro` | **Read Only** | Read-only operations: `SELECT`, `SHOW`, `EXPLAIN`, schema inspection |
| `rw` | **Read/Write** | Read operations plus data-modifying statements and DDL, with explicit confirmation |

### Per-connection override

You can also set the access mode on individual connections. In the connection dialog, expand the **Copilot** section (**AI** in Cursor) and set **Copilot access mode** (**AI access mode** in Cursor) to one of:

| Option | Behavior |
| --- | --- |
| **Use Global Setting** | Falls back to the global `pgsql.copilot.accessMode` value (default) |
| **Read Only** | Forces read-only access for this connection regardless of the global setting |
| **Read/Write** | Forces read/write access for this connection regardless of the global setting |

The extension resolves the effective access mode using this fallback chain: per-connection value → global `pgsql.copilot.accessMode` setting → default (`rw`).

> [!CAUTION]  
> Use **Read Only** for production databases unless you intentionally want schema or data changes available through the AI assistant.

## Configure additional settings

| Setting | What it controls | Default |
| --- | --- | --- |
| `pgsql.copilot.enable` | Enables or disables all AI integration in the extension | `true` |
| `pgsql.copilot.accessMode` | Global AI access mode (**Read Only** or **Read/Write**) | `rw` |
| `pgsql.copilot.autoAttachQuery` | Whether SQL query text is included when analyzing plans with AI: **Ask Every Time**, **Always Include**, or **Never Include** | `ask` |
| `pgsql.copilot.modelOptions` | Advanced model tuning (max tokens, temperature, top_p) for the extension's AI workflows | - |

Setting IDs keep the `pgsql.copilot.*` prefix in both editors for backward compatibility, even where the user-visible labels say "AI".

## Feature-specific AI integrations

Several features include dedicated AI integration points:

| Feature | AI capability |
| --- | --- |
| [Query plan visualizer](query-plan-visualizer.md) | Analyze execution-plan data with **Analyze with Copilot** (or **Analyze with AI** in Cursor) |
| [Server dashboard](server-dashboard.md) | Open chat sessions from **Ask Copilot** buttons (**Ask AI** in Cursor) on the **Queries**, **Waits**, **Sessions**, and metric chart panels |
| [Schema visualizer](schema-visualizer.md) | Visualize schema relationships from an Agent mode workflow |

## Related content

- [@pgsql chat participant](copilot/postgresql-chat-participant.md)
- [Agent mode](copilot/agent-mode.md)
- [MCP server](mcp-server.md)
- [Copilot tools reference](reference/copilot-tools.md)
