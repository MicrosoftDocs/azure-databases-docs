---
title: Troubleshoot Service Unavailable Exceptions
description: Learn how to diagnose and fix Azure Cosmos DB service unavailable exceptions.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 07/18/2025
appliesto:
  - ✅ NoSQL
---

# Diagnose and troubleshoot Azure Cosmos DB service unavailable exceptions

This article explains how to troubleshoot when the SDK can't connect to Azure Cosmos DB. This scenario can be transient or permanent depending on the network conditions.

It's important to make sure the application design follows our [guide for designing resilient applications with Azure Cosmos DB SDKs](conceptual-resilient-sdk-applications.md) to make sure it correctly reacts to different network conditions. Your application should have retries in place for service unavailable errors.

When evaluating the case for service unavailable errors:

* What is the effect measured in volume of operations affected compared to the operations succeeding? Is it within the service SLAs?
* Is the P99 latency or availability affected?
* Are the failures affecting all your application instances or only a subset? When the issue is reduced to a subset of instances, it's commonly a problem related to those instances.

## Troubleshooting steps

The following list contains known causes and solutions for service unavailable exceptions.

### Verify the substatus code

In certain conditions, the HTTP 503 "Service Unavailable" error includes a substatus code that helps to identify the cause.

| Substatus code | Description |
|----------|-------------|
| 20001 | The service unavailable error happened because there are client side [connectivity issues](#client-side-transient-connectivity-issues) (failures attempting to connect). The client attempted to recover by [retrying](conceptual-resilient-sdk-applications.md#timeouts-and-connectivity-related-failures-http-408503) but all retries failed. |
| 20002 | The service unavailable error happened because there are client side [timeouts](troubleshoot-dotnet-sdk-request-time-out.md#troubleshooting-steps). The client attempted to recover by [retrying](conceptual-resilient-sdk-applications.md#timeouts-and-connectivity-related-failures-http-408503) but all retries failed. |
| 20003 | The service unavailable error happened because there are underlying I/O errors related to the operating system. See the exception details for the related I/O error. |
| 20004 | The service unavailable error happened because [client machine's CPU is overloaded](troubleshoot-dotnet-sdk-request-time-out.md#high-cpu-utilization). |
| 20005 | The service unavailable error happened because client machine's thread pool is starved. Verify any potential [blocking async calls in your code](https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md#avoid-using-taskresult-and-taskwait). |
| 20006 | The connection between the service and client was interrupted or terminated in an unexpected manner. |
| >= 21001 | This service unavailable error happened due to a transient service condition. Verify the conditions in the previous section, and confirm if you have retry policies in place. If the volume of these errors is high compared with successes, reach out to Azure Support. |

### The required ports are being blocked

Verify that all the [required ports](sdk-connection-modes.md#service-port-ranges) are enabled.

### Client-side transient connectivity issues

Service unavailable exceptions can surface when there are transient connectivity problems that are causing timeouts and can be safely retried following the [design recommendations](conceptual-resilient-sdk-applications.md#timeouts-and-connectivity-related-failures-http-408503).

To resolve them, follow the [request timeout troubleshooting steps](troubleshoot-dotnet-sdk-request-time-out.md#troubleshooting-steps).

### Service outage

Check the [Azure status](https://azure.status.microsoft/status) to see if there's an ongoing issue.

## Next steps

* [Diagnose and troubleshoot issues when using Azure Cosmos DB .NET SDK](troubleshoot-dotnet-sdk.md)
* [Troubleshoot issues when you use Azure Cosmos DB Java SDK v4 with API for NoSQL accounts](troubleshoot-java-sdk-v4.md)
* [Performance tips for Azure Cosmos DB and .NET](performance-tips-dotnet-sdk-v3.md)
* [Performance tips for Azure Cosmos DB Java SDK v4](performance-tips-java-sdk-v4.md)
