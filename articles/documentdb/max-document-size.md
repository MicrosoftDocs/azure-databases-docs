---
title: Document Size and Batch Write Limits
description: Learn about document size limits, nesting depth, and batch write operations in Azure DocumentDB. Understand the 16-MB document limit and 25,000 writes per batch.
author: suvishodcitus
ms.author: suvishod
ms.topic: concept-article
ms.date: 11/12/2025
ms.custom:
  - references_regions
ai-usage: ai-assisted
---

# Document size and batch write limits in Azure DocumentDB

Azure DocumentDB provides high compatibility with MongoDB wire protocol behaviors while optimizing for scalability, performance, and availability. This article describes the supported maximum document size, nesting depth, and batch write limits.

## Document size limits

The maximum Binary JavaScript Object Notation (BSON) document size supported in Azure DocumentDB is 16 MB per document.

| Property | Value |
| --- | --- |
| Maximum document size | **16 MB** |

### Nesting depth

Unlike traditional MongoDB implementations that enforce a strict nesting depth limit, Azure DocumentDB doesn't impose a fixed maximum nesting depth. However, deeply nested document structures might:

- Affect query and read performance
- Increase document processing overhead
- Reduce maintainability

## Batch write and bulk operation limits

Azure DocumentDB supports batch write and bulk operations.

> [!NOTE]
> A batch refers to a **single request** to the server.

| Limit type | Supported value |
| --- | --- |
| Maximum writes per batch operation | **25,000 writes** |
| Behavior when exceeding 25,000 writes in a batch | The batch operation **fails** |
| Number of total batch operations | **No limit** |

## Related content

- [Azure DocumentDB feature compatibility with MongoDB](compatibility-features.md)
- [Azure DocumentDB limitations](limitations.md)
- [Compute and storage tiers in Azure DocumentDB](compute-storage.md)
