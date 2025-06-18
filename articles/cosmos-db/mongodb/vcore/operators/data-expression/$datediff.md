--- 
title: $dateDiff usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Calculates the difference between two dates in various units.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 01/29/2025
---
# $dateDiff
The `$dateDiff` operator calculates the difference between two dates in various units such as years, months, days, etc. It's useful for determining the duration between two timestamps in your dataset.

## Syntax
```
$dateDiff: {
   startDate: <expression>,
   endDate: <expression>,
   unit: <string>,
   timezone: <string>, // Optional
   startOfWeek: <string> // Optional
}
```

## Parameters  
| | Description |
| --- | --- |
| **`startDate`**| The beginning date for the calculation.|
| **`endDate`**| The ending date for the calculation.|
| **`unit`**| The unit of time to measure the difference. Valid values include: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`, `millisecond`.|
| **`timezone`**| Optional. The timezone to use for the calculation.|
| **`startOfWeek`**| Optional. The starting day of the week. Valid values are: `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`.|

## Example
Calculate the difference in days between the start and end dates of promotional events:

```json
db.collection.aggregate([
  {
    $project: {
      eventName: 1,
      startDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.startDate.Year",
          month: "$promotionEvents.promotionalDates.startDate.Month",
          day: "$promotionEvents.promotionalDates.startDate.Day"
        }
      },
      endDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.endDate.Year",
          month: "$promotionEvents.promotionalDates.endDate.Month",
          day: "$promotionEvents.promotionalDates.endDate.Day"
        }
      },
      durationInDays: {
        $dateDiff: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.startDate.Year",
              month: "$promotionEvents.promotionalDates.startDate.Month",
              day: "$promotionEvents.promotionalDates.startDate.Day"
            }
          },
          endDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.endDate.Year",
              month: "$promotionEvents.promotionalDates.endDate.Month",
              day: "$promotionEvents.promotionalDates.endDate.Day"
            }
          },
          unit: "day"
        }
      }
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]