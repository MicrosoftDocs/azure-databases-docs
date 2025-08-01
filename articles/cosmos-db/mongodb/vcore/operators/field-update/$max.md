---
  title: $max
  titleSuffix: Overview of the $max operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $max operator updates the value of a field to a specified value if the specified value is greater than the current value of the field.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $max

The `$max` operator updates the value of a field to a specified value if the specified value is greater than the current value of the field. If the field does not exist, `$max` creates the field and sets it to the specified value. This operator is useful for maintaining maximum thresholds, tracking peak values, or ensuring values don't fall below a certain level.

## Syntax

The syntax for the `$max` operator is as follows:

```javascript
{
  $max: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The name of the field to update with the maximum value. |
| **`value`** | The value to compare with the current field value. The field will be updated only if this value is larger. |

## Example

Consider this sample document from the stores collection.

```json
{
  "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
  "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
  "staff": {
    "totalStaff": {
      "fullTime": 3,
      "partTime": 2
    }
  },
  "sales": {
    "totalSales": 31211,
    "salesByCategory": [
      {
        "categoryName": "Phone Mounts",
        "totalSales": 8911
      },
      {
        "categoryName": "Dash Cameras",
        "totalSales": 22300
      }
    ]
  }
}
```

### Example 1: Setting maximum staff capacity

Set a maximum staff capacity, updating only if the current value is lower.

```javascript
db.stores.updateOne(
  { "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.totalStaff.fullTime": 10
    }
  }
)
```

Since the current `fullTime` value is 3, and 10 is greater than 3, the field will be updated to 10.

### Example 2: Multiple field updates

Update multiple fields with maximum values simultaneously.

```javascript
db.stores.updateOne(
  { "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.totalStaff.partTime": 1,
      "sales.totalSales": 50000
    }
  }
)
```

In this case:
- `partTime` (2) will remain 2 since 1 < 2 (no change)
- `totalSales` (31211) will be updated to 50000 since 50000 > 31211

### Example 3: Creating new fields

If a field doesn't exist, `$max` creates it with the specified value.

```javascript
db.stores.updateOne(
  { "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "staff.maxStaffCapacity": 25,
      "sales.peakSalesRecord": 100000
    }
  }
)
```

### Example 4: Working with dates

Set maximum dates for tracking latest events or deadlines.

```javascript
db.stores.updateOne(
  { "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "lastPromotionDate": new Date("2024-12-31"),
      "inventoryDeadline": new Date("2024-06-30")
    }
  }
)
```

### Example 5: Updating array elements

Update maximum values within array elements using positional operators.

```javascript
db.stores.updateOne(
  {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "sales.salesByCategory.categoryName": "Phone Mounts"
  },
  {
    $max: {
      "sales.salesByCategory.$.totalSales": 12000
    }
  }
)
```

### Example 6: Tracking peak performance

Set peak performance metrics that only update when exceeded.

```javascript
db.stores.updateOne(
  { "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66" },
  {
    $max: {
      "performance.peakDailySales": 5000,
      "performance.maxCustomersPerDay": 150,
      "performance.highestSalesMonth": 45000
    }
  }
)
```

After these operations, the document would be updated as follows:

```json
{
  "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
  "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
  "staff": {
    "totalStaff": {
      "fullTime": 10,
      "partTime": 2
    },
    "maxStaffCapacity": 25
  },
  "sales": {
    "totalSales": 50000,
    "peakSalesRecord": 100000,
    "salesByCategory": [
      {
        "categoryName": "Phone Mounts",
        "totalSales": 12000
      },
      {
        "categoryName": "Dash Cameras",
        "totalSales": 22300
      }
    ]
  },
  "performance": {
    "peakDailySales": 5000,
    "maxCustomersPerDay": 150,
    "highestSalesMonth": 45000
  },
  "lastPromotionDate": ISODate("2024-12-31T00:00:00.000Z"),
  "inventoryDeadline": ISODate("2024-06-30T00:00:00.000Z")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]