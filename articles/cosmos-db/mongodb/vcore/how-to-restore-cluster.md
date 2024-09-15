---
title: Restore a cluster backup
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Restore an Azure Cosmos DB for MongoDB vCore cluster from a point in time encrypted backup snapshot.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 08/28/2023
---

# Restore a cluster in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Azure Cosmos DB for MongoDB vCore provides automatic backups that enable point-in-time recovery (PITR) without any action required from users. Backups allow customers to restore a server to any point in time within the retention period.

> [!NOTE]
> The backup and restore feature is designed to protect against data loss, but it doesn't provide a complete disaster recovery solution. You should ensure that you already have your own disaster recovery plan in place to protect against larger scale outages.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB vCore cluster.
  - If you don't have an Azure subscription, [create an account for free](https://azure.microsoft.com/free).
  - If you have an existing Azure subscription, [create a new Azure Cosmos DB for MongoDB vCore cluster](quickstart-portal.md).

## Backups

Backups are **performed automatically** in the background. Backups are retained for 35 days for active clusters and 7 days for deleted clusters. All backups are encrypted using AES 256-bit encryption.

> [!NOTE]
> Backup files can't be exported. They may only be used for restore operations in Azure Cosmos DB for MongoDB vCore.

In Azure regions that support availability zones, backup snapshots are stored in three availability zones. As long as at least one availability zone is online, the cluster is restorable.

## Restore from a backup

> [!IMPORTANT]
> Restore in Azure Cosmos DB for MongoDB vCore is currently in preview.
> This preview version is provided without a service level agreement (SLA), and it's not recommended
> for production workloads. Certain features might not be supported or might have constrained
> capabilities.

To enable restore functionality preview in the Azure portal for a subscription, follow these steps:

1. Open [Preview features](https://portal.azure.com/#view/Microsoft_Azure_Resources/PreviewFeatures.ReactView) in Azure portal.
1. Make sure that Azure subscription with your Azure Cosmos DB for MongoDB vCore cluster is selected in the **Subscription** list.
1. Search for Azure Cosmos DB for MongoDB vCore previews by typing *MongoDB vCore* in the search box.
1. Select **Azure Cosmos DB for MongoDB vCore Point-In-Time Database Restore** in the list of previews.
1. Select **Register**.

The restore process creates a new cluster with the same configuration in the same Azure region, subscription, and resource group as the original. Follow these steps to restore data.

1. Select an existing Azure Cosmos DB for MongoDB vCore cluster in the subscription where the restore preview is enabled.
1. On the cluster sidebar, under **Settings**, select **Point In Time Restore**.
1. Select a date and provide a time (in UTC time zone) in the date and time fields.
1. Enter a cluster name in the **Restore target cluster name** field. 
1. Enter a cluster admin name for the restored cluster in the **Admin user name** field.
1. Enter a password for the admin role in the **Password** and **Confirm password** fields.
1. Select **Submit** to initiate cluster restore.

> [!NOTE]
> Cluster backups are stored for 35 days. If your cluster was created 35 days or more ago and you don't see the desired date in the restore date field, you might need to open a support request to restore the cluster to that point.

To create an Azure support request, follow these steps:

1. Select an existing Azure Cosmos DB for MongoDB vCore cluster that you need to restore.
1. On the cluster sidebar, under **Help**, select **Support + Troubleshooting**. For more information, see [create an Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request#problem-description).

## Next steps

In this guide, we covered the backup and restore features for Azure Cosmos DB for MongoDB vCore.

> [!div class="nextstepaction"]
> [Review cross-region replication capabilities in Azure Cosmos DB for MongoDB vCore](./cross-region-replication.md)
