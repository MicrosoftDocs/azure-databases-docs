---
  title: $group (aggregation)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $group stage groups documents by specified identifier expressions and applies accumulator expressions.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/20/2025
---

# $group (aggregation)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$group` aggregation stage groups documents by specified identifier expressions and applies accumulator expressions to create computed fields for each group. This stage is essential for data aggregation and summarization operations.

## Syntax

The syntax for the `$group` stage is as follows:

```javascript
{
  $group: {
    _id: <expression>,
    <field1>: { <accumulator1>: <expression1> },
    <field2>: { <accumulator2>: <expression2> },
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`_id`** | Required. The expression to group by. Use null to calculate accumulated values for all input documents. |
| **`field`** | Optional. Computed using accumulator operators like $sum, $avg, $max, $min, $count, etc. |

## Example

### Example 1: Group by city and analyze staff distribution

The example groups stores by city and analyzes the staffing patterns across different locations.

```javascript
db.stores.aggregate([
  {
    $group: {
      _id: "$city",
      totalFullTimeStaff: { $sum: "$staff.employeeCount.fullTime" },
      totalPartTimeStaff: { $sum: "$staff.employeeCount.partTime" },
      avgFullTimeStaff: { $avg: "$staff.employeeCount.fullTime" },
      storesInCity: { $count: {} }
    }
  },
  {
    $project: {
      city: "$_id",
      totalFullTimeStaff: 1,
      totalPartTimeStaff: 1,
      avgFullTimeStaff: { $round: ["$avgFullTimeStaff", 1] },
      storesInCity: 1,
      fullTimeRatio: {
        $round: [
          { $divide: ["$totalFullTimeStaff", { $add: ["$totalFullTimeStaff", "$totalPartTimeStaff"] }] },
          2
        ]
      }
    }
  },
  { $limit : 2}
])
```

The query returns staffing analysis by city location.

```json
  {
    "_id": "New Ellsworth",
    "totalFullTimeStaff": 11,
    "totalPartTimeStaff": 1,
    "avgFullTimeStaff": 11,
    "storesInCity": 1,
    "city": "New Ellsworth",
    "fullTimeRatio": 0.92
  },
  {
    "_id": "Jalonborough",
    "totalFullTimeStaff": 4,
    "totalPartTimeStaff": 1,
    "avgFullTimeStaff": 4,
    "storesInCity": 1,
    "city": "Jalonborough",
    "fullTimeRatio": 0.8
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
