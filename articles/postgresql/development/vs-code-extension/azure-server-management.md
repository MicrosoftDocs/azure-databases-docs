---
title: Azure Server Management
titleSuffix: PostgreSQL extension for Visual Studio Code
description: "Manage supported Azure Database for PostgreSQL resources from Visual Studio Code: flexible server lifecycle, network access, parameters, backups, restore, clone, and server logs, plus Azure HorizonDB (Preview) firewall rules."
author: mmcfarland
ms.author: mmcfarland
ms.reviewer: nachoalonsoportillo, maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to manage Azure Database for PostgreSQL resources from Visual Studio Code, so that I can handle server operations without switching tools.
---

# Azure server management

The PostgreSQL extension for Visual Studio Code lets you manage supported Azure Database for PostgreSQL resources directly from Visual Studio Code. After you connect to an Azure Database for PostgreSQL flexible server, you can open the **server dashboard** to control the server lifecycle, manage network access, change parameters, create or restore backups, clone the server, and download captured logs. Azure HorizonDB (Preview) connections support a smaller Network Configuration page for firewall rules.

> [!NOTE]  
> Most tasks in this article apply only to Azure Database for PostgreSQL flexible server connections. Azure HorizonDB (Preview) supports firewall-rule management only. Local PostgreSQL instances and Docker containers don't expose these Azure management pages.

> [!TIP]  
> If you still need to create the server or connect to it, start with [Create a PostgreSQL server](create-server.md) or [Connections and identity](connections.md).

## Open Azure management pages

1. In the **Connections** tree, connect to the Azure Database for PostgreSQL resource that you want to manage.
1. Right-click the server node and select **Dashboard**.
1. For Azure Database for PostgreSQL flexible server lifecycle actions, select **Actions** > **Start**, **Stop**, or **Restart** in the **server dashboard**.
1. To open Azure management pages, select **Server Settings**, then choose a supported page such as **Network Configuration**, **Server Parameters**, **Backups**, or **Server Logs**.

# [Visual Studio Code](#tab/vscode)

:::image type="content" source="azure-server-management/default-server-dashboard-default.png" alt-text="Screenshot of server dashboard showing Azure management entry points." lightbox="azure-server-management/default-server-dashboard-default.png":::

# [Cursor](#tab/cursor)

:::image type="content" source="azure-server-management/cursor-editor-server-dashboard-default.png" alt-text="Screenshot of server dashboard showing Azure management entry points." lightbox="azure-server-management/cursor-editor-server-dashboard-default.png":::

---

## Start, stop, or restart a server

You can run lifecycle actions from the **Actions** menu in the dashboard toolbar or from the server's context menu in the **Connections** tree.

### Start a server

1. In the **Connections** tree, right-click the server and select **Start server**, or open the dashboard and select **Actions** > **Start**.
1. Wait while the extension shows a progress notification and polls Azure for the operation result.
1. Confirm that the server returns to the **Ready** state before you reconnect or open management pages.

### Stop a server

1. In the **Connections** tree, right-click the server and select **Stop server**, or open the dashboard and select **Actions** > **Stop**.
1. In the confirmation dialog, select **Stop**.
1. Wait while the extension finishes the stop operation.
1. Reconnect after you start the server again.

> [!CAUTION]  
> Stopping the server disconnects the current **Connections** session. The extension closes the connection automatically after the stop operation finishes.

> [!NOTE]  
> When the server is stopped, Azure stops billing for compute, but storage charges still apply.

### Restart a server

If you save parameters that require a restart and select **Yes** in the restart prompt, the extension initiates the restart automatically. Use these steps when you want to restart the server yourself.

1. In the **Connections** tree, right-click the server and select **Restart server**, or open the dashboard and select **Actions** > **Restart**.
1. Wait while the extension restarts the server and refreshes the server state.
1. Continue working after the server returns to the **Ready** state.

## Manage network access

Open **Server Settings** > **Network Configuration** to manage network access.

| Platform | Supported Network Configuration settings |
| --- | --- |
| Azure Database for PostgreSQL flexible server | Firewall rules, public access, Azure services access, and broad IPv4 allow-list rules |
| Azure HorizonDB (Preview) | Firewall rules and Azure services access |

For Azure Database for PostgreSQL flexible server, the **Network Configuration** page disables firewall editing until public access is enabled. It also keeps **Save** disabled until you make a valid change. Azure HorizonDB (Preview) doesn't show public access controls, but does include the **Allow public access from any Azure service within Azure to this server** checkbox.

### Add or edit a firewall rule

1. Open **Server Settings** > **Network Configuration**.
1. For Azure Database for PostgreSQL flexible server, under **Public access**, turn on public access if it's currently off.
1. In the firewall rules table, use the empty row to enter a **Firewall rule name**, **Start IP address**, and **End IP address**, or update an existing row.
1. Select **Save**.

Use these validation rules when you edit a rule:

| Field | Requirement |
| --- | --- |
| **Firewall rule name** | Required, unique, 1-80 characters, letters, numbers, hyphens (`-`), and underscores (`_`) only |
| **Start IP address** | Required, valid IPv4 address |
| **End IP address** | Required, valid IPv4 address, and not lower than the start IP address |

> [!NOTE]  
> The page shows validation errors inline and blocks **Save** until every edited rule is valid.

### Allow your current client IP address

1. Open **Server Settings** > **Network Configuration**.
1. Under the firewall rules table, select the link that starts with **Add current client IP address**.
1. Review the inserted rule and select **Save**.

If the dashboard can't detect your public IP address, the link changes to **Unable to determine current IP address automatically**. Enter the address manually in the empty firewall-rule row instead.

### Configure broader access settings

Use these Azure Database for PostgreSQL flexible server options on the **Network Configuration** page when individual IP rules aren't enough:

| Option | Use it when |
| --- | --- |
| **Public access** | You want the server to accept connections over public IP addresses. |
| **Allow public access from any Azure service within Azure to this server** | You want Azure-hosted services to reach the server without adding each service IP range manually. |
| **Add 0.0.0.0 - 255.255.255.255** | You want to create a rule that allows any IPv4 address. Use this only in tightly controlled environments. |

> [!IMPORTANT]  
> Don't enter `0.0.0.0` for both the start and end IP addresses. The extension treats that range as invalid. If you want Azure-hosted services to connect, use **Allow public access from any Azure service within Azure to this server** instead.

> [!NOTE]  
> Azure HorizonDB (Preview) Network Configuration doesn't include public access, parameters, backups, server logs, clone, or lifecycle actions.

> [!TIP]  
> If the **Network Configuration** page shows an unavailable message for an Azure HorizonDB (Preview) connection because Azure identity information is missing, select **Fetch Metadata** on the page to retrieve it. This is the same metadata fetch available on the [Server dashboard](server-dashboard.md#azure-metadata-prompt).

## Change parameters

Open **Server Settings** > **Server Parameters** to search, filter, edit, and reset PostgreSQL parameters for the server.

### Find a parameter

1. Open **Server Settings** > **Server Parameters**.
1. Use the filter buttons such as **All**, **Modified**, **Static**, **Dynamic**, or **Read-Only** to narrow the list.
1. Use the text box to search by parameter name or description.
1. If you need a larger working set, change **Rows per page** to `25`, `50`, or `100`.
1. If you want to group similar settings before you edit them, sort a column.

### Save parameter changes

1. Open **Server Settings** > **Server Parameters**.
1. Find the parameter you want to change.
1. Edit the value directly in the **Value** column.
1. If the parameter shows an info button, hover it to review the allowed values.
1. Select **Save**.

If the parameter requires a restart, the page adds a **Pending Restart** row below the parameter. When you save one or more static parameters, the extension asks whether you want to restart the server immediately.

### Reset a parameter to the default value

1. Open **Server Settings** > **Server Parameters**.
1. Find the parameter you want to reset.
1. Select the reset icon next to the parameter.
1. Select **Save**.

## Manage backups

Open **Server Settings** > **Backups** to work with automatic and on-demand backups.

### Create an on-demand backup

1. Open **Server Settings** > **Backups**.
1. Select **Backup now**.
1. In **Create backup**, enter a **Backup name**.
1. Select **Create**.

Backup names can contain only letters, numbers, hyphens (`-`), and underscores (`_`).

> [!NOTE]  
> The page can disable **Backup now** while the server isn't in the **Ready** state, while another backup is already running, or when the current workload doesn't support manual backups.

### Restore from a backup

1. Open **Server Settings** > **Backups**.
1. Find the backup you want to use.
1. Select **Restore from this backup**.
1. Complete the restore workflow to create a new Azure Database for PostgreSQL flexible server from that backup.

### Delete an on-demand backup

1. Open **Server Settings** > **Backups**.
1. Find the on-demand backup you want to remove.
1. Select **Delete**.
1. In **Delete backup**, select **Delete** again to confirm.

Automatic backups stay managed by Azure and can't be deleted from the extension.

### Change backup retention

1. Open **Server Settings** > **Backups**.
1. Move the retention slider to the number of days you want.
1. Select **Save**.

You can also filter the backup list with **Automatic** or **On-demand**, narrow it with time filters such as **Last 24 hours** or **Last 7 days**, and sort the table by **Name**, **Status**, **Completion time**, **Retained until**, or **Type**.

## Clone a server

Use **Clone Server** when you want to create a new Azure Database for PostgreSQL flexible server based on the current server.

1. Open the dashboard.
1. Select **Server Settings** > **Clone Server**.
1. Complete the clone workflow to create the new server.

## Capture and download server logs

Open **Server Settings** > **Server Logs** to capture diagnostic logs and download them for troubleshooting.

### Turn log capture on or off

1. Open **Server Settings** > **Server Logs**.
1. Turn **Capture logs for download** on or off.
1. If log capture is on, set **Log retention period**.
1. Select **Save**.

### Filter and download log files

1. Open **Server Settings** > **Server Logs**.
1. Use **All types**, **Server log**, or **Upgrade log** to narrow the list.
1. Use the time filter or the filename search box to find the files you need.
1. Select one or more log files, or use the download button in a single row.
1. Select **Download**.

The log table supports sorting by **Name**, **Last modified**, **Size (KB)**, and **Type**. When more than 100 files match the current filters, the page shows pagination controls.

## Related content

- [Server dashboard](server-dashboard.md)
- [Create a PostgreSQL server](create-server.md)
- [Connections and identity](connections.md)
