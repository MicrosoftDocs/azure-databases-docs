---
title: Choose a partition key for a real-world IoT application
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to choose a partition key for a real-world IoT application.
author: richagaur
ms.author: richagaur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 03/24/2025
appliesto:
  - ✅ NoSQL
---

# Choose a partition key for IoT workloads

In this guide, we walk through a real-world scenario demonstrating how to select a partition key for an IoT application using Azure Cosmos DB. Through this use case, we see how partition key choices affect data distribution, query performance, and overall application efficiency. We explore how to evaluate different partitioning strategies based on the unique requirements of an IoT system and apply best practices for optimizing Azure Cosmos DB performance.

## Scenario overview

Imagine an IoT application that collects environmental data from thousands of IoT devices placed across various urban zones. Each device measures parameters like temperature, humidity, air quality, and noise levels every second. The data collected: Each device logs data every second, generating around 4.32 billion records per day across 50,000 devices.


**Workload Details:**

-	**Devices**: 50,000 sensors across 10 districts
-	**Data collected**: Each device logs data every second, generating 4.32 billion records per day.
-	**Typical queries**: 
     - Real-time readings for specific devices 


**Sample Document:**
```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",      
    "districtId": "d12345",                           
    "deviceId": "s67890",
    "day": "2024-01-01",
    "timestamp": "2024-01-01T08:30",              
    "temperature": 22.5,                              
    "humidity": 55.2,                                 
    "airQualityIndex": 42,                            
    "noiseLevel": 35,                                 
    "location": {
        "latitude": 37.7749,                          
        "longitude": -122.4194                        
    },
    "batteryLevel": 88,                              
    "status": "active"                              
}
```
**Access Pattern:**
In this scenario, we're' logging data every second, making it a write-heavy application. We'd like to optimize our partitioning strategy for ingesting data at high throughput. 

For real-time analytics (for example, aggregating device data across districts), we can explore [Azure Synapse Link](synapse-link.md).

## Recommended partitioning strategy

### Hierarchical partition key

It's important to note that Azure Cosmos DB limits the data per logical partition to 20-GB. In our scenario, each device is logging data per second. On average, our document size is around 1 KB, so we're guaranteed to hit the 20-GB data limit per device ID during the year by partitioning by device ID alone. 

To ensure that we never run into the 20-GB data limit for any of our device IDs, we can use [hierarchical partition keys](hierarchical-partition-keys.md). We can set the following two levels:

- **First Level**: DeviceId (*for example "s67890"*)
- **Second Level**: Timestamp (*for example "2024-01-01T08:30"*)



By using a hierarchical partition key, we can surpass the 20-GB data limit per device ID as each logical partition is uniquely defined by a combination of DeviceId and Timestamp (date/hour/minute, in this case). Documents with the same DeviceId (first-level key) are collocated on the same physical partition, minimizing fan-out costs for queries by DeviceId that would occur with a synthetic key combining these two properties.

> [!NOTE] 
>We use the timestamp as the second-level partition key because each device will always generate less than 20 GB of data per minute. However, if your workload has the potential to exceed 20-GB of data per minute, **using the property Id (or another property that is a GUID) as the second level key** ensures that your workload remains within the 20-GB limit per device ID. This approach guarantees that writes won't be blocked due to partition size limits.

> [!IMPORTANT]
> In this scenario, device ID has 50,000 unique values. A hierarchical partition key with a low-cardinality first level is **not recommended** because it restricts data ingestion to a limited number of physical partitions. This bottleneck significantly reduces the overall throughput your workload can utilize, leading to suboptimal performance and potential hot partitions under heavy write loads.

While this strategy is recommended, let's also take a look at other potential options customers often consider and their trade-offs. 

## Other potential partition keys and tradeoffs

### Device ID


- **Pros:** This choice might work as it clusters data for each device onto the same logical partition and will distribute writes across many physical partitions since we have over 50,000 devices. Any queries for data from a specific device ID are optimized. Now, they can be scoped to the specific logical/physical partition it refers to, avoiding cross-partition queries.

- **Cons:** Since we're logging device data every second, a single device generates ~31,536,000 records per year. Let's assume that our document size is around 1 KB. The total data size for one year for one device is around 30-GB. By partitioning by device ID, our workload is guaranteed to run into the 20-GB data size logical partition key limit for a specific device in around five months. Once this occurs on Azure Cosmos DB, any future write operations are blocked. Many of our queries will also be for specific districts, and partitioning by solely device ID will result in cross-partition queries, adding 2-3 RU/s for each physical partition we visit. 

Because we do not want stop write operations for device IDs once it reaches 20-GB of data, we should **not** be using device ID as the final key. In cases where we're 100% confident that we would never run into the 20-GB limit, using device ID as the partition key is fine. However, it is safer to use a hierarchical partition key with the second level key being a GUID or another high cardinality value because it is a 100% guarantee that we will never hit the 20-GB limit. 

### Time-based key (month, date, hour, etc.)

The granularity of a time-based key directly impacts cardinality, and this comes with tradeoffs. For example, using a month-level granularity (for example, 2024-12) limits the number of partition key values to 12 per year. This approach is **not** recommended, as it will lead to hot partitions, impacting workload performance. 

For example, let's say our workload is provisioned with 100,000 RU/s and we have 10 physical partitions that can use up to 10K RU/s each. By partitioning our workload with a time-based key which only includes the month, all writes for the month would funnel into the same logical and physical partition, limiting our overall throughput to just 10K RU/s, rather than the 100K we have provisioned.

Increasing granularity to a day-level key (for example, 2024-12-18) spreads our data across many physical partitions, but writes for a specific day still funnel into a single logical partition, leading to hot partitions under heavy write loads. In addition to hot partitions, the workload is guaranteed to hit the 20-GB logical partition limit by using this key since **all** device data would funnel into the same logical partition, and each device ID alone is guaranteed to hit the 20-GB limit. 

For even finer granularity, a time-stamp-based key (for example, 2024-12-18T10:00) includes the month, day, and time (down to the hour or minute). This approach reduces the likelihood of hot partitions and helps you stay within the 20-GB data limit per partition key value. However, the more granular the time-based partition key, the higher the likelihood of cross-partition queries when accessing data over broader time ranges. 

For example, querying all device data for a specific day or month will result in cross-partition queries because the data is distributed across multiple logical partitions. Since the partition key includes the full path (for example, month, date, hour, and minute), the data for a single day is spread across different logical and multiple physical partitions. So, querying for all data within a specific day requires accessing multiple physical partitions to retrieve the complete dataset.

> [!IMPORTANT]
>**Time-based partition keys are not recommended:**
>-   A more granular time-based key avoids hitting the 20-GB partition limit but may result in increased cross-partition queries if we query for broader time ranges (like device data for a specific date).
>-   A less granular key reduces cross-partition queries on date, but risks hot partitions and reaching the 20-GB storage limit.

Your choice should align with your application's access patterns and data distribution needs. We do not want to run into hot partitions, and by partitioning solely on a time-based key we will inevitably run into this since our workload would be writing to one logical partition during all of our write operations. 

### Synthetic Key: DeviceId + Time-based-key (Date + Hour + Minute)

-   **Pros:** By using a [synthetic key](synthetic-partition-keys.md) that combines device ID and a time-based key with date/hour/minute granularity, writes are distributed across multiple logical partitions. This approach prevents all device data from being concentrated in a single logical and physical partition, as happens when partitioning solely by a time-based key. Instead, the inclusion of the device ID ensures writes are spread across many logical partitions, which are then mapped to multiple physical partitions, improving scalability and reducing the risk of hot partitions. We are also less likely to run into the 20-GB logical partition limit since we're adding a time-based key as a second property in the key.

-   **Cons:** Many of our queries filter only by DeviceId. With a synthetic key, this would result in a cross-partition query, leading to higher RU costs (an additional 2-3 RUs per physical partition scanned). Since the partition key is a combination of DeviceId and Date/Hour/Minute, Azure Cosmos DB cannot route the query to a single partition based on specifying the DeviceId alone.

While this partition key helps us surpass the 20-GB limit, our frequent queries for specific Device ID data make hierarchical partition keys a better fit. Hierarchical partition keys not only bypass the 20-GB limit, but also add second and third levels of granularity, enabling queries to target only the relevant physical partitions. This avoids the fan-out costs associated with synthetic keys and improves query efficiency.

## Final partition key choice

After considering several partition key options for our IoT system, using a hierarchical partition key with DeviceId as the first-level key and Time-based-key as the second-level key seems like the best choice. This approach offers the best balance between even data distribution and query efficiency for our use case.

We ruled out DeviceId as a standalone partition key due to the high risk of exceeding the 20-GB limit per logical partition, given the frequent data ingestion from over 50K devices. Similarly, time-based partitioning would concentrate all writes for the current time period into a single partition, creating performance bottlenecks.

By using DeviceId +Time-based-key (Date + Hour + Minute) as a hierarchical partition key, we can:

-   Distribute writes efficiently across physical partitions, reducing the likelihood of hot partitions.
-   Avoid the 20-GB data size limit per logical partition by using multiple levels of partitioning, allowing us to scale as needed. 
> [!TIP]
> - We recommend  adding ID as the last level of your hierarchical partition key to ensure you never reach the 20-GB limit for a logical partition key.
-   Optimize our most common query patterns that frequently filter by DeviceId and Date/Hour/Minute, minimizing cross-partition queries and reducing RU costs.

For more information on how partitioning works in Azure Cosmos DB, you can learn more [here](partitioning-overview.md).
