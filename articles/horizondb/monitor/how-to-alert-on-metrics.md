---
title: Configure Alerts - Azure Portal in Azure HorizonDB
description: This article describes how to configure and access metric alerts for your Azure HorizonDB instance from the Azure portal in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Use the Azure portal to set up alerts on metrics in Azure HorizonDB

This article shows you how to set up alerts for your Azure HorizonDB instance using the Azure portal. You can receive an alert based on monitoring metrics for your Azure services.

The alert triggers when the value of a specified metric crosses a threshold you assign. The alert triggers both when the condition is first met, and then afterwards when that condition is no longer being met. Metric alerts are stateful, that is, they only send out notifications when the state changes.

You can configure an alert to do the following actions when it triggers:

- Send email notifications to the service administrator and co-administrators.
- Send email to additional emails that you specify.
- Call a webhook.

You can configure and get information about alert rules using:

- [Azure portal](/azure/azure-monitor/alerts/alerts-metric#create-with-azure-portal)
- [Azure CLI](/azure/azure-monitor/alerts/alerts-metric#with-azure-cli)
- [Azure Monitor REST API](/rest/api/monitor/metricalerts)

## Create an alert rule on a metric from the Azure portal

1. In the [Azure portal](https://portal.azure.com/), select the Azure HorizonDB instance you want to monitor

1. Under the **Monitoring** section of the sidebar, select **Alerts**.

1. Select **+ New alert rule**.

1. The **Create rule** page opens as shown below. Fill in the required information:

1. Current Azure HorizonDB instance is automatically added to the alert **Scope**.

1. Within the **Condition** section, select **Add condition**.

1. You'll see a list of supported signals, select the metric you want to create an alert on. For example, select `storage percent`.

1. You'll see a chart for the metric for the last six hours. Use the **Chart period** dropdown list to select to see longer history for the metric.

1. Select the **Threshold type** (ex. "Static" or "Dynamic"), **Operator** (ex. "Greater than"), and **Aggregation type** (ex. average). This selection determines the logic that the metric alert rule will evaluate.
   - If you're using a Static threshold, continue to define a Threshold value (ex. 85 percent). The metric chart can help determine what might be a reasonable threshold.
   - If you're using a Dynamic threshold, continue to define the Threshold sensitivity. The metric chart will display the calculated thresholds based on recent data. [Learn more about Dynamic Thresholds condition type and sensitivity options](/azure/azure-monitor/alerts/alerts-dynamic-thresholds).

1. Refine the condition by adjusting **Aggregation granularity (Period)** interval over which data points are grouped using the aggregation type function (ex. "Lookback period 30 minutes"), and **Frequency** (ex "Check every 15 Minutes").

1. Select **Done** when complete.
1. Add an action group. An action group is a collection of notification preferences defined by the owner of an Azure subscription. Within the **Action Groups** section, choose **Select action group** to select an already existing action group to attach to the alert rule.
   - You can also create a new action group to receive notifications on the alert. For more information, see [create and manage action group](/azure/azure-monitor/alerts/action-groups).
   - To create a new action group, choose **+ Create action group**. Fill out the **create action group** form with a **subscription**, **resource group**, **action group name** and **display name**.
   - Configure **Notifications** for action group.

   In **Notification type**, choose **Email Azure Resource Manager Role** to select subscription Owners, Contributors, and Readers to receive notifications. Choose the **Azure Resource Manager Role** for sending the email. You can also choose **Email/SMS message/Push/Voice** to send notifications to specific recipients. Provide **Name** to the notification type and select **Review + Create** when completed.

1. Fill in **Alert rule details** like **severity**, **alert rule name** and **description**.
1. Select **Create alert rule** to create the alert.
1. Within a few minutes, the alert is active and triggers as previously described.

## Monitor multiple resources

Azure HorizonDB also supports multi-resource metric alert rule. You can monitor at scale by applying the same metric alert rule to multiple Azure HorizonDB in the same Azure region. Individual notifications are sent for each monitored resource.

To [set up a new metric alert rule](/azure/azure-monitor/alerts/alerts-create-new-alert-rule), in the alert rule creation experience, in Scope definition (step 5.) from the previous section use the checkboxes to select all the Azure HorizonDB you want the rule to be applied to.

> [!IMPORTANT]  
> The resources you select must be within the same resource type, location, and subscription. Resources that don't fit these criteria aren't selectable.

You can also use [Azure Resource Manager templates](/azure/azure-monitor/alerts/alerts-create-new-alert-rule#create-a-new-alert-rule-using-an-arm-template) to deploy multi-resource metric alerts. To learn more about multi-resource alerts, refer our blog [Scale Monitoring with Azure PostgreSQL Multi-Resource Alerts](https://techcommunity.microsoft.com/blog/adforpostgresql/azure-postgresql-multi-resource-alerts-with-metrics/3866526).

## Manage your alerts

Once you have created an alert, you can select it and do the following actions:

- View a graph showing the metric threshold and the actual values from the previous day relevant to this alert.
- **Edit** or **Delete** the alert rule.
- **Disable** or **Enable** the alert, if you want to temporarily stop or resume receiving notifications.

## Related content

- [Schedule maintenance in Azure HorizonDB](../configure-maintain/how-to-configure-scheduled-maintenance.md)
- [Configure and access logs in Azure HorizonDB](how-to-configure-and-access-logs.md)
- [Configure autonomous tuning in Azure HorizonDB](how-to-configure-autonomous-tuning.md)
