---
  title: $minN (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $minN operator returns the n smallest values from an array.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $minN (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$minN` operator returns the n smallest values from an array. It is useful when you want to find the lowest performing items based on numerical values, such as the smallest sales figures or lowest discount percentages.

## Syntax

The syntax for the `$minN` operator is as follows:

```javascript
{
  $minN: {
    input: <array>,
    n: <number>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The array from which to return the n smallest values. The array should contain numerical values. |
| **`n`** | The number of smallest values to return. Must be a positive integer. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
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
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  }
}
```

### Example 1: Get lowest two sales values

Suppose you want to find the lowest two sales values from all sales categories to identify underperforming products.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lowestTwoSales: {
        $minN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  }
])
```

This produces the following output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    lowestTwoSales: [ 2120, 28946 ]
  }
]
```

### Example 2: Find smallest discount percentages

You can also use `$minN` to find the smallest discount percentages from a promotion event.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  { $match: {"promotionEvents.eventName": "Major Bargain Bash"} },
  {
    $project: {
      name: 1,
      eventName: "$promotionEvents.eventName",
      smallestDiscounts: {
        $minN: {
          input: "$promotionEvents.discounts.discountPercentage",
          n: 3
        }
      }
    }
  }
])
```

This will return the three smallest discount percentages from the "Major Bargain Bash" promotion event.

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    eventName: 'Major Bargain Bash',
    smallestDiscounts: [ 7, 8, 9 ]
  }
]
```

### Example 3: Compare staff numbers across stores

You can use `$minN` to analyze staffing levels by finding stores with the lowest staff counts.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      staffNumbers: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"],
      lowestStaffCount: {
        $minN: {
          input: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"],
          n: 1
        }
      }
    }
  },
  { $limit: 5 }
])
```

This query shows the lowest staff count (either full-time or part-time) for each store, helping identify stores with minimal staffing.

```json
[
  {
    _id: 'af9015d8-3f6b-455f-8967-a83cc22ff018',
    name: 'VanArsdel, Ltd. | Party Goods Nook - Kunzeshire',
    staffNumbers: [ 15, 1 ],
    lowestStaffCount: [ 1 ]
  },
  {
    _id: 'ed319c06-731d-45fc-8a47-b05af8637cdf',
    name: 'Relecloud | Computer Outlet - Langoshfort',
    staffNumbers: [ 10, 3 ],
    lowestStaffCount: [ 3 ]
  },
  {
    _id: '62438f5f-0c56-4a21-8c6c-6bfa479494ad',
    name: 'First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort',
    staffNumbers: [ 20, 18 ],
    lowestStaffCount: [ 18 ]
  },
  {
    _id: '71c50be7-5c69-4a01-9218-e479fdeb6cee',
    name: 'Wide World Importers | Carpets Market - Port Newtonburgh',
    staffNumbers: [ 1, 14 ],
    lowestStaffCount: [ 1 ]
  },
  {
    _id: '4dc0275d-b554-4b0a-a1b2-0f14154be71d',
    name: 'VanArsdel, Ltd. | DJ Equipment Outlet - Lake Edmond',
    staffNumbers: [ 2, 13 ],
    lowestStaffCount: [ 2 ]
  }
]
```


### Example 4: Identify underperforming categories across all stores

Find the bottom two sales values across all stores to identify consistently underperforming product categories.

```javascript
db.stores.aggregate([
  { $match: { "sales.salesByCategory": { $exists: true, $ne: [] } } },
  {
    $project: {
      name: 1,
      location: 1,
      bottomTwoSales: {
        $minN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  },
  { $sort: { "bottomTwoSales.0": 1 } },
  { $limit: 3 }
])
```

This query returns the three stores with the overall lowest minimum sales values, helping identify locations that may need additional support or different product strategies.

```json
[
  {
    _id: 'c601ced7-d472-47e8-91c1-f213e3f60250',
    name: 'Tailwind Traders | Bed and Bath Bazaar - West Imaniside',
    location: { lat: -41.113, lon: -108.3752 },
    bottomTwoSales: [ 101, 12774 ]
  },
  {
    _id: '09782c05-a134-43a1-a65b-6a332bc89d7c',
    name: 'Tailwind Traders | Microphone Deals - Sonnytown',
    location: { lat: -61.9575, lon: 55.2523 },
    bottomTwoSales: [ 102, 18531 ]
  },
  {
    _id: '57303916-24f1-43a9-a50c-b96fb76ae40c',
    name: 'Fabrikam, Inc. | Art Supply Boutique - Port Geovanni',
    location: { lat: 63.9018, lon: -125.7517 },
    bottomTwoSales: [ 102, 6352 ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]