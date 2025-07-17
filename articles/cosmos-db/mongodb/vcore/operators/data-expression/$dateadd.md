---
title: $dateAdd usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Adds a specified number of time units to a date.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 01/29/2025
---

# $dateAdd

The `$dateAdd` operator adds a specified number of time units to a date. It's useful in scenarios where you need to calculate future dates based on a given date and a time interval.

## Syntax

```shell
$dateAdd: {
   startDate: <expression>,
   unit: <string>,
   amount: <number>,
   timezone: <string>  // Optional
}
```

## Parameters

| | Description |
| --- | --- |
| **`startDate`** | The starting date for the addition operation. |
| **`unit`** | The unit of time to add. Valid units include: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`, `millisecond`. |
| **`amount`** | The number of units to add. |
| **`timezone`** | Optional. The timezone to use for the operation. |

## Examples

### Example 1: Adding days to a date

```json
db.collection.aggregate([
   {
      $project: {
         eventName: 1,
         newEndDate: {
            $dateAdd: {
               startDate: {
                  $dateFromParts: {
                     year: "$promotionEvents.promotionalDates.endDate.Year",
                     month: "$promotionEvents.promotionalDates.endDate.Month",
                     day: "$promotionEvents.promotionalDates.endDate.Day"
                  }
               },
               unit: "day",
               amount: 7
            }
         }
      }
   }
])
```

### Example 2: Adding months to a date

```json
db.collection.aggregate([
   {
      $project: {
         eventName: 1,
         newStartDate: {
            $dateAdd: {
               startDate: {
                  $dateFromParts: {
                     year: "$promotionEvents.promotionalDates.startDate.Year",
                     month: "$promotionEvents.promotionalDates.startDate.Month",
                     day: "$promotionEvents.promotionalDates.startDate.Day"
                  }
               },
               unit: "month",
               amount: 1
            }
         }
      }
   }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]