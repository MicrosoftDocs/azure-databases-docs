---
title: Enable and manage alerts on metrics in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Enable and manage metric alerts on Azure Cosmos DB for MongoDB vCore clusters.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 01/10/2025
#Customer Intent: As a database adminstrator, I want to get notifications when certain operational metrics on my Azure Cosmos DB for MongoDB vCore cluster reach pre-defined thresholds.
---

# Use the Azure portal to set up alerts on metrics for Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

This article shows how to set up and manage alerts on operational metrics for Azure Cosmos DB for MongoDB vCore using the Azure portal. You can create alerts based on monitoring metrics for your Azure services to proactively manage your clusters.

You'll set up an alert to trigger when a specified metric crosses a threshold. The alert triggers when the condition is first met and continues to trigger afterward until the condition is no longer true.

You can configure an alert to perform the following actions when triggered:
- Send email notifications to the service administrator and co-administrators.
- Send emails to extra specified addresses.
- Call a webhook.

You can configure and manage alert rules using the following tools:
- Azure portal
- Azure CLI
- Azure Monitor REST API

## Create an alert rule on a metric from the Azure portal

Follow these steps to create an alert rule based on a metric:

1. In the Azure portal, select the **Azure Cosmos DB for MongoDB vCore** cluster you want to monitor.
1. Under the **Monitoring** section of the sidebar, select **Alerts**, then select **Create** and then **Alert rule**.
1. On the **Condition** tab, select **See all signals** next to **Select a signal** drop-down list. 
1. Choose a metric from the list of available signals. For example, select **Storage percent** and then select **Apply**.
1. On the **Condition** tab of the **Create an alert rule** page, under **Alert logic**, configure the following:
   - For **Threshold**, select **Static**.
   - For **Aggregation type**, select **Average**.
   - For **Operator**, select **Greater than**.
   - For **Threshold value**, enter **85**.
1. Select the **Actions** tab.
1. Make sure **Use action groups** is selected, then choose **Create action group** to create a new group that will receive notifications when the alert triggers.
1. On the **Create an action group** form, specify the **Subscription**, **Resource group**, and **Region**, and enter an **Action group name** and **Display name** for the group.
1. Select **Next: Notifications** at the bottom of the page.
1. On the **Notifications** tab, under **Notification type**, select **Email/SMS message/Push/Voice**.
1. On the **Email/SMS message/Push/Voice** form, enter the email addresses and phone numbers of the recipients you want to notify. Then select **OK**.
1. On the **Create an action group** form, provide a name for the notification.
1. Select **Review + create**, then select **Create** to complete the action group setup. The new action group appears under **Action group name** on the **Actions** tab of the **Create an alert rule** page.
1. Select **Next: Details** at the bottom of the page.
1. On the **Details** tab, set a **Severity** level for the alert rule. Provide an easily identifiable **Name** and an optional **Description** for the rule.
1. Select **Review + create**, then select **Create** to finalize the alert rule. The alert will be active within a few minutes and will trigger as configured.

## Manage alerts

After creating an alert, you can view, modify, or manage it in several ways:

- **View a graph** showing the metric threshold and the actual values from the past day.
- **Edit or delete** the alert rule.
- **Disable or enable** the alert to temporarily stop or resume receiving notifications.

## Suggested alerts

The following alerts are recommended to help you monitor and maintain your Azure Cosmos DB for MongoDB vCore clusters.

### Disk space

Monitoring disk space is essential for every production cluster. The underlying database requires sufficient free disk space to function correctly. If the disk becomes full, the cluster's physical shard (node) may go offline and refuse to start until more space is available. In such cases, you must submit a support request to Microsoft to resolve the issue.

We recommend setting disk space alerts on all nodes in every cluster, including non-production environments. Disk space usage alerts provide early warnings that help you take proactive steps to maintain node health. 

For best results, set up a series of alerts at **75%**, **85%**, and **95%** usage thresholds. The specific percentages you choose may depend on the data ingestion speed, as fast ingestion can fill the disk quickly.

To free up disk space, consider the following actions:
- **Review your data retention policy** and move older data to cold storage if possible.
- **Increase the node capacity** if necessary. Each node can support up to **32 TiB** of storage.

### CPU usage

Monitoring CPU usage helps you establish a performance baseline. For example, if your cluster's CPU usage typically hovers around **40-60%**, a sudden increase to **95%** could indicate an anomaly.

CPU usage spikes can result from organic growth or inefficient queries. When creating CPU usage alerts, set a long aggregation period to catch sustained increases and ignore momentary spikes.

With these alerts in place, you can proactively monitor and manage your Azure Cosmos DB for MongoDB vCore clusters to maintain high availability and performance.

## Related content
- [Learn more about alerts in Azure](/azure/azure-monitor/alerts/alerts-overview)
- [See details on metrics in Azure Cosmos DB for MongoDB vCore](./monitor-metrics.md)
