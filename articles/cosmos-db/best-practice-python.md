---
title: Best practices for Python SDK
description: Review a list of best practices for using the Azure Cosmos DB Python SDK in a performant manner.
author: kushagraThapar
ms.author: kuthapar
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: devx-track-python
ms.topic: best-practice
ms.date: 04/08/2024
appliesto:
  - ✅ NoSQL
---

# Best practices for Python SDK in Azure Cosmos DB for NoSQL

This guide includes best practices for solutions built using the latest version of the Python SDK for Azure Cosmos DB for NoSQL. The best practices included here helps improve latency, improve availability, and boost overall performance for your solutions.

## Account configuration

**Account configuration parameters**  
| Parameter | Default or constraint | When to use |
| --- | --- | --- |
| Region colocation | Same as app region | Reduce latency |
| Multi-region replication | Disabled by default | Enable 2+ regions for availability |
| Service-managed failover | Optional | Enable for production workloads |

```python
from azure.cosmos import CosmosClient
client = CosmosClient(url, credential)
print(client.client_connection._global_endpoint_manager.write_endpoint)
# Expected: write endpoint resolves to configured write region
```

For more information on how to add multiple regions using the Python SDK, see the [global distribution tutorial](tutorial-global-distribution.md).

## SDK usage

**SDK usage parameters**  
| Parameter | Default or constraint | When to use |
| --- | --- | --- |
| SDK version | Latest available | Always for optimal performance |
| CosmosClient instance | One per app | Reuse for lifetime of app |
| preferred_locations | None | Optimize reads and failover |

```python
client = CosmosClient(
    url,
    credential,
    preferred_locations=["East US", "West US"]
)
print(client.client_connection._preferred_locations)
# Expected: ['East US', 'West US']
```

A transient error is an error that has an underlying cause that soon resolves itself. Applications that connect to your database should be built to expect these transient errors. To handle them, implement retry logic in your code instead of surfacing them to users as application errors. The SDK has built-in logic to handle these transient failures on retryable requests like read or query operations. The SDK can't retry on writes for transient failures as writes aren't idempotent. The SDK does allow users to configure retry logic for throttles. For details on which errors to retry on, see [resilient application guidance](conceptual-resilient-sdk-applications.md#should-my-application-retry-on-errors).

Use SDK logging to [capture diagnostic information](troubleshoot-python-sdk.md#logging-and-capturing-the-diagnostics) and troubleshoot latency issues.

## Data design

**Data design parameters**  
| Parameter | Default or constraint | When to use |
| --- | --- | --- |
| Document size | N/A | Keep small to reduce RU cost |
| Identifier characters | No special chars | Avoid unexpected behavior |
| Indexing paths | All paths indexed | Exclude unused paths for faster writes |

```python
container_properties = {
    "id": "items",
    "indexingPolicy": {
        "excludedPaths": [{"path": "/*"}]
    }
}
print(container_properties["indexingPolicy"])
# Expected: excludedPaths configured
```

For more information, see [creating indexes using the SDK sample](performance-tips-python-sdk.md#indexing-policy).

## Host characteristics

**Host characteristics parameters**  
| Parameter | Default or constraint | When to use |
| --- | --- | --- |
| CPU utilization | <70% recommended | Scale up or out if high |
| Accelerated Networking | Disabled | Enable on VMs for high traffic |
| Query page size | 100 items / 4 MB | Increase to reduce round trips |

```python
items = container.query_items(
    query="SELECT * FROM c",
    max_item_count=500
)
print("Page size set to 500")
# Expected: fewer round trips
```

## Next steps
To learn more about performance tips for Python SDK, see [Performance tips for Azure Cosmos DB Python SDK](performance-tips-python-sdk.md).

To learn more about designing your application for scale and high performance, see [Partitioning and scaling in Azure Cosmos DB](partitioning-overview.md).

Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
* If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md) 
* If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)
