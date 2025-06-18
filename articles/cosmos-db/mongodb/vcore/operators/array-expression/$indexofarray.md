---
  title: $indexOfArray (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $indexOfArray operator is used to search for an element in an array and return the index of the first occurrence of the element. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---

# $indexOfArray (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$indexOfArray` operator is used to search for an element in an array and return the index of the first occurrence of the element. If the element isn't found, it returns `-1`. This operator is useful for queries where you need to determine the position of an element within an array. For example,  finding the index of a specific value or object in a list.

## Syntax

```javascript
{ $indexOfArray: [ <array>, <searchElement>, <start>, <end> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<array>`**| The array in which you want to search for the element.|
| **`<searchElement>`**|  The element you're searching for in the array.|
| **`<start>`**| (Optional) The index from which to start the search. If omitted, the search starts from the beginning of the array.|
| **`<end>`**| (Optional) The index at which to end the search. If omitted, the search goes until the end of the array.|

## Examples

Let's understand the usage with the following sample json.
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
  ]
}
```

### Example 1: Finding the index of the first occurrence

To find the index of the category "DJ Headphones" in the `salesByCategory` array across all documents:

```javascript
db.stores.aggregate([
  {
    $project: {
      index: {
        $indexOfArray: [
          "$sales.salesByCategory.categoryName",
          "DJ Headphones"
        ]
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```

This query would return the following document.

```json
[
  { "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41", "index": -1 },
  { "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34", "index": -1 },
  { "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197", "index": -1 }
]
```

### Example 2: Finding the index in a range

To find documents having index between 3 and 5 for "Bargain Blitz Days" event in the `promotionEvents` array:

```javascript
db.stores.aggregate([
  // Step 1: Project the index of the "Bargain Blitz Days" event name within the specified range
  {
    $project: {
      index: {
        $indexOfArray: [
          "$promotionEvents.eventName",
          "Bargain Blitz Days",
          3,
          5
        ]
      }
    }
  },
  // Step 2: Match documents where index > 0
  {
    $match: {
      index: { $gt: 0 }
    }
  },
 // Limit the result to the first 3 documents
  { $limit: 3 }                          
])
```


This query would return the following document.

```json
[
  { "_id": "ced8caf0-051a-48ce-88d3-2935815261c3", "index": 3 },
  { "_id": "509be7ce-539a-41b5-8fde-b85fb3ef3faa", "index": 3 },
  { "_id": "d06e8136-9a7f-4b08-92c8-dc8eac73bad3", "index": 3 }
]

```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]