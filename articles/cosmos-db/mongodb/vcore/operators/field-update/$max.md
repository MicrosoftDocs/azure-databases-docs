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

## Examples

Consider this sample document from the stores collection.

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1: Setting maximum staff capacity

To update the full time staff to 10 only if the current full time staff count is lower, use the $max operator on the field to perform the update. Since the current `fullTime` value is 3, and 10 is greater than 3, the field will be updated to 10.

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

### Example 2: Multiple field updates

To update multiple fields with maximum values, use the $max operator with multiple fields and their corresponding max values to set.

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

### Example 4: Updating array elements

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

### Example 5: Tracking peak performance

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

After these operations, the updated document is:

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
