---
  title: $comment (Misc. Query) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $comment operator adds a comment to a query to help identify the query in logs and profiler output.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $comment (Misc. Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$comment` operator adds comments to queries to help identify them in logs and profiler output. This is particularly useful for debugging and monitoring database operations.

## Syntax

The syntax for the `$comment` operator is as follows:

```javascript
{ $comment: <string> }
```

## Parameters

| | Description |
| --- | --- |
| **`string`** | A string containing the comment to be included with the query. |

## Example

Let's understand the usage with sample data from the `stores` dataset.

```javascript
db.stores.find(
   { "sales.totalSales": { $gt: 100000 } },
   { name: 1, "sales.totalSales": 1 }
).comment("Query to find high-performing stores")
```

This query finds stores with total sales greater than 100,000 and includes a comment for easy identification in logs. When executed against our sample dataset, it returns:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "sales": {
    "totalSales": 151864
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]