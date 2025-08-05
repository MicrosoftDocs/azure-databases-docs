---
  title: $currentDate
  titleSuffix: Overview of the $currentDate operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $currentDate operator sets the value of a field to the current date, either as a Date or a timestamp.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $currentDate

The `$currentDate` operator sets the value of a field to the current date, either as a Date or a timestamp. This operator is useful for tracking when documents were last modified or for setting creation timestamps.

## Syntax

The syntax for the `$currentDate` operator is as follows:

```javascript
{
  $currentDate: {
    <field1>: <typeSpecification1>,
    <field2>: <typeSpecification2>,
    ...
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The name of the field to set to the current date. |
| **`typeSpecification`** | Optional. Specifies the type of the date value. Can be `true` (for Date type) or `{ $type: "timestamp" }` for timestamp type. Default is `true` (Date). |

## Example

Consider this sample document from the stores collection.

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
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### Example 1: Setting current date

Add a `lastUpdated` field with the current date to a store document.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastUpdated": true
    }
  }
)
```

This will add a `lastUpdated` field with the current date as a Date object and produce the following result:

```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}

```


### Example 2: Setting current timestamp

Add both a date field and a timestamp field to track modifications.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "lastModified": true,
      "lastModifiedTimestamp": { $type: "timestamp" }
    }
  }
)
```

This query will return  the following document 

```json
{
  acknowledged: true,
  insertedId: null,
  matchedCount: Long("1"),
  modifiedCount: Long("1"),
  upsertedCount: 0
}
```


### Example 3: Updating nested fields

Set current date for nested fields in the document structure.

```javascript
db.stores.updateOne(
  { "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f" },
  {
    $currentDate: {
      "sales.lastSalesUpdate": true,
      "staff.lastStaffUpdate": { $type: "timestamp" }
    }
  }
)
```

After these operations, the document would include the new timestamp fields:

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "lastUpdated": ISODate("2025-02-12T10:30:45.123Z"),
  "lastModified": ISODate("2025-02-12T10:30:45.123Z"),
  "lastModifiedTimestamp": Timestamp(1739450445, 1),
  "sales": {
    "totalSales": 37701,
    "lastSalesUpdate": ISODate("2025-02-12T10:30:45.123Z"),
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    },
    "lastStaffUpdate": Timestamp(1739450445, 1)
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
