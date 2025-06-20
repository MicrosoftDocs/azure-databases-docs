---
title: $densify usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Adds missing data points in a sequence of values within an array or collection.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/09/2025
---

# $densify usage on Azure Cosmos DB for MongoDB vCore

The `$densify` stage in an aggregation pipeline is used to fill in missing data points within a sequence of values. It helps in creating a more complete dataset by generating missing values based on a specified field, range, and step. This is particularly useful in scenarios like time-series data analysis, where gaps in data points need to be filled to ensure accurate analysis.

## Syntax

```javascript
{
  $densify: {
    field: <field>,
    range: {
      step: <number>,
      unit: <string>, // Optional, e.g., "hour", "day", "month", etc.
      bounds: [<lowerBound>, <upperBound>] // Optional
    },
    partitionByFields: [<field1>, <field2>, ...] // Optional
  }
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`field`** | The field on which densification is performed. |
| **`range.step`** | The step size for generating missing values. |
| **`range.unit`** | (Optional) The unit of the step size, such as time units (e.g., "hour", "day"). |
| **`range.bounds`** | (Optional) Specifies the range (lower and upper bounds) for densification. |
| **`partitionByFields`** | (Optional) Fields used to group data for densification. |

## Examples

### Example 1: Densify a time-series dataset

The following pipeline fills in missing days in the date field:

```javascript
db.aggregate([
    {
      $documents: [
        { date: new ISODate("2024-01-01"), value: 10 },
        { date: new ISODate("2024-01-03"), value: 15 }
      ]
    },
    {
      $densify: {
        field: "date",
        range: {
          step: 1,
          unit: "day",
          bounds: "full"
        }
      }
    }
  ]);
```
This query would return the following document.
```json
[
  { date: ISODate("2024-01-01T00:00:00.000Z"), value: 10 },
  { date: ISODate("2024-01-02T00:00:00.000Z") },
  { date: ISODate("2024-01-03T00:00:00.000Z"), value: 15 }
]

```

### Example 2: Densify numeric data

The following pipeline fills in missing numeric values in the `sales.fullSales` field:

```javascript
db.aggregate([
    {
      $documents: [
        { level: 1, score: 10 },
        { level: 3, score: 30 }
      ]
    },
    {
      $densify: {
        field: "level",
        range: {
          step: 1,
          bounds: [1, 5] 
        }
      }
    }
  ]);
```
This query would return the following document.
```json
[
  { level: 1, score: 10 },
  { level: 2 },
  { level: 3, score: 30 },
  { level: 4 }
]
```


## Limitations

The following table summarizes the key restrictions and behaviors associated with the $densify stage in MongoDB aggregation pipelines:

| Category               | Condition / Behavior                                                                                                                                         |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Field Restrictions     | - Errors if any document has a **date** value and `unit` is **not specified**. <br> - Errors if any document has a **numeric** value and `unit` is **specified**. <br> - Field name **starts with `$`**. Use `$project` to rename it. |
| partitionByFields      | - Any field evaluates to a **non-string** value. <br> - Field name **starts with `$`**.                                                                      |
| range.bounds           | - **Lower bound** defines the start value, regardless of existing documents. <br> - **Lower bound is inclusive**. <br> - **Upper bound is exclusive**. <br> - `$densify` does **not filter out** documents outside the bounds. |


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
