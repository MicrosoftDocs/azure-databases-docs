---
title: $redact
titleSuffix: Overview of the $redact operation in Azure Cosmos DB for MongoDB (vCore)
description: Filters the content of the documents based on access rights.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 06/23/2025
---

# $redact
The `$redact` stage in aggregation pipeline is used to filter fields of the documents in a collection dynamically based on access rights or other conditions. It processes each document in the pipeline and removes or retains fields based on the specified logic.

## Syntax
```javascript
{
  $redact: <expression>
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`<expression>`** | A valid MongoDB expression that evaluates to one of the following: `$$DESCEND`, `$$PRUNE`, or `$$KEEP`. These variables determine whether to keep, remove, or traverse deeper into the document. |

## Examples

Consider this sample document from the stores collection.
```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1: Redacting sensitive information
To filter out the `promotionEvents` field for documents where the `discountPercentage` in a promotion exceeds 15%.

```javascript
db.collection.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $gt: ["$promotionEvents.discounts.discountPercentage", 15]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```

### Example 2: Restricting access based on tags
To remove all documents that contain the tag `#MembershipDeals`.

```javascript
db.collection.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $in: ["#MembershipDeals", "$tag"]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]