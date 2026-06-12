---
title: Chat Participant Reference for the PostgreSQL Extension for Visual Studio Code
description: Chat participants provided by the PostgreSQL extension for GitHub Copilot Chat.
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
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
- [Copilot tools reference](copilot-tools.md)
- [MCP server reference](mcp-server.md)
