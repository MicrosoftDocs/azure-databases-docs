---
title: $toObjectId
titleSuffix: Overview of the $toObjectId operator in Azure Cosmos DB for MongoDB vCore
description: The $toObjectId operator in Azure Cosmos DB for MongoDB vCore converts an expression into an ObjectId
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $toObjectId 

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$toObject` operator converts a specified string value into an ObjectId.

## Syntax

The syntax for the `$toObject` operator is:

```mongodb
{ "$toObject": <expression> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The specified string value to convert into an ObjectId|

## Examples

### Example 1: Convert the first 24 alphanumeric characters in the _id field into an ObjectId value

This query removes all occurrences of the "-" character and takes the first twenty four characters in the _id field and converts the result into an ObjectId. The ObjectId operator must strictly have a string of length twenty four with only alphanumeric characters.

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "idAsObjectId": {
            "$toObjectId": {
                "$substr": [
                    {
                        "$replaceAll": {
                            "input": "$_id",
                            "find": "-",
                            "replacement": ""
                        }
                    }, 0, 24]
            }
        }
    }
}])
```

This results in the following output:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "idAsObjectId": "ObjectId('b010763193704acdaafa8ac3')"
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$type to determine the BSON type of a value]($type.md)
- [$toInt to convert a value to a String type]($tostring.md)
