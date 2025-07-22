---
title: $gte
titleSuffix: Overview of the $gte operator in Azure Cosmos DB for MongoDB (vCore)
description: The $gte operator retrieves documents where the value of a field is greater than or equal to a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $gte

The `$gte` operator retrieves documents where the value of a field is greater than or equal to a specified value. The `$gte` operator retrieves documents that meet a minimum threshold for the value of a field.

## Syntax

```javascript
{
    field: {
        $gte: <value>
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to compare|
| **`value`** | The value that the field should be greater than|

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
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### Example 1: Find a store with sales >= $35,000

To retrieve a store with at least $35,000 in sales, first run a query using the $gte operator on the sales.totalSales field. Then project only the name of the store and its total sales and limit the result set to one document.

```javascript
db.stores.find({
    "sales.totalSales": {
        "$gte": 35000
    }
}, {
    "name": 1,
    "sales.totalSales": 1
}, {
    "limit": 1
})
```

This returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "sales": { "totalSales": 37701 }
    }
]
```

### Example 2: Find a store with 12 or more full-time staff

To retrieve a store with at least 12 full time staff, first run a query with the $gte operator on the staff.totalStaff.fullTime field. Then, project only the name and full time staff count and limit the results to a single document from the result set.

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        "$gte": 12
    }
}, {
    "name": 1,
    "staff.totalStaff.fullTime": 1
}, {
    "limit": 1
})
```

This query returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "staff": { "totalStaff": { "fullTime": 18 } }
    }
]
```

### Example 3: Find promotion events with a discount percentage greater than or equal to 15% for Laptops

To find two stores with promotions with a discount of at least 15% for laptops, first run a query to filter stores with laptop promotions. Then use the $gte operator on the discountPercentage field. Lastly, project only the name of the store and limit the results to two documents from the result set.


```javascript
db.stores.find({
    "promotionEvents.discounts": {
        "$elemMatch": {
            "categoryName": "Laptops",
            "discountPercentage": {
                "$gte": 15
            }
        }
    }
}, {
    "name": 1
}, {
    "limit": 2
})
```

This returns the following results:

```json
[
  {
    "_id": "60e43617-8d99-4817-b1d6-614b4a55c71e",
    "name": "Wide World Importers | Electronics Emporium - North Ayanashire"
  },
  {
    "_id": "3c441d5a-c9ad-47f4-9abc-ac269ded44ff",
    "name": "Contoso, Ltd. | Electronics Corner - New Kiera"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
