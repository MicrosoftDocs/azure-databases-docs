---
title: Optimize Performance When Using Pgvector in Azure HorizonDB
description: Best practices to optimize performance pgvector enabled vector database queries and indexes in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
ms.collection:
  - ce-skilling-ai-copilot
ms.update-cycle: 180-days
ms.custom:
  - build-2023
  - ignite-2023
---

# Optimize performance when using pgvector in Azure HorizonDB

The `pgvector` extension adds an open-source vector similarity search to Azure HorizonDB.

This article explores the limitations and tradeoffs of [`pgvector`](https://github.com/pgvector/pgvector) and shows how to use partitioning, indexing, and search settings to improve performance.

For more on the extension itself, see [basics of `pgvector`](how-to-use-pgvector.md). You might also want to refer to the official [README](https://github.com/pgvector/pgvector/blob/master/README.md) of the project.

[!INCLUDE [Performance](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-performance.md)]

## Related content

- [Generate vector embeddings with Azure OpenAI in Azure HorizonDB](../azure-ai/generative-ai-azure-openai.md)
