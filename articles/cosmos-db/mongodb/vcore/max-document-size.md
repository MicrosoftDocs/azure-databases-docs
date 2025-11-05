---
title: Maximum Document Size
titleSuffix: Summarize maximum document size, nesting limit and batch size supported in Azure Cosmos DB for MongoDB (vCore)
description: Summarize maximum document size, nesting limit and batch size supported in Azure Cosmos DB for MongoDB (vCore).
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 11/02/2025
appliesto:
  - ✅ MongoDB (vCore)
ms.custom:
  - build-2025
---

# Maximum Document Size and Batch Write Limits in vCore-based Azure Cosmos DB for MongoDB

vCore-based Azure Cosmos DB for MongoDB provides high compatibility with MongoDB wire protocol behaviors while optimizing for scalability, performance, and availability. This article describes the supported maximum document size, nesting depth, and batch write limits.

## Maximum document size

The maximum BSON document size supported in vCore-based Azure Cosmos DB for MongoDB is 16 MB per document.

| Property | Value |
|---------|-------|
| Maximum document size | **16 MB** |

### Nesting depth

Unlike traditional MongoDB implementations that enforce a strict nesting depth limit, vCore-based Azure Cosmos DB for MongoDB does not impose a fixed maximum nesting depth. However, deeply nested document structures may:

- Impact query and read performance
- Increase document processing overhead
- Reduce maintainability


## Write command batch size limits

vCore-based Azure Cosmos DB for MongoDB supports batch write and bulk operations. A batch refers to a **single request** to the server.

| Limit type | Supported value |
|-----------|----------------|
| Maximum writes per batch operation | **25,000 writes** |
| Behavior when exceeding 25,000 writes in a batch | The batch operation **fails** |
| Number of total batch operations | **No limit** |


## Next steps

> [!div class="nextstepaction"]
> [Feature Compatibility with MongoDB vCore](compatibility.md)