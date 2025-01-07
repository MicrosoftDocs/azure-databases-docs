---
title: Configure capture of server logs
description: This article describes how to configure, list, and download PostgreSQL server logs and major version upgrade logs.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 01/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn about how to configure my Azure Database for PostgreSQL flexible server, so that I can download PostgreSQL server logs and major version upgrade logs for further inspection.
---

# Configure capture of PostgreSQL server logs and major version upgrade logs

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You can use PostgreSQL server logs and major version upgrade logs to troubleshoot and diagnose specific behaviors of an instance of Azure Database for PostgreSQL flexible server, and to gain detailed insights into the activities that have run on your servers.

By default, capturing server logs for download in an Azure Database for PostgreSQL flexible server is disabled. However, after you enable the feature, your Azure Database for PostgreSQL flexible server starts capturing those server logs to files which you can download for detailed inspection. You can use Azure portal or Azure CLI commands to list and  download these files that can assist you with any troubleshooting efforts.

This article explains how to enable and disable the feature. It also describes how you can list all available server logs, and how can you download any of them.

## Enable the capture of PostgreSQL server logs and major version upgrade logs for download

### [Portal](#tab/portal-enable-capture-of-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-disabled.png" alt-text="Screenshot showing the Server logs page." lightbox="./media/how-to-configure-server-logs/server-logs-page-disabled.png":::

3. Under **Download server logs**, mark the **Enable** checkbox.

    :::image type="content" source="./media/how-to-configure-server-logs/enable-server-logs.png" alt-text="Screenshot showing how to configure the server so that PostgreSQL server logs and major version upgrade logs are captured, so that you can download them for inspection." lightbox="./media/how-to-configure-server-logs/enable-server-logs.png":::

4. By default, log files are retained for 3 days, but you can adjust the retention period from 1 to 7 days. Use the **Retention period (in days)** slicer to adjust to your desired configuration.

    :::image type="content" source="./media/how-to-configure-server-logs/adjust-retention.png" alt-text="Screenshot showing how to adjust the retention period for PostgreSQL server logs and major version upgrade logs captured." lightbox="./media/how-to-configure-server-logs/adjust-retention.png":::

5. Select the **Save** button.

    :::image type="content" source="./media/how-to-configure-server-logs/save-changes.png" alt-text="Screenshot showing how to save configuration changes made to Server logs page." lightbox="./media/how-to-configure-server-logs/save-changes.png":::

6. A notification informs you that the service is configuring the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-server-logs/notification-configuring.png":::

7. Once the operation ends, a notification informs you that the service has completed the configuration of the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-server-logs/notification-configured.png":::

### [CLI](#tab/cli-enable-capture-of-logs)

You can enable the capture of PostgreSQL server logs and major version upgrade logs, to be able to download them for inspection, via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

To enable the capture of the logs for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter --resource-group <resource_group> --server-name <server> --name logfiles.download_enable --value on
```

To adjust the retention period for the logs that have been captured for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter --resource-group <resource_group> --server-name <server> --name logfiles.retention_days --value <retention_period_in_days>
```

Allowed values for server parameter `logfiles.retention_days` can be between 1 and 7 days. If you try to set it to a different value, you'll get this error:

```output
Code: ServerParameterToCMSUnAllowedParameterValue
Message: The value: [<value>] of Server Parameter: [logfiles.retention_days] is invalid, the allowed values are: [1-7]
```

---

> [!NOTE]
> Initially, and for approximately one hour, server logs occupy data disk space. Then, they're moved to backup storage and kept there for the configured retention period.


## Disable the capture of PostgreSQL server logs and major version upgrade logs for download

### [Portal](#tab/portal-disable-capture-of-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled.png" alt-text="Screenshot showing the Server logs page." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled.png":::

3. Under **Download server logs**, clear the **Enable** checkbox.

    :::image type="content" source="./media/how-to-configure-server-logs/disable-server-logs.png" alt-text="Screenshot showing how to configure the server so that PostgreSQL server logs and major version upgrade logs stop being captured for download." lightbox="./media/how-to-configure-server-logs/disable-server-logs.png":::

4. Select the **Save** button.

    :::image type="content" source="./media/how-to-configure-server-logs/save-changes.png" alt-text="Screenshot showing how to save configuration changes made to Server logs page." lightbox="./media/how-to-configure-server-logs/save-changes.png":::

5. A notification informs you that the service is configuring the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-server-logs/notification-configuring.png":::

6. Once the operation ends, a notification informs you that the service has completed the configuration of the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-server-logs/notification-configured.png":::

### [CLI](#tab/cli-disable-capture-of-logs)

You can disable the capture of PostgreSQL server logs and major version upgrade logs via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

To disable the capture of the logs for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter --resource-group <resource_group> --server-name <server> --name logfiles.download_enable --value off
```

---

## Download Server logs

To download server logs, perform the following steps.

> [!Note]
> After enabling logs, the log files will be available to download after few minutes.

1. Under **Name**, select the log file you want to download, and then, under **Action**, select **Download**.

    :::image type="content" source="./media/how-to-server-logs-portal/3-how-to-server-log.png" alt-text="Screenshot showing Server Logs - Download.":::

2. To download multiple log files at one time, under **Name**, select the files you want to download, and then above **Name**, select **Download**.

    :::image type="content" source="./media/how-to-server-logs-portal/4-how-to-server-log.png" alt-text="Screenshot showing server Logs - Download all.":::

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Restart an instance of Azure Database for PostgreSQL flexible server](how-to-restart-server.md).
- [Start an instance of Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an instance of Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Restart an instance of Azure Database for PostgreSQL flexible server](how-to-restart-server.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
