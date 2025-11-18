---
title: Fleet Analytics Schema Reference (Preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Get answers to frequently asked questions about Azure Cosmos DB fleets, fleetspaces, and fleetspace accounts.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.date: 05/07/2025
appliesto:
- ✅ NoSQL
ms.custom:
  - build-2025
---

# Fleet analytics schema reference (preview)

[!INCLUDE[Preview](includes/notice-preview.md)]

These tables document the entire schema of the data exposed by Azure Cosmos DB fleet analytics.

## Dimension tables

### DimResource

| | Description |
| --- | --- |
| **`ResourceId` *(PK)*** | A unique identifier for the resource. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`SubscriptionId` *(NK)*** | A unique identifier for the subscription with which the record is associated. |
| **`AccountName`** | The name of the Azure Cosmos DB database account. |
| **`Region`** | The Azure region associated with this resource. |
| **`DatabaseName`** | The name of the Azure Cosmos DB database. |
| **`CollectionName`** | The name of the Azure Cosmos DB collection. |
| **`ResourceType`** | Type of resource. Values can be: `Account`, `Database`, or `Collection`. |

### DimFleet

| | Description |
| --- | --- |
| **`FleetId` *(PK)*** | A unique identifier for the fleet. |
| **`FleetName`** | The name of the fleet. |

### DimRegion

| | Description |
| --- | --- |
| **`Region` *(PK)*** | The Azure region associated with this resource. |

### DimTime

| | Description |
| --- | --- |
| **`Timestamp` *(PK)*** | The timestamp of when this record was generated aggregated at the hour-level. |

### DimStatusCode

| | Description |
| --- | --- |
| **`StatusCode` *(PK)*** | The HTTP status code response for the request, highlighting details of the success/failure of the request. |

### DimOperationName

| | Description |
| --- | --- |
| **`OperationName` *(PK)*** | The specific operation executed against the resource. |

### DimResourceName

| | Description |
| --- | --- |
| **`ResourceName` *(PK)*** | The types of resources that an operation can be executed against. Values can be `Collection`, `Document`, or `StoredProcedure`. |

### DimSubStatusCode

| | Description |
| --- | --- |
| **`SubStatusCode` *(PK)*** | The HTTP substatus code response for the request, used to debug root cause of the issue. |

### DimMeter

| | Description |
| --- | --- |
| **`MeterId` *(PK)*** | A unique identifier for the Meter. |
| **`Product`** | The product or service associated with the meter (for example, Azure Cosmos DB - 100 RU/s/Hour) |
| **`MeterName`** | The name of the meter (for example, 100 RU/s or Data Stored) |
| **`MeterDescription`** | A more detailed description of the meter, explaining what it tracks including Region (for example, Azure Cosmos DB - Data Stored (GB/Month) - DE North) |
| **`BasePrice`** | The base price for the meter (that is $0.008) |

## Fact Tables

### FactFleetHourly

| | Description |
| --- | --- |
| **`Timestamp` *(FK)*** | The timestamp of when this record was generated aggregated at the hour-level. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`FleetName`** | The name of the fleet. |
| **`AccountName`** | The name of the Azure Cosmos DB Database Account associated with the fleet. |

### FactRequestHourly

| | Description |
| --- | --- |
| **`Timestamp` *(FK)*** | The timestamp of when this record was generated aggregated at the hour-level. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`ResourceId` *(FK)*** | A unique identifier for the resource. |
| **`ResourceName` *(FK)*** | The resource that an operation can be executed against. For example, Collection, Document, StoredProcedure. |
| **`OperationName` *(FK)*** | The specific operation executed against the resource. |
| **`StatusCode` *(FK)*** | The HTTP status code response for the request, highlighting details of the success/failure of the request. |
| **`SubStatusCode` *(FK)*** | The HTTP substatus code response for the request, used to debug root cause of the issue. |
| **`TotalRequestCount`** | The total number of requests made during the timestamp period. |
| **`MaxRequestSizeInBytes`** | The maximum payload size (in bytes) of a request in the timestamp. |
| **`TotalRequestSizeInBytes`** | The total (sum) payload size (in bytes) of requests in the timestamp. |
| **`MaxRequestChargeInRU`** | The max RU (Request Unit) consumption of a request in the timestamp. |
| **`TotalRequestChargeInRU`** | The total RU (Request Unit) consumption of requests in the timestamp. |
| **`TotalResponseSizeInBytes`** | The total payload size (in bytes) of the server response. |
| **`TotalBurstCapacityRequestCount`** | The total count of requests using Burst Capacity during the timestamp period. |
| **`TotalBurstCapacityRequestChargeInRU`** | The total request charge of requests using Burst Capacity during the timestamp period. |

### FactMeterUsageHourly

| | Description |
| --- | --- |
| **`Timestamp` *(FK)*** | The timestamp of when this record was generated aggregated at the hour-level. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`ResourceId` *(FK)*** | A unique identifier for the resource. |
| **`MeterId` *(FK)*** | The unique identifier for the meter used. |
| **`ConsumedUnits`** | The total amount of usage consumed for the meter during the specified timestamp period. |

### FactAccountHourly

| | Description |
| --- | --- |
| **`Timestamp` *(FK)*** | The timestamp of when this record was generated aggregated at the hour-level. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`ResourceId` *(FK)*** | A unique identifier for the resource. |
| **`DefaultConsistencyLevel`** | The default consistency level configured for the Azure Cosmos DB account (for example, Strong, Bounded Staleness, Session, Consistent Prefix, Eventual). |
| **`ResourceGroup`** | The name of the Resource Group this resource is associated with. |
| **`APIKind`** | The type of API this Azure Cosmos DB account uses. Values can be: `NoSQL`, `MongoDB`, or etc. |
| **`IsSynapseLinkEnabled`** | Indicates whether Azure Synapse Link is enabled on the Azure Cosmos DB account (true or false). |
| **`IsFreeTierEnabled`** | Indicates whether the account is utilizing the Azure Cosmos DB Free Tier (true or false). |
| **`IsBurstEnabled`** | Indicates whether burst capacity is enabled for the account (true or false). |
| **`BackupMode`** | The type of backup that is configured (for example, Periodic, Continuous). |
| **`BackupStrategy`** | The strategy used for backup, such as point-in-time restore or snapshot-based. |
| **`BackupRedundancy`** | The redundancy configuration for backups. Values could be: locally redundant storage (LRS), zone redundant storage (ZRS), or geo redundant storage (GRS). |
| **`BackupIntervalInMinutes`** | The interval, in minutes, between successive backups for the resource. |
| **`BackupRetentionIntervalInHours`** | The duration, in hours, that backups are retained. |
| **`TotalRUPerSecLimit`** | The maximum provisioned RU/s (Request Units per second) allowed for the account. |
| **`APISettings`** | JSON or structured settings defining API-specific configuration options (for example, `{"MongoDBServerSideRetriesEnabled":null,"MongoDBServerVersion":""}`). |
| **`AccountKeySettings`** | The most recent date on which each Azure Cosmos DB account keys were rotated. (for example, `{"PrimaryKey":"2025-04-08T19:47:15.2501537Z","PrimaryReadonlyKey":"2025-04-08T19:57:48.8462857Z","SecondaryKey":"2025-05-06T19:41:11.2381063Z","SecondaryReadonlyKey":"2025-05-06T19:51:28.6159307Z"}`) |
| **`LastDateAccountKeyRotated`** | The most recent date on which the Azure Cosmos DB account keys were rotated (for example, `2025-05-06T19:51:28.6159307Z`) |

### FactResourceUsageHourly

| | Description |
| --- | --- |
| **`Timestamp` *(FK)*** | The timestamp of when this record was generated aggregated at the hour-level. |
| **`FleetId` *(FK)*** | A unique identifier for the fleet. |
| **`ResourceId` *(FK)*** | A unique identifier for the resource. |
| **`MaxPartitionCount`** | The maximum number of partitions in the hour. |
| **`MaxDocumentCount`** | The maximum number of documents stored during the hour. |
| **`MaxDataStorageInKB`** | The max storage used for data in kilobytes during the hour. |
| **`MaxIndexStorageInKB`** | The max storage used for indexes in kilobytes during the hour. |
| **`MaxAnalyticalStorageInKB`** | The max storage used by the analytical store in kilobytes during the hour. |
| **`MaxProvisionedRUPerSec`** | The highest provisioned RU/s during the hour. |
| **`MaxRUPercentageConsumed`** | The highest percentage of RU/s consumed during the hour. |
| **`AvgRUPercentageConsumed`** | The average percentage of RU/s consumed during the hour. |
| **`MaxThroughputConsumedPerPartitionInRUPerSec`** | The highest RU/s consumed by a single partition during the hour. |
| **`MaxThroughputConsumedPerContainerInRUPerSec`** | The highest RU/s consumed by a single container during the hour. |
| **`NormalizedProvisionedThroughputConsumedPercent`** | The normalized throughput utilization during the hour. |
| **`MaxCompositeIndexCount`** | The maximum number of composite indexes present during the hour. |
| **`ConsistencyLevel`** | The effective consistency level in use for operations. This value could differ from the default if overridden. |
| **`MaxProvisionedRUPerSecLimit`** | The maximum provisioned throughput capacity set by the user. |
| **`AutoScaleMaxRUPerSec`** | The highest level of throughput (RU/s) that a database or container can automatically scale to. |
| **`IsAutoScaleEnabled`** | Indicates whether autoscale is enabled for the resource (true or false). |
| **`IsDatabaseOffer`** | Indicates whether the resource is a shared throughput database-level offer (true or false). |
| **`IsMultiRegionWrite`** | Indicates if multi-region writes are enabled for the account (true or false). |
| **`IsServerless`** | Indicates if the account is configured as serverless (true or false). |
| **`IsAnalyticalStoreEnabled`** | Indicates whether the analytical store is enabled for the resource (true or false). |
| **`IsDefaultIndexingPolicy`** | Indicates whether the default indexing policy is in use (true or false). |
| **`IsTTLEnabled`** | Indicates whether time-to-live (TTL) is enabled on the resource (true or false). |
| **`TTLDefaultValue`** | The default TTL value (in seconds) applied to documents if TTL is enabled. |
