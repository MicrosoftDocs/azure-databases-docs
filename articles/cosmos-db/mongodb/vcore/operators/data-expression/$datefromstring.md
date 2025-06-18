---
title: $dateFromString usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Converts a date/time string to a date object.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 01/29/2025
---

# $dateFromString
The `$dateFromString` operator is used to convert a date/time string to a date object in MongoDB. This operation can be useful when dealing with string representations of dates that need to be manipulated or queried as date objects.

## Syntax
```plaintext
{ $dateFromString: { dateString: <string>, format: <string>, timezone: <string>, onError: <expression>, onNull: <expression> } }
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`dateString`** | The date/time string to convert to a date object. |
| **`format`** | (Optional) The date format specification of the `dateString`. |
| **`timezone`** | (Optional) The timezone to use to format the date. |
| **`onError`** | (Optional) The value to return if an error occurs while parsing the `dateString`. |
| **`onNull`** | (Optional) The value to return if the `dateString` is `null` or missing. |

## Example
### Converting promotional event dates
This example demonstrates how to convert the `startDate` and `endDate` of promotional events from string representations to date objects.

```json
db.collection.aggregate([
  {
    $project: {
      eventName: 1,
      startDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.startDate.Year" },
              "-",
              { $toString: "$promotionEvents.promotionalDates.startDate.Month" },
              "-",
              { $toString: "$promotionEvents.promotionalDates.startDate.Day" }
            ]
          }
        }
      },
      endDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.endDate.Year" },
              "-",
              { $toString: "$promotionEvents.promotionalDates.endDate.Month" },
              "-",
              { $toString: "$promotionEvents.promotionalDates.endDate.Day" }
            ]
          }
        }
      }
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
