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

# Azure Cosmos DB integration with Azure AI Agent

## Overview

Azure Cosmos DB for NoSQL has a data connector in Azure AI Foundry that enables scenarios in Azure AI Agent Service. This enables developers to build intelligent, stateful agentic applications with persistent thread storage taking of Azure Cosmos DB's scalability and reliability.

The Azure Cosmos DB connector in Azure AI Foundry is a foundational building block that enables Azure Cosmos DB to be used in AI scenarios. While the connector itself doesn’t implement a specific AI task, it unlocks critical capabilities in downstream services such as the Azure AI Agent Service  Store and retrieve agent session threads.


## Get Started

### 1. **Connect Cosmos DB in Azure AI Foundry**
- Use Azure AI Foundry to register your Cosmos DB for NoSQL account.
- Ensure your Cosmos DB container is properly indexed (for example, full-text, vector search, etc.) depending on your use case.

### 2. Select the connection to Azure Cosmos DB. 

:::image type="content" source="../media/ai-agent-service/ai-foundry-db-setup.png" lightbox="../media/ai-agent-service/ai-foundry-db-setup.png" alt-text="Screenshot of selecting the Azure Cosmos DB data connector":::

### 3. Fill in the required parameters

Populate the fields for Azure Subscription, Azure Cosmos DB account, Entra ID authentication, and connection name. Once filled in, select "create connection".

:::image type="content" source="../media/ai-agent-service/ai-foundry-db-config.png" lightbox="../media/ai-agent-service/ai-foundry-db-config.png" alt-text="Screenshot of configuring the connector to Azure Cosmos DB":::

  
### 2. **Get started with sample code**
- We have a GitHub repo with [sample code](https://aka.ms/CosmosDB/AIAgentSamples) to get you started quickly using Azure Cosmos DB for threads your agentic apps.
  
## Related content

- [Azure AI Foundry Connections](/azure/ai-foundry/concepts/connections)
- [What is Azure AI Agent Service?](/azure/ai-services/agents/overview)
- [Vector search](../nosql/vector-search.md)
- [Full-text search](full-text-search.md)
- [Hybrid Search](hybrid-search.md)
