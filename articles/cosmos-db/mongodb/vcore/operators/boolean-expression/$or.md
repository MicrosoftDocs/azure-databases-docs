---
  title: $or
  titleSuffix: Overview of the $or operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $or operator returns true when at least one expression evaluates to true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/04/2025
---

# $or

The `$or` operator returns `true` when at least one expression evaluates to `true`. It performs a logical OR operation on an array of expressions. If all expressions evaluate to `false`, the entire `$or` expression returns `false`. This operator is useful for creating flexible conditions where any one of multiple criteria can be satisfied.

## Syntax

```javascript
{
  $or: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<expression1>, <expression2>, ...`** | Two or more expressions to be evaluated. If any expression evaluates to `true`, the `$or` operation returns `true`. |

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

### Example 1: Identify stores with either high sales or large staff

This query finds stores that have either total sales greater than 50,000 or more than 25 total staff members.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: { 
        $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] 
      },
      qualifiesForProgram: {
        $or: [
          { $gt: ["$sales.totalSales", 50000] },
          { $gt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 25] }
        ]
      }
    }
  },
  { $limit: 4 }
])
```

This query returns the following results.

```json
[
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalStaff": 31,
    "qualifiesForProgram": true
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalStaff": 27,
    "qualifiesForProgram": true
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "totalStaff": 13,
    "qualifiesForProgram": false
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "totalStaff": 2,
    "qualifiesForProgram": false
  }
]
```

### Example 2: Check for discount eligibility

This query determines if a store offers discounts that are either high percentage (>15%) or for specific popular categories.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      _id: 1,
      name: 1,
      hasAttractiveDealOptions: {
        $or: [
          { $gt: [{ $max: "$promotionEvents.discounts.discountPercentage" }, 15] },
          { $in: ["Bath Accessories", "$promotionEvents.discounts.categoryName"] },
          { $in: ["Mattress Toppers", "$promotionEvents.discounts.categoryName"] }
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
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "hasAttractiveDealOptions": true
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
