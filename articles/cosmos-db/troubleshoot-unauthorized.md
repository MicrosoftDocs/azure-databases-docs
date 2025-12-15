---
title: Troubleshoot Unauthorized Exceptions
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to diagnose and fix Azure Cosmos DB unauthorized exceptions. Get solutions and troubleshooting steps.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 08/20/2025
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
---

# Diagnose and troubleshoot Azure Cosmos DB for NoSQL unauthorized exceptions

Unauthorized exceptions in Azure Cosmos DB for NoSQL, such as HTTP 401 errors, typically occur when the MAC signature in the request doesn't match the expected value. Incorrect keys, incomplete key rotations, or using read-only keys for write operations are often causes of this error message.

## Symptoms

A common symptom of unauthorized exceptions is receiving an HTTP 401 error message. This error indicates that the request wasn't properly authenticated.

```output
HTTP 401: The MAC signature found in the HTTP request isn't the same as the computed signature.
```

For older software development kits (SDKs), the exception might appear as an invalid JSON exception instead of the correct 401 unauthorized exception. Newer SDKs handle this scenario and show a valid error message.

## Cause

This error occurs when the authentication signature (MAC) in your request doesn't match what Azure Cosmos DB expects. Common reasons include using the wrong key, incomplete key rotation, or trying to perform write operations with a read-only key. This mismatch prevents Cosmos DB from verifying your identity, resulting in an HTTP 401 unauthorized error.

## Solution: Wait for key rotation to complete

Apply this solution if you encounter 401 MAC signature errors immediately after rotating your account keys. Key rotation in Azure Cosmos DB can take anywhere from a few seconds to several days, depending on the account size.

Ensure your application waits until the key rotation process is fully completed before using the new key for authentication. The error should resolve automatically once the rotation is finished.

## Solution: Fix misconfigured keys

Use this solution if you consistently receive 401 MAC signature errors for all requests using a particular key. This scenario usually means the key is incorrect or incomplete in your application configuration.

Verify that the key in your application matches the correct account key and ensure the entire key is copied without truncation.

## Solution: Use read/write keys for write operations

Apply this solution if 401 MAC signature errors only occur during write operations, while read requests succeed. This scenario indicates the application is using read-only keys for write actions.

Update your application to use a read/write key or an authorization mechanism with write access for all write operations.

## Solution: Wait for container creation to complete

Choose this solution if 401 MAC signature errors appear immediately after creating a container, especially when containers are deleted and re-created with the same name.

Ensure your application waits until the container creation process is fully completed before attempting to access or perform operations on the container.

## Related content

* [Diagnose and troubleshoot](troubleshoot-dotnet-sdk.md) issues when you use the Azure Cosmos DB .NET SDK.
* Learn about performance guidelines for [.NET v3](performance-tips-dotnet-sdk-v3.md) and [.NET v2](performance-tips.md).
* [Diagnose and troubleshoot](troubleshoot-java-sdk-v4.md) issues when you use the Azure Cosmos DB Java v4 SDK.
* Learn about performance guidelines for [Java v4 SDK](performance-tips-java-sdk-v4.md).