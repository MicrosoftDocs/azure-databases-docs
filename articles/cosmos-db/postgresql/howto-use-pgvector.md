---
title: How to enable and use pgvector - Azure Cosmos DB for PostgreSQL
description: How to enable and use pgvector for Azure Cosmos DB for PostgreSQL
ms.author: avijitgupta
author: AvijitkGupta
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.custom: build-2023
ms.topic: how-to
ms.date: 05/10/2023
appliesto:
  - ✅ PostgreSQL
---

# How to enable and use `pgvector` on Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

[!INCLUDE [Introduction to `pgvector`](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-introduction.md)]

## Enable extension

PostgreSQL extensions must be enabled in your database before you can use them. To enable the extension, run the command from the psql tool to load the packaged objects into your database.

```postgresql
SELECT CREATE_EXTENSION('vector');
```

> [!Note]
> To disable an extension use `drop_extension()`

[!INCLUDE [Getting Started](~/reusable-content/ce-skilling/azure/includes/cosmos-db/postgresql/includes/pgvector-basics.md)]

## Next Steps

Learn more around performance, indexing and limitations using `pgvector`.

> [!div class="nextstepaction"]
> [Optimize performance using pgvector](howto-optimize-performance-pgvector.md)