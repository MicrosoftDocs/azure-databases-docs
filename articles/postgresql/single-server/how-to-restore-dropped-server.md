---
title: Restore a dropped Azure Database for PostgreSQL server
description: This article describes how to restore a dropped server in Azure Database for PostgreSQL using the Azure portal.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 09/18/2024
ms.service: azure-database-postgresql
ms.subservice: single-server
ms.topic: how-to
---

# Restore a dropped Azure Database for PostgreSQL server

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

[!INCLUDE [azure-database-for-postgresql-single-server-deprecation](../includes/azure-database-for-postgresql-single-server-deprecation.md)]

When a server is dropped, the database server backup is retained for five days in the service. The database backup can be accessed and restored only from the Azure subscription where the server originally resided. The following recommended steps can be followed to recover a dropped PostgreSQL server resource within five days from the time of server deletion. The recommended steps work only if the backup for the server is still available and not deleted from the system.

## Prerequisites

To restore a dropped Azure Database for PostgreSQL server:
- Azure Subscription name hosting the original server
- Location where the server was created

## Steps to restore

1. Browse to the [Azure portal](https://portal.azure.com/#blade/Microsoft_Azure_ActivityLog/ActivityLogBlade). Select the **Azure Monitor** service, then select **Activity Log**.

1. In Activity Log, select **Add filter** as shown and set filters for the following:

    - **Subscription** = Your Subscription hosting the deleted server
    - **Resource Type** = Azure Database for PostgreSQL servers (Microsoft.DBforPostgreSQL/servers)
    - **Operation** = Delete PostgreSQL Server (Microsoft.DBforPostgreSQL/servers/delete)

    :::image type="content" source="media/how-to-restore-dropped-server/activity-log-azure.png" alt-text="Screenshot of Activity log filtered for delete PostgreSQL server operation." lightbox="media/how-to-restore-dropped-server/activity-log-azure.png":::

1. Select the **Delete PostgreSQL Server** event, then select the **JSON tab**. Copy the `resourceId` and `submissionTimestamp` attributes in JSON output. The resourceId is in the following format: `/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/TargetResourceGroup/providers/Microsoft.DBforPostgreSQL/servers/deletedserver`.

1. Browse to the PostgreSQL [Create Server REST API Page](/rest/api/postgresql/singleserver/servers/create) and select the **Try It** tab highlighted in green. Sign in with your Azure account.

1. Provide the **resourceGroupName**, **serverName** (deleted server name), **subscriptionId** properties, based on the resourceId attribute JSON value captured in the preceding step 3. The api-version property is prepopulated and can be left alone.

1. Scroll below on Request Body section and paste the following replacing the "Dropped server Location" (for example, CentralUS, EastUS etc.), "submissionTimestamp", and "resourceId". For "restorePointInTime", specify a value of "submissionTimestamp" minus **15 minutes** to ensure the command doesn't error out.

    ```json
    {
      "location": "Dropped Server Location",
      "properties":
      {
        "restorePointInTime": "submissionTimestamp - 15 minutes",
        "createMode": "PointInTimeRestore",
        "sourceServerId": "resourceId"
      }
    }
    ```

    For example, if the current time is 2020-11-02T23:59:59.0000000Z, we recommend a minimum of 15 minutes prior restore point in time 2020-11-02T23:44:59.0000000Z. See below example and ensure that you're changing three parameters (location,restorePointInTime,sourceServerId) as per your restore requirements.

    ```json
    {
      "location": "EastUS",
      "properties":
      {
        "restorePointInTime": "2020-11-02T23:44:59.0000000Z",
        "createMode": "PointInTimeRestore",
        "sourceServerId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/SourceResourceGroup/providers/Microsoft.DBforPostgreSQL/servers/sourceserver"
      }
    }
    ```

1. If you see Response Code 201 or 202, the restore request is successfully submitted.

    The server creation can take time depending on the database size and compute resources provisioned on the original server. The restore status can be monitored from Activity log by filtering for
   - **Subscription** = Your Subscription
   - **Resource Type** = Azure Database for PostgreSQL servers (Microsoft.DBforPostgreSQL/servers)
   - **Operation** = Update PostgreSQL Server Create

## Troubleshooting

If you encounter any issues during the restore process, ensure that the `resourceId` and `submissionTimestamp` values are correct and that the backup is still available within the five-day retention period.

## Next step

> [!div class="nextstepaction"]
> [Resource Locks](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/preventing-the-disaster-of-accidental-deletion-for-your-PostgreSQL/ba-p/825222)
