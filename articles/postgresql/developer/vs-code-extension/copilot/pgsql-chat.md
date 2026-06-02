---
title: "@pgsql chat participant"
description: "Ask schema-aware questions in GitHub Copilot Chat by using the PostgreSQL extension's @pgsql chat participant. Visual Studio Code only."
author: mmcfarland
ms.author: mmcfarland
ms.date: 05/11/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
---


# @pgsql chat participant

The PostgreSQL extension registers an **@pgsql** chat participant in GitHub Copilot Chat. Use it when you want schema-aware help about the database you already use in the extension, such as object discovery, query drafting, query explanation, or next-step suggestions.

The participant works best when you already have an active connection because it can use live schema context from that database.

> [!IMPORTANT]
> **The `@pgsql` chat participant is available in Visual Studio Code only.** It plugs into GitHub Copilot Chat, which is not available in Cursor or other forks. In **Cursor**, use **Connect AI** from a database node in **Object Explorer** to start [Agent mode](agent-mode.md) with the same schema context, or invoke the extension's PostgreSQL tools directly from Cursor's native chat through the [MCP server](../mcp-server.md).

## Prerequisites

Before you start, make sure you have:

- GitHub Copilot or GitHub Copilot Chat installed and active in Visual Studio Code.
- The PostgreSQL extension installed.
- Copilot/AI features enabled in the extension (`pgsql.copilot.enable` is `true`).
- A PostgreSQL connection configured in the extension.

> [!NOTE]
> If you ask `@pgsql` a question without an active connection, it can still answer general PostgreSQL questions, but it will not be able to reference your actual schema, tables, or columns.

## Start a schema-aware chat

1. Connect to the target database in the PostgreSQL extension.
2. Open GitHub Copilot Chat.
3. Type `@pgsql` followed by your question.
4. Review the answer and decide whether you need a follow-up question, a query draft, or a deeper workflow in [Agent mode](agent-mode.md).

## Bring database context into Agent mode

If you already know which database you want to work with, start from the database node in **Object Explorer** and select **Connect AI** to open Agent mode with database context already in scope. This path works in both Visual Studio Code and Cursor.

Use that path when you want the AI assistant to connect, inspect schema, and work through a task such as:

- "What tables are in this database?"
- "Which tables look related to customers and orders?"
- "Write a query that shows the top 10 customers by order count."

## Ask questions that work well with @pgsql

The @pgsql chat participant is especially useful for these task types:

| Goal | Example prompt |
|---|---|
| Explore schema | `@pgsql What tables are in the public schema?` |
| Understand relationships | `@pgsql Which tables connect orders to customers?` |
| Draft SQL | `@pgsql Write a query that shows monthly revenue by region.` |
| Explain existing SQL | `@pgsql Explain what this query is doing and where it might be slow.` |
| Plan next steps | `@pgsql I need to add a customer status field. What should I review before I change the schema?` |

Ask for one decision at a time when you want the clearest results. If you need a multi-step workflow that connects, inspects schema, runs a query, and returns results in one conversation, move to [Agent mode](agent-mode.md).

## Review and use the response

Use @pgsql responses as working guidance, not as unreviewed final output.

- Review generated SQL before you run it.
- Use the query editor when you want to test or refine a query manually.
- Use Object Explorer or the schema visualizer to confirm the objects the participant mentions.
- Use Agent mode when you want the AI assistant to take actions instead of only answering.

> [!TIP]
> Start with schema-discovery questions before you ask for large query rewrites. The better the participant understands your database context, the better the next answers tend to be.

## Troubleshoot @pgsql answers

### The answer is too generic

Make sure you are connected to the correct database and ask a schema-specific question instead of a broad PostgreSQL question.

### The participant cannot find the right objects

Confirm the object names in Object Explorer first, then include the schema or table names directly in your prompt.

### I'm in Cursor and don't see `@pgsql`

The chat participant is registered only in Visual Studio Code. In Cursor, use **Connect AI** from **Object Explorer** to start [Agent mode](agent-mode.md), or rely on the [MCP server](../mcp-server.md) to expose the same tools to Cursor's native chat.

### I want the AI to do more than answer

Use [Agent mode](agent-mode.md) when you want the AI to combine connection, schema inspection, queries, scripts, or data operations in one workflow.

## Related content

- [Copilot integration](../copilot-integration.md)
- [Agent mode](agent-mode.md)
- [MCP server](../mcp-server.md)
- [Connections and identity](../connections.md)
- [Query editor and IntelliSense](../query-editor-intellisense.md)
- [Chat participant reference](../reference/chat-participant.md)
