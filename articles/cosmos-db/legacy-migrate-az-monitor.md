---
title: Migrate legacy monitoring metrics to Azure Monitor
description: Learn how to migrate from the legacy Azure Cosmos DB monitoring metrics REST APIs to Azure Monitor.
#customer intent: As a customer I want to centralize all my monitoring to Azure Monitor
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 03/18/2025
---

# Migrate legacy monitoring metrics to Azure Monitor

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

The goal of this article is to make it easier for users of the legacy metrics to migrate to Azure Monitor. This article describes the differences between the two APIs, provides a mapping between the two and provides examples of usages to aide in migration.

Customers using Azure Cosmos DB's legacy monitoring metrics REST APIs are encouraged to migrate to Azure Monitor. Azure Monitor provides a centralized REST API for querying metrics across all Azure resources and provides features and metrics not available with the legacy Cosmos DB Resource Provider (RP) API.

## What is Azure Cosmos DB Metrics API

The Azure Cosmos DB Metrics API is a legacy system for getting monitoring data for your accounts, databases and collections. The number of metrics it provides is limited compared to what is now available with Azure Monitor.

Due to its legacy nature, the path structure for the REST API calls uses the resource ID (RID) for databases and collections. Resource IDs are specific to Cosmos DB and aren't valid for anything else in Azure. All resource provider APIs refer to Cosmos DB resources by name.

## What is the Azure Monitor REST API

The Azure Monitor REST API provides metric definitions, dimension and metrics values for your applications in Azure. This data can be used directly in your applications, or stored in a database for later analysis. Users can also list alert rules and view activity logs using the Azure Monitor API.

If you're new to using this API, please see [Azure monitoring REST API walkthrough](/azure/azure-monitor/essentials/rest-api-walkthrough) for an introduction and to become familiar.


### Listing of legacy Cosmos DB metrics APIs

This table lists the legacy metrics APIs that customers should migrate to Azure Monitor. Each operation is linked to its corresponding REST API documentation to provide reference.

| Cosmos Resource | Operation | URI |
|---|---|---|
| Database Account | [List Metric Definitions](/rest/api/cosmos-db-resource-provider/database-accounts/list-metric-definitions) | Microsoft.DocumentDB/databaseAccounts/{accountName}/metricDefinitions |
| Database Account | [List Metrics](/rest/api/cosmos-db-resource-provider/database-accounts/list-metrics) | Microsoft.DocumentDB/databaseAccounts/{accountName}/metrics |
| Database | [List Metric Definitions](/rest/api/cosmos-db-resource-provider/database/list-metric-definitions) | Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/metricDefinitions  |
| Database | [List Metrics](/rest/api/cosmos-db-resource-provider/database/list-metrics) | Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/metrics  |
| Collection | [List Metric Definitions](/rest/api/cosmos-db-resource-provider/collection/list-metric-definitions) | Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/collections/{collectionRid}/metricDefinitions |
| Collection | [List Metrics](/rest/api/cosmos-db-resource-provider/collection/list-metrics) | Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/collections/{collectionRid}/metrics |

### Listing of Azure Monitor metrics APIs

Azure Monitor has two APIs that are the equivalent to *list metric definitions* and to retrieve individual *metrics*. The links will direct you to REST API documentation with URI parameters and examples.

| Operation | URI |
|---|---|
| [List Metric Definitions](/rest/api/monitor/metric-definitions/list/) | Microsoft.Insights/metricDefinitions |
| [List Metrics](/rest/api/monitor/metrics/list/) | Microsoft.Insights/metrics |


### Mapping Cosmos DB RP Metrics to Azure Monitor Metrics

This table provides a mapping of all legacy Cosmos DB metrics in Azure Monitor to assist in migrating individual API calls for specific metrics.

| Cosmos Metrics | Azure Monitor Metric | Notes |
|---|---|---|
| Data Size | DataUsage |  |
| Index Size | IndexUsage |  |
| Storage Capacity | DocumentQuota |  |
| Available Storage | Deprecated | Collection Storage is now Unlimited (Metric not needed) |
| Document Count | DocumentCount |  |
| Read Latency | ServerSideLatency |  |
| Write Latency | ServerSideLatency |  |
| Service Availability | ServiceAvailability |  |
| Total Requests | TotalRequests |  |
| Http 2xx | TotalRequests | Filter by status code |
| Http 3xx | TotalRequests | Filter by status code |
| Http 400 | TotalRequests | Filter by status code |
| Http 401 | TotalRequests | Filter by status code |
| Throttled Requests | TotalRequests | Filter by status code |
| Service Unavailable | TotalRequests | Filter by status code |
| Total Request Units | TotalRequestUnits |  |
| Average Requests Per Second/RUs Per Second  | N/A | Not supported |
| Max RUMP (RUs Per Minute) | NormalizedRUConsumption |  |
| Mongo * Request Charge | MongoRequestCharge |  |
| Mongo * Request Rate | MongoRequests | Filter by status code |
| Mongo * Failed Requests | MongoRequests | Filter by status code |
| Replication Latency | ReplicationLatency |  |


### Examples migrating Cosmos DB legacy metrics to Azure Monitor metrics

Here's a comparison for two calls between the two REST APIs. Azure Monitor supports all of the metrics returned by the legacy Cosmos DB metrics APIs and has hundreds more. It also has metrics for every other Azure service making it easy to monitor multiple Azure services together.

### Example 1 - List Metrics Definition

List the available metrics for a NoSQL API collection

#### [Legacy List Metrics Definitions](#tab/legacy-list-metrics-definitions)

```rest
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/collections/{collectionRid}/metricDefinitions?api-version=2024-11-15
   ```

   ```json
   {
      "value": [
        {
         "metricAvailabilities": [
            {
              "timeGrain": "PT5M",
              "retention": "P2D"
            },
            {
              "timeGrain": "PT1H",
              "retention": "P14D"
            },
            {
              "timeGrain": "P1D",
              "retention": "P60D"
            }
         ],
         "primaryAggregationType": "Total",
         "unit": "Count",
         "resourceUri": "/subscriptions/subId/resourceGroups/rg1/providers/Microsoft.DocumentDB/databaseAccounts/ddb1",
         "name": {
            "value": "Total Requests",
            "localizedValue": "Total Requests"
         }
        },
        // Additional metric definitions...
      ]
   } 
   ```

#### [Azure Monitor List Metrics Definitions](#tab/azure-monitor-list-metrics-definitions)

   ```rest
   GET https://management.azure.com/subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroup}/providers/Microsoft.DocumentDb/databaseAccounts/{DocumentDBAccountName}/providers/microsoft.insights/metricDefinitions?api-version=2018-01-01
   ```

   ```json
   {
      "value": [
      {
         "name": {
           "value": "TotalRequests",
           "localizedValue": "Total Requests"
         },
         "unit": "Count",
         "primaryAggregationType": "Total",
         "supportedAggregationTypes": [
           "Average",
           "Minimum",
           "Maximum",
           "Total",
           "Count"
         ],
         "metricAvailabilities": [
           {
             "timeGrain": "PT1M",
             "retention": "P93D"
           },
           {
             "timeGrain": "PT1H",
             "retention": "P93D"
           },
           {
             "timeGrain": "P1D",
             "retention": "P93D"
           }
         ],
         "isDimensionRequired": false,
         "dimensions": []
      },
      {
         "name": {
           "value": "NormalizedRUConsumption",
           "localizedValue": "Normalized RU Consumption"
         },
         "unit": "Count",
         "primaryAggregationType": "Total",
         "supportedAggregationTypes": [
           "Average",
           "Minimum",
           "Maximum",
           "Total",
           "Count"
         ],
         "metricAvailabilities": [
           {
             "timeGrain": "PT1M",
             "retention": "P93D"
           },
           {
             "timeGrain": "PT1H",
             "retention": "P93D"
           },
           {
             "timeGrain": "P1D",
             "retention": "P93D"
           }
         ],
         "isDimensionRequired": false,
         "dimensions": []
      }
      // Additional metric definitions...
      ]
   }
   ```
---

### Example 2 - Total Database Requests

Get the total requests for a database (and all collections within it)

#### [Legacy Total Requests](#tab/legacy-total-requests)

   ```rest
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/metrics?api-version=2024-11-15&$filter=(name.value eq 'Total Requests' and statusCode eq '200')
   ```

   ```json
   {
      "value": [
         {
            "timeGrain": "PT5M",
            "startTime": "2023-01-01T00:00:00Z",
            "endTime": "2023-01-01T01:00:00Z",
            "unit": "Count", 
            "metricValues": [
               {
                  "timestamp": "2023-01-01T00:00:00Z",
                  "count": 80
               },
               {
                  "timestamp": "2023-01-01T00:05:00Z",
                  "count": 120
               }
            ],
            "name": {
               "value": "Total Requests",
               "localizedValue": "Total Requests"
            }
         }
      ]
   } 
   ```

#### [Azure Monitor Total Requests](#tab/azure-monitor-total-requests)

   ```rest
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/sqlDatabases/{databaseName}/providers/microsoft.insights/metrics?api-version=2024-11-15&$filter=(name.value eq 'Total Requests' and statusCode eq '200')
   ```

   ```json
   {
      "value": [
        {
            "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/sqlDatabases/{databaseName}/providers/microsoft.insights/metrics/TotalRequests",
            "type": "Microsoft.Insights/metrics",
            "name": {
               "value": "Total Requests",
               "localizedValue": "Total Requests"
            },
            "unit": "Count",
            "timeseries": [
               {
                  "data": [
                     {
                        "timeStamp": "2023-01-01T00:00:00Z",
                        "total": 80
                     },
                     {
                        "timeStamp": "2023-01-01T00:05:00Z",
                        "total": 120
                     }
                  ]
               }
            ]
         }
      ]
   }
   ```
---

### Example 2 - Max collection RU consumption

Retrieve the Max RU/s for a collection

#### [Legacy Max RU consumption](#tab/legacy-ru-consumption)

   ```rest
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/databases/{databaseRid}/collections/{collectionRid}/metrics?api-version=2024-11-15&$filter=(name.value eq 'Max RU/s') and timeGrain eq duration'PT5M' and startTime eq '2023-01-01T00:00:00Z' and endTime eq '2023-01-01T01:00:00Z' 
   ```

   ```json
   {
      "value": [
      {
         "timeGrain": "PT5M",
         "startTime": "2023-01-01T00:00:00Z",
         "endTime": "2023-01-01T01:00:00Z",
         "unit": "RU",
         "metricValues": [
            {
               "timestamp": "2023-01-01T00:00:00Z",
               "maximum": 1000
            },
            {
               "timestamp": "2023-01-01T00:05:00Z",
               "maximum": 1200
            }
         ],
         "name": {
            "value": "Max RU/s",
            "localizedValue": "Max RU/s"
         }
      }
      ]
   }
   ```

#### [Azure Monitor Max RU consumption](#tab/azure-monitor-ru-consumption)

   ```rest
   GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}/sqlDatabases/{databaseName}/sqlContainers/{containerName}/providers/microsoft.insights/metrics?api-version=2024-11-15&$filter=(name.value eq 'Normalized RU Consumption') and timeGrain eq duration'PT5M' and startTime eq '2023-01-01T00:00:00Z' and endTime eq '2023-01-01T01:00:00Z'
   ```

   ```json
   {
      "value": [
      {
         "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{accountName}//sqlDatabases/{databaseName}/sqlContainers/{containerName}/providers/microsoft.insights/metrics/NormalizedRUConsumption",
         "type": "Microsoft.Insights/metrics",
         "name": {
            "value": "Normalized RU Consumption",
            "localizedValue": "Normalized RU Consumption"
         },
         "unit": "Percent",
         "timeseries": [
         {
            "data": [
               {
                  "timeStamp": "2023-01-01T00:00:00Z",
                  "average": 75
               },
               {
                  "timeStamp": "2023-01-01T00:05:00Z",
                  "average": 80
               }
            ]
         }
         ]
      }
      ]
   }
   ```
---



## Next steps

For more information on how to use Azure Monitor for Azure Cosmos DB, see [Monitor and debug with insights in Azure Cosmos DB](../use-metrics.md).
