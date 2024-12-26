---
  title: Distinct command usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The distinct command is used to find the unique values for a specified field across a single collection.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# distinct

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `distinct` command is used to find the unique values for a specified field across a single collection. This command is useful when you need to identify the set of distinct values for a field without retrieving all the documents or when you need to perform operations like filtering or grouping based on unique values.

## Syntax

The basic syntax of the `distinct` command is as follows:

```javascript
db.collection.distinct(field, query, options)
```

- `field`: The field that receives the returned distinct values.
- `query`: Optional. A query that specifies the documents from which to retrieve the distinct values.
- `options`: Optional. Other options for the command.

## Examples

Here are examples using the provided sample JSON structure.

### Example 1: Find distinct categories in sales

To find the distinct `categoryName` in the `salesByCategory` array:

```javascript
db.stores.distinct("sales.salesByCategory.categoryName")
```

#### Sample output

```javascript
[mongos] StoreData> db.stores.distinct("sales.salesByCategory.categoryName")
[
  {
    _id: 'Discount Derby',
    discounts: [
      { categoryName: 'Bath Sheets', discountPercentage: 25 },
      { categoryName: 'Tablecloths', discountPercentage: 25 },
      { categoryName: 'Drapes', discountPercentage: 25 }
    ]
  }
]
[mongos] StoreData> db.stores.distinct("sales.salesByCategory.categoryName")
[
  'Music Theory Books',
  'Superfoods',
  'Harmonicas',
  'Garden Tools',
  ... 883 more items
]  
```

### Example 2: Find distinct event names in promotion events

To find the distinct `eventName` in the `promotionEvents` array:

```javascript
db.stores.distinct("promotionEvents.eventName")
```

#### Sample output

```javascript
[mongos] StoreData> db.stores.distinct("promotionEvents.eventName")
[
{
    _id: 'Super Saver Celebration',
    discounts: [
      { categoryName: 'Face Towels', discountPercentage: 25 },
      { categoryName: 'Printer Ribbons', discountPercentage: 25 },
      { categoryName: 'Chromebooks', discountPercentage: 25 }
    ]
    }
]
```

### Example 3: Find distinct discount percentages for a specific event

To find the distinct `discountPercentage` in the `discounts` array for the "Summer Sale" event:

```javascript
db.stores.distinct("promotionEvents.discounts.discountPercentage", { "promotionEvents.eventName": "Incredible Discount Days" })
```
#### Sample output

```javascript
[mongos] StoreData> db.stores.distinct("promotionEvents.discounts.discountPercentage", { "promotionEvents.eventName": "Incredible Discount Days" })
[
   6, 17, 22, 25,  9, 15, 14,
   7, 12, 19, 24,  5, 20, 10,
  23, 16, 18, 21, 13, 11,  8
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
