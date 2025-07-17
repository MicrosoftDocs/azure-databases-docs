---
  title: $lastN (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $lastN operator returns the last n elements from an array.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $lastN (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$lastN` operator returns the last n elements from an array. It is useful when you want to limit the number of elements returned from the end of an array, such as getting the most recent items from a chronologically ordered list.

## Syntax

The syntax for the `$lastN` operator is as follows:

```javascript
{
  $lastN: {
    input: <array>,
    n: <number>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The array from which to return the last n elements. |
| **`n`** | The number of elements to return from the end of the array. Must be a positive integer. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 6, "Day": 29 },
        "endDate": { "Year": 2023, "Month": 7, "Day": 9 }
      }
    },
    {
      "eventName": "Fantastic Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 7 }
      }
    },
    {
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 5 }
      }
    },
    {
      "eventName": "Super Sale Spectacular",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
        "endDate": { "Year": 2024, "Month": 4, "Day": 2 }
      }
    },
    {
      "eventName": "Grand Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 30 }
      }
    },
    {
      "eventName": "Major Bargain Bash",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 9, "Day": 21 },
        "endDate": { "Year": 2024, "Month": 9, "Day": 30 }
      }
    }
  ]
}
```

### Example 1: Get last two promotion events

Suppose you want to get the most recent two promotion events from a store.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lastTwoPromotions: {
        $lastN: {
          input: "$promotionEvents",
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
    lastTwoPromotions: [
      {
        eventName: 'Grand Deal Days',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 6, Day: 30 }
        },
        discounts: [
          { categoryName: 'Remote Controls', discountPercentage: 7 },
          { categoryName: 'Televisions', discountPercentage: 11 },
          {
            categoryName: 'Business Projectors',
            discountPercentage: 13
          },
          { categoryName: 'Laser Projectors', discountPercentage: 6 },
          { categoryName: 'Projectors', discountPercentage: 6 },
          { categoryName: 'Projector Screens', discountPercentage: 24 }
        ]
      },
      {
        eventName: 'Major Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 30 }
        },
        discounts: [
          { categoryName: 'Sound Bars', discountPercentage: 9 },
          { categoryName: 'VR Games', discountPercentage: 7 },
          { categoryName: 'Xbox Games', discountPercentage: 25 },
          {
            categoryName: 'Projector Accessories',
            discountPercentage: 18
          },
          { categoryName: 'Mobile Games', discountPercentage: 8 },
          { categoryName: 'Projector Cases', discountPercentage: 22 }
        ]
      }
    ]
  }
]
```

### Example 2: Get last three sales categories

You can also use `$lastN` to get the last few sales categories.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lastThreeCategories: {
        $lastN: {
          input: "$sales.salesByCategory",
          n: 3
        }
      }
    }
  }
])
```

This returns the last three sales categories from the salesByCategory array.

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    lastThreeCategories: [
      { categoryName: 'Game Controllers', totalSales: 43522 },
      { categoryName: 'Remote Controls', totalSales: 28946 },
      { categoryName: 'VR Games', totalSales: 32272 }
    ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]