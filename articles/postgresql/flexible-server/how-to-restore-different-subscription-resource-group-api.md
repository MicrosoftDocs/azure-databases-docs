---
title: Cross subscription and cross resource group restore - Azure REST API
description: This article describes how to restore to a different Subscription or resource group server in Azure Database for PostgreSQL - Flexible Server using  Azure REST API.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Cross subscription and cross resource group restore in Azure Database for PostgreSQL - Flexible Server using Azure REST API

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]
In this article, you learn how to restore an Azure Database for PostgreSQL flexible server instance to a different subscription or resource group using the REST API [Azure REST API](/rest/api/azure/). To learn more about backup and restore see the [overview](concepts-backup-restore.md).

## Prerequisites
An [Azure Database for PostgreSQL flexible server instance](quickstart-create-server-portal.md) to be the primary server.

### Restore to a different Subscription or Resource group

 1. Browse to the [Azure Database for PostgreSQL flexible server Create Server REST API Page](/rest/api/postgresql/flexibleserver/servers/create) and select the **Try It** tab highlighted in green. Sign in with your Azure account.

2. Provide the **resourceGroupName**(Target Resource group name), **serverName** (Target server name), **subscriptionId** (Target subscription) properties. Please use the latest api-version that is available. For this example we're using 2023-06-01-preview.

    ![Screenshot showing the REST API Try It page.](media/how-to-restore-server-portal/geo-restore-different-subscription-or-resource-group-api.png)



3. Go to **Request Body** section and paste the following replacing the "location" (e.g. CentralUS, EastUS etc.), "pointInTimeUTC", and ))"SourceServerResourceID", For "pointInTimeUTC", specify a timestamp value  to which you want to restore. Finally, you can use createMode as **PointInTimeRestore** for performing regular restore and **GeoRestore** for restoring geo-redundant backups.

 **GeoRestore**

```json
   {
  "location": "NorthEurope",  
  "properties": 
  {
    "pointInTimeUTC": "2023-10-03T16:05:02Z",
    "SourceServerResourceID": "/subscriptions/fffffffff-ffff-ffff-fffffffffff/resourceGroups/source-resourcegroupname-rg/providers/Microsoft.DBforPostgreSQL/flexibleServers/SourceServer-Name",
       "createMode": "GeoRestore"
   }
}
```
**Point In Time Restore**

```json
    {
      "location": "EastUS",  
      "properties": 
      {
        "pointInTimeUTC": "2023-06-15T16:05:02Z",
        "createMode": "PointInTimeRestore",
        "sourceServerResourceId": "/subscriptions/ffffffff-ffff-ffff-ffff-ffffffffffff/resourceGroups/SourceResourceGroup-Name/providers/Microsoft.DBforPostgreSQL/flexibleServers/SourceServer-Name"
      }
    }
```


4. If you see Response Code 201 or 202, the restore request is successfully submitted.

    The server creation can take time depending on the database size and compute resources provisioned on the original server. The restore status can be monitored from Activity log by filtering for 
   - **Subscription** = Your Subscription
   - **Resource Type** = Azure Database for PostgreSQL flexible servers (Microsoft.DBforPostgreSQL/flexibleServers) 
   - **Operation** =  Update PostgreSQL Server Create


## Common Errors

 - If you utilize the incorrect API version, you might experience restore failures or timeouts. Please use 2023-06-01-preview API to avoid such issues.
 - To avoid potential DNS errors, it's recommended to use a different name when initiating the restore process, as some restore operations might fail with the same name.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
