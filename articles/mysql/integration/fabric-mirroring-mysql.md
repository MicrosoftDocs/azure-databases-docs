---
title: Azure Database for MySQL Mirroring in Microsoft Fabric
description: Learn about Mirroring in Microsoft Fabric for Azure Database for MySQL instances.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: jingwang, maghan
ms.date: 03/18/2026
ms.service: azure-database-mysql
ms.topic: concept-article
ai-usage: ai-assisted
# customer intent: As a database administrator, I want to learn how to use Fabric Mirroring for my Azure Database for MySQL instances.
---

# Azure Database for MySQL mirroring in Microsoft Fabric

[Mirroring in Fabric](/fabric/mirroring/azure-database-mysql) provides an easy experience to avoid complex ETL (Extract Transform Load) and integrate your existing Azure Database for MySQL estate with the rest of your data in Microsoft Fabric. You can continuously replicate your existing Azure Database for MySQL directly into Fabric OneLake. Inside Fabric, you can unlock powerful business intelligence, artificial intelligence, Data Engineering, Data Science, and data sharing scenarios.

## Architecture

Fabric mirroring in Azure Database for MySQL is built on concepts like logical replication and Change Data Capture (CDC) design pattern.

Once you establish Fabric mirroring for a database in an Azure Database for MySQL, a MySQL background process creates an initial snapshot for selected tables to be mirrored. It ships the snapshot to a Fabric OneLake landing zone in Parquet format. A Replicator process running in Fabric takes these initial snapshot files and creates Delta tables in the Mirrored database artifact.

The source database captures subsequent changes applied to selected tables. It ships these changes to the OneLake landing zone in batches to be applied to the respective Delta tables in the Mirrored database artifact.

:::image type="content" source="media/fabric-mirroring-mysql/architecture.png" alt-text="Diagram of Fabric Database mirroring architecture.":::

## Prerequisites

Before you set up Fabric mirroring for an Azure Database for MySQL, make sure the following requirements are met:

- **Supported service tiers**: General Purpose and Business-Critical.
- **Supported MySQL versions**: 8.0 (LTS minor versions only).
- **Binary log configuration**: `binlog_row_image` must be set to `FULL` or `NOBLOB`. If it's not set to one of these values, modify this setting in the Azure portal for Azure Database for MySQL. Go to **Settings > Server parameters** to make the necessary changes and save them.
- **User permissions**: A MySQL user account with **SELECT** permissions on all databases and tables selected for mirroring.
- **Fabric capacity**: An active Microsoft Fabric capacity (or Fabric trial).

## Set up mirroring in Azure Database for MySQL

By using Fabric mirroring in the Azure portal for an Azure Database for MySQL, you can replicate your MySQL databases into Microsoft Fabric. This feature helps you integrate your data seamlessly with other services in Microsoft Fabric, enabling advanced analytics, business intelligence, and data science scenarios. The configuration experience follows a two-step process spanning the Azure portal and the Fabric portal.

### Enable Fabric mirroring in the Azure portal

To enable Fabric mirroring, complete these steps in the Azure portal:

1. Go to your Azure Database for MySQL in the Azure portal.

1. Open **Fabric Mirroring (preview)** under **Settings**.

   :::image type="content" source="media/fabric-mirroring-mysql/settings-fabric-mirroring.png" alt-text="Screenshot of the Fabric Mirroring option under Settings in the Azure portal.":::

1. Check that your server meets all the prerequisites.

   :::image type="content" source="media/fabric-mirroring-mysql/enable-fabric-mirroring.png" alt-text="Screenshot of the enable message in the Azure portal.":::

1. Select **Enable Fabric Mirroring**.

1. Choose an existing user-assigned managed identity or create a new one. Use this identity to securely write data into OneLake.

1. Save the configuration to enable mirroring.

   :::image type="content" source="media/fabric-mirroring-mysql/save-fabric-mirroring.png" alt-text="Screenshot of the Save button to enable Fabric Mirroring in the Azure portal.":::

### Create a mirrored database in Fabric

After you enable Fabric Mirroring in the Azure portal, create the mirrored database artifact in the Fabric portal:

1. Open the [Microsoft Fabric portal](https://app.fabric.microsoft.com/).

1. Select your workspace, or create a new one.

1. Select **New item** > **Mirrored Azure Database for MySQL**.

1. Select your Azure Database for MySQL connection or create a new one by providing your server name and the user credentials with the required permissions.

1. Choose the databases and tables you want to mirror, then select **Mirror database**.

For detailed instructions, see [Configure Microsoft Fabric Mirrored Databases from Azure Database for MySQL](/fabric/mirroring/azure-database-mysql-tutorial).

After you create the mirrored database, Fabric starts the initial data replication and then continues with continuous change replication. You can monitor the replication status and health directly from the mirrored database management view in Fabric.

## Monitor replication

Fabric provides built-in monitoring for mirrored databases, including replication health and status, rows replicated per table, and the ability to start and stop replication from the Fabric portal.

For more information, see [Monitor Mirrored Database Replication - Microsoft Fabric](/fabric/mirroring/monitor).

## Data availability and consumption

After replication finishes, all tables are available in the SQL Analytics endpoint. For guidance on how to use this data in near-real time for analytics, see [Explore Data in Your Mirrored Database Using Microsoft Fabric - Microsoft Fabric](/fabric/mirroring/explore).

## Recommended MySQL parameters

| **Parameter** | **Required Value** | **Notes** |
| --- | --- | --- |
| log_bin | ON | Required for binlog replication |
| binlog_row_image | FULL or NOBLOB | MINIMAL unsupported |
| binlog_format | ROW | Required for row-level replication |
| innodb_flush_log_at_trx_commit | 1 | Recommended for durability |

## Related content

- [Microsoft Fabric Mirrored Databases From Azure Database for MySQL](/fabric/mirroring/azure-database-mysql)
- [Configure Microsoft Fabric Mirrored Databases from Azure Database for MySQL](/fabric/mirroring/azure-database-mysql-tutorial)
- [Limitations of Fabric Mirrored Databases From Azure Database for MySQL](/fabric/mirroring/azure-database-mysql-limitations)
- [Troubleshoot Fabric Mirrored Databases From Azure Database for MySQL](/fabric/mirroring/azure-database-mysql-troubleshoot)
