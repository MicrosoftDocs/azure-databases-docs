---
title: $redact usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Filters the content of the documents based on access rights.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $redact
The `$redact` stage in aggregation pipeline is used to filter fields of the documents in a collection dynamically based on access rights or other conditions. It processes each document in the pipeline and removes or retains fields based on the specified logic.

## Syntax
```javascript
{
  $redact: <expression>
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`<expression>`** | A valid MongoDB expression that evaluates to one of the following: `$$DESCEND`, `$$PRUNE`, or `$$KEEP`. These variables determine whether to keep, remove, or traverse deeper into the document. |

## Example(s)

### Example 1: Redacting sensitive information
The following aggregation pipeline uses `$redact` to filter out the `promotionEvents` field for documents where the `discountPercentage` in a promotion exceeds 15%.

```javascript
db.collection.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $gt: ["$promotionEvents.discounts.discountPercentage", 15]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```

### Example 2: Restricting access based on tags
The following example removes all documents that contain the tag `#MembershipDeals`.

```javascript
db.collection.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $in: ["#MembershipDeals", "$tag"]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]