---
  title: $not (boolean expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $not operator returns the opposite boolean value of the expression.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $not (boolean expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$not` operator returns the opposite boolean value of the expression. It performs a logical NOT operation on a single expression. If the expression evaluates to `true`, `$not` returns `false`. If the expression evaluates to `false`, `$not` returns `true`. This operator is useful for negating conditions and finding documents that don't meet specific criteria.

## Syntax

The syntax for the `$not` operator is as follows:

```javascript
{
  $not: <expression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`<expression>`** | A single expression to be negated. The `$not` operator returns the logical opposite of this expression's boolean value. |

## Example

### Example 1: Identify stores that aren't high-volume

The example finds stores that don't have high sales volume (not greater than 50,000).

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      isNotHighVolume: {
        $not: { $gt: ["$sales.salesByCategory.totalSales", 20000] }
      },
      storeCategory: {
        $cond: [
          { $not: { $gt: ["$sales.salesByCategory.totalSales", 20000] } },
          "Small-Medium Store",
          "High Volume Store"
        ]
      }
    }
  },
  { $limit: 2 }
])
```

The query identifies stores that aren't high-volume operations.

```json
 {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalSales": [ 37978 ],
    "isNotHighVolume": false,
    "storeCategory": "High Volume Store"
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalSales": [ 25731 ],
    "isNotHighVolume": false,
    "storeCategory": "High Volume Store"
  }
```

### Example 2: Validate stores without understaffing issues

The example identifies stores that don't have understaffing issues (not fewer than 10 total staff members).

```javascript
db.stores.aggregate([
  { $match: {"_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6"} },
  {
    $project: {
      name: 1,
      totalStaff: { $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] },
      isNotUnderstaffed: {
        $not: { $lt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 10] }
      },
      staffingStatus: {
        $cond: [
          { $not: { $lt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 10] } },
          "Adequately Staffed",
          "Understaffed"
        ]
      }
    }
  }
])
```

The query determines if the store isn't understaffed.

```json
{
  "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
  "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
  "totalStaff": 14,
  "isNotUnderstaffed": true,
  "staffingStatus": "Adequately Staffed"
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
