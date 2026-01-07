---
title: Integration with Azure AI Agent Service
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn about Integrations with Azure AI Agent Service through Azure AI Foundry connection
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 4/30/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Azure Cosmos DB integration with Azure AI Agents Service

## Overview

Azure Cosmos DB for NoSQL has a data connector in Azure AI Foundry that enables thread storage and management in Azure AI Agent Service. This feature lets developers persist and retrieve multi-turn threads directly within their own Azure Cosmos DB resource. Learn more [here](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/securely-build-and-manage-agents-in-azure-ai-foundry/4415186).

With BYO Thread Storage, user-agent conversations, model transactions are stored in your own Azure Cosmos DB account—giving you full control and enhanced security. Azure Cosmos DB will contain three dedicated containers within a new database called enterprise_memory to manage this data.

- thread-message-store: Stores end-user conversation messages.
- system-thread-message-store: Manages internal system messages.
- agent-entity-store: Captures and stores model inputs and outputs.

This helps ensure that AI agents maintain contextual awareness and securely track thread information in your own Azure Cosmos DB account. It’s also easy to set up using the official Bicep template provided [here](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/41-standard-agent-setup).

Agentic threads and conversational histories play a critical role in improving the performance and reliability of agentic applications. By maintaining structured interaction records, developers can gain valuable insights into user behavior, agent decision-making, and overall system performance. These histories enhance an agent’s contextual understanding, enabling more coherent and relevant responses. In addition, analyzing this data can help identify patterns in user queries, making it easier to troubleshoot agent behaviors and optimize outcomes.


  
## Related content

- [Azure AI Foundry Connections](/azure/ai-foundry/concepts/connections)
- [What is Azure AI Agent Service?](/azure/ai-services/agents/overview)
- [Vector search](../vector-search.md)
- [Full-text search](full-text-search.md)
- [Hybrid Search](hybrid-search.md)
