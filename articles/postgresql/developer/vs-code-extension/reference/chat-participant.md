---
title: "Chat participant reference"
description: "Chat participants provided by the PostgreSQL extension for GitHub Copilot Chat."
author: mmcfarland
ms.author: mattmcfarland
ms.date: 04/02/2026
ms.service: postgresql
ms.subservice: vs-code-pgsql-extensions
ms.topic: reference
---


# Chat participant reference

This page describes the chat participants registered by the PostgreSQL extension for GitHub Copilot Chat.

## pgsql

**ID:** `vscode-postgresql.chat-agent`
**Mention name:** `@pgsql`
**Description:** Helps you query, explore, and interact with PostgreSQL databases.
**Sticky:** Yes

### Disambiguation categories

**databases:** The user wants help with their PostgreSQL database.

Example prompts:

- "What is in my database?"
- "Write a query that tells me how many rows are in the table."
- "How can I make this query faster?"


## Related content

- [Copilot integration](../copilot-integration.md)
- [Copilot tools](copilot-tools.md)
- [MCP server](mcp-server.md)
