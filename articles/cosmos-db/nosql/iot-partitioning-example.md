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

# Choosing a partition key for IoT workloads

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This guide walks you through a real-world scenario that illustrates the selection of partition keys in an IoT application using Azure Cosmos DB. By examining a specific use case, we’ll explore how the choice of partition key can significantly impact data distribution, query performance, and overall application efficiency. You’ll see step-by-step how to assess the unique requirements of your IoT solution, choose the appropriate partition key, and apply best practices to optimize your Cosmos DB setup. This guide aims to provide practical insights and actionable strategies that will help you effectively manage your IoT data and scale your application as needed.

## The scenario

 Imagine a IOT application that collects environmental data from thousands of IoT devices placed across various urban zones. Each device measures parameters like temperature, humidity, air quality, and noise levels every minute. The data collected is used for real-time monitoring, historical analysis, and predictive modeling to improve city planning and quality of life. 


**Workload details:**

-	**Devices**: 50,000 sensors spread across multiple districts within the city 
-	**Data collected**: Each device logs data every minute, generating around 72 million records per day.
-	**Data retained**: We’d like to keep the data for 1 year for historical analysis and then delete the data. 
-	**Typical queries**: 
     - Real-time air quality in a specific district
    - Average temperature readings for a specific device or a district over the past month
    - Aggregated noise levels by district or for specific time ranges to identify noise pollution trends

**Sample document:**
```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",      
    "districtId": "d12345",                           
    "deviceId": "s67890",
    "day": "2024-01-01"                             
    "timestamp": "2024-01-01T08:30:00Z",              
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
- **Cons:** However, it is very likely to run into the 20 GB data size logical partition key limit for a specific device since we are logging device data every minute. Once this occurs on Azure Cosmos DB, any future writes will be blocked. 

**DistrictId**

- **Pros:** If the number of districts is evenly distributed, this could be an option. Because we frequently filter for specific district IDs in our access patterns, partitioning by DistrictId would help optimize those queries as we would scope to just the logical/physical partition we are looking for. 

- **Cons:** There is a risk of running into hot partitions if some districts have significantly more devices than others. We are also likely to run into the 20 GB data size logical partition limit.

**Time-based (timestamp or day)**

- **Pros:** Since we are frequently querying for specific time periods to generate reports, partitioning by time could work since we can efficiently filter and retrieve data by specifying the partition key and scoping our queries to the specific physical partition. This would also help us periodically delete old data by deleting entire partitions that refer to old dates.
 
- **Cons:** However, the biggest drawback of time-based partitioning in a write-heavy scenario, like an IoT system with continuous real-time data ingestion, is the risk of concentrating all writes for a specific time period (e.g., day or timestamp) into a single partition. This can lead to throttling and poor performance. With 50K devices writing data simultaneously, all writes would funnel into the partition for the current time, limiting throughput to that single partition's throughput while other partitions remain underutilized. This creates a bottleneck that restricts overall write scalability.

**DistrictId + DeviceId (synthetic key)**

- **Pros:** By combining DistrictId and DeviceId into a synthetic key, data from different devices across various districts will be distributed across multiple physical partitions. This reduces the risk of hot partitions and ensures balanced write distribution in a write-heavy workload. Additionally, the risk of exceeding the 20 GB limit per logical partition is minimized since each unique combination of DistrictId and DeviceId creates a distinct logical partition. Writes will only be blocked if a specific DistrictId + DeviceId combination exceeds the 20 GB limit.

- **Cons:** Many of our queries filter only by DistrictId. With a synthetic key, this would result in a cross-partition query, leading to higher RU costs (an additional 2-3 RUs per physical partition scanned). Since the partition key is a combination of DistrictId and DeviceId, Azure Cosmos DB cannot route the query to a single partition based on DistrictId alone.

**DistrictId + DeviceId (HPK)**

- **Pros:** Using DistrictId as the first level and DeviceId as the second level in a hierarchical partition key allows us to go beyond the 20 GB limit per district. We can even add a third level of partitioning (e.g., the document’s default ID property) if necessary to ensure we never exceed the data size limit per district and device. Moreover, since many of our queries filter by DistrictId, hierarchical partition keys help narrow the query scope to specific physical partitions associated with the DistrictId. This reduces the fan-out costs that would occur with a synthetic key.

- **Cons:** The first-level partition key must have high cardinality to ensure good data distribution. In this case, DistrictId has high cardinality, and it's included in all of our query patterns, making it an appropriate choice. However, if DistrictId had low cardinality or if we primarily queried by DeviceId, it would be better to select DeviceId as the first-level key. It’s crucial that the first-level partition key has high cardinality and is included in most queries to avoid performance bottlenecks.

## Final partition key choice ##

After considering several partition key options for our IoT system, using a hierarchical partition key with DistrictId as the first-level key and DeviceId as the second-level key seems like the best choice. This approach offers the best balance between even data distribution and query efficiency for our use case.

We ruled out DeviceId as a standalone partition key due to the high risk of exceeding the 20 GB limit per logical partition, given the frequent data ingestion from over 50K devices. Similarly, DistrictId alone could lead to hot partitions if some districts have significantly more devices than others, and time-based partitioning would concentrate all writes for the current time period into a single partition, creating performance bottlenecks.

By using DistrictId + DeviceId as an HPK, we can:

- Distribute writes efficiently across physical partitions, reducing the likelihood of hot partitions.
- Avoid the 20 GB data size limit per partition by using multiple levels of partitioning, allowing us to scale as needed.
- Optimize our most common query patterns that frequently filter by DistrictId, minimizing cross-partition queries and reducing RU costs.

This hierarchical structure also gives us the flexibility to add additional partitioning levels (e.g., default ID property) if our data continues to grow, ensuring long-term scalability while supporting both write-heavy workloads and efficient query performance.
