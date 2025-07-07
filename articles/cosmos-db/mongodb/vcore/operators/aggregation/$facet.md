---
  title: $facet (aggregation)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $facet allows for multiple parallel aggregations to be executed within a single pipeline stage.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $facet (aggregation)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$facet` stage aggregation pipelines allow for multiple parallel aggregations to be executed within a single pipeline stage. It's useful for performing multiple analyses on the same dataset in a single query.

## Syntax

The syntax for the `$facet` stage is as follows:

```json
{
  "$facet": {
    "outputField1": [ { "stage1": {} }, { "stage2": {} } ],
    "outputField2": [ { "stage1": {} }, { "stage2": {} } ]
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`outputFieldN`**| The name of the output field.|
| **`stageN`**| The aggregation stage to be executed.|

## Example

The example accesses all the associated records to product categories like `Laptops`, `Smartphones`, `Cameras` & `Watches` from `stores` collection.

### Example 1: Faceted search on sales and promotions

The example uses the `$facet` stage to perform simultaneous analyses on sales and promotions, for specified product categories. The `salesAnalysis` pipeline unwinds the `salesByCategory`, filters for certain categories, and groups them to sum `totalSales`. The promotion analysis pipeline unwinds promotional events and their discounts, filters for specific categories like `Laptops`, `Smartphones` etc., and groups them to calculate the average discount percentage. The input documents from `stores` collection are fetched from the database only once, at the beginning of this operation.

```javascript
db.stores.aggregate([
  {
    $facet: {
      salesAnalysis: [
        { $unwind: "$sales.salesByCategory" },
        { $match: { "sales.salesByCategory.categoryName": { $in: ["Laptops", "Smartphones", "Cameras", "Watches"] } } },
        { $group: { _id: "$sales.salesByCategory.categoryName", totalSales: { $sum: "$sales.salesByCategory.totalSales" } } }
      ],
      promotionAnalysis: [
        { $unwind: "$promotionEvents" },
        { $unwind: "$promotionEvents.discounts" },
        { $match: { "promotionEvents.discounts.categoryName": { $in: ["Laptops", "Smartphones", "Cameras", "Watches"] } } },
        { $group: { _id: "$promotionEvents.discounts.categoryName", avgDiscount: { $avg: "$promotionEvents.discounts.discountPercentage" } } }
      ]
    }
  }
]).pretty();
```

The returned output from query displays the aggregated insights.

```json
{
  "salesAnalysis": [
    { "_id": "Smartphones", "totalSales": 440815 },
    { "_id": "Laptops", "totalSales": 679453 },
    { "_id": "Cameras", "totalSales": 481171 },
    { "_id": "Watches", "totalSales": 492299 }
  ],
  "promotionAnalysis": [
    { "_id": "Smartphones", "avgDiscount": 14.32 },
    { "_id": "Laptops", "avgDiscount": 14.780645161290323 },
    { "_id": "Cameras", "avgDiscount": 15.512195121951219 },
    { "_id": "Watches", "avgDiscount": 15.174418604651162 }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
