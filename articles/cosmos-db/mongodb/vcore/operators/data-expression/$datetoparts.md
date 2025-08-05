---
title: $dateToParts
titleSuffix: Overview of the $dateToParts operator in Azure Cosmos DB for MongoDB vCore
description: The $dateToParts operator in Azure Cosmos DB for MongoDB vCore decomposes a date into its individual parts such as year, month, day, and more.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateToParts
The `$dateToParts` operator is used to extract individual components (Year, Month, Day, Hour, Minute, Second, Millisecond, etc.) from a date object. This is useful for scenarios where manipulation or analysis of specific date parts is required, such as sorting, filtering, or aggregating data based on individual date components.

## Syntax
```javascript
$dateToParts: {
  date: <dateExpression>,
  timezone: <string>, // optional
  iso8601: <boolean> // optional
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`date`** | The date expression to extract parts from. |
| **`timezone`** | Optional. Specifies the timezone for the date. Defaults to UTC if not provided. |
| **`iso8601`** | Optional. If true, the operator will use ISO 8601 week date calendar system. Defaults to false. |

## Examples
We'll use this document from the `stores` collection to demonstrate how `$dateToParts` works:
```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Extracting date parts from a field
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dateParts: {
        $dateToParts: { 
          date: "$metadata.lastUpdated" 
        }
      }
    }
  }
])
```
This example extracts the constituent parts of the `lastUpdated` field in the `metadata` object.

### Example 2: Using timezone
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      datePartsWithTimezone: {
        $dateToParts: { 
          date: "$metadata.lastUpdated", 
          timezone: "America/New_York" 
        }
      }
    }
  }
])
```
This example extracts the date parts while considering the timezone `America/New_York`.

### Example 3: Using ISO 8601 week date system
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      iso8601Parts: {
        $dateToParts: { 
          date: "$metadata.lastUpdated", 
          iso8601: true 
        }
      }
    }
  }
])
```
This example extracts date parts using the ISO 8601 week date calendar system.

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]