---
title: Visualize PostgreSQL metrics and logs with dashboards with Grafana
description: Learn how to use dashboards with Grafana in the Azure portal to monitor Azure Database for PostgreSQL metrics and logs.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 04/23/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Visualize PostgreSQL metrics and logs with dashboards with Grafana

Dashboards with Grafana are now natively integrated into the Azure portal for Azure Database for PostgreSQL. This experience enables you to visualize key metrics and logs in a unified, interactive dashboard—without needing to deploy or manage a separate Grafana instance.

With just a few select, you can explore Azure PostgreSQL server metrics, correlate them with log entries by timestamp, and build visual insights into performance and availability.

## What are dashboards with Grafana?

Dashboards with Grafana are a built-in monitoring experience powered by Azure Monitor and Grafana. It surfaces featured and customizable dashboards directly within the Azure portal, scoped to your PostgreSQL server resource.

Unlike Azure Managed Grafana, this experience requires no provisioning, no cost, and is fully integrated into the PostgreSQL flexible server blade.

## Benefits

- No setup or hosting required
- Built-in access to metrics and logs
- Timestamp-based correlation between events and queries
- Prebuilt dashboards available out of the box
- Fully customizable dashboards with support for filters, variables, and panel edits
- Governance support via Azure Role-Based Access Control (RBAC) and resource scoping

## Access dashboards with Grafana

To launch the experience:

1. Open the **Azure portal**
2. Navigate to your **Azure Database for PostgreSQL flexible server**
3. Left navigation pane, select **Dashboards with Grafana**
4. Choose a featured dashboard (e.g., *Azure PostgreSQL Monitoring v2*)

## Customize dashboards

To create a custom version of a dashboard:

1. Open a featured dashboard
2. Select **Save As** to create a copy
3. Add or edit panels
4. Connect additional data sources such as Azure Monitor Logs, Prometheus, or Resource Graph
5. Save and optionally export your dashboard as a template

You can export dashboards as ARM/Bicep templates or provision them using Terraform.

## Metrics and logs

Dashboards with Grafana uses the Azure Monitor platform to surface PostgreSQL metrics, such as:

- CPU and memory utilization
- Active connections
- Disk I/O and storage usage
- WAL (Write-Ahead Log) usage
- Query throughput and commit rates

For complete set of metrics available for visualization, refer [Azure PostgreSQL monitoring metrics](concepts-monitoring.md).  

In addition to metrics, you can also view PostgreSQL logs if diagnostic settings are enabled to send logs to Azure Monitor Logs. This allows you to:

- View and search logs by timestamp
- Correlate high CPU events with slow queries
- Filter logs by log level, process ID, or error code

> [!NOTE]
> To view logs in dashboards with Grafana, make sure diagnostic settings are enabled for your PostgreSQL server. [Learn how to configure logging](how-to-configure-and-access-logs.md).

## Considerations

- Dashboards are scoped to a single resource and do not span multiple PostgreSQL servers.
- To build cross-resource dashboards or access plugin support, use [Azure Managed Grafana](https://learn.microsoft.com/azure/managed-grafana/overview).
- Log ingestion and retention in Log Analytics is subject to [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/).

## Related content

- [Monitor metrics in Azure Database for PostgreSQL](concepts-monitoring.md)
- [Configure and access logs in Azure Database for PostgreSQL](how-to-configure-and-access-logs.md)
- [Visualize Azure Monitor data with Grafana](https://learn.microsoft.com/azure/azure-monitor/visualize/visualize-grafana-overview)
- [GA blog: Dashboards with Grafana — Now in Azure portal for PostgreSQL](https://aka.ms/azure-postgres-dashboards-grafana)