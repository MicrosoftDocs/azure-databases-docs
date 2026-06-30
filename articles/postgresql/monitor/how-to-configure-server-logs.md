---
title: Download PostgreSQL and upgrade logs
description: This article describes how to configure, list, and download PostgreSQL and upgrade logs.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 06/26/2025
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
# customer intent: As a user, I want to learn how to configure, list, and download PostgreSQL and upgrade logs.
---

# Download PostgreSQL and upgrade logs

You can use PostgreSQL server logs to diagnose specific issues experienced in an Azure Database for PostgreSQL flexible server, and to gain detailed insights about the activities that run on your servers. Use major version upgrade logs to troubleshoot errors that might occur during an attempt to upgrade your server to a higher major version of PostgreSQL.

By default, capturing server logs for download in an Azure Database for PostgreSQL flexible server is disabled. However, after you enable the feature, your Azure Database for PostgreSQL flexible server starts capturing the server logs to files, which you can download for detailed inspection. Use the Azure portal or Azure CLI commands to list and download these files that can assist you with any troubleshooting efforts.

This article explains how to enable and disable the feature. It also describes how you can list all available server logs, and how you can download any of them.

## Steps to enable the capture of PostgreSQL and upgrade logs for download

### [Portal](#tab/portal-enable-capture-of-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-disabled.png" alt-text="Screenshot showing the Server logs page." lightbox="./media/how-to-configure-server-logs/server-logs-page-disabled.png":::

1. Select the **Capture logs for download** checkbox.

    :::image type="content" source="./media/how-to-configure-server-logs/enable-server-logs.png" alt-text="Screenshot showing how to configure the server for PostgreSQL server logs and major version upgrade logs to be captured. You can download captured log files for inspection." lightbox="./media/how-to-configure-server-logs/enable-server-logs.png":::

1. By default, the service retains log files for three days, but you can adjust the retention period from one to seven days. Use the **Log retention period (in days)** slicer to set your desired configuration.

    :::image type="content" source="./media/how-to-configure-server-logs/adjust-retention.png" alt-text="Screenshot showing how to adjust the retention period for PostgreSQL server logs and major version upgrade logs captured." lightbox="./media/how-to-configure-server-logs/adjust-retention.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-configure-server-logs/save-changes-enable.png" alt-text="Screenshot showing how to save configuration changes made to Server logs page." lightbox="./media/how-to-configure-server-logs/save-changes-enable.png":::

1. A notification informs you that the service is configuring the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-server-logs/notification-configuring.png":::

1. When the operation finishes, a notification informs you that the service completed the configuration of the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-server-logs/notification-configured.png":::

### [CLI](#tab/cli-enable-capture-of-logs)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to turn on capturing PostgreSQL server logs and major version upgrade logs.

To enable the capture of the logs for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name logfiles.download_enable \
  --value on
```

To adjust the retention period for the logs that are captured for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name logfiles.retention_days \
  --value <retention_period_in_days>
```

Allowed values for parameter `logfiles.retention_days` are between 1 and 7 days. If you try to set it to a different value, you get this error:

```output
Code: ServerParameterToCMSUnAllowedParameterValue
Message: The value: [<value>] of Parameter: [logfiles.retention_days] is invalid, the allowed values are: [1-7]
```

---

> [!NOTE]
> * A few minutes after enabling the capture of server logs for download, the first log is available for download.
>
> * Initially, and for approximately one hour, server logs occupy data disk space. Then, they're moved to backup storage and kept there for the configured retention period.


## Steps to disable the capture of PostgreSQL and upgrade logs for download

### [Portal](#tab/portal-disable-capture-of-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png" alt-text="Screenshot showing the Server logs page." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png":::

1. Clear the **Capture logs for download** checkbox.

    :::image type="content" source="./media/how-to-configure-server-logs/disable-server-logs.png" alt-text="Screenshot showing how to configure the server so that PostgreSQL server logs and major version upgrade logs stop being captured for download." lightbox="./media/how-to-configure-server-logs/disable-server-logs.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-configure-server-logs/save-changes-disable.png" alt-text="Screenshot showing how to save configuration changes made to Server logs page." lightbox="./media/how-to-configure-server-logs/save-changes-disable.png":::

1. A notification informs you that the service is configuring the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configuring.png" alt-text="Screenshot showing the notification informing that configuration changes are being applied." lightbox="./media/how-to-configure-server-logs/notification-configuring.png":::

1. When the operation finishes, a notification informs you that the service completed the configuration of the capture of logs for download.

    :::image type="content" source="./media/how-to-configure-server-logs/notification-configured.png" alt-text="Screenshot showing the notification informing that configuration changes were successfully applied." lightbox="./media/how-to-configure-server-logs/notification-configured.png":::

### [CLI](#tab/cli-disable-capture-of-logs)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to disable the capture of PostgreSQL server logs and major version upgrade logs.

To disable the capture of the logs for download, use this command:

```azurecli-interactive
az postgres flexible-server parameter \
  --resource-group <resource_group> \
  --server-name <server> \
  --name logfiles.download_enable \
  --value off
```

---

## Steps to list captured logs available for download

### [Portal](#tab/portal-list-captured-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png" alt-text="Screenshot showing the Server logs page with some logs captured." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png":::

1. A table shows all captured log files that aren't deleted yet. You can't see or access files that were captured but deleted because they exceeded the configured retention period. Use the **Search for files with names that contain**, **Time range**, and **Log type** boxes to filter the logs. By selecting a column header, you can sort the list of visible log files, in ascending or descending order, by the value of the attribute represented by the selected header. Under each available column, you can see the different attributes of each file:
    - **Name**: Name of the log file. The service assigns each log file a name with this pattern `postgresql_yyyy_mm_dd_hh_00_00.log`.
    - **Last update time**: Timestamp of the last time each log file was uploaded. Log files are uploaded, approximately, every 10 minutes.
    - **Size**: Size in bytes occupied by the log file.
    - **Log type**: **Server log** indicates the file corresponds to a PostgreSQL server log. **Upgrade log** indicates the file corresponds to a major version upgrade log.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-filter-sort.png" alt-text="Screenshot showing the Server logs page with some logs captured and highlighting column headers." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-filter-sort.png":::

1. The table doesn't automatically update. To see the most recent information, select **Refresh**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-refresh.png" alt-text="Screenshot showing the Server logs page and highlighting the Refresh button to update the contents of the page." lightbox="./media/how-to-configure-server-logs/server-logs-page-refresh.png":::

### [CLI](#tab/cli-list-captured-logs)

Use the [az postgres flexible-server-logs list](/cli/azure/postgres/flexible-server/server-logs#az-postgres-flexible-server-server-logs-list) command to list the captured PostgreSQL server logs and major version upgrade logs.

To list all captured logs available for download that were updated in the last 72 hours (default value), use this command:

```azurecli-interactive
az postgres flexible-server-logs list \
  --resource-group <resource_group> \
  --server-name <server>
```

To list all captured logs available for download that were updated in the last 10 hours, use this command:

```azurecli-interactive
az postgres flexible-server server-logs list \
  --resource-group <resource_group> \
  --server-name <server> \
  --file-last-written 10
```

To list all captured logs available for download whose size is under 30 KiB, use this command:

```azurecli-interactive
az postgres flexible-server-logs list \
  --resource-group <resource_group> \
  --server-name <server> \
  --max-file-size 30
```

To list all captured logs available for download whose name contains `01_07`, use this command:

```azurecli-interactive
az postgres flexible-server-logs list \
  --resource-group <resource_group> \
  --server-name <server> \
  --filename-contains 01_07
```

---

## Steps to download captured logs

### [Portal](#tab/portal-download-captured-logs)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Monitoring** section, select **Server logs**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png" alt-text="Screenshot showing the Server logs page with some logs captured." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured.png":::

1. A table shows all captured log files that aren't deleted yet. You can't see or access files that were captured but deleted because they exceeded the configured retention period. Use the **Search for files with names that contain**, **Time range**, and **Log type** boxes to filter the logs. By selecting a column header, you can sort the list of visible log files, in ascending or descending order, by the value of the attribute represented by the selected header. Find the log that you want to download and, under the **Actions** column, select **Download**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-download.png" alt-text="Screenshot showing the Server logs page with some logs captured and highlighting how to download one of them." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-download.png":::

1. If you want to download multiple log files at one time, select all the files that you want to download, and select **Download** in the toolbar.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-download-multiple.png" alt-text="Screenshot showing the Server logs page with some logs captured and highlighting how to download multiple files." lightbox="./media/how-to-configure-server-logs/server-logs-page-enabled-with-logs-captured-download-multiple.png":::

1. The table doesn't automatically update. To see the most recent information, select **Refresh**.

    :::image type="content" source="./media/how-to-configure-server-logs/server-logs-page-refresh.png" alt-text="Screenshot showing the Server logs page and highlighting the Refresh button to update the contents of the page." lightbox="./media/how-to-configure-server-logs/server-logs-page-refresh.png":::

### [CLI](#tab/cli-download-captured-logs)

Use the [az postgres flexible-server-logs download](/cli/azure/postgres/flexible-server/server-logs#az-postgres-flexible-server-server-logs-download) command to download the captured PostgreSQL server logs and major version upgrade logs.

To download a specific log, use the following command:

```azurecli-interactive
az postgres flexible-server-logs download \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <log_name>
```

To download a specific group of logs, use the following command:

```azurecli-interactive
az postgres flexible-server-logs download \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <log1_name log2_name ...logn_name>
```

> [!NOTE]
> * For the file names you provide, the command creates a local file with the same name and contents when log files with matching names are available to download.
> 
> * If you provide any file names that aren't available to download, the command doesn't report any error. It simply doesn't download that file.

---

## Related content

- [Configure high availability](../high-availability/how-to-configure-high-availability.md).
- [Configure scheduled maintenance](../configure-maintain/how-to-configure-scheduled-maintenance.md).
- [Create alerts on metrics using portal](how-to-alert-on-metrics.md).

