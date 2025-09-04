--- 
  title:  $cond
  titleSuffix: Overview of the $cond operation in Azure Cosmos DB for MongoDB (vCore)
  description: The $cond operator is used to evaluate a condition and return one of two expressions based on the result. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/27/2024
---

# $cond

The `$cond` operator is used to evaluate a condition and return one of two expressions based on the result. It's similar to the ternary operator in many programming languages. The `$cond` operator can be used within aggregation pipelines to add conditional logic to your queries.

## Syntax

```javascript
{
   $cond: {
      if: <boolean-expression>,
      then: <true-case>,
      else: <false-case>
   }
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| **if**| A boolean expression that is evaluated.|
| **then**| The expression to return if the `if` condition evaluates to true.|
| **else**| The expression to return if the `if` condition evaluates to false.|

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

### Example 1: Determine high sales categories

To determine if the sales for each category are considered "high" or "low" based on a threshold value of $250,000.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      storeId: "$storeId",
      category: "$sales.salesByCategory.categoryName",
      sales: "$sales.salesByCategory.totalSales",
      salesCategory: {
        $cond: {
          if: { $gte: ["$sales.salesByCategory.totalSales", 250000] },
          then: "High",
          else: "Low"
        }
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 }  
])
```
This query returns the following result.

```json
[
  {
    "sales": [ 35921, 1000 ],
    "category": [ "DJ Headphones", "DJ Cables" ],
    "salesCategory": "High"
  },
  { "sales": [ 4760 ], "category": [ "Guitars" ], "salesCategory": "High" },
  {
    "sales": [
      14697, 44111,
      37854, 46211,
       7269, 25451,
      21083
    ],
    "category": [
      "Washcloths",
      "Innerspring Mattresses",
      "Microfiber Towels",
      "Shower Curtains",
      "Bathrobes",
      "Tablecloths",
      "Bath Accessories"
    ],
    "salesCategory": "High"
  }
]
```

### Example 2: Determine full-time or part-time dominance

To determine whether a store employs more full-time or part-time staff.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      staffType: {
        $cond: {
          if: { $gte: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"] },
          then: "More Full-Time",
          else: "More Part-Time"
        }
      }
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
    "staffType": "More Full-Time"
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "staffType": "More Full-Time"
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "staffType": "More Part-Time"
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
