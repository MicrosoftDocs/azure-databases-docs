---
title: $dateFromParts usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Constructs a date from individual components.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 01/29/2025
---

# $dateFromParts

The `$dateFromParts` operator constructs a date from individual components such as year, month, day, hour, minute, second, and millisecond. This operator can be useful when dealing with data that stores date components separately.

## Syntax

```plaintext
{ $dateFromParts: { year: <year>, month: <month>, day: <day>, hour: <hour>, minute: <minute>, second: <second>, millisecond: <millisecond>, timezone: <timezone> } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`year`** | The year component of the date. |
| **`month`** | The month component of the date. |
| **`day`** | The day component of the date. |
| **`hour`** | The hour component of the date. |
| **`minute`** | The minute component of the date. |
| **`second`** | The second component of the date. |
| **`millisecond`** | The millisecond component of the date. |
| **`timezone`** | Optional. A timezone specification. |

## Examples

### Example 1: Constructing a start date

To construct the start date of a promotional event:

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
      }
    }
  }
])
```

### Example 2: Constructing an end date

To construct the end date of a promotional event:

```json
db.collection.aggregate([
  {
    $project: {
      eventName: 1,
      endDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.endDate.Year",
          month: "$promotionEvents.promotionalDates.endDate.Month",
          day: "$promotionEvents.promotionalDates.endDate.Day"
        }
      }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
