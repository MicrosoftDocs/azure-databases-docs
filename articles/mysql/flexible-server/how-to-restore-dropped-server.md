---
title: Restore a Deleted Server
description: This article describes how to restore a deleted server in Azure Database for MySQL - Flexible Server by using the Azure portal.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 02/25/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Restore a deleted Azure Database for MySQL

When an Azure Database for MySQL Flexible Server instance is deleted, the server backup can be retained for up to five days in the service. The server backup can be accessed and restored only from the Azure subscription where the server initially resided. The following recommended steps can be followed to recover a deleted Azure Database for MySQL Flexible Server resource within five days from the time of server deletion. The recommended steps work only if the backup for the server is still available and not deleted from the system.

## Prerequisites

To restore a deleted Azure Database for MySQL Flexible Server instance, you need the following:
- Azure Subscription name hosting the original server
- Location where the server was created

- The resource group where the deleted server previously resided must exist. If it no longer exists, it’s recommended to create a new resource group with the same name before attempting the restore

## Restore steps

1. Go to the [Activity Log](https://portal.azure.com/#blade/Microsoft_Azure_ActivityLog/ActivityLogBlade) from the Monitor page in Azure portal.

1. In the Activity Log, select **Add filter** as shown and set the following filters for the:
    1. **Subscription** = Your Subscription hosting the deleted server
    1. **Resource Type** = Azure Database for MySQL Flexible Server (Microsoft.DBforMySQL/flexibleServers)
    1. **Operation** = Delete MySQL Server (Microsoft.DBforMySQL/flexibleServers/delete)

    :::image type="content" source="media/how-to-restore-dropped-server/monitor-log-delete-server.png" alt-text="Screenshot of Activity Log filtered for delete MySQL server operation." lightbox="media/how-to-restore-dropped-server/monitor-log-delete-server.png":::

1. Select the **Delete MySQL Server** event, select the JSON tab, and note the "resourceId" and "submissionTimestamp" attributes in JSON output. The resourceId is in the following format: `/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/TargetResourceGroup/providers/Microsoft.DBforMySQL/flexibleServers/deletedserver`. 

1. Go to [Create Server REST API Page](/rest/api/mysql/flexibleserver/servers/create) and select "Try It" tab highlighted in green and sign in with your Azure account. The Azure Resource Manager URL varies by the Azure environment. Verify you're using the correct one by referring to the [Azure Resource Manager environment URLs](#azure-resource-manager-environment-urls) section.

1. Provide the resourceGroupName, serverName (deleted Azure Database for MySQL Flexible Server instance name), and subscriptionId, derived from the "resourceId" attribute captured in Step 3. At the same time, the version is prepopulated, as shown in the image.

    :::image type="content" source="media/how-to-restore-dropped-server/server-create-rest-api.png" alt-text="Screenshot of Create server using REST API." lightbox="media/how-to-restore-dropped-server/server-create-rest-api.png":::

1. Scroll below on the Request Body section and paste the following:

    ```json
       {
           "location": "Dropped Server Location",
           "properties":
        {
                   "restorePointInTime": "submissionTimestamp - 15 minutes",
                   "createMode": "PointInTimeRestore",
                   "sourceServerResourceId": "resourceId"
        }
       }
    ```
    
1. Replace the following values in the request body above:
    1. **Dropped server Location** with the Azure region where the deleted server was created
    1. `submissionTimestamp` and `resourceId` with the values captured in Step 3.
    1. For `restorePointInTime`, specify a value of `submissionTimestamp` minus **15 minutes** to ensure the command doesn't error out.

1. If you see Response Code 201 or 202, the restore request is successfully submitted.

1. The server creation can take time, depending on the database size and computing resources provided on the original server. The restore status can be monitored from:
    1. Activity log by filtering for:
        1. **Subscription** = Your Subscription
        1. **Resource Type** = Azure Database for MySQL Flexible Server (Microsoft.DBforMySQL/flexibleServers)
        1. **Operation** = Update MySQL Server Create

## Azure Resource Manager environment URLs

The Azure Resource Manager URL varies by the Azure environment.

- For Azure Global, the URL is `https://management.azure.com`.
- For Azure Government, the URL is `https://management.usgovcloudapi.net/`.
- For Azure Germany, the URL is `https://management.microsoftazure.de/`.
- For Microsoft Azure operated by 21Vianet, the URL is `https://management.chinacloudapi.cn`.

## Next step

> [!div class="nextstepaction"]
> [Resource Locks](https://techcommunity.microsoft.com/blog/adformysql/preventing-the-disaster-of-accidental-deletion-for-your-mysql-database-on-azure/825222)
