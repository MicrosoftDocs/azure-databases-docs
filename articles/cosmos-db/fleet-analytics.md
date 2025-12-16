---
title: Fleet Analytics (Preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Fleet Analytics for Azure Cosmos DB is a centralized solution that helps organizations monitor and manage their usage and costs effectively.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 05/07/2025
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Fleet analytics in Azure Cosmos DB (preview)

[!INCLUDE[Preview](includes/notice-preview.md)]

Fleet Analytics is a centralized analytics solution designed to help organizations monitor and manage Azure Cosmos DB usage and costs at scale. This feature enables teams to gain deep insights across all Azure Cosmos DB accounts and subscriptions within their fleet. These fleet-level insights include; resource utilization, provisioning patterns, and cost trends. Data is consolidated into a single hub and delivered as **open-source Apache Delta Lake tables** in both **Azure Data Lake Storage Gen2 (ADLS Gen2)** and **Microsoft Fabric OneLake** at an hourly grain. This unified structure makes it easier to create customized views and enables ad-hoc querying for deeper trend and cost analysis.

:::image source="media/fleet-analytics/components.png" alt-text="Diagram of all the components of an Azure Cosmos DB fleet including storage and Azure services.":::

Fleet Analytics is especially valuable for organizations that want to:

- **Track resource usage and provisioning trends** across their Azure Cosmos DB fleet

- **Perform cost analysis** at scale across accounts, subscriptions, or fleetspaces

- **Visualize and share insights** using enterprise-grade tools such as Power BI and Spark

## Choosing a monitoring tool

To help you decide which monitoring solution best fits your needs, use this mental model:

- **Fleet Analytics**: Aggregated logs at one hour granularity for analyzing patterns and trends across multiple accounts and subscriptions.

- **Metrics**: Near real-time data aggregated at one-minute intervals for quick insights.

- **Logs**: Request-level details for in-depth troubleshooting and root cause analysis.

Also, use this table to compare various monitoring options for Azure Cosmos DB fleets:

| | Azure Monitor metrics | Azure Monitor logs | Fleet Analytics |
| --- | --- | --- | --- |
| **Stored** | Account-level | Account-level | Fleet-wide |
| **Costs** | No | Yes (storage costs apply) | Yes (Fabric or OneLake Storage costs) |
| **Aggregation** | 1-minute (preaggregated) | Per-request (raw data) | one hour (preaggregated) |
| **Retention** | 90 days | User-defined | User-defined |
| **Analysis tool** | Metrics Explorer | Log Analytics Workspace | Fabric (SQL Endpoint, KQL), Azure Data Lake Storage (Gen2) |
| **Alerts** | Metric alert rules | Log alert rules | Fabric alert rules |
| **Visualization tool** | Azure Monitor Dashboards, Grafana | Azure Monitor Workbooks, Grafana | Power BI, Spark |

## Components

When you enable Fleet Analytics, a structured dataset is automatically created in your **Microsoft Fabric workspace** or **Azure Data Lake Storage (ADLS Gen2) storage account**. The data is stored in **Parquet format** and follows a **star schema**, a widely used model in enterprise analytics.

- The **fact table** includes essential usage, performance, and cost metrics.

- **Dimension tables** provide extra context such as time, region, resource type, and more.
 
This structure is optimized for high-performance analytics and enables you to build scalable dashboards and reports customized for your organization’s operational and financial goals. 

## Supported storage locations

Fleet analytics for Azure Cosmos DB supports both Microsoft Fabric and Azure Data Lake Storage (Gen2).

> [!NOTE]
> Microsoft Fabric requires creation of a Fabric workspace and Fabric OneLake resource.

Once this feature is enabled, standard billing applies for the storage consumed and query compute used within your own Fabric workspace or Azure Storage account.

## Next step

> [!div class="nextstepaction"]
> [Enable fleet analytics](how-to-enable-fleet-analytics.md)
