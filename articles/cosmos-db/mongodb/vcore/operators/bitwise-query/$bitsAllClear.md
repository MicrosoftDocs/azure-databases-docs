---
title: $bitsallclear bitwise query object expression in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $bitsallclear operator is used to match documents where all the bit positions specified in a bitmask are clear.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 11/01/2024
---

# $bitsAllClear  as bitwise query operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bitsAllClear` operator is used to match documents where all the bit positions specified in a bitmask are clear (that is, 0). This operator is useful in scenarios where you need to filter documents based on specific bits being unset in a binary representation of a field.

## Syntax

The syntax for the `$bitsAllClear` operator is as follows:

```javascript
{
  <field>: {
    $bitsAllClear: <bitmask>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field in the document to be evaluated. |
| **`count`** | A bitmask where each bit position specifies the corresponding bit position in the field's value that must be clear (0). |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
