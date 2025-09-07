---
title: $centerSphere
titleSuffix: Overview of the $centerSphere operator in Azure Cosmos DB for MongoDB (vCore)
description: The $centerSphere operator specifies a circle using spherical geometry for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/28/2025
---

# $centerSphere

The `$centerSphere` operator specifies a circle using spherical geometry for `$geoWithin` queries. This operator is useful for geographic calculations that need to account for Earth's spherical shape.

## Syntax

```javascript
{
  $geoWithin: {
    $centerSphere: [ [ <x>, <y> ], <radius in radians> ]
  }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<x>` | The longitude of the circle's center point |
| `<y>` | The latitude of the circle's center point |
| `<radius in radians>` | The radius of the sphere in radians (divide distance in kilometers by 6371 to convert to radians) |

## Examples

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
  "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
  "location": { "lat": -74.0427, "lon": 160.8154 },
  "staff": { "employeeCount": { "fullTime": 9, "partTime": 18 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Stockings", "totalSales": 25731 } ],
    "revenue": 25731
  },
  "promotionEvents": [
    {
      "eventName": "Mega Savings Extravaganza",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 6, "Day": 29 },
        "endDate": { "Year": 2023, "Month": 7, "Day": 7 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 16 },
        { "categoryName": "Tree Ornaments", "discountPercentage": 8 }
      ]
    },
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 11 },
        { "categoryName": "Holiday Cards", "discountPercentage": 9 }
      ]
    },
    {
      "eventName": "Massive Deal Mania",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 2 }
      },
      "discounts": [
        { "categoryName": "Gift Bags", "discountPercentage": 21 },
        { "categoryName": "Bows", "discountPercentage": 19 }
      ]
    },
    {
      "eventName": "Super Saver Soiree",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
        "endDate": { "Year": 2024, "Month": 4, "Day": 1 }
      },
      "discounts": [
        { "categoryName": "Tree Ornaments", "discountPercentage": 15 },
        { "categoryName": "Stockings", "discountPercentage": 14 }
      ]
    },
    {
      "eventName": "Fantastic Savings Fiesta",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 30 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 24 },
        { "categoryName": "Gift Wrap", "discountPercentage": 16 }
      ]
    },
    {
      "eventName": "Price Plunge Party",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 9, "Day": 21 },
        "endDate": { "Year": 2024, "Month": 9, "Day": 28 }
      },
      "discounts": [
        { "categoryName": "Holiday Tableware", "discountPercentage": 13 },
        { "categoryName": "Holiday Cards", "discountPercentage": 11 }
      ]
    }
  ],
  "company": "Lakeshore Retail",
  "city": "Marvinfort",
  "storeOpeningDate": { "$date": "2024-10-01T18:24:02.586Z" },
  "lastUpdated": { "$timestamp": { "t": 1730485442, "i": 1 } },
  "storeFeatures": 38
}
```

### Example 1: Find stores within a circular area (calculation over earth's spherical shape)

The example query finds two stores within approximately 1,000 kilometers (radius ≈ 0.157 radians) of the Wide World Importers Headphone Corner store location. The query can help identify nearby stores for regional marketing campaigns or supply chain optimization.

```javascript
// Convert 1000km to radians: 1000/6371 ≈ 0.157
db.stores.find(
  {
    location: {
      $geoWithin: {
        $centerSphere: [[-82.5543, -65.105], 0.157]
      }
    }
  },
  {
    _id: 0,
    name: 1,
    location: 1,
    city: 1
  }
).limit(2)
```

The query returns the nearest stores from Wide World Importers Headphone Corner location.

```json
  {
    "name": "Fourth Coffee | Electronics Bazaar - O'Keefeburgh",
    "location": { "lat": -64.5856, "lon": -115.5241 },
    "city": "O'Keefeburgh"
  },
  {
    "name": "Boulder Innovations | Footwear Outlet - West Sybleberg",
    "location": { "lat": -72.73, "lon": -60.2306 },
    "city": "West Sybleberg"
  }
```

> [!IMPORTANT]
> The `$centerSphere` operator calculates distances using spherical geometry, making it more accurate for Earth-based calculations than `$center`.
>
> The radius must be specified in radians.
>
> Coordinates should be specified in the order: [longitude, latitude].
>
> If the geographic buffer extends beyond a UTM zone or crosses the international dateline, the results may be inaccurate or unpredictable.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
