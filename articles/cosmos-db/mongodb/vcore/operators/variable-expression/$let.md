---
  title: $let (variable expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $let operator allows defining variables for use in a specified expression, enabling complex calculations and reducing code repetition.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $let (variable expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$let` operator is used to define variables for use in a specified expression. It allows you to create temporary variables that can be referenced within the expression, making complex calculations more readable and preventing redundant computations.

## Syntax

The syntax for the `$let` operator is as follows:

```javascript
{
  $let: {
    vars: { 
      <var1>: <expression1>,
      <var2>: <expression2>,
      ...
    },
    in: <expression>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`vars`** | An object that defines the variables and their values. Each variable is assigned the result of an expression. |
| **`in`** | The expression that uses the variables defined in the `vars` object. Variables are referenced using `$$<variable_name>`. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 5,
      "partTime": 20
    }
  },
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
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 12,
          "Day": 26
        },
        "endDate": {
          "Year": 2024,
          "Month": 1,
          "Day": 5
        }
      },
      "discounts": [
        {
          "categoryName": "Game Controllers",
          "discountPercentage": 22
        },
        {
          "categoryName": "Home Theater Projectors",
          "discountPercentage": 23
        }
      ]
    }
  ]
}
```

### Example 1: Basic variable usage

Calculate staff efficiency metrics using defined variables.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      staffMetrics: {
        $let: {
          vars: {
            fullTime: "$staff.totalStaff.fullTime",
            partTime: "$staff.totalStaff.partTime",
            totalSales: "$sales.totalSales"
          },
          in: {
            totalStaff: { $add: ["$$fullTime", "$$partTime"] },
            salesPerEmployee: { $divide: ["$$totalSales", { $add: ["$$fullTime", "$$partTime"] }] },
            fullTimeRatio: { $divide: ["$$fullTime", { $add: ["$$fullTime", "$$partTime"] }] }
          }
        }
      }
    }
  }
])
```

This will produce the following output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    staffMetrics: {
      totalStaff: 39,
      salesPerEmployee: 3893.948717948718,
      fullTimeRatio: 0.5128205128205128
    }
  }
]
```

### Example 2: Nested $let expressions

Calculate location-based insights with nested variable definitions.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      locationInsights: {
        $let: {
          vars: {
            lat: "$location.lat",
            lon: "$location.lon"
          },
          in: {
            coordinates: { lat: "$$lat", lon: "$$lon" },
            hemisphere: {
              $let: {
                vars: {
                  northSouth: { $cond: [{ $gte: ["$$lat", 0] }, "North", "South"] },
                  eastWest: { $cond: [{ $gte: ["$$lon", 0] }, "East", "West"] }
                },
                in: {
                  latitudeHemisphere: "$$northSouth",
                  longitudeHemisphere: "$$eastWest",
                  quadrant: { $concat: ["$$northSouth", " ", "$$eastWest"] }
                }
              }
            },
            distanceFromEquator: { $abs: "$$lat" },
            distanceFromPrimeMeridian: { $abs: "$$lon" }
          }
        }
      }
    }
  }
])
```

This will produce comprehensive location analysis with nested calculations.

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    locationInsights: {
      coordinates: { lat: 70.1272, lon: 69.7296 },
      hemisphere: {
        latitudeHemisphere: 'North',
        longitudeHemisphere: 'East',
        quadrant: 'North East'
      },
      distanceFromEquator: 70.1272,
      distanceFromPrimeMeridian: 69.7296
    }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
