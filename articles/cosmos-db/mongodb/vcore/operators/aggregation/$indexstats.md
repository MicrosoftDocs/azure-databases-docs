---
  title: $indexStats
  titleSuffix: Overview of the $group operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $indexStats stage returns usage statistics for each index in the collection.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/20/2025
---

# $indexStats

The `$indexStats` aggregation stage returns usage statistics for each index in the collection. This stage is useful for analyzing index performance, identifying unused indexes, and optimizing query performance.

## Syntax

The syntax for the `$indexStats` stage is as follows:

```javascript
{
  $indexStats: {}
}
```

## Parameters

The `$indexStats` stage takes no parameters.

## Example

To retrieve usage statistics for all indexes on the stores collection.

```javascript
db.stores.aggregate([
  { $indexStats: {} }
])
```

The query returns statistics for each index including access patterns and usage frequency.

```json
  {
    "name": "_id_",
    "key": { "_id": 1 },
    "accesses": { "ops": 41675, "since": "2025-06-07T13:51:41.231Z" },
    "spec": { "v": 2, "key": { "_id": 1 }, "name": "_id_" }
  },
  {
    "name": "location_2dsphere",
    "key": { "location": "2dsphere" },
    "accesses": { "ops": 0, "since": "2025-06-07T13:51:41.231Z" },
    "spec": {
      "v": 2,
      "key": { "location": "2dsphere" },
      "name": "location_2dsphere",
      "2dsphereIndexVersion": 3
    }
  },
  {
    "name": "name_text_sales.salesByCategory.categoryName_text_promotionEvents.eventName_text_promotionEvents.discounts.categoryName_text",
    "key": {
      "name": "text",
      "sales.salesByCategory.categoryName": "text",
      "promotionEvents.eventName": "text",
      "promotionEvents.discounts.categoryName": "text"
    },
    "accesses": { "ops": 8, "since": "2025-06-07T13:51:41.231Z" },
    "spec": {
      "v": 2,
      "key": {
        "name": "text",
        "sales.salesByCategory.categoryName": "text",
        "promotionEvents.eventName": "text",
        "promotionEvents.discounts.categoryName": "text"
      },
      "name": "name_text_sales.salesByCategory.categoryName_text_promotionEvents.eventName_text_promotionEvents.discounts.categoryName_text"
    }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
