---
title: Common Workflows
titleSuffix: PostgreSQL extension for Visual Studio Code
description: Choose the right PostgreSQL extension article for common tasks such as connecting, exploring schemas, tuning queries, and managing Azure servers.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
# customer intent: As a user, I want to find the right PostgreSQL extension workflow for my task, so that I can quickly move from goal to guidance.
---

# Common workflows

Use this page when you know the task you want to complete, but you don't yet know which PostgreSQL extension article or surface to start with. If you want a feature-by-feature tour instead, start with the [PostgreSQL extension for Visual Studio Code](postgresql-extension-overview.md).

## Choose the workflow that matches your task

| If you want to... | Start here | Then continue to... |
| --- | --- | --- |
| Connect and run a first query | [Quickstart: Connect and query PostgreSQL](quickstart-connect-query.md) | [Connections and identity](connections.md), [Query editor and IntelliSense](query-editor-intellisense.md) |
| Explore an unfamiliar database | [Object explorer](object-explorer.md) | [Schema visualizer](schema-visualizer.md), [Copilot integration](copilot-integration.md) |
| Investigate a slow query | [Query editor and IntelliSense](query-editor-intellisense.md) | [Query plan visualizer](query-plan-visualizer.md), [Copilot integration](copilot-integration.md), [Server dashboard](server-dashboard.md) |
| Manage an Azure Database for PostgreSQL flexible server | [Connections and identity](connections.md) | [Server dashboard](server-dashboard.md), [Azure server management](azure-server-management.md), [Create a PostgreSQL server](create-server.md) |
| Use Copilot or host-integrated AI workflows | [Copilot integration](copilot-integration.md) | [@pgsql chat participant](copilot/postgresql-chat-participant.md), [Agent mode](copilot/agent-mode.md), [MCP server](mcp-server.md) |
| Use terminal-based PostgreSQL workflows | [Use psql in the terminal](postgresql-terminal.md) | [Query editor and IntelliSense](query-editor-intellisense.md) |

## Connect and run your first query

Use this path when you're installing the extension for the first time or validating that a server is reachable.

1. Start with [Quickstart: Connect and query PostgreSQL](quickstart-connect-query.md) for the shortest end-to-end setup.
1. If you need saved profiles, Microsoft Entra ID authentication, AWS IAM authentication for Amazon RDS/Aurora PostgreSQL, or advanced SSL/TLS settings, continue to [Connections and identity](connections.md).
1. After the connection works, move to [Query editor and IntelliSense](query-editor-intellisense.md) to open **New Query**, run statements, and inspect output in the **PostgreSQL Query Results** panel.

## Explore an unfamiliar database

Use this path when you inherit an existing schema and need to understand the structure before you write SQL.

1. Start with [Object explorer](object-explorer.md) to browse servers, databases, schemas, and objects in the **Connections** tree.
1. If you need to find a specific object quickly, use **Search Objects** from [Object explorer](object-explorer.md) instead of expanding the tree manually.
1. If you need a relationship map, continue to [Schema visualizer](schema-visualizer.md).
1. If you want schema-aware AI help identifying relevant objects or drafting the next query, continue to [Copilot integration](copilot-integration.md).

## Investigate and optimize a slow query

Use this path when a query is slow, you need to understand why PostgreSQL chose a specific plan, or you want help narrowing down bottlenecks.

1. Reproduce the statement in [Query editor and IntelliSense](query-editor-intellisense.md).
1. Open [Query plan visualizer](query-plan-visualizer.md) to inspect the execution plan in **Tree View**, **Table View**, **Icicle View**, or **Source View**.
1. If you want AI assistance, use [Copilot integration](copilot-integration.md) to choose between **Analyze Query Performance**, query-focused editor actions, or Agent mode analysis of the cached plan.
1. For Azure-hosted servers, open the [Server dashboard](server-dashboard.md) to correlate query findings with CPU percentage, IOPS, and connection metrics.

## Manage an Azure Database for PostgreSQL flexible server

Use this path when you want to monitor or administer Azure Database for PostgreSQL flexible server without switching to the Azure portal for every step.

1. Set up the connection and identity flow in [Connections and identity](connections.md).
1. Select **Dashboard** on the server node to open the [Server dashboard](server-dashboard.md) and review server details, metrics, and quick actions.
1. Continue to [Azure server management](azure-server-management.md) for firewall rules, parameters, backups, logs, and Azure-specific administration.
1. When you need a new environment, use [Create a PostgreSQL server](create-server.md) to provision an Azure Database for PostgreSQL flexible server or create a local Docker-based instance.

## Use Copilot or host-integrated AI workflows

Use this path when you want schema-aware chat, tool-driven automation, or host-level AI integration beyond a single editor command.

1. Start with [Copilot integration](copilot-integration.md) to choose the right entry point for the task in front of you.
1. Continue to [@pgsql chat participant](copilot/postgresql-chat-participant.md) when you want schema-aware chat in Copilot Ask mode.
1. Continue to [Agent mode](copilot/agent-mode.md) when you want Copilot to connect, inspect schema, run queries, and work through multi-step database tasks.
1. Continue to [MCP server](mcp-server.md) when your host supports automatic MCP registration and you want the extension's PostgreSQL tool surface available there.

## Use native `psql` capabilities

Use this path when you need an interactive terminal session, `\` meta-commands, `COPY` workflows, or script execution in a native `psql` environment.

1. Start with [Use psql in the terminal](postgresql-terminal.md) to open **Connect with PSQL** from a database node or to run **Run file with PSQL** for a saved `.sql` file.
1. Return to [Query editor and IntelliSense](query-editor-intellisense.md) when you want IntelliSense, visual results, charts, query history, and export options in the editor.

## Related content

- [PostgreSQL extension for Visual Studio Code](postgresql-extension-overview.md)
- [Quickstart: Connect and query PostgreSQL](quickstart-connect-query.md)
- [Connections and identity](connections.md)
- [Object explorer](object-explorer.md)
- [Query editor and IntelliSense](query-editor-intellisense.md)
