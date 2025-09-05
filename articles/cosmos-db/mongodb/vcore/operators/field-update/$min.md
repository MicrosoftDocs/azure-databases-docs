---
  title: $min
  titleSuffix: Overview of the $min operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $min operator updates the value of a field to a specified value if the specified value is less than the current value of the field.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/04/2025
---

# $min

The `$min` operator updates the value of a field to a specified value if the specified value is less than the current value of the field. If the field does not exist, `$min` creates the field and sets it to the specified value. This operator is useful for maintaining minimum thresholds or tracking the lowest values.

## Syntax

```javascript
{
  $min: {
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The name of the field to update with the minimum value. |
| **`value`** | The value to compare with the current field value. The field will be updated only if this value is smaller. |

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

### Example 1: Setting minimum staff requirements

To set a minimum staff requirement, update the full time stagg count only if the current value of the field is higher. Since the current `fullTime` value is 14, and 10 is less than 14, the field will be updated to 10.

```javascript
db.stores.updateOne(
  { "_id": "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.totalStaff.fullTime": 10
    }
  }
)
```

### Example 2: Multiple field updates

To update multiple fields with minimum values simultaneously, use the $min operator with multiple fields and corresponding min values.

```javascript
db.stores.updateOne(
  { "_id": "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.totalStaff.partTime": 12,
      "sales.totalSales": 50000
    }
  }
)
```

In this case:
- `partTime` (8) will be updated to 8 since 12 > 8 (no change)
- `totalSales` (83865) will be updated to 50000 since 50000 < 83865

### Example 3: Creating new fields

If a field doesn't exist, `$min` creates it with the specified value.

```javascript
db.stores.updateOne(
  { "_id": "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "staff.minStaffRequired": 15,
      "sales.minimumSalesTarget": 30000
    }
  }
)
```

### Example 4: Working with Dates

Set minimum dates for tracking earliest events.

```javascript
db.stores.updateOne(
  { "_id": "26afb024-53c7-4e94-988c-5eede72277d5" },
  {
    $min: {
      "lastInventoryCheck": new Date("2024-01-15"),
      "firstSaleDate": new Date("2023-06-01")
    }
  }
)
```

### Example 5: Updating array elements

Update minimum values within array elements using positional operators.

```javascript
db.stores.updateOne(
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "sales.salesByCategory.categoryName": "Lavalier Microphones"
  },
  {
    $min: {
      "sales.salesByCategory.$.totalSales": 40000
    }
  }
)
```

After these operations, the updated document is:

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "staff": {
    "totalStaff": {
      "fullTime": 10,
      "partTime": 8
    },
    "minStaffRequired": 15
  },
  "sales": {
    "totalSales": 50000,
    "minimumSalesTarget": 30000,
    "salesByCategory": [
      {
        "categoryName": "Lavalier Microphones",
        "totalSales": 40000
      },
      {
        "categoryName": "Wireless Microphones",
        "totalSales": 39691
      }
    ]
  },
  "lastInventoryCheck": ISODate("2024-01-15T00:00:00.000Z"),
  "firstSaleDate": ISODate("2023-06-01T00:00:00.000Z")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
