---
title: Schedule maintenance
description: This article describes how to schedule maintenance of an Azure Database for PostgreSQL flexible server instance.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
#customer intent: As a user, I want to learn how to schedule maintenance of an Azure Database for PostgreSQL flexible server instance.
---

# Schedule maintenance

You can specify scheduled maintenance options for each Azure Database for PostgreSQL flexible server instance in your Azure subscription. Options include the type of scheduled maintenance and notification settings for upcoming and finished maintenance events.

## Steps to schedule maintenance

### [Portal](#tab/portal-maintenance-settings)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Maintenance**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/maintenance.png" alt-text="Screenshot showing the Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/maintenance.png":::

3. If you select **System-managed schedule**, the system automatically assigns a random day of the week, and a 60-minute window which begins somewhere between 11pm and 7am (local server time).

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/system-managed-schedule.png" alt-text="Screenshot showing the selection of system managed schedule in Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/system-managed-schedule.png":::

4. If you want to have more granular control, select **Custom schedule**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/custom-schedule.png" alt-text="Screenshot showing the selection of custom schedule in Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/custom-schedule.png":::

5. Select a preferred day of the week, and a start time for the 60-minute window in which you want maintenance to occur.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/day-time.png" alt-text="Screenshot showing the selection of custom day of the week and start time for the maintenance window." lightbox="./media/how-to-configure-scheduled-maintenance/day-time.png":::

5. Select **Save**.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/save-changes-enable.png" alt-text="Screenshot showing how to save configuration changes made to Maintenance page." lightbox="./media/how-to-configure-scheduled-maintenance/save-changes-enable.png":::

6. A notification informs you that the service is updating the maintenance window settings.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-scheduled-maintenance/notification-configuring.png":::

7. Once the operation ends, a notification informs you that the service completed the update of the maintenance window settings.

    :::image type="content" source="./media/how-to-configure-scheduled-maintenance/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-scheduled-maintenance/notification-configured.png":::

### [CLI](#tab/cli-maintenance-settings)

You can configure the maintenance schedule settings via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

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

## Notifications about scheduled maintenance events
 
You can use Azure Service Health to [view notifications](/azure/service-health/service-notifications) about upcoming and performed scheduled maintenance on your Azure Database for PostgreSQL flexible server instance.

You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.

## Related content

- [Download PostgreSQL server logs and major version upgrade logs](../monitor/how-to-configure-server-logs.md).
- [Create alerts on metrics using portal](../monitor/../monitor/how-to-alert-on-metrics.md).
- [Configure and access logs](../monitor/how-to-configure-and-access-logs.md)
