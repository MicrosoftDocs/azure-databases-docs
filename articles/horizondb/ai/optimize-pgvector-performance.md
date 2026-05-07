---
title: Optimize performance when using pgvector in Azure HorizonDB
description: Best practices to optimize performance pgvector enabled vector database queries and indexes on Azure HorizonDB.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 05/08/2026
ms.update-cycle: 180-days
ms.service: azure-database-postgresql
ms.subservice: ai-vector-search
ms.topic: how-to
ms.collection: ce-skilling-ai-copilot
ms.custom:
  - build-2026
---

# Optimize performance when using pgvector in Azure HorizonDB 

The `pgvector` extension adds an open-source vector similarity search to Azure HorizonDB flexible server.

This article explores the limitations and tradeoffs of [`pgvector`](https://github.com/pgvector/pgvector) and shows how to use partitioning, indexing, and search settings to improve performance.

For more on the extension itself, see [basics of `pgvector`](how-to-use-pgvector.md). You might also want to refer to the official [README](https://github.com/pgvector/pgvector/blob/master/README.md) of the project.

[!INCLUDE [Performance](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-performance.md)]

## Related content

- [Generate vector embeddings with Azure OpenAI on Azure HorizonDB flexible server](../azure-ai/generative-ai-azure-openai.md).
