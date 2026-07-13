---
title: Restore a Deleted Server in Azure Database for PostgreSQL Flexible Server
description: Restore a deleted Azure Database for PostgreSQL flexible server within five days of deletion using the Azure portal or CLI. Follow these instructions to restore your deleted server backup.
#customer intent: As a user, I want to learn how to restore a deleted Azure Database for PostgreSQL flexible server.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/05/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
ai-usage: ai-assisted
---

# Restore a deleted server in Azure Database for PostgreSQL flexible server

When you delete a server, the service retains its Azure Database for PostgreSQL flexible server backup for five days. You can only access and restore that backup from the Azure subscription where the server originally resided.

To recover a deleted Azure Database for PostgreSQL flexible server within five days from the time it was deleted, follow the recommended steps. These steps only work if the backup for the server is still available and not deleted from the system. While restoring a deleted server often succeeds, it isn't always guaranteed, as restoring a deleted server depends on several other factors.

## Prerequisites

To restore a deleted Azure Database for PostgreSQL flexible server, you need the following items:
- Access to the Azure subscription that hosted the server before you deleted it.
- Location where the server existed.
- Use 2025-08-01 version of the [Servers - Create or Update](/rest/api/postgresql/servers/create-or-update?view=rest-postgresql-2025-08-01&tabs=HTTP) REST API.

## Steps to restore a deleted server

Use the [Azure portal](https://portal.azure.com/):

1. Search for the **Monitor** service. In the resource menu, select **Activity log**.

1. In the activity log page, set **Subscription** to the subscription that hosted your server, and select **Add filter** to set  **Operation** to **Delete PostgreSQL server (Microsoft.DBforPostgreSQL/flexibleServers/delete)**.

    :::image type="content" source="media/how-to-restore-deleted-server/activity-log-filtered.png" alt-text="Screenshot showing activity log filtered for the subscription where the deleted server existed and for the Delete PostgreSQL server operation." lightbox="media/how-to-restore-deleted-server/activity-log-filtered.png":::

1. Select the **Delete PostgreSQL Server** event, and then select the **JSON** tab. Scroll until you find the `resourceId` and `submissionTimestamp` attributes in the JSON output. The `resourceId` is in the following format: `/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/example-resource-group/providers/Microsoft.DBforPostgreSQL/flexibleServers/example-deleted-server`.

    :::image type="content" source="media/how-to-restore-deleted-server/deleted-server-resource-identifier.png" alt-text="Screenshot showing activity log JSON from where the necessary attributes to restore the deleted server can be retrieved." lightbox="media/how-to-restore-deleted-server/deleted-server-resource-identifier.png":::

1. Browse to the Azure Database for PostgreSQL flexible server [Create Server REST API Page](/rest/api/postgresql/servers/create-or-update?view=rest-postgresql-2025-08-01&tabs=HTTP) and select the **Try It** button. Sign in with your Azure account.

1. Provide the values for **resourceGroupName** (previously created resource group where you want the restored server to be created), **serverName** (name of the newly restored server, which doesn't have to match the name of the originally deleted server), and **subscriptionId** (must match the subscription where the deleted server existed, which you can get from the `resourceId` attribute in the JSON inspected earlier).

1. In the **Body** section, paste the following JSON and replace the value of `<original-deleted-server-location>` with the location where the deleted server existed (for example, CanadaCentral, CentralUS, EastUS, and so on), `<value-copied-from-submissionTimestamp>` with the value retrieved from `submissionTimestamp` in the JSON inspected on the Activity log event, and `<value-copied-from-resourceId>` with the value retrieved from `resourceId` in that same JSON.

  ```json
    {
      "location": "<original-deleted-server-location>",
      "properties":
      {
        "createMode": "ReviveDropped",
        "pointInTimeUTC": "<value-copied-from-submissionTimestamp>",
        "sourceServerResourceId": "<value-copied-from-resourceId>"
      }
    }
  ```
    
  Ensure that you change three parameters (`location`, `pointInTimeUTC`, `sourceServerResourceId`) as per your restore requirements. 
  
  ```json
  {
    "location": "CanadaCentral",
    "properties": {
      "createMode": "ReviveDropped",
      "pointInTimeUTC": "2026-06-09T06:08:02Z",
      "sourceServerResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/example-restored-resource-group/providers/Microsoft.DBforPostgreSQL/flexibleServers/example-deleted-server"
    }
  }
  ```

  > [!IMPORTANT]  
  > There's a time limit of five days after the server is deleted. After five days, an error occurs because the backup can't be found.

If you see Response Code 201 or 202, the restore request is successfully submitted.

  The server creation can take time depending on the database size and compute resources provisioned on the original server. You can monitor the restore status from Activity log if you filter by:
  - **Subscription**: Subscription where you're restoring the deleted server.
  - **Resource Type**: Azure Database for PostgreSQL flexible servers (Microsoft.DBforPostgreSQL/flexibleServers).
  - **Operation**: Update PostgreSQL Server Create.

## Restore a deleted virtual network enabled server

Restoring a deleted virtual network enabled server requires specifying other network properties, such as the resource identifiers of the delegated subnet and the private DNS zone. Follow the steps in the following section to restore your server with the necessary network configurations.

  ```json
  {
    "location": "EastUS",
    "properties": {
      "createMode": "ReviveDropped",
      "pointInTimeUTC": "2026-06-09T06:08:02Z",
      "sourceServerResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/example-restored-resource-group/providers/Microsoft.DBforPostgreSQL/flexibleServers/example-deleted-server",
      "network": {
        "delegatedSubnetResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/example-restored-resource-group/providers/Microsoft.Network/virtualNetworks/example-virtual-network/subnets/example-subnet",
        "privateDnsZoneArmResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/example-restored-resource-group/providers/Microsoft.Network/privateDnsZones/example-private-dns-zone"
      }
    }
  }
  ```

## Common errors

If you use the incorrect API version, restore failures or timeouts can occur. Use version 2025-08-01 to avoid these problems.

To avoid potential DNS errors, use a different name when you initiate the restore process. Some restore operations might fail if you use the same name.

## Related content

[Resource locks](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/preventing-the-disaster-of-accidental-deletion-for-your-PostgreSQL/ba-p/825222)