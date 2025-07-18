---
title: $dateToString
titleSuffix: Overview of the $dateToString operator in Azure Cosmos DB for MongoDB vCore
description: The $dateToString operator in Azure Cosmos DB for MongoDB vCore converts a date object into a formatted string.
author: patty-chow
ms.author: yourpattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateToString

The `$dateToString` operator is used to convert a date object to a string in a specified format. It's commonly used in aggregation pipelines to format date fields for reporting, querying, or display purposes. This operator is highly versatile and allows you to define custom date formats.

## Syntax

```javascript
{
  $dateToString: {
    format: "<format_string>",
    date: <date_expression>,
    timezone: "<timezone>",
    onNull: "<replacement_value>"
  }
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`format`** | A string that specifies the format of the output date. |
| **`date`** | The date expression to format. |
| **`timezone`** | (Optional) A string that specifies the timezone. Defaults to UTC if not provided. |
| **`onNull`** | (Optional) A value to return if the `date` field is `null` or missing. |

## Format Specifiers

| Symbol | Meaning                  |
| ------ | ------------------------ |
| `%Y`   | Year (four digits)          |
| `%m`   | Month (two digits)         |
| `%d`   | Day of month (two digits)  |
| `%H`   | Hour (24-hour, two digits) |
| `%M`   | Minute (two digits)        |
| `%S`   | Second (two digits)        |
| `%L`   | Millisecond (three digits)   |


## Examples
We'll use this document from the `stores` collection to demonstrate how `$dateToString` works:
```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Formatting a date field to an ISO-like string

This example returns the `lastUpdated` field as a formatted date string in `YYYY-MM-DD` format.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      formattedDate: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$metadata.lastUpdated"
        }
      }
    }
  }
])
```

### Example 2: Including time in formatted output

This query formats the date to include both date and time.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      formattedDateTime: {
        $dateToString: {
          format: "%Y-%m-%d %H:%M:%S",
          date: "$metadata.lastUpdated"
        }
      }
    }
  }
])
```

### Example 3: Handling Null Values

This example uses the `onNull` parameter to provide a default string when the `lastUpdated` date field is null or missing.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      formattedDateOrDefault: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$metadata.lastUpdated",
          onNull: "No date available"
        }
      }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]