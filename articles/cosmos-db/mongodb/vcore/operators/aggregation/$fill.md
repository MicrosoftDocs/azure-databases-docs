---
  title: $fill (aggregation pipeline stage) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $fill stage allows filling missing values in documents based on specified methods and criteria.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $fill (aggregation pipeline stage)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$fill` stage is used to fill missing or null values in documents within the aggregation pipeline. It provides various methods to populate missing data, including using static values, linear interpolation, or values from previous/next documents.

## Syntax

The syntax for the `$fill` stage is as follows:

```javascript
{
  $fill: {
    sortBy: <sort specification>,
    partitionBy: <partition fields>,
    partitionByFields: <array of partition field names>,
    output: {
      <field1>: { value: <expression> },
      <field2>: { method: <string> },
      ...
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`sortBy`** | Specifies the sort order for documents when applying fill methods that depend on document order. |
| **`partitionBy`** | Optional. Groups documents into partitions. Fill operations are applied within each partition separately. |
| **`partitionByFields`** | Optional. Alternative syntax for partitionBy using an array of field names. |
| **`output`** | Specifies the fields to fill and the method or value to use for filling missing data. |

### Fill Methods

| Method | Description |
| --- | --- |
| **`value`** | Fill with a specified static value or expression result. |
| **`linear`** | Fill using linear interpolation between known values (numeric fields only). |
| **`locf`** | Last Observation Carried Forward - use the last known value. |
| **`linear`** | Linear interpolation between surrounding values. |

## Examples

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        }
      ]
    }
  ]
}
```

### Example 1: Fill missing values with static value

Suppose you want to fill missing `totalSales` values in the `salesByCategory` array with a default value of 0.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $fill: {
      output: {
        "sales.salesByCategory.totalSales": { value: 0 }
      }
    }
  },
  {
    $group: {
      _id: "$_id",
      name: { $first: "$name" },
      salesByCategory: { $push: "$sales.salesByCategory" }
    }
  }
])
```

This will ensure all category entries have a `totalSales` value, replacing any missing values with 0.

### Example 2: Fill missing staff data using last observation carried forward

Fill missing part-time staff data using the last known value within each store group.

```javascript
db.stores.aggregate([
  {
    $fill: {
      sortBy: { "_id": 1 },
      output: {
        "staff.totalStaff.partTime": { method: "locf" }
      }
    }
  },
  {
    $project: {
      name: 1,
      "staff.totalStaff": 1
    }
  }
])
```

### Example 3: Fill missing discount percentages with average value

Fill missing discount percentages with the average discount percentage across all stores.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $fill: {
      partitionBy: "$promotionEvents.eventName",
      sortBy: { "promotionEvents.discounts.categoryName": 1 },
      output: {
        "promotionEvents.discounts.discountPercentage": { 
          value: { $avg: "$promotionEvents.discounts.discountPercentage" } 
        }
      }
    }
  },
  {
    $group: {
      _id: { storeId: "$_id", eventName: "$promotionEvents.eventName" },
      storeName: { $first: "$name" },
      eventName: { $first: "$promotionEvents.eventName" },
      discounts: { $push: "$promotionEvents.discounts" }
    }
  }
])
```


## Use Cases

- **Data Cleaning**: Fill missing values in imported datasets
- **Time Series Data**: Handle gaps in sequential data using interpolation
- **Default Values**: Assign default values to optional fields
- **Data Normalization**: Ensure consistent data structure across documents

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]