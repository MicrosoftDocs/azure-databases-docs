---
  title: $and
  titleSuffix: Overview of the $and operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $and operator returns true when all expressions evaluate to true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/04/2025
---

# $and

The `$and` operator returns `true` when all expressions evaluate to `true`. It performs a logical AND operation on an array of expressions. If any expression evaluates to `false`, the entire `$and` expression returns `false`. This operator is useful for combining multiple conditions that must all be satisfied.

## Syntax

```javascript
{
  $and: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<expression1>, <expression2>, ...`** | Two or more expressions to be evaluated. All expressions must evaluate to `true` for the `$and` operation to return `true`. |

## Examples

Consider this sample document from the stores collection.

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1: Find stores with high sales and sufficient staff

This query finds stores that have both total sales greater than 100,000 and more than 30 total staff members.

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

This query returns the following results:

```json
[
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
]
```

### Example 2: Validate promotion event dates

This query checks if promotion events have valid start and end dates (all date components are positive numbers).

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

This query returns the following result.

```json
[
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
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
