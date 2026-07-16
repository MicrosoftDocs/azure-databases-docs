---
title: Configure Alerts on Metrics in Azure Database for PostgreSQL Flexible Server
description: This article describes how to configure and access metric alerts for your Azure Database for PostgreSQL flexible server from the Azure portal.
#customer intent: As a user, I want to configure metric alerts for my Azure Database for PostgreSQL flexible server, so that I can be notified when performance metrics cross critical thresholds.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Configure alerts on metrics in Azure Database for PostgreSQL flexible server

This article shows you how to set up alerts for your Azure Database for PostgreSQL flexible server by using the Azure portal. You can receive an alert based on monitoring metrics for your Azure services.

The alert triggers when the value of a specified metric crosses a threshold you assign. The alert triggers both when the condition is first met, and then afterwards when that condition is no longer met. Metric alerts are stateful, so they only send notifications when the state changes.

When an alert triggers, you can configure it to take the following actions:

* Send email notifications to the service administrator and co-administrators.
* Send email to additional recipients that you specify.
* Call a webhook.

You can configure and get information about alert rules by using:

* [Azure portal](/azure/azure-monitor/alerts/alerts-metric#create-with-azure-portal)
* [Azure CLI](/azure/azure-monitor/alerts/alerts-metric#with-azure-cli)
* [Azure Monitor REST API](/rest/api/monitor/metricalerts)

## Create an alert rule on a metric from the Azure portal

1.	In the [Azure portal](https://portal.azure.com/), select the Azure Database for PostgreSQL flexible server you want to monitor.

1.	Under the **Monitoring** section of the sidebar, select **Alerts**.

1.	Select **+ New alert rule**.

1.	The **Create rule** page opens. Fill in the required information:

1.	The current Azure Database for PostgreSQL flexible server is automatically added to the alert **Scope**.

1.	Within the **Condition** section, select **Add condition**.

1.	You see a list of supported signals. Select the metric you want to create an alert on. For example, select `storage percent`.

1.	You see a chart for the metric for the last six hours. Use the **Chart period** dropdown to select to see longer history for the metric.

1.	Select the **Threshold type** (for example, "Static" or "Dynamic"), **Operator** (for example, "Greater than"), and **Aggregation type** (for example, average). This selection determines the logic that the metric alert rule evaluates.
    - If you use a static threshold, continue to define a threshold value (for example, 85 percent). The metric chart can help determine what might be a reasonable threshold.
    - If you use a dynamic threshold, continue to define the threshold sensitivity. The metric chart displays the calculated thresholds based on recent data. [Learn more about Dynamic Thresholds condition type and sensitivity options](/azure/azure-monitor/alerts/alerts-dynamic-thresholds).

1.	Refine the condition by adjusting **Aggregation granularity (Period)** interval over which data points are grouped using the aggregation type function (for example, "Lookback period 30 minutes"), and **Frequency** (for example, "Check every 15 Minutes").

1.	Select **Done** when complete.
1.	Add an action group. An action group is a collection of notification preferences defined by the owner of an Azure subscription. Within the **Action Groups** section, choose **Select action group** to select an already existing action group to attach to the alert rule.
    - You can also create a new action group to receive notifications on the alert. For more information, see [create and manage action group](/azure/azure-monitor/alerts/action-groups).
    - To create a new action group, choose **+ Create action group**. Fill out the **create action group** form with a **subscription**, **resource group**, **action group name**, and **display name**.
    -	Configure **Notifications** for action group.

    In **Notification type**, choose **Email Azure Resource Manager Role** to select subscription Owners, Contributors, and Readers to receive notifications. Choose the **Azure Resource Manager Role** for sending the email. You can also choose **Email/SMS message/Push/Voice** to send notifications to specific recipients. Provide **Name** to the notification type and select **Review + Create** when completed.

1.	Fill in **Alert rule details** like **severity**, **alert rule name**, and **description**.
1.	Select **Create alert rule** to create the alert.
1.	Within a few minutes, the alert is active and triggers as previously described.

## Monitor multiple resources

Azure Database for PostgreSQL also supports multiresource metric alert rules. You can monitor at scale by applying the same metric alert rule to multiple Azure Database for PostgreSQL flexible servers in the same Azure region. The system sends individual notifications for each monitored resource.

To [set up a new metric alert rule](/azure/azure-monitor/alerts/alerts-create-new-alert-rule), use the checkboxes in Scope definition (step 5) to select all the Azure Database for PostgreSQL flexible servers you want the rule to apply to. 

> [!IMPORTANT]
> You must select resources that are in the same resource type, location, and subscription. You can't select resources that don't fit these criteria.

You can also use [Azure Resource Manager templates](/azure/azure-monitor/alerts/alerts-create-new-alert-rule#create-a-new-alert-rule-using-an-arm-template) to deploy multiresource metric alerts. To learn more about multiresource alerts, see the blog [Scale Monitoring with Azure PostgreSQL Multi-Resource Alerts](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/scale-monitoring-with-azure-postgresql-multi-resource-alerts/ba-p/3866526).

## Manage your alerts

After you create an alert, select it and you can perform the following actions:

* View a graph that shows the metric threshold and the actual values from the previous day that are relevant to this alert.
* **Edit** or **Delete** the alert rule.
* **Disable** or **Enable** the alert, if you want to temporarily stop or resume receiving notifications.

## Related content

- [Configure scheduled maintenance](../configure-maintain/how-to-configure-scheduled-maintenance.md).
- [Configure and access logs](how-to-configure-and-access-logs.md).
- [Configure autonomous tuning](how-to-configure-autonomous-tuning.md).
