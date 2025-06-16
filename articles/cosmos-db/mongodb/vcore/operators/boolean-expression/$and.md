---
  title: $and (boolean expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $and operator returns true when all expressions evaluate to true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/16/2025
---

# $and (boolean expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$and` operator returns `true` when all expressions evaluate to `true`. It performs a logical AND operation on an array of expressions. If any expression evaluates to `false`, the entire `$and` expression returns `false`. This operator is useful for combining multiple conditions that must all be satisfied.

## Syntax

The syntax for the `$and` operator is as follows:

```javascript
{
  $and: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`<expression1>, <expression2>, ...`** | Two or more expressions to be evaluated. All expressions must evaluate to `true` for the `$and` operation to return `true`. |

## Example

### Example 1: Find stores with high sales and sufficient staff

The example finds stores that have both total sales greater than 100,000 and more than 30 total staff members.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: {
        $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"]
      },
      meetsHighPerformanceCriteria: {
        $and: [
          { $gt: ["$sales.totalSales", 100000] },
          { $gt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 30] }
        ]
      }
    }
  },
  { $limit: 2 }
])
```

The query returns stores that meet both high sales and staffing criteria.

```json
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalStaff": 31,
    "meetsHighPerformanceCriteria": false
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalStaff": 27,
    "meetsHighPerformanceCriteria": false
  }
```

### Example 2: Validate promotion event dates

The example checks if promotion events have both valid start and end dates (all date components are positive numbers).

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      promotionEvents: {
        $map: {
          input: "$promotionEvents",
          as: "event",
          in: {
            eventName: "$$event.eventName",
            hasValidDates: {
              $and: [
                { $gt: ["$$event.promotionalDates.startDate.Year", 0] },
                { $gt: ["$$event.promotionalDates.startDate.Month", 0] },
                { $gt: ["$$event.promotionalDates.startDate.Day", 0] },
                { $gt: ["$$event.promotionalDates.endDate.Year", 0] },
                { $gt: ["$$event.promotionalDates.endDate.Month", 0] },
                { $gt: ["$$event.promotionalDates.endDate.Day", 0] }
              ]
            }
          }
        }
      }
    }
  }
])
```

The query validates that all date components are positive numbers for both start and end dates.

```json
 {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "promotionEvents": [
      { "eventName": "Massive Markdown Mania", "hasValidDates": true },
      { "eventName": "Fantastic Deal Days", "hasValidDates": true },
      { "eventName": "Discount Delight Days", "hasValidDates": true },
      { "eventName": "Super Sale Spectacular", "hasValidDates": true },
      { "eventName": "Grand Deal Days", "hasValidDates": true },
      { "eventName": "Major Bargain Bash", "hasValidDates": true }
    ]
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
