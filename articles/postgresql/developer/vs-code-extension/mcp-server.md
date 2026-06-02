---
title: "MCP server"
description: "Understand how the PostgreSQL extension registers an MCP server in supported hosts (Visual Studio Code and Cursor) and what tools it exposes."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 05/11/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: how-to
---


# MCP server

The PostgreSQL extension can register a Model Context Protocol (MCP) server definition in supported AI-enabled hosts. That registration lets the host discover PostgreSQL tools for connection management, schema exploration, query execution, and related workflows without asking you to configure each tool by hand.

Use this page when you want to understand how MCP support works in the extension, what hosts are supported today, and which tool families become available after registration.

## Prerequisites

Before you rely on the MCP server, make sure you have:

- The PostgreSQL extension installed in Visual Studio Code or Cursor.
- Copilot/AI features enabled in the extension (`pgsql.copilot.enable` is `true`). The setting ID keeps its `pgsql.copilot.*` prefix in both editors; the label appears as **AI** in Cursor.
- At least one saved connection profile if you want MCP tools to connect to a server quickly.
- A supported host that exposes an MCP registration API.

## Understand how MCP registration works

The extension registers the MCP server automatically when all of the following are true:

1. The host exposes a supported MCP registration API.
2. The extension can retrieve a valid MCP server URL and bearer token from its language service.
3. Copilot integration is enabled.

Today, the code path explicitly supports:

- **Visual Studio Code 1.102 and later** through the MCP server definition provider API
- **Cursor** through Cursor's `registerServer` MCP API

In Visual Studio Code, the extension registers the server as **PostgreSQL MCP**. In Cursor, it registers the server as **pgsql-mcp**.

> [!IMPORTANT]
> The extension does not currently expose a manual copy-and-paste setup flow for standalone clients that expect you to enter the MCP URL and token yourself. If your client does not support host-level discovery or registration, use the extension's built-in AI workflows instead.

## Prepare connection profiles for MCP tools

Most useful MCP flows depend on saved connection information.

1. Open [Connections and identity](connections.md) and create or update the connection profiles you want the host to use.
2. Save credentials where your workflow requires them.
3. Verify that you can connect to the target database from the extension before you rely on MCP-based automation.

This matters because connection-oriented MCP tools resolve the target profile from the extension's connection store rather than from a separate database configuration in the AI host.

## Use MCP tools in a supported host

After the host discovers the PostgreSQL MCP server, it can call the tool surface exposed by the extension.

| Tool family | What it helps with | Typical use |
|---|---|---|
| **List Connection Profiles** | Discover saved profiles | Find the right profile before connecting |
| **Connect to PostgreSQL Database** | Open a database session from a saved profile | Start a task on the right server or database |
| **List Databases** | Enumerate databases on the connected server | Switch context or inspect available databases |
| **Get Database Objects** | Fetch schema context | Identify tables, views, functions, and other objects before asking follow-up questions |
| **Run a Query** | Execute read-oriented SQL | Inspect data or validate assumptions |
| **Modify Database** | Execute data or schema changes | Apply DDL or DML in workflows that require write access |
| **Open SQL Script** | Create a script for review | Move from agent output to a human-reviewed query editor flow |
| **Query Plan** | Inspect cached plan data | Analyze performance workflows |
| **Visualize Database Schema** | Render a schema view | Understand relationships before writing or changing SQL |
| **Get Dashboard Context** | Retrieve active dashboard session context, including available metrics and configuration | Discover which metrics are available before requesting metric data |
| **Get Dashboard Metric Data** | Fetch batched cached time-series data from an open server dashboard | Analyze server performance trends without running live queries |

> [!TIP]
> For safer workflows, start with discovery tools such as **List Connection Profiles**, **Connect to PostgreSQL Database**, and **Get Database Objects** before you run queries or modifications.

## Choose between MCP and the built-in AI experiences

Use the MCP server when your host supports MCP discovery and you want the extension to expose its PostgreSQL tool surface there.

Use the built-in extension experiences when:

- you want to chat directly with the [@pgsql chat participant](copilot/pgsql-chat.md) (Visual Studio Code only),
- you want multi-step automation inside [Agent mode](copilot/agent-mode.md) (Visual Studio Code and Cursor), or
- your current host does not surface the extension's MCP registration automatically.

## Troubleshoot MCP availability

### The host does not show a PostgreSQL MCP server

Confirm that you are running a supported host and that Copilot/AI integration is enabled in the extension. If needed, reload the window after you sign in or change Copilot/AI settings.

### Registration is skipped

The extension skips registration when it cannot retrieve a usable MCP URL or token from the language service. Check the extension output logs if the host never discovers the server after reload.

### A tool cannot connect to my database

Verify that the target connection profile exists and that the extension can use it directly. MCP flows depend on the same connection store and credential resolution as the rest of the extension.

### I need a manual endpoint for another MCP client

The extension does not currently provide a user-facing manual endpoint workflow for standalone MCP clients. Use a supported host or fall back to the built-in AI experiences documented in this doc set.

## Related content

- [Copilot integration](copilot-integration.md)
- [@pgsql chat participant](copilot/pgsql-chat.md)
- [Agent mode](copilot/agent-mode.md)
- [Connections and identity](connections.md)
- [Copilot tools reference](reference/copilot-tools.md)
