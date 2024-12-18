---
title: On-demand-backup - Azure portal Preview
description: This article describes how to perform on-demand backup in Azure Database for PostgreSQL - Flexible Server through the Azure portal.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 11/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# On-demand backup Azure Database for PostgreSQL - Flexible Server using Azure portal Preview

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step procedure to perform an on-demand backup of the Azure Database for PostgreSQL flexible server instance through the Azure portal. The procedure is same for servers configured with zone redundant high availability. 

> [!IMPORTANT]
> On-demand backups are retained according to your configured retention window, but you can delete them earlier if they’re no longer needed.

## Prerequisites

-   Make sure that Microsoft.DBforPostgreSQL/flexibleServers/backups/write permission is granted to the role performing on-demand backup. 


## Perform On-demand backup 

Follow these steps to take on-demand backups for your Azure Database for PostgreSQL flexible server instance.

1.  In the [Azure portal](https://portal.azure.com/), choose your Azure Database for PostgreSQL flexible server.

2.  Click **Settings** from the left panel and choose **Backup and Restore**.
   
     :::image type="content" source="./media/how-to-perform-on-demand-backup-portal/on-demand-back-up.png" alt-text="Screenshot of back up now selection.":::

3. Click **Backup now** and provide your backup name

:::image type="content" source="./media/how-to-perform-on-demand-backup-portal/back-up-now-trigger.png"  alt-text="Screenshot of back up Trigger":::

4.  Click **Trigger**.
   
      
5.  A notification is shown that **On-demand backup trigger has been initiated.**



## Delete On-demand backup 

Follow these steps to take on-demand backups for your Azure Database for PostgreSQL flexible server instance.

1.  In the [Azure portal](https://portal.azure.com/), choose your Azure Database for PostgreSQL flexible server.

2.  Click **Settings** from the left panel and choose **Backup and Restore**.
   
     :::image type="content" source="./media/how-to-perform-on-demand-backup-portal/delete-back-up.png" alt-text="Screenshot of delete backup selection.":::

3. Click **Delete** 

4.  A notification is shown that **On-demand backup deletion has been initiated.**

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
