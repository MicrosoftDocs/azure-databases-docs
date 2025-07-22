---
title: $min
titleSuffix: Overview of the $min operator in Azure Cosmos DB for MongoDB (vCore)
description: Retrieves the minimum value for a specified field
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $min

The `$min` operator is used within aggregation stages like `$group`, `$bucket`, `$bucketAuto`, or `$setWindowFields`. The min operator is particularly useful in summarizing data or finding the smallest value in a dataset.

## Syntax

```javascript
$min: <expression>
```

The `<expression>` can be a field path or an aggregation expression that specifies the values to be considered for the minimum calculation.

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<expression>`** | Specifies the field or computed value to determine the minimum value. |

## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### Example 1: Using `$min` in `$group`

This query calculates the minimum sales value for each category in the `sales.salesByCategory` array by first grouping documents by sales category and then calculating the minimum sales volume within each category.

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            minSales: {
                $min: "$sales.salesByCategory.totalSales"
            }
        }
    }
])
```

This query returns the following results.

```json
[
    {
        "_id": "Christmas Trees",
        "minSales": 391
    },
    {
        "_id": "Nuts",
        "minSales": 257
    },
    {
        "_id": "Camping Tables",
        "minSales": 171
    },
    {
        "_id": "Music Theory Books",
        "minSales": 323
    },
    {
        "_id": "Fortified Wine",
        "minSales": 521
    },
    {
        "_id": "Children's Mystery",
        "minSales": 1470
    },
    {
        "_id": "Short Throw Projectors",
        "minSales": 111
    },
    {
        "_id": "Pliers",
        "minSales": 1981
    },
    {
        "_id": "Bluetooth Headphones",
        "minSales": 465
    },
    {
        "_id": "Video Storage",
        "minSales": 1568
    },
    {
        "_id": "Cleansers",
        "minSales": 170
    },
    {
        "_id": "Camera Straps",
        "minSales": 127
    },
    {
        "_id": "Carry-On Bags",
        "minSales": 149
    },
    {
        "_id": "Disinfectant Wipes",
        "minSales": 647
    },
    {
        "_id": "Insignia Smart TVs",
        "minSales": 451
    },
    {
        "_id": "Toner Refill Kits",
        "minSales": 3525
    },
    {
        "_id": "iPads",
        "minSales": 325
    },
    {
        "_id": "Storage Baskets",
        "minSales": 1151
    },
    {
        "_id": "Memory Foam Mattresses",
        "minSales": 422
    },
    {
        "_id": "Body Spray",
        "minSales": 448
    }
]
```

### Example 2: Using `$min` in `$bucket`

This example creates buckets based on sales values and calculates the minimum sales value for each bucket.

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales",
        boundaries: [0, 1000, 5000, 10000],
        default: "Other",
        output: {
            minSales: {
                $min: "$sales.totalSales"
            }
        }
    }
}])
```

This query returns the following results.

```json
[
    {
        "_id": 1000,
        "minSales": 1000
    },
    {
        "_id": "Other",
        "minSales": null
    },
    {
        "_id": 0,
        "minSales": 108
    },
    {
        "_id": 5000,
        "minSales": 5001
    }
]
```

### Example 3: Using `$min` in `$setWindowFields`

To get the minimum discount for the category "Laptops" by company, in the year 2023:

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },

    // Filter only Laptops category and events in 2023
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023,
            "promotionEvents.discounts.categoryName": "Laptops"
        }
    },

    // Use $setWindowFields to calculate average discount by city
    {
        $setWindowFields: {
            partitionBy: "$company",
            output: {
                minDiscount: {
                    $min: "$promotionEvents.discounts.discountPercentage",
                    window: {
                        documents: ["unbounded", "unbounded"]
                    }
                }
            }
        }
    },

    // Group by city to return one result per city
    {
        $group: {
            _id: "$company",
            minDiscount: {
                $first: "$minDiscount"
            }
        }
    }
])
```

This query returns the following results.

```json
[
    {
        "_id": "VanArsdel, Ltd.",
        "minDiscount": 6
    },
    {
        "_id": "Proseware, Inc.",
        "minDiscount": 8
    },
    {
        "_id": "Fabrikam, Inc.",
        "minDiscount": 5
    },
    {
        "_id": "Contoso, Ltd.",
        "minDiscount": 5
    },
    {
        "_id": "Fourth Coffee",
        "minDiscount": 6
    },
    {
        "_id": "Trey Research",
        "minDiscount": 7
    },
    {
        "_id": "Adatum Corporation",
        "minDiscount": 5
    },
    {
        "_id": "Relecloud",
        "minDiscount": 5
    },
    {
        "_id": "Lakeshore Retail",
        "minDiscount": 7
    },
    {
        "_id": "Northwind Traders",
        "minDiscount": 8
    },
    {
        "_id": "First Up Consultants",
        "minDiscount": 9
    },
    {
        "_id": "Wide World Importers",
        "minDiscount": 10
    },
    {
        "_id": "Tailwind Traders",
        "minDiscount": 5
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
