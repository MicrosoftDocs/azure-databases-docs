---
title: $bitsallclear
titleSuffix: Overview of the $bitsallclear operator in Azure Cosmos DB for MongoDB (vCore)
description: The $bitsallclear operator is used to match documents where all the bit positions specified in a bitmask are clear.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 11/01/2024
---

# $bitsAllClear

The `$bitsAllClear` operator is used to match documents where all the bit positions specified in a bitmask are clear (that is, 0). This operator is useful in scenarios where you need to filter documents based on specific bits being unset in a binary representation of a field.

## Syntax

```javascript
{
  <field>: { $bitsAllClear: <bitmask> }
}
```
## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document on which the bitwise operation is to be performed.|
| **`<bitmask>`** | A bitmask where each bit position specifies the corresponding bit position in the field's value that must be clear (0).|

## Example

Consider this sample document from the stores collection.


```json
{
  _id: 'a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6',
  name: 'Lakeshore Retail | Holiday Supply Hub - Marvinfort',
  location: {
    lat: -74.0427,
    lon: 160.8154
  },
  staff: {
    employeeCount: {
      fullTime: 9,
      partTime: 18
    }
  },
  sales: {
    salesByCategory: [
      {
        categoryName: 'Stockings',
        totalSales: 25731
      }
    ],
    revenue: 25731
  },
  promotionEvents: [
    {
      eventName: 'Mega Savings Extravaganza',
      promotionalDates: {
        startDate: {
          Year: 2023,
          Month: 6,
          Day: 29
        },
        endDate: {
          Year: 2023,
          Month: 7,
          Day: 7
        }
      },
      discounts: [
        {
          categoryName: 'Stockings',
          discountPercentage: 16
        },
        {
          categoryName: 'Tree Ornaments',
          discountPercentage: 8
        }
      ]
    },
    {
      eventName: 'Incredible Discount Days',
      promotionalDates: {
        startDate: {
          Year: 2023,
          Month: 9,
          Day: 27
        },
        endDate: {
          Year: 2023,
          Month: 10,
          Day: 4
        }
      },
      discounts: [
        {
          categoryName: 'Stockings',
          discountPercentage: 11
        },
        {
          categoryName: 'Holiday Cards',
          discountPercentage: 9
        }
      ]
    },
    {
      eventName: 'Massive Deal Mania',
      promotionalDates: {
        startDate: {
          Year: 2023,
          Month: 12,
          Day: 26
        },
        endDate: {
          Year: 2024,
          Month: 1,
          Day: 2
        }
      },
      discounts: [
        {
          categoryName: 'Gift Bags',
          discountPercentage: 21
        },
        {
          categoryName: 'Bows',
          discountPercentage: 19
        }
      ]
    },
    {
      eventName: 'Super Saver Soiree',
      promotionalDates: {
        startDate: {
          Year: 2024,
          Month: 3,
          Day: 25
        },
        endDate: {
          Year: 2024,
          Month: 4,
          Day: 1
        }
      },
      discounts: [
        {
          categoryName: 'Tree Ornaments',
          discountPercentage: 15
        },
        {
          categoryName: 'Stockings',
          discountPercentage: 14
        }
      ]
    },
    {
      eventName: 'Fantastic Savings Fiesta',
      promotionalDates: {
        startDate: {
          Year: 2024,
          Month: 6,
          Day: 23
        },
        endDate: {
          Year: 2024,
          Month: 6,
          Day: 30
        }
      },
      discounts: [
        {
          categoryName: 'Stockings',
          discountPercentage: 24
        },
        {
          categoryName: 'Gift Wrap',
          discountPercentage: 16
        }
      ]
    },
    {
      eventName: 'Price Plunge Party',
      promotionalDates: {
        startDate: {
          Year: 2024,
          Month: 9,
          Day: 21
        },
        endDate: {
          Year: 2024,
          Month: 9,
          Day: 28
        }
      },
      discounts: [
        {
          categoryName: 'Holiday Tableware',
          discountPercentage: 13
        },
        {
          categoryName: 'Holiday Cards',
          discountPercentage: 11
        }
      ]
    }
  ],
  company: 'Lakeshore Retail',
  city: 'Marvinfort',
  storeOpeningDate: 2024-10-01T18:24:02.586Z,
  lastUpdated: Timestamp({ t: 1730485442, i: 1 }),
  storeFeatures: 38
}
```

The `storeFeatures` field is a bitmask integer representing various store capabilities. Each bit corresponds to a feature:

| Bit | Value | Feature                 |
|-----|-------|--------------------------|
| 0   | 1     | In-Store Pickup          |
| 1   | 2     | Parking                  |
| 2   | 4     | Wheelchair Access        |
| 3   | 8     | Open 24 Hours            |
| 4   | 16    | Pet-Friendly             |
| 5   | 32    | Free Wi-Fi               |
| 6   | 64    | Restrooms                |
| 7   | 128   | Home Delivery            |

Find stores that are NOT open 24 hours AND do NOT allow pets (bits 3 and 4)

```javascript
db.stores.find({
  storeFeatures: {  $bitsAllClear: [3, 4] }},
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Equivalent:

```javascript
db.stores.find({
  storeFeatures: { $bitsAnySet: 24  }},  // 8 + 16
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Sample output:

```JSON
[
  {
    _id: 'a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6',
    name: 'Lakeshore Retail | Holiday Supply Hub - Marvinfort',
    storeFeatures: 38
  },
  {
    _id: '94792a4c-4b03-466b-91f6-821c4a8b2aa4',
    name: 'Fourth Coffee | Eyewear Shop - Lessiemouth',
    storeFeatures: 225
  },
  {
    _id: '1a2c387b-bb43-4b14-a6cd-cc05a5dbfbd5',
    name: 'Contoso, Ltd. | Smart Home Device Vault - Port Katarina',
    storeFeatures: 36
  },
  {
    _id: 'e88f0096-4299-4944-9788-695c40786d97',
    name: 'Adatum Corporation | Handbag Shoppe - Lucienneberg',
    storeFeatures: 135
  },
  {
    _id: 'bfb213fa-8db8-419f-8e5b-e7096120bad2',
    name: 'First Up Consultants | Beauty Product Shop - Hansenton',
    storeFeatures: 135
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
