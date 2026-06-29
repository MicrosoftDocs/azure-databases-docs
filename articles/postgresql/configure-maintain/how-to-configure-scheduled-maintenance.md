---
title: Schedule maintenance
description: This article describes how to schedule maintenance of an Azure Database for PostgreSQL flexible server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 06/09/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
#customer intent: As a user, I want to learn how to schedule maintenance of an Azure Database for PostgreSQL flexible server.
---

# Schedule maintenance

You can specify scheduled maintenance options for each Azure Database for PostgreSQL flexible server in your Azure subscription. Options include the type of scheduled maintenance and notification settings for upcoming and finished maintenance events.

## Steps to schedule maintenance

### [Portal](#tab/portal-maintenance-settings)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Maintenance**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/maintenance.png" alt-text="Screenshot showing the Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/maintenance.png":::

1. If you select **System-managed schedule**, the system automatically assigns a random day of the week, and a 60-minute window that begins somewhere between 11 PM and 7 AM (local server time).

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/system-managed-schedule.png" alt-text="Screenshot showing the selection of system managed schedule in Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/system-managed-schedule.png":::

1. If you want more granular control, select **Custom schedule**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/custom-schedule.png" alt-text="Screenshot showing the selection of custom schedule in Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/custom-schedule.png":::

1. Select a preferred day of the week, and a start time for the 60-minute window in which you want maintenance to occur.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/day-time.png" alt-text="Screenshot showing the selection of custom day of the week and start time for the maintenance window." lightbox="./media/how-to-configure-scheduled-maintenance/day-time.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/save-changes-enable.png" alt-text="Screenshot showing how to save configuration changes made to Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/save-changes-enable.png":::

1. Make sure that you understand the implications of changing the currently configured schedule and confirm the operation or cancel it.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/confirm-changes.png" alt-text="Screenshot showing how to confirm or cancel configuration changes made to Maintenance schedule." lightbox="./media/how-to-configure-scheduled-maintenance/confirm-changes.png":::

1. A notification informs you that the service is updating the maintenance window settings.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-scheduled-maintenance/notification-configuring.png":::

1. When the operation finishes, a notification informs you that the service completed the update of the maintenance window settings.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-scheduled-maintenance/notification-configured.png":::

### [CLI](#tab/cli-maintenance-settings)

Use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command to configure the maintenance schedule settings.

To configure system managed schedule, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --maintenance-window Disabled
```

To configure custom schedule, for a one hour window starting on Wednesdays at 2:29PM (UTC), use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --maintenance-window Wed:14:29
```

To configure custom schedule, for a one hour window starting on Saturdays at midnight (UTC), use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --maintenance-window Wed
```

---
## Steps to view upcoming maintenance

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.
 
1. On the server **Overview** page, review the **Next maintenance** field. If upcoming maintenance is available, the **Next maintenance** field displays the scheduled maintenance time. 
    
    :::image type="content" source="./media/configure-maintenance/next-maintenance-date.png" alt-text="Screenshot showing the next maintenance date." lightbox="./media/configure-maintenance/next-maintenance-date.png":::

1. Select the **Next maintenance** value to open the **Maintenance** page.

1. On the **Maintenance** page, review the **Maintenance status** section. That section shows upcoming maintenance events that apply to your server, including the scheduled time, status, maintenance type, and available actions.

    :::image type="content" source="./media/configure-maintenance/upcoming-maintenance.png" alt-text="Screenshot showing upcoming maintenance." lightbox="./media/configure-maintenance/upcoming-maintenance.png":::

## Steps to reschedule maintenance to a future date

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Maintenance**.

1. In the **Maintenance status** section, review the upcoming maintenance event.

1. If the event is eligible, select **Reschedule**.
    
    :::image type="content" source="./media/configure-maintenance/reschedule-button.png" alt-text="Screenshot showing the reschedule maintenance button." lightbox="./media/configure-maintenance/reschedule-button.png":::

1. Choose an eligible future date and time. Only dates and times that meet the service rules and your maintenance policy are available for selection.

    :::image type="content" source="./media/configure-maintenance/choose-eligible-reschedule-date-time.png" alt-text="Screenshot showing eligible reschedule date and time to choose from." lightbox="./media/configure-maintenance/choose-eligible-reschedule-date-time.png":::

1. Select **Reschedule** to confirm the new maintenance time.

    :::image type="content" source="./media/configure-maintenance/initiate-reschedule.png" alt-text="Screenshot showing reschedule to initiate rescheduling." lightbox="./media/configure-maintenance/initiate-reschedule.png":::

1. After confirmation, review the **Maintenance status** section to verify that the new start time is displayed. The portal shows a confirmation after the maintenance event is successfully rescheduled.

    :::image type="content" source="./media/configure-maintenance/reschedule-successful.png" alt-text="Screenshot showing reschedule successful." lightbox="./media/configure-maintenance/reschedule-successful.png":::

### Troubleshooting

#### The Reschedule button isn't available

The **Reschedule** action appears only when there's an upcoming maintenance event and the event is eligible for rescheduling. Some events aren't eligible, especially if they're required for critical security or compliance reasons.

#### I can't select the date or time I want

You can select only eligible future maintenance slots. The selected time must be within the allowed reschedule window and must comply with the server maintenance policy.

#### I receive an error that the maintenance window is locked

Rescheduling isn't available starting 15 minutes before the initially scheduled maintenance time. This lock-in period helps maintain service reliability as the maintenance workflow prepares to start.

#### I receive an error that maintenance can't be rescheduled or applied now because the custom maintenance window was configured after the event was scheduled 

Rescheduling is available only for flexible servers that are already on a custom maintenance schedule. Any changes to the maintenance schedule take effect on the next maintenance event.

## Steps to apply maintenance on demand

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Maintenance**.

1. In the **Maintenance status** section, review the upcoming maintenance event.

1. If the event is eligible, select **Reschedule** followed by **Apply now**.

    :::image type="content" source="./media/configure-maintenance/apply-now-button.png" alt-text="Screenshot showing apply maintenance now button." lightbox="./media/configure-maintenance/apply-now-button.png":::

1. Review the confirmation message. The confirmation dialog explains that maintenance starts immediately and that the server might restart during the maintenance process.

1. Select **Yes - Apply Maintenance Now** to start maintenance.

    :::image type="content" source="./media/configure-maintenance/apply-now-confirmation-dialog.png" alt-text="Screenshot showing apply maintenance now confirmation dialog box." lightbox="./media/configure-maintenance/apply-now-confirmation-dialog.png":::

1. Monitor the **Maintenance status** section. The maintenance event status updates as the workflow progresses. When maintenance completes, the status changes to **Complete** and it moves to the maintenance history section.

    :::image type="content" source="./media/configure-maintenance/applying-maintenance-now.png" alt-text="Screenshot showing applying maintenance now." lightbox="./media/configure-maintenance/applying-maintenance-now.png":::

## Steps to view maintenance history

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Maintenance**.

1. On the **Maintenance** page, review the **Maintenance history** section.

    :::image type="content" source="./media/configure-maintenance/maintenance-history-section.png" alt-text="Screenshot showing maintenance history section." lightbox="./media/configure-maintenance/maintenance-history-section.png":::

1. Select a maintenance event Tracking ID to view more details, such as the maintenance type, start time, end time, and final status.

    :::image type="content" source="./media/configure-maintenance/maintenance-history-tracking-id.png" alt-text="Screenshot showing maintenance event tracking ID." lightbox="./media/configure-maintenance/maintenance-history-tracking-id.png":::

1. Select **Export to CSV** to download maintenance history.

    :::image type="content" source="./media/configure-maintenance/export-to-csv.png" alt-text="Screenshot showing export maintenance history to csv." lightbox="./media/configure-maintenance/export-to-csv.png":::


> [!NOTE]
> If no past maintenance events are available for the server, the maintenance history section might be empty.

## Notifications about scheduled maintenance events
 
You can use Azure Service Health to [view notifications](/azure/service-health/service-health-planned-maintenance) about upcoming and performed scheduled maintenance on your Azure Database for PostgreSQL flexible server.

You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.

## Related content

- [Download PostgreSQL server logs and major version upgrade logs](../monitor/how-to-configure-server-logs.md).
- [Create alerts on metrics using portal](../monitor/../monitor/how-to-alert-on-metrics.md).
- [Configure and access logs](../monitor/how-to-configure-and-access-logs.md)
