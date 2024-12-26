---
title: Configure Metrics Alerts
description: This article describes how to configure and access metrics alerts for Azure Database for MySQL - Flexible Server from the Azure portal.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - kr2b-contr-experiment
---

# Set up alerts on metrics for Azure Database for MySQL - Flexible Server

This article shows you how to set up Azure Database for MySQL flexible server instance alerts using the Azure portal. You can receive an alert based on monitoring metrics for your Azure services.

The alert triggers when the value of a specified metric crosses a threshold you assign. The alert triggers both when the condition is first met, and then afterwards when that condition is no longer being met. Metric alerts are stateful, that is, they only send out notifications when the state changes.

You can configure an alert to do the following actions when it triggers:

- Send email notifications to the service administrator and co-administrators
- Send email to other emails that you specify
- Call a webhook

You can configure and get information about alert rules using:

- [Azure portal](/azure/azure-monitor/alerts/alerts-metric#create-with-azure-portal)
- [Azure CLI](/azure/azure-monitor/alerts/alerts-metric#with-azure-cli)
- [Azure Monitor REST API](/rest/api/monitor/metricalerts)

## Create an alert rule on a metric from the Azure portal

1. In the [Azure portal](https://portal.azure.com/), select the Azure Database for MySQL flexible server instance you want to monitor.
1. Under the **Monitoring** section of the sidebar, select **Alerts**.
1. Select **+ New alert rule**.
1. The **Create rule** page opens. Fill in the required information.
1. Within the **Condition** section, choose **Select condition**.
1. You'll see a list of supported signals, select the metric you want to create an alert on. For example, select Storage percent.
1. You'll see a chart for the metric for the last six hours. Use the **Chart period** dropdown list to select to see longer history for the metric.
1. Select the **Threshold** type (ex. "Static" or "Dynamic"), **Operator** (ex. "Greater than"), and **Aggregation type** (ex. average). This selection determines the logic that the metric alert rule will evaluate.
   * If you're using a **Static** threshold, continue to define a **Threshold value** (ex. 85 percent). The metric chart can help determine what might be a reasonable threshold.
   * If you're using a **Dynamic** threshold, continue to define the **Threshold sensitivity**. The metric chart will display the calculated thresholds based on recent data. [Learn more about Dynamic Thresholds condition type and sensitivity options](/azure/azure-monitor/alerts/alerts-dynamic-thresholds).
1. Refine the condition by adjusting **Aggregation granularity (Period)** interval over which data points are grouped using the aggregation type function (ex. "30 minutes"), and **Frequency** (ex "Every 15 Minutes").
1. Select **Done**.
1. Add an action group. An action group is a collection of notification preferences defined by the owner of an Azure subscription. Within the **Action Groups** section, choose **Select action group** to select an already existing action group to attach to the alert rule.
1. You can also create a new action group to receive notifications on the alert. For more information, see [create and manage action group](/azure/azure-monitor/alerts/action-groups).
1. To create a new action group, choose **+ Create action group**. Fill out the **Create action group** form with a **Subscription**, **Resource group**, **Action group name** and **Display Name**.
1. Configure **Notifications** for action group.

    In **Notification type**, choose **Email Azure Resource Manager Role** to select subscription Owners, Contributors, and Readers to receive notifications. Choose the **Azure Resource Manager Role** for sending the email.
    You can also choose **Email/SMS message/Push/Voice** to send notifications to specific recipients.

    Provide **Name** to the notification type and select **Review + Create** when completed.

1. Fill in **Alert rule details** like **Alert rule name**, **Description**, **Save alert rule to resource group** and **Severity**.

1. Select **Create alert rule** to create the alert.
    Within a few minutes, the alert is active and triggers as previously described.

## Manage your alerts

Once you create an alert, you can select it and do the following actions:

- View a graph showing the metric threshold and the actual values from the previous day relevant to this alert.
- **Edit** or **Delete** the alert rule.
- **Disable** or **Enable** the alert, if you want to temporarily stop or resume receiving notifications.

## Related content

- [Setting alert on metrics](/azure/azure-monitor/alerts/alerts-metric)
- [Metrics in Azure Database for MySQL flexible server](concepts-monitoring.md)
- [Understand how metric alerts work in Azure Monitor](/azure/azure-monitor/alerts/alerts-metric-overview)
