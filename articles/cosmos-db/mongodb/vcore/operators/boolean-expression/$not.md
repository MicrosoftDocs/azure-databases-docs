---
  title: $not
  titleSuffix: Overview of the $not operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $not operator returns the opposite boolean value of the expression.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $not

The `$not` operator returns the opposite boolean value of the expression. It performs a logical NOT operation on a single expression. If the expression evaluates to `true`, `$not` returns `false`. If the expression evaluates to `false`, `$not` returns `true`. This operator is useful for negating conditions and finding documents that don't meet specific criteria.

## Syntax

```javascript
{
  $not: <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<expression>`** | A single expression to be negated. The `$not` operator returns the logical opposite of this expression's boolean value. |

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

### Example 1: Identify stores that aren't high-volume

This query finds stores that don't have high sales volume (not greater than 50,000).

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

This query returns the following results.

```json
[
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
]
```

### Example 2: Validate stores without understaffing issues

This query returns stores that don't have understaffing issues (not fewer than 10 total staff members).

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

This query returns the following result.

```json
[
  {
    "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
    "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
    "totalStaff": 14,
    "isNotUnderstaffed": true,
    "staffingStatus": "Adequately Staffed"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
