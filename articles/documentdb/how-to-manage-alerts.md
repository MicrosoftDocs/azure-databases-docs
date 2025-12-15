---
title: Enable and manage alerts on metrics in Azure DocumentDB
description: Enable and manage metric alerts on Azure DocumentDB clusters.
author: abinav2307
ms.author: abramees
ms.topic: how-to
ms.date: 01/10/2025
#Customer Intent: As a database adminstrator, I want to get notifications when certain operational metrics on my Azure DocumentDB cluster reach pre-defined thresholds.
---

# Use the Azure portal to set up alerts on metrics for Azure DocumentDB

This article shows how to set up and manage alerts on [operational metrics](./monitor-metrics.md) for Azure DocumentDB using the Azure portal. You can create alerts based on monitoring metrics for your Azure services to proactively manage your clusters.

You'll set up an alert to trigger when a specified metric crosses a threshold. The alert triggers when the condition is first met and continues to trigger afterward until the condition is no longer true.

You can configure an alert to perform the following actions when triggered:
- Send email notifications to the service administrator and co-administrators.
- Send emails to extra specified addresses.
- Call a webhook.

You can configure and manage alert rules using the following tools:
- [Azure portal](/azure/azure-monitor/alerts/alerts-create-metric-alert-rule)
- [Azure CLI, PowerShell, and ARM templates](/azure/azure-monitor/alerts/alerts-create-rule-cli-powershell-arm)
- [Azure Monitor REST API](/rest/api/monitor/metric-alerts)

## Create an alert rule on a metric from the Azure portal

Follow these steps to create an alert rule based on a metric:

1. In the [Azure portal](https://portal.azure.com/), select the **Azure DocumentDB** cluster you want to monitor.
1. Under the **Monitoring** section of the sidebar, select **Alerts**, then select **Create** and then **Alert rule**.
   :::image type="content" source="./media/how-to-manage-alerts/create-alert-rule.png" alt-text="Screenshot of the alert rule creation page in Azure DocumentDB in the Azure portal.":::
1. On the **Condition** tab, select **See all signals** next to **Select a signal** drop-down list.
1. Choose a metric from the list of available signals. For example, select **Storage percent** and then select **Apply**.
   :::image type="content" source="./media/how-to-manage-alerts/select-metric-for-the-rule.png" alt-text="Screenshot of the alert condition selection panel with a metric selected in the Azure portal.":::
1. On the **Condition** tab of the **Create an alert rule** page, under **Alert logic**, configure the following:
   - For **Threshold**, select **Static**.
   - For **Aggregation type**, select **Average**.
   - For **Operator**, select **Greater than**.
   - For **Threshold value**, enter **85**.
1. Select the **Actions** tab.
   :::image type="content" source="./media/how-to-manage-alerts/condition-definition.png" alt-text="Screenshot of the alert definition for a selected metric in the Azure portal.":::
1. Make sure **Use action groups** is selected, then choose **Create action group** to create a new group that will receive notifications when the alert triggers.
   :::image type="content" source="./media/how-to-manage-alerts/create-action-group.png" alt-text="Screenshot of the action group creation panel in the Azure portal.":::
1. On the **Create an action group** form, confirm the **Subscription**, **Resource group**, specify **Region**, and enter an **Action group name** and **Display name** for the group.
1. Select **Next: Notifications** at the bottom of the page.
   :::image type="content" source="./media/how-to-manage-alerts/action-group-basics.png" alt-text="Screenshot of the action group basics in the Azure portal.":::
1. On the **Notifications** tab, under **Notification type**, select **Email/SMS message/Push/Voice**.
1. On the **Email/SMS message/Push/Voice** form, enter the email addresses and phone numbers of the recipients you want to notify. Then select **OK**.
1. On the **Create an action group** form, provide a name for the notification.
   :::image type="content" source="./media/how-to-manage-alerts/email-notification-creation.png" alt-text="Screenshot of the e-mail notification creation in the Azure portal.":::
1. Select **Review + create**, then select **Create** to complete the action group setup. 
1. The new action group appears under **Action group name** on the **Actions** tab of the **Create an alert rule** page.
1. Select **Next: Details** at the bottom of the page.
   :::image type="content" source="./media/how-to-manage-alerts/alert-rules-actions-completed.png" alt-text="Screenshot of the completed alert rule actions tab in the Azure portal.":::
1. On the **Details** tab, set a **Severity** level for the alert rule. Provide an easily identifiable **Name** and an optional **Description** for the rule.
   :::image type="content" source="./media/how-to-manage-alerts/alert-rule-details.png" alt-text="Screenshot of the completed alert rule details tab in the Azure portal.":::
1. Select **Review + create**, then select **Create** to finalize the alert rule. The alert will be active within a few minutes and will trigger as configured.

## Manage alerts

After creating an alert, you can view, modify, or manage it in several ways:

- **Disable or enable** the alert to temporarily stop or resume receiving notifications.
- **Edit or delete** the alert rule.

To get access to the alerts, under the **Monitoring** section of the sidebar in the cluster properties, select **Alerts**, then select **Alert rules** in the toolbar.
:::image type="content" source="./media/how-to-manage-alerts/manage-alerts.png" alt-text="Screenshot of the alerts page in Azure DocumentDB in the Azure portal.":::

## Suggested alerts

The following alerts are recommended to help you monitor and maintain your Azure DocumentDB clusters.

### Disk space

Monitoring disk space is essential for every production cluster. The underlying database requires sufficient free disk space to function correctly. If the disk becomes full, the cluster's physical shard (node) may go offline and refuse to start until more space is available. In such cases, you must submit a support request to Microsoft to resolve the issue.

We recommend setting disk space alerts on all nodes in every cluster, including non-production environments. Disk space usage alerts provide early warnings that help you take proactive steps to maintain node health. 

For best results, set up a series of alerts at **75%**, **85%**, and **95%** usage thresholds. The specific percentages you choose may depend on the data ingestion speed, as fast ingestion can fill the disk quickly.

To free up disk space, consider the following actions:
- **Review your data retention policy** and move older data to cold storage if possible.
- **Increase the node capacity** if necessary. Each node can support up to [**32 TiB** of storage](./compute-storage.md#storage-in-azure-documentdb).

### CPU usage

Monitoring CPU usage helps you establish a performance baseline. For example, if your cluster's CPU usage typically hovers around **40-60%**, a sudden increase to **95%** could indicate an anomaly.

CPU usage spikes can result from organic growth or inefficient queries. When creating CPU usage alerts, set a long aggregation period to catch sustained increases and ignore momentary spikes. Longer aggregation period can help make decisions on scaling [cluster compute](./compute-storage.md#compute-in-azure-documentdb) up or down. For workloads with business patterns including CPU usage spikes on a regular basis and prolonged valley periods in between, consider using [autoscale compute](./autoscale.md).

With these alerts in place, you can proactively monitor and manage your Azure DocumentDB clusters to maintain high availability and performance.

## Related content
- [Learn more about alerts in Azure](/azure/azure-monitor/alerts/alerts-overview)
- [See details on metrics in Azure DocumentDB](./monitor-metrics.md)

> [!div class="nextstepaction"]
> [Migration options for Azure DocumentDB](migration-options.md)
