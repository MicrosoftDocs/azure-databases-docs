---
title: Troubleshoot HTTP 408 or request time out issues with the Java v4 SDK
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to diagnose and fix Java SDK request time out exceptions with the Java v4 SDK.
author: kushagrathapar
ms.author: kuthapar
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: troubleshooting
ms.date: 04/03/2025
ms.custom: devx-track-extended-java
appliesto:
  - ✅ NoSQL
---

# Diagnose and troubleshoot Azure Cosmos DB for NoSQL Java v4 SDK request time out exceptions

The HTTP 408 error occurs if the software development kit (SDK) was unable to complete the request before the time out limit occurred.

## Troubleshooting steps

The following list contains known causes and solutions for request time out exceptions. 

### End-to-end time out policy

There are scenarios where 408 network time out errors occurs even when all preemptive solutions here are implemented. A general best practice for reducing tail latency, and improving availability in these scenarios, is to implement end-to-end time out policy. Tail latency is reduced by failing faster, and [request units](../request-units.md) and client-side compute costs are reduced by stopping retries after the time out. The time out duration can be set on `CosmosItemRequestOptions`. The options can then be passed to any request sent to Azure Cosmos DB for NoSQL:

```java
CosmosEndToEndOperationLatencyPolicyConfig endToEndOperationLatencyPolicyConfig = new CosmosEndToEndOperationLatencyPolicyConfigBuilder(Duration.ofSeconds(1)).build();

CosmosItemRequestOptions options = new CosmosItemRequestOptions();
options.setCosmosEndToEndOperationLatencyPolicyConfig(endToEndOperationLatencyPolicyConfig);

container.readItem("id", new PartitionKey("pk"), options, TestObject.class);
```

### Existing issues

If you're seeing requests getting stuck for longer duration or timing out more frequently, please upgrade the Java v4 SDK to the latest version. 
NOTE: We strongly recommend using the version 4.18.0 and above. Check out the [Java v4 SDK release notes](sdk-java-v4.md) for more details.

### High CPU utilization

High CPU utilization is the most common case. For optimal latency, CPU usage should be roughly 40 percent. Use `10` seconds as the interval to monitor maximum (not average) CPU utilization. CPU spikes are more common with cross-partition queries where it might do multiple connections for a single query.

#### Solution

The client application that uses the SDK should be scaled up or out.

### Connection throttling

Connection throttling can happen because of either a connection limit on a host machine or Azure source network address translation (SNAT) port exhaustion.

### Connection limit on a host machine

Some Linux systems, such as Red Hat, have an upper limit on the total number of open files. Sockets in Linux are implemented as files, so this number limits the total number of connections, too. Run the following command.

```bash
ulimit -a
```

#### Solution

The number of max allowed open files, which are identified as `nofile`, needs to be at least 10,000 or more. For more information, see the Azure Cosmos DB for NoSQL Java SDK v4 [performance tips](performance-tips-java-sdk-v4.md).

### Socket or port availability might be low

When your solution is running in Azure, clients using the Java SDK can hit Azure SNAT port exhaustion.

#### Solution 1

If you're running on Azure VMs, follow the [SNAT port exhaustion guide](troubleshoot-java-sdk-v4.md#snat).

#### Solution 2

If you're running on Azure App Service, follow the [connection errors troubleshooting guide](/azure/app-service/troubleshoot-intermittent-outbound-connection-errors#cause) and [use App Service diagnostics](https://azure.github.io/AppService/2018/03/01/Deep-Dive-into-TCP-Connections-in-App-Service-Diagnostics.html).

#### Solution 3

If you're running on Azure Functions, verify you're following the [Azure Functions recommendation](/azure/azure-functions/manage-connections#static-clients) of maintaining singleton or static clients for all of the involved services (including Azure Cosmos DB for NoSQL). Check the [service limits](/azure/azure-functions/functions-scale#service-limits) based on the type and size of your Function App hosting.

#### Solution 4

If you use an HTTP proxy, make sure it can support the number of connections configured in the SDK `GatewayConnectionConfig`. Otherwise, you face connection issues.

### Create multiple client instances

Creating multiple client instances might lead to connection contention and time out issues.

#### Solution 1

Follow the [performance tips](performance-tips-java-sdk-v4.md#sdk-usage), and use a single CosmosClient instance across an entire application.

#### Solution 2

If singleton `CosmosClient` isn't possible to have in an application, we recommend using connection sharing across multiple Azure Cosmos DB for NoSQL clients through this API `connectionSharingAcrossClientsEnabled(true)` in CosmosClient. 
When you have multiple instances of the client interacting with multiple accounts, enabling this setting allows connection sharing in **Direct** mode. This mode is only enabled if connection sharing is possible between instances of Azure Cosmos DB for NoSQL client. Note, when setting this sharing option, the connection configuration (for example, socket time out config, idle time out config) of the first instantiated client are used for all other client instances.

### Hot partition key

Azure Cosmos DB for NoSQL distributes the overall provisioned throughput evenly across physical partitions. When there's a hot partition, one or more logical partition keys on a physical partition are consuming all the physical partition's Request Units per second (RU/s). At the same time, the RU/s on other physical partitions are going unused. As a symptom, the total RU/s consumed are less than the overall provisioned RU/s at the database or container, but you still see throttling (429 errors) on the requests against the hot logical partition key. Use the [Normalized RU Consumption metric](../monitor-normalized-request-units.md) to see if the workload is encountering a hot partition. 

#### Solution

Choose a good partition key that evenly distributes request volume and storage. Learn how to [change your partition key](https://devblogs.microsoft.com/cosmosdb/how-to-change-your-partition-key/).

### High degree of concurrency

The application is doing a high level of concurrency, which can lead to contention on the channel.

#### Solution

The client application that uses the SDK should be scaled up or out.

### Large requests or responses

Large requests or responses can lead to head-of-line blocking on the channel and exacerbate contention, even with a relatively low degree of concurrency.

#### Solution

The client application that uses the SDK should be scaled up or out.

### Failure rate is within the Azure Cosmos DB for NoSQL service level agreement (SLA)

The application should be able to handle transient failures and retry when necessary. Any 408 exceptions aren't retried because on create paths it's impossible to know if the service created the item or not. Sending the same item again for create causes a conflict exception. User applications business logic might have custom logic to handle conflicts, which would break from the ambiguity of an existing item versus conflict from a create retry.

### Failure rate violates the Azure Cosmos DB for NoSQL SLA

Contact [Azure Support](https://aka.ms/azure-support).

## Related content

- [Diagnose and troubleshoot](troubleshoot-java-sdk-v4.md) issues when you use the Azure Cosmos DB for NoSQL Java v4 SDK.
- Learn about performance guidelines for [Java v4](performance-tips-java-sdk-v4.md).
