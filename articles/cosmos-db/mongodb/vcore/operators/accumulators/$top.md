---
  title: $top (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $top accumulator operator returns the top element from a group based on a specified sort order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $top (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$top` accumulator operator returns the top element from a group based on a specified sort order. It combines sorting and selection in a single operation, making it efficient for finding the highest or lowest values without requiring a separate sort stage.

## Syntax

The syntax for the `$top` accumulator operator is as follows:

```javascript
{
  $group: {
    _id: <expression>,
    <field>: { 
      $top: {
        sortBy: { <field1>: <sort order>, <field2>: <sort order>, ... },
        output: <expression>
      }
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`sortBy`** | Specifies the sort order using a document with field names and sort directions (1 for ascending, -1 for descending). |
| **`output`** | The expression that specifies the field or value to return from the top document. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        }
      },
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 22
        }
      ]
    }
  ]
}
```

### Example 1: Get top selling category per store

Find the highest-selling category for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      topSellingCategory: {
        $top: {
          sortBy: { "sales.salesByCategory.totalSales": -1 },
          output: {
            categoryName: "$sales.salesByCategory.categoryName",
            totalSales: "$sales.salesByCategory.totalSales"
          }
        }
      }
    }
  }
])
```

This will produce output showing the top-selling category for each store:

```json
[
  {
    _id: 'b1d86d1f-8705-4157-b64c-a9eda0df4921',
    storeName: 'VanArsdel, Ltd. | Baby Products Haven - West Kingfort',
    topSellingCategory: { categoryName: 'Baby Monitors', totalSales: 49585 }
  },
  {
    _id: '22e6367e-8341-415f-9795-118d2b522abf',
    storeName: 'Adatum Corporation | Outdoor Furniture Mart - Port Simone',
    topSellingCategory: { categoryName: 'Outdoor Benches', totalSales: 4976 }
  },
.
.
.
]
```

### Example 2: Get highest discount by category

Find the category with the highest discount percentage across all promotion events for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      highestDiscount: {
        $top: {
          sortBy: { "promotionEvents.discounts.discountPercentage": -1 },
          output: {
            categoryName: "$promotionEvents.discounts.categoryName",
            discountPercentage: "$promotionEvents.discounts.discountPercentage",
            eventName: "$promotionEvents.eventName"
          }
        }
      }
    }
  }
])
```

This will show the category with the highest discount percentage for each store:

```json
[
  {
    _id: '64ec6589-068a-44a6-be5b-9d37bb0a90f1',
    storeName: 'First Up Consultants | Computer Gallery - West Cathrine',
    highestDiscount: {
      categoryName: 'Gaming Accessories',
      discountPercentage: 24,
      eventName: 'Crazy Markdown Madness'
    }
  },
  {
    _id: 'a58d0356-493b-44e6-afab-260aa3296930',
    storeName: 'Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie',
    highestDiscount: {
      categoryName: 'Fire Pits',
      discountPercentage: 22,
      eventName: 'Savings Showdown'
    }
  },
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
