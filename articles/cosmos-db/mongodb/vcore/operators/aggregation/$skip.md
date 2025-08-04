---
title: $skip
titleSuffix: Overview of the $skip operator in Azure Cosmos DB for MongoDB vCore
description: The $skip stage in the aggregation pipeline is used to skip a specified number of documents from the input and pass the remaining documents to the next stage in the pipeline.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $skip
The $skip stage in the aggregation pipeline is used to skip a specified number of documents from the input and pass the remaining documents to the next stage in the pipeline. The stage is useful for implementing pagination in queries and for controlling the subset of documents that subsequent stages in the pipeline operate on.

## Syntax
The syntax for the $skip stage is straightforward. It accepts a single parameter, which is the number of documents to skip.

```javascript
{
  $skip: <number>
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| **`number`** | The number of documents to skip before passing the remaining documents to the next stage. |

## Examples
Consider this sample document from the stores collection.

```json
{
    _id: '0fcc0bf0-ed18-4ab8-b558-9848e18058f4',
    name: 'First Up Consultants | Beverage Shop - Satterfieldmouth',
    location: { lat: -89.2384, lon: -46.4012 },
    staff: { employeeCount: { fullTime: 2, partTime: 20 } },
    sales: {
      salesByCategory: [
        { categoryName: 'Wine Accessories', totalSales: 34450 },
        { categoryName: 'Bitters', totalSales: 39496 },
        { categoryName: 'Rum', totalSales: 1734 }
      ],
      revenue: 75670
    },
    promotionEvents: [
      {
        eventName: 'Unbeatable Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 7, Day: 2 }
        },
        discounts: [
          { categoryName: 'Whiskey', discountPercentage: 7 },
          { categoryName: 'Bitters', discountPercentage: 15 },
          { categoryName: 'Brandy', discountPercentage: 8 },
          { categoryName: 'Sports Drinks', discountPercentage: 22 },
          { categoryName: 'Vodka', discountPercentage: 19 }
        ]
      },
      {
        eventName: 'Steal of a Deal Days',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 29 }
        },
        discounts: [
          { categoryName: 'Organic Wine', discountPercentage: 19 },
          { categoryName: 'White Wine', discountPercentage: 20 },
          { categoryName: 'Sparkling Wine', discountPercentage: 19 },
          { categoryName: 'Whiskey', discountPercentage: 17 },
          { categoryName: 'Vodka', discountPercentage: 23 }
        ]
      },
      {
        eventName: 'Summer Sale',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 1 },
          endDate: { Year: 2024, Month: 6, Day: 15 }
        },
        discounts: [ { categoryName: 'DJ Speakers', discountPercentage: 20 } ]
      }
    ],
    company: 'First Up Consultants',
    city: 'Satterfieldmouth',
    storeOpeningDate: ISODate("2024-09-20T18:28:57.302Z"),
    lastUpdated: Timestamp({ t: 1729448937, i: 1 }),
    store: { promotionEvents: null },
    tag: [ '#ShopLocal' ]
  }
```

### Example 1: Skipping Documents in a Collection

To skip the first 2 documents and return the rest, you can use the following aggregation pipeline:

```javascript
db.stores.aggregate([
  { $skip: 2 }
])
``` 
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
    "store": {
      "name": "Uptown Store",
      "promotionEvents": ["Back to School", "Winter Sale"]
    }
  }
]
```

### Example 2: Skipping Documents and Then Limiting the Result
To skip the first 2 documents and then limit the result to the next 3 documents, you can combine $skip with $limit:

```javascript
db.stores.aggregate([
  { $skip: 2 },
  { $limit: 3 }
])
```

### Example 3: Skipping Documents in a More Complex Pipeline
To skip the first promotion event and then project the remaining events for a specific store:

```javascript 
db.stores.aggregate([
  { $match: { "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4", } },
  { $unwind: "$promotionEvents" },
  { $skip: 1 },
  { $project: { "promotionEvents": 1, _id: 0 } }
])
``` 

Sample output:

```json
[
  {
    promotionEvents: {
      eventName: 'Steal of a Deal Days',
      promotionalDates: {
        startDate: { Year: 2024, Month: 9, Day: 21 },
        endDate: { Year: 2024, Month: 9, Day: 29 }
      },
      discounts: [
        { categoryName: 'Organic Wine', discountPercentage: 19 },
        { categoryName: 'White Wine', discountPercentage: 20 },
        { categoryName: 'Sparkling Wine', discountPercentage: 19 },
        { categoryName: 'Whiskey', discountPercentage: 17 },
        { categoryName: 'Vodka', discountPercentage: 23 }
      ]
    }
  },
  {
    promotionEvents: {
      eventName: 'Summer Sale',
      promotionalDates: {
        startDate: { Year: 2024, Month: 6, Day: 1 },
        endDate: { Year: 2024, Month: 6, Day: 15 }
      },
      discounts: [ { categoryName: 'DJ Speakers', discountPercentage: 20 } ]
    }
  }
]
```


## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).