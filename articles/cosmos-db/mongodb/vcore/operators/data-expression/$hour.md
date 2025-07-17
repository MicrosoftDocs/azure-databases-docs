---
  title: $hour (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $hour operator returns the hour portion of a date as a number between 0 and 23.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $hour (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$hour` operator returns the hour portion of a date as a number between 0 and 23. The operator accepts a date expression that resolves to a Date, Timestamp, or ObjectId.

## Syntax

The syntax for the `$hour` operator is as follows:

```javascript
{
  $hour: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, Timestamp, or ObjectId. If the expression resolves to null or is missing, `$hour` returns null. |

## Example

### Example 1: Extract hour from current date

This example demonstrates extracting the hour from the current date and time.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      currentHour: { $hour: new Date() },
      documentHour: { $hour: "$storeOpeningDate" }
    }
  }
])
```

The query returns the current hour and the hour from the ObjectId creation time.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
  "currentHour": 10,
  "documentHour": 13
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
