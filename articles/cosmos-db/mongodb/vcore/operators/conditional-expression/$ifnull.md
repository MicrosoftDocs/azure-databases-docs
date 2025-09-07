---
  title: $ifNull
  titleSuffix: Overview of the $ifNull operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $ifNull operator is used to evaluate an expression and return a specified value if the expression resolves to null.  
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/27/2024
---

# $ifNull

The `$ifNull` operator is used to evaluate an expression and return a specified value if the expression resolves to `null`. This operator is useful in scenarios where you want to provide a default value for fields that may not exist or may have `null` values.

## Syntax

```javascript
{
  $ifNull: [ <expression>, <replacement-value> ]
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| **`<expression>`**| The expression to evaluate.|
| **`<replacement-value>`**| The value to return if the expression evaluates to `null`|

## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
   "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### Example 1: Default value for missing `store.manager` field

To ensure that the `$staff.totalStaff.intern` field is always a number, you can use `$ifNull` to replace `null` values with `0`.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      interns: { $ifNull: ["$staff.totalStaff.intern", 0] }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

This query returns the following results.

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "interns": 0
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "interns": 0
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "interns": 0
  }
]

```
## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
