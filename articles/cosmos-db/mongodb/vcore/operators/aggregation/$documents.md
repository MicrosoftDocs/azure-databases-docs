---
title: $documents usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $documents stage creates a pipeline from a set of provided documents.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/09/2025
---

# $documents

The `$documents` aggregation pipeline stage is used to create a pipeline from a set of provided documents. This stage is particularly useful when you want to process specific documents without querying a collection.

## Syntax

```javascript
{
  $documents: [
    <document1>,
    <document2>,
    ...
  ]
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<document>`** | A JSON object representing a document to include in the pipeline. |

## Examples

### Example 1: Create a pipeline from specific documents

The following example demonstrates how to use the `$documents` stage to process a set of predefined documents:

```javascript
db.aggregate([
  {
    $documents: [
      {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "location": {
          "lat": 60.1441,
          "lon": -141.5012
        },
        "sales": {
          "fullSales": 3700
        },
        "tag": ["#ShopLocal", "#SeasonalSale"]
      },
      {
        "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
        "location": {
          "lat": 40.7128,
          "lon": -74.0060
        },
        "sales": {
          "fullSales": 5400
        },
        "tag": ["#TechDeals", "#FreeShipping"]
      }
    ]
  },
  {
    $project: {
      _id: 1,
      name: 1,
      "location.lat": 1,
      "location.lon": 1,
      "sales.fullSales": 1,
      tags: "$tag"  // renames "tag" to "tags"
    }
  }
]);
```

This query would return the following document.

```json
[
  {
    _id: '7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5',
    name: 'Lakeshore Retail | Holiday Supply Hub - Marvinfort',
    location: { lat: 60.1441, lon: -141.5012 },
    sales: { fullSales: 3700 },
    tags: [ '#ShopLocal', '#SeasonalSale' ]
  },
  {
    _id: '7e53ca0f-6e24-4177-966c-fe62a11e9af5',
    name: 'Contoso, Ltd. | Office Supply Deals - South Shana',
    location: { lat: 40.7128, lon: -74.006 },
    sales: { fullSales: 5400 },
    tags: [ '#TechDeals', '#FreeShipping' ]
  }
]

```


### Example 2: Combine `$documents` with other pipeline stages

```javascript
db.aggregate([
  {
    $documents: [
      {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "location": {
          "lat": 60.1441,
          "lon": -141.5012
        },
        "sales": {
          "fullSales": 3700
        },
        "tag": ["#ShopLocal", "#SeasonalSale"]
      },
      {
        "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
        "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
        "location": {
          "lat": 40.7128,
          "lon": -74.0060
        },
        "sales": {
          "fullSales": 5400
        },
        "tag": ["#TechDeals", "#FreeShipping"]
      }
    ]
  },
  {
    $match: { "sales.fullSales": { $gt: 4000 } }
  },
  {
    $sort: { "sales.fullSales": -1 }
  }
]);
```

This query would return the following document.

```json
[
  {
    _id: '7e53ca0f-6e24-4177-966c-fe62a11e9af5',
    name: 'Contoso, Ltd. | Office Supply Deals - South Shana',
    location: { lat: 40.7128, lon: -74.006 },
    sales: { fullSales: 5400 },
    tag: [ '#TechDeals', '#FreeShipping' ]
  }
]

```


## Limitations

- The $documents stage is only supported in database-level aggregation pipelines.
It must be the first stage in the pipeline to function correctly.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
