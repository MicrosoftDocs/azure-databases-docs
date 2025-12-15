---
title: Monitor Data Using Aggregated Diagnostics Logs (Preview)
titleSuffix: Azure Cosmos DB
description: Learn how to use aggregated diagnostics logs to monitor the performance and availability of data stored in Azure Cosmos DB for NoSQL.
author: stefarroyo
ms.author: esarroyo
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 05/08/2025
ms.custom:
  - devx-track-azurecli
  - build-2025
appliesto:
  - ✅ NoSQL
#Customer Intent: As an operations user, I want to monitor metrics using Azure Monitor, so that I can use a Log Analytics workspace to perform complex analysis.
---

# Monitor Azure Cosmos DB data using Azure Monitor aggregated diagnostics logs (preview)

This article helps you diagnose **data plane request issues** in **Azure Cosmos DB for NoSQL** using the `CDBDataPlaneRequests5M` table. This table is part of the **aggregated diagnostics logs** feature.

The **aggregated diagnostics logs** feature is designed to deliver significant **cost savings** and enhanced **troubleshooting capabilities** by summarizing diagnostics data into **5-minute** and **15-minute** intervals. Aggregated logs are written to **resource-specific tables**, which improves schema discoverability, ingestion latency, and overall query efficiency.

> [!TIP]
> Logging detailed per-request traces can be costly at scale. Aggregated diagnostics provide a compact and efficient alternative with up to **95% reduction in logging costs**.

## Prerequisites

- An Azure subscription

    - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

- An existing Azure Cosmos DB for NoSQL account

    - If you don't have an account, create a [new account](quickstart-portal.md).

- An existing Azure Monitor - Log Analytics workspace

## Configure diagnostic settings

First, you must enable **diagnostic settings**. This step is required before using the `CDBDataPlaneRequests5M` table. Configure your diagnostics with these settings and values:

| | Value |
| --- | --- |
| **Destination** | *Select your target Log Analytics workspace* |
| **Table format** | `Resource-specific` |
| **Category** | `DataPlaneRequests5M` or `DataPlaneRequests15M` (aggregated version only, not per-request) |

> [!WARNING]
> Avoid selecting the **classic `DataPlaneRequests`** category unless you explicitly need detailed per-request logs or query analysis. The aggregated tables (`CDBDataPlaneRequests5M`, `CDBDataPlaneRequests15M`) offer significant cost benefits.

## Query the data source

Here's a list of queries you can perform using the aggregated diagnostics logs feature. These queries can help with common troubleshooting scenarios.

```kusto
//1. Are you experiencing spikes in server-side latency?
//2. Was the latency on a particular Operation?
CDBDataPlaneRequests5M
//| where TimeGenerated > now(-6h)
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize TotalDurationInMs=sum(TotalDurationMs), MaxRequestCharge=max(MaxDurationMs), AverageRequestCharge=max(AvgDurationMs) by OperationName, TimeGenerated//, bin(TimeGenerated, 1d)
| render timechart

//3. Was the latency on a particular partition or many partitions?
CDBDataPlaneRequests5M
//| where TimeGenerated > now(-6h)
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize TotalDurationInMs=sum(TotalDurationMs), MaxRequestCharge=max(MaxDurationMs), AverageRequestCharge=max(AvgDurationMs) by PartitionId//, bin(TimeGenerated, 1d)
| render timechart

//4. Were you also experiencing throttling? If throttled percentage is above 5% and you are experiencing high latency this is a sign to continue troubleshooting.
CDBDataPlaneRequests5M
//| where TimeGenerated > now(-6h)
//| where OperationName == "Insert from previous step if latency was on a particular operation"
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize throttledOperations=sumif(SampleCount, StatusCode == 429), totalOperations=sum(SampleCount) by TimeGenerated, OperationName
| extend throttledPercentage =  throttledOperations/ totalOperations * 1.0
//| summarize count() by  TimeGenerated
//| render timechart

//5. Did transaction volume drastically increase/decrease recently?
CDBDataPlaneRequests5M
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize count() by TimeGenerated
| render timechart

//6. Did RU/s per operation increase?
//7. Did RU/s per partition increase?
CDBDataPlaneRequests5M
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize TotalRequestCharge=sum(TotalRequestCharge), MaxRequestCharge=max(MaxRequestCharge), AverageRequestCharge=max(AvgRequestCharge) by OperationName, bin(TimeGenerated, 1d)//, PartitionId
| order by TotalRequestCharge desc

//8. Was there an increase in payload size for write operations?
CDBDataPlaneRequests5M
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| where OperationName in ("Create", "Upsert", "Delete", "Execute")
| summarize sum(TotalRequestLength) by TimeGenerated, OperationName
| render timechart

//9. Was there an increase in response size for read operations?
CDBDataPlaneRequests5M
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| where OperationName in ("Read", "Query")
| summarize sum(TotalResponseLength) by TimeGenerated, OperationName
| render timechart

//10. Was there an increase in server-side timeouts?
CDBDataPlaneRequests5M
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| where StatusCode == 408
| summarize sum(SampleCount) by TimeGenerated
| render timechart

//11. Was the latency on a particular client or app?
CDBDataPlaneRequests5M
//| where TimeGenerated > now(-6h)
| where DatabaseName == "ContosoDemo" and CollectionName == "Transactions"
| summarize TotalDurationInMs=sum(TotalDurationMs) by UserAgent, ClientIpAddress, TimeGenerated
| render timechart
```

## Related content

- [Diagnostic queries in API for NoSQL](diagnostic-queries.md)
- [Diagnostic queries in API for MongoDB](mongodb/diagnostic-queries.md)
- [Diagnostic queries in API for Apache Cassandra](cassandra/diagnostic-queries.md)
