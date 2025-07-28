---
  title: $isArray
  titleSuffix: Overview of the $isArray operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $isArray operator is used to determine if a specified value is an array. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $isArray

The `$isArray` operator is used to determine if a specified value is an array. It returns `true` if the value is an array and `false` otherwise. This operator is often used in aggregation pipelines to filter or transform documents based on whether a field contains an array.

## Syntax

```javascript
{ $isArray: <expression> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a value you want to check.|

## Example

Let's understand the usage with sample json from `stores` dataset.

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

### Example 1: Checking if a field is an array

The aggregation query checks whether the `sales.salesByCategory` field in each store document is an array and returns that information for the first three documents.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 1,
      isSalesByCategoryArray: { $isArray: "$sales.salesByCategory" }
    }
  },
 // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

This query returns the array categorization for first three documents.

```json
[
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "isSalesByCategoryArray": true
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "isSalesByCategoryArray": true
  },
  {
    "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
    "isSalesByCategoryArray": true
  }
]
```

### Example 2: Filtering documents based on array fields

The example demonstrates use of `$isArray` to filter documents where the `promotionEvents` field is an array.

```javascript
db.stores.aggregate([
  {
    $match: {
      $expr: { $isArray: "$promotionEvents" }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 },
   // Include only _id and name fields in the output 
  { $project: { _id: 1, name: 1 } }    
])
```

The query returns three documents having `promotionEvents` as array.

```json
[
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie"
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland"
  },
  {
    "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
    "name": "Wide World Importers | Bed and Bath Store - West Vitafort"
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
