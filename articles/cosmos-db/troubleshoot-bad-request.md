---
title: Troubleshoot Azure Cosmos DB Bad Request Exceptions
description: Learn how to diagnose and fix bad request exceptions such as input content or partition key is invalid, partition key doesn't match in Azure Cosmos DB.
author: ealsur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.date: 07/17/2025
ms.author: maquaran
ms.topic: troubleshooting
---

# Diagnose and troubleshoot bad request exceptions in Azure Cosmos DB
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

The HTTP status code 400 indicates that the request contains invalid data or is missing required parameters.

## <a name="missing-id-property"></a>Missing the ID property

In this scenario, it's common to see the error:

  "The input content is invalid because the required properties - 'id; ' - are missing"

A response with this error means the JSON document that is being sent to the service lacks the required ID property.

### Solution

Specify an `id` property with a string value as per the [REST specification](/rest/api/cosmos-db/documents) as part of your document, The SDKs don't autogenerate values for this property.

## <a name="invalid-partition-key-type"></a>Invalid partition key type

In this scenario, it's common to see errors like:

  "Partition key ... is invalid"

A response with this error means the partition key value is an invalid type.

### Solution

The value of the partition key should be a string or a number. Make sure the value is of the expected types.

## <a name="wrong-partition-key-value"></a>Wrong partition key value

In this scenario, it's common to see these errors:

  "Response status code does not indicate success: BadRequest (400); Substatus: 1001"

  "PartitionKey extracted from document doesn’t match the one specified in the header"

A response with this error means you're executing an operation and passing a partition key value that doesn't match the document's body value for the expected property. If the collection's partition key path is `/myPartitionKey`, the document has a property called `myPartitionKey` with a value that doesn't match what was provided as partition key value when calling the SDK method.

### Solution

Send the partition key value parameter that matches the document property value.

## Numeric partition key value precision loss

In this scenario, it's common to see errors like:

  "The requested partition key is out of key range, possibly because of loss of precision of partition key value"

A response with this error is likely caused by an operation on a document with a numeric partition key whose value is outside what Azure Cosmos DB supports. For the maximum length of numeric property value, see [Per-item limits](/azure/cosmos-db/concepts-limits#per-item-limits).

### Solution

Consider using type `string` for the partition key if you require precise numeric values.

## Next steps

* [Diagnose and troubleshoot issues when using Azure Cosmos DB .NET SDK](troubleshoot-dotnet-sdk.md)
* Learn about performance guidelines for [.NET v3](performance-tips-dotnet-sdk-v3.md) and [.NET v2](performance-tips.md)
* [Troubleshoot issues when you use Azure Cosmos DB Java SDK v4 with API for NoSQL accounts](troubleshoot-java-sdk-v4.md)
* [Performance tips for Azure Cosmos DB Java SDK v4](performance-tips-java-sdk-v4.md)
