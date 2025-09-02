--- 
  title: $switch
  titleSuffix: Overview of the $switch operation in Azure Cosmos DB for MongoDB (vCore)
  description: The $switch operator is used to evaluate a series of conditions and return a value based on the first condition that evaluates to true.  
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/27/2024
---


# $switch

The `$switch` operator is used to evaluate a series of conditions and return a value based on the first condition that evaluates to true. This is useful when you need to implement complex conditional logic within aggregation pipelines.

## Syntax

The syntax for the `$switch` operator is as follows:

```JavaScript
{
  $switch: {
    branches: [
      { case: <expression>, then: <expression> },
      { case: <expression>, then: <expression> },
      ...
    ],
    default: <expression>
  }
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| **branches**| An array of documents, each containing|
| **case**| An expression that evaluates to either `true` or `false`|
| **then**| The expression to return if the associated `case` expression evaluates to `true`|
| **default**| The expression to return if none of the `case` expressions evaluate to `true`. This field is optional.|

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
### Example 1: To determine staff type based on full-time and part-time counts

To determine the type of staff based on their count.

```JavaScript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      staffType: {
        $switch: {
          branches: [
            {
              case: { $eq: ["$staff.totalStaff.partTime", 0] },
              then: "Only Full time"
            },
            {
              case: { $eq: ["$staff.totalStaff.fullTime", 0] },
              then: "Only Part time"
            }
          ],
          default: "Both"
        }
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

This query would return the following document.

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "staffType": "Only Full time"
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "staffType": "Both"
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "staffType": "Both"
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
