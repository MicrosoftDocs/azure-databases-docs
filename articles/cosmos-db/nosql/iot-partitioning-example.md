---
title: Choosing a partition key for a real-world IoT application
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to choose a partition key for a real-world IoT application.
author: tarabhatia
ms.author: tarabhatia
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: conceptual
ms.date: 11/04/2024
---

# Choosing a Partition Key for an IoT Application Using Azure Cosmos DB

In this guide, we walk through a real-world scenario demonstrating how to select a partition key for an IoT application using Azure Cosmos DB. Through this use case, we’ll see how partition key choices affect data distribution, query performance, and overall application efficiency. We’ll explore how to evaluate different partitioning strategies based on the unique requirements of an IoT system and apply best practices for optimizing Cosmos DB performance.

## Scenario Overview

Imagine an IoT application that collects environmental data from thousands of IoT devices placed across various urban zones. Each device measures parameters like temperature, humidity, air quality, and noise levels every minute. The data collected is used for real-time monitoring and historical analysis to improve city planning and quality of life.

**Workload details:**

-	**Devices**: 50,000 sensors across 10 districts
-	**Data collected**: Each device logs data every minute, generating around 72 million records per day.
-	**Data retained**: We’d like to keep the data for 1 year for historical analysis and then delete the data. 
-	**Typical queries**: 
     - Real-time readings for specific devices or districts over the past month
     - Average temperature readings for devices or districts over the past month
     - Aggregate noise levels by district over specific time ranges

**Sample document:**
```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",      
    "districtId": "d12345",                           
    "deviceId": "s67890",
    "day": "2024-01-01"                             
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

## Step-by-step approach to choosing a partition key

**Identify access patterns**

In this scenario, we are logging data every minute, making it a write-heavy application. We do query for attributes like air quality index for a specific district, average temperature per district per month, and aggregate noise levels by district over time ranges to identify trends.

**Evaluate potential partition keys**

**DeviceId**
- **Pros:** This choice might work as it clusters data for each device onto the same logical partition and will distribute writes across many physical partitions since we have over 50K devices. Any queries for data from a specific device ID will be optimized because they can be scoped to the specific logical/physical partition it refers to, avoiding cross-partition queries.
- **Cons:** However, it is likely to run into the 20 GB data size logical partition key limit for a specific device over time since we are logging device data every minute. Once this occurs on Azure Cosmos DB, any future write operations will be blocked. Many of our queries will also be for specific districts, and partitioning by solely DeviceId will result in cross-partition queries, adding 2-3 RU/s for each physical partition we visit. 

Because we do not want stop write operations for device IDs once it reaches 20 GB of data, we should keep evaluating other options instead of using DeviceID as the final key. Moreover, there might be some different partitioning strategies to help us avoid cross partition queries.

**Time-based key (month, date, hour, etc.)**

The granularity of a time-based key directly impacts cardinality, and this comes with tradeoffs. For example, using a month-level granularity (e.g., 2024-12) limits the number of partition key values to 12 per year. This approach is not recommended, as it can lead to hot partitions---all writes for a given month would funnel into the same logical and physical partition.

Increasing granularity to a day-level key (e.g., 2024-12-18) spreads the data across more physical partitions. However, writes for a specific day still funnel into a single logical partition, potentially leading to hot partitions under heavy write loads.

For even finer granularity, a time-stamp-based key (e.g., 2024-12-18T10:00) includes the month, day, and time (down to the hour or minute). This approach reduces the likelihood of hot partitions and helps you stay within the 20 GB data limit per partition key value. However, the more granular the time-based key, the greater the likelihood of cross-partition queries when accessing data over broader time ranges.

**Choosing the right time-based key is a tradeoff:**

-   A more granular key avoids hitting the 20 GB partition limit but may result in increased cross-partition queries.
-   A less granular key reduces cross-partition queries but risks hot partitions and reaching the storage limit.

Your choice should align with your application's access patterns and data distribution needs. Since we're logging data every minute and want to avoid hitting the 20 GB limit, a time-based key that includes date/hour/minute granularity would work.

-   **Pros:** Since we are frequently querying for specific time periods to generate reports, using a time-based partition key could work since we can efficiently filter and retrieve data by specifying the partition key and scoping our queries to the specific physical partition. This would also help us periodically delete old data by deleting entire partitions that refer to old dates.
-   **Cons:** However, the biggest drawback of time-based partitioning in a write-heavy scenario, like an IoT system with continuous real-time data ingestion, is the risk of concentrating all writes for a specific time into a single partition. This can lead to throttling and poor performance. With 50K devices writing data simultaneously, all writes would funnel into the partition for the current data, month, and minute key, limiting throughput to that single partition's throughput while other partitions remain underutilized. This creates a bottleneck that restricts overall write scalability.

We don't want to run into hot partitions, and with solely partitioning using a time-based key we will inevitably run into this since we'd be writing to one logical partition during all of our write operations. Let's explore other options to see if we can avoid this.

**Synthetic Keys: DeviceId + Time-based-key (Date + Hour + Minute)**

-   **Pros:** By using a synthetic key that combines device ID and a time-based key with date/hour/minute granularity, writes are distributed across multiple logical partitions. This approach prevents all device data from being concentrated in a single logical and physical partition, as happens when partitioning solely by a time-based key. Instead, the inclusion of the device ID ensures writes are spread across many logical partitions, which are then mapped to multiple physical partitions, improving scalability and reducing the risk of hot partitions. We are also less likely to run into the 20 GB logical partition limit since we're adding a time-based key as a second property in the key.
-   **Cons:** Many of our queries filter only by DeviceId and/or DistrictId. With a synthetic key, this would result in a cross-partition query, leading to higher RU costs (an additional 2-3 RUs per physical partition scanned). Since the partition key is a combination of DeviceId and Date/Hour/Minute, Azure Cosmos DB cannot route the query to a single partition based on specifying the DeviceId alone. Moreover, anytime we query for a District Id, this would result in a cross-partition query as well.

While this partition key helps us surpass the 20 GB limit, our frequent queries for specific Device ID data make hierarchical partition keys a better fit. Hierarchical keys not only bypass the 20 GB limit but also add second and third levels of granularity, enabling queries to target only the relevant physical partitions. This avoids the fan-out costs associated with synthetic keys and improves query efficiency.

**Hierarchical Partition Key: DeviceId + Time-based-key (Date + Hour + Minute)**

-   **Pros:** By using a hierarchical partition key, we can surpass the 20 GB data limit per DeviceId as each logical partition is uniquely defined by a combination of DeviceId and Timestamp. Documents with the same DeviceId (first-level key) will be collocated on the same physical partition, minimizing fan-out costs that would have occurred with a synthetic key combining these two properties.
-   **Cons:** While our queries by DeviceId avoid fan-out charges with this selection, Azure Cosmos DB charges customers 2-3 RU/s for each physical partition when doing queries by District Id or any other property that we have not partitioned by.

At first glance, using DistrictId as the first level of a hierarchical partition key might seem like a good choice to ensure all queries are scoped to the correct physical partition. However, in this scenario, DistrictId has very low cardinality (only 10 unique values), which makes it a poor fit.

A hierarchical partition key with a low-cardinality first level is not recommended because it restricts data ingestion to a limited number of physical partitions. This bottleneck significantly reduces the overall throughput your workload can utilize, leading to suboptimal performance and potential hot partitions under heavy write loads.

To optimize queries that filter by DistrictId and avoid cross-partition queries, consider implementing a **materialized view**. This approach enables efficient queries on the base container without requiring a filter on the original partition key.

To prevent hitting the 20 GB limit per DistrictId, the materialized view should use a **hierarchical partition key**, with DistrictId as the first level and a more granular key, such as ID or a time-based value, as the second level. This ensures data is evenly distributed and avoids storage limitations while maintaining query efficiency for district-specific data.

## Final partition key choice: DeviceId + Time-based-key (Date + Hour + Minute) ##

After considering several partition key options for our IoT system, using a hierarchical partition key with DeviceId as the first-level key and Time-based-key as the second-level key seems like the best choice. This approach offers the best balance between even data distribution and query efficiency for our use case.

We ruled out DeviceId as a standalone partition key due to the high risk of exceeding the 20 GB limit per logical partition, given the frequent data ingestion from over 50K devices. Similarly, time-based partitioning would concentrate all writes for the current time period into a single partition, creating performance bottlenecks.

By using DeviceId +Time-based-key (Date + Hour + Minute)as an HPK, we can:

-   Distribute writes efficiently across physical partitions, reducing the likelihood of hot partitions.
-   Avoid the 20 GB data size limit per partition by using multiple levels of partitioning, allowing us to scale as needed. We recommend always adding ID as the last level of your hierarchical partition key to ensure you never reach the 20 GB limit.
-   Optimize our most common query patterns that frequently filter by DeviceId and Date/Hour/Minute, minimizing cross-partition queries and reducing RU costs.
-   Utilize materialized view with DistrictId + ID as the first and second level keys to optimize our queries by DistrictId
