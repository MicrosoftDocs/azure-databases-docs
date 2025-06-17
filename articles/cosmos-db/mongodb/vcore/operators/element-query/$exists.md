---
  title: $exists (element query)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $exists operator matches documents that have the specified field.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/17/2025
---

# $exists (element query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$exists` operator matches documents that have the specified field. When `$exists` is `true`, it selects documents that contain the field, including documents where the field value is `null`. When `$exists` is `false`, the query returns only documents that do not contain the field.

## Syntax

The syntax for the `$exists` operator is as follows:

```javascript
{
  <field>: { $exists: <boolean> }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field to check for existence. |
| **`boolean`** | `true` to match documents that contain the field (including null values), `false` to match documents that do not contain the field. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "location": { "lat": -48.9752, "lon": -141.6816 },
  "staff": { "employeeCount": { "fullTime": 12, "partTime": 19 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Desk Lamps", "totalSales": 37978 } ],
    "revenue": 37978
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Desks", "discountPercentage": 22 },
        { "categoryName": "Filing Cabinets", "discountPercentage": 23 }
      ]
    }
  ],
  "company": "Trey Research",
  "city": "Lake Freeda",
  "storeOpeningDate": "2024-09-26T22:55:25.779Z",
  "lastUpdated": "Timestamp({ t: 1729983325, i: 1 })"
}
```

### Example 1: Find stores with promotion events

The example finds all stores that have promotion events defined.

```javascript
db.stores.find(
  { "promotionEvents": { $exists: true }},
  { "_id": 1, "promotionEvents": { $slice: 1 }}
).limit(2)
```

The query returns all documents where the `promotionEvents` field exists, regardless of whether the array is empty or contains elements.

```json
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "location": { "lat": -74.0427, "lon": 160.8154 },
    "staff": { "employeeCount": { "fullTime": 9, "partTime": 18 } },
    "sales": {
      "salesByCategory": [
        { "categoryName": "Stockings", "totalSales": 25731 }
      ],
      "revenue": 25731
    },
    "promotionEvents": [
      {
        "eventName": "Mega Savings Extravaganza",
        "promotionalDates": {
          "startDate": { "Year": 2023, "Month": 6, "Day": 29 },
          "endDate": { "Year": 2023, "Month": 7, "Day": 7 }
        },
        "discounts": [
          { "categoryName": "Stockings", "discountPercentage": 16 },
          { "categoryName": "Tree Ornaments", "discountPercentage": 8 }
        ]
      }
    ],
    "company": "Lakeshore Retail",
    "city": "Marvinfort",
    "storeOpeningDate": "2024-10-01T18:24:02.586Z",
    "lastUpdated": "2024-10-02T18:24:02.000Z"
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "location": { "lat": 61.3945, "lon": -3.6196 },
    "staff": { "employeeCount": { "fullTime": 7, "partTime": 6 } },
    "sales": {
      "salesByCategory": [
        { "categoryName": "Lamps", "totalSales": 19880 },
        { "categoryName": "Rugs", "totalSales": 20055 }
      ],
      "revenue": 39935
    },
    "promotionEvents": [
      {
        "eventName": "Unbeatable Markdown Mania",
        "promotionalDates": {
          "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
          "endDate": { "Year": 2024, "Month": 4, "Day": 1 }
        },
        "discounts": [
          { "categoryName": "Vases", "discountPercentage": 8 },
          { "categoryName": "Lamps", "discountPercentage": 5 }
        ]
      }
    ],
    "company": "Lakeshore Retail",
    "city": "Franciscoton",
    "lastUpdated": "2024-12-02T12:01:46.000Z",
    "storeOpeningDate": "2024-09-03T07:21:46.045Z"
  }
```

### Example 2: Check for nested field existence

This example finds stores that have full-time employee count information.

```javascript
db.stores.find(
 { "staff.employeeCount.fullTime": { $exists: true }},
 { "_id": 1, "staff.employeeCount": 1 }).limit(2)
```

The query returns stores where the nested field `staff.employeeCount.fullTime` exists.

```json
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "staff": {
      "employeeCount": {
        "fullTime": 9,
        "partTime": 18
      }
    }
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "staff": {
      "employeeCount": {
        "fullTime": 7,
        "partTime": 6
      }
    }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
