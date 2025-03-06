---
title: Automigration
description: This tutorial describes how to configure notifications, review migration details, and FAQs for an Azure Database for PostgreSQL Single Server instance schedule for automigration to Flexible Server.
author: hariramt
ms.author: hariramt
ms.reviewer: shriramm, maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - mvc
  - mode-api
---

# Automigration from Azure Database for Postgresql – Single Server to Flexible Server

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

**Automigration** from Azure Database for PostgreSQL – Single Server to Flexible Server is a service-initiated migration that takes place during a planned downtime window for Single Server, separate from its patching or maintenance window. The service identifies eligible servers and sends advance notifications with detailed steps about the automigration process. You can review and adjust the migration schedule if needed or submit a support request to opt out of automigration for your servers.

Automigration uses the [Azure PostgreSQL migration service](./migration-service/overview-migration-service-postgresql.md) to deliver a resilient offline migration during the planned migration window. Downtime varies based on workload characteristics. For migration speed benchmarks, see [Azure PostgreSQL Migration Speed Benchmarking](./migration-service/best-practices-migration-service-postgresql.md#migration-speed-benchmarking). This migration eliminates the need for manual server migration, allowing you to benefit from Flexible Server features post-migration, including improved price-performance, granular database configuration control, and custom maintenance windows.

> [!NOTE]  
> The Automigration service selects Single server to migrate based on the following criteria:
> - Servers with no complex feature such as CMK, Microsoft Entra ID, Read Replica and Private end-point.
> - Size of data <= 300 GB
> - Public access is enabled

> [!NOTE]  
> In case any of these features such as CMK, Microsoft Entra ID, Read Replica and Private end-point are used, extra planning would be required. Mention the details in the nomination form below and we will get in touch with you.

## Nominate Single servers for Automigration

The nomination process is for users who want to voluntarily fast-track their migration to Flexible server. If you own a Single Server workload, you can now nominate yourself (if not already scheduled by the service) for automigration. Submit your server details through this [form](https://forms.office.com/r/4pF55L8TxY).

## Prerequisite checks for automigration

Review the following prerequisites to ensure a successful automigration:

- The Single Server instance should be in **ready state** during the planned migration window for automigration to take place.

- The Single Server instance must have the **Deny public network access** setting configured to **No**. You can find this option under the **Connection Security** blade in the Azure portal.

- For Single Server instance with **SSL enabled**, ensure you have all certificates (**[DigiCertGlobalRootG2 Root CA](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem) and [DigiCertGlobalRootCA Root CA](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem)**) available in the trusted root store. Additionally, if you have the certificate pinned to the connection string create a combined CA certificate with all three certificates before scheduled automigration to ensure business continuity post-migration.

- If your source Azure Database for postgresql Single Server has firewall rule names exceeding 80 characters, rename them to ensure length of name is fewer than 80 characters. (The firewall rule name length supported on Flexible Server is 80 characters whereas on Single Server the allowed length is 128 characters.)

## Automigration Process

The automigration process includes several key phases:

- **Target Flexible Server Creation** - A Flexible Server is created to match the performance and cost of your Single Server SKU. It inherits all firewall rules from the source Single Server.

- **Data Migration** - Data migration occurs during the designated migration window, typically scheduled outside business hours for the server's hosting region (if the window is chosen by the service). The source Single Server is set to read-only, and all data, schemas, user roles, privileges, and ownership of database objects are migrated to the Flexible Server. Additionally, it copies all existing firewall rules to the flexible server, ensuring uninterrupted connectivity.

- **DNS Switch** - After data migration, a DNS switch is performed, allowing the existing Single Server connection string to seamlessly connect to the new Flexible Server. Both Single and Flexible Server connection string formats, as well as username formats (**username@server_name** and **username**), are supported on the migrated Flexible Server.

- **Flexible Server Visibility** - After a successful data migration and DNS switch, the new Flexible Server appears under your subscription and can be managed via the Azure portal or CLI.

- **Updated Single Server Connection Strings** - Updated connection strings for the legacy Single Server are sent via Service Health notifications on the Azure portal. They are also accessible on the Single Server portal page under **Settings -> Connection Strings**.

- **Single Server Deletion** - The Single Server is retained for seven days post-migration before it is deleted.

## How is the target postgresql Flexible Server provisioned?

The compute tier and SKU for the target flexible server is provisioned based on the source single server's pricing tier and VCores as shown below.

| Single Server Pricing Tier | Single Server VCores | Flexible Server Tier | Flexible Server SKU Name |
| --- | --- | :---: | :---: |
| Basic | 1 | Burstable | B1ms |
| Basic | 2 | Burstable | B2s |
| General Purpose | 2 | GeneralPurpose | Standard_D2s_v3 |
| General Purpose | 4 | GeneralPurpose | Standard_D4s_v3 |
| General Purpose | 8 | GeneralPurpose | Standard_D8s_v3 |
| General Purpose | 16 | GeneralPurpose | Standard_D16s_v3 |
| General Purpose | 32 | GeneralPurpose | Standard_D32s_v3 |
| General Purpose | 64 | GeneralPurpose | Standard_D64s_v3 |
| Memory Optimized | 2 | MemoryOptimized | Standard_E2s_v3 |
| Memory Optimized | 4 | MemoryOptimized | Standard_E4s_v3 |
| Memory Optimized | 8 | MemoryOptimized | Standard_E8s_v3 |
| Memory Optimized | 16 | MemoryOptimized | Standard_E16s_v3 |
| Memory Optimized | 32 | MemoryOptimized | Standard_E32s_v3 |

- The postgresql version, region, connection string, subscription, and resource group for the target Flexible Server will remain the same as that of the source Single Server.
- For Single Servers with less than 20-GiB storage, the storage size is set to 32 GiB as that is the minimum storage limit on Azure Database for postgresql - Flexible Server.
- For Single Servers with greater storage requirement, sufficient storage equivalent to 1.25 times or 25% more storage than what is being used in the Single server is allocated. During the initial base copy of data, multiple insert statements are executed on the target, which generates WALs (Write Ahead Logs). Until these WALs are archived, the logs consume storage at the target and hence the margin of safety.
- Both username formats – username@server_name (Single Server) and username (Flexible Server) are supported on the migrated Flexible Server.
- Both connection string formats – Single Server and Flexible Server are supported on the migrated Flexible Server.

## Automigration Across Major PostgreSQL Versions

This migration might involve moving data from PostgreSQL Single Server (versions 9.5, 9.6, or 10) to PostgreSQL 11 on Flexible Server. These earlier versions have been retired by the PostgreSQL community. To ensure security, stability, and performance, it is recommended to adopt supported community versions.

When migrating across major PostgreSQL versions, consider the following key factors to ensure a successful and smooth transition:

- **Retired Features** - Features that were retired in older versions might no longer be available in PostgreSQL 11. It is important to review the [release notes](https://www.postgresql.org/docs/11/release-11-22.html) for any breaking changes or deprecated features that could affect your application.

- **Application Testing** - Conduct thorough testing of your application on PostgreSQL 11. Pay attention to potential issues with SQL queries, functions, or third-party tools, as these might behave differently or fail entirely due to changes in the newer version.

- **Configuration Changes** - Major version upgrades often introduce changes to server parameters, either by adding new parameters or altering the default values of existing ones. These changes can affect collation, query execution, and data storage. To ensure compatibility, test your application against these updated settings and address any issues that arise. If you encounter problems, use the script provided in the [**post-migration steps section**](#post-migration-steps) to copy the existing server parameters from your Single Server instance to the automigrated Flexible Server.

## Post-migration steps

Here's the information you need regarding the post-automigration steps.
- If automigration involves migrating across major PostgreSQL versions, thoroughly test your application to identify the impact of breaking changes and parameter adjustments. Make the necessary changes to ensure compatibility and optimal performance.

- Any Terraform/CLI scripts you host to manage your Single Server instance should be updated with Flexible Server references.

- The server parameters in Flexible server are tuned to the community standards. If you want to retain the same server parameter values as your Single server, you can log in via PowerShell and run the script [here](https://github.com/hariramt/auto-migration/tree/main) to copy the parameter values.

- Access Control (IAM) settings for your flexible server will be inherited from the Subscription settings. If you have provided any role assignments specific to the single server, then you must create these role assignments on your flexible server.

- Copy monitoring page settings (Alerts, Metrics, and Diagnostic settings) to Flexible server.

- To enable [query perf insights](../flexible-server/concepts-query-performance-insight.md), you need to enable query store on the Flexible server which isn't enabled by default.

- If [High Availability](/azure/reliability/reliability-postgresql-flexible-server) is needed, you can enable it with zero downtime.

- Please verify that your flexible server SKU matches the one mentioned in the Service Health automigration notification. If it's different, [revert it to the SKU specified](../flexible-server/how-to-scale-compute.md) in the notification. This is crucial to ensure accurate billing.

- The existing connection strings of your Single Server will now point to the Flexible Server. To access your Single Server, a new set of connection strings has been generated. You can retrieve them from the Service Health notification sent for the automigration of your Single Server.

### Handling VNet rules in Flexible server

In Azure Database for PostgreSQL Single Server, a virtual network (VNet) rule is a subnet listed in the server's access control list (ACL). This rule allows the Single Server to accept communication from nodes within that particular subnet.
For Flexible Server, VNet rules are not supported. Instead, Flexible Server allows the creation of [private endpoints](../flexible-server/concepts-networking-private-link.md), enabling the server to function within your virtual network. A private endpoint assigns a private IP to the Flexible Server, and all traffic between your virtual network and the server travels securely via the Azure backbone network, eliminating the need for public internet exposure.

After the migration, you must add a private endpoint to your Flexible Server for all the subnets previously covered by VNet rules on your Single Server. You can complete this process using either the [Azure portal](../flexible-server/how-to-manage-virtual-network-private-endpoint-portal.md) or the [Azure CLI](../flexible-server/how-to-manage-virtual-network-private-endpoint-cli.md).
Once this step is completed, your network connectivity will remain intact on the Flexible Server after the migration from Single Server.

### Long-term retention backup

Auto migration of single servers does not automatically configure long-term retention (LTR) backup after migration to Flexible server. You can backup Azure Database for PostgreSQL Flexible server with long-term retention using [Azure Backup](/azure/backup/backup-azure-database-postgresql-flex).

## How to check if your Single Server is scheduled for Automigration

To determine if your Single Server is selected for automigration, follow these steps:

- **[Service Health Notifications](/azure/service-health/service-health-portal-update)** - In the Azure portal, go to **Service Health > Planned Maintenance** events. Look for events labeled **'Notification for Scheduled Auto Migration to Azure Database for PostgreSQL Single Server'**. The notifications are sent 30, 14, and 7 days before the migration date, and again during migration stages: in progress, completed, and six days before the Single Server is decommissioned.

  > [!NOTE]  
  > These notifications do not land in your inbox by default. To receive them via email or SMS, you need to set up Service Health Alerts. For more information, see [Set up Service Health Alerts](../single-server/concepts-planned-maintenance-notification.md#to-receive-planned-maintenance-notification).

- **Single Server Overview Page** - Navigate to your Single Server instance in the Azure portal and check the Overview page. If scheduled for automigration, you'll find details here, including an option to defer the migration by one month at a time or reschedule within the current month.

  > [!NOTE]  
  > The migration schedule is locked 7 days prior to the scheduled migration window during which you'll be unable to reschedule.

- **Azure CXP email notifications** - Azure Customer Experience(CXP) also sends direct emails to classic roles and RBAC roles associated with the subscription containing the Single Server, providing information on upcoming automigrations.

## Frequently Asked Questions (FAQs)

**Q. Why am I being auto-migrated​?**

**A.** Your Azure Database for Postgresql - Single Server instance is eligible for automigration to our flagship offering Azure Database for Postgresql - Flexible Server. This automigration removes the overhead to manually migrate your server. You can take advantage of the benefits of Flexible Server, including better price & performance, granular control over database configuration, and custom maintenance windows.

**Q. How does the automigration take place? What all does it migrate?​**

**A.** The Flexible Server is provisioned to closely match the same VCores and storage as that of your Single Server. Next the source Single Server is put in a read-only state, schema and data is copied to target Flexible Server. The DNS switch is performed to route all existing connections to target and the target Flexible Server is brought online. The automigration migrates the databases (including schema, data, users/roles, and privileges). The migration is offline where you see downtime of a few minutes up to 2 hours depending on the size of your workload. For migration speed benchmarks, see [Azure PostgreSQL Migration Speed Benchmarking](./migration-service/best-practices-migration-service-postgresql.md#migration-speed-benchmarking).

**Q. How can I set up or view automigration alerts?​**

**A.** Following are the ways you can set up alerts:

- Configure service health alerts to receive automigration schedule and progress notifications via email/SMS by following steps [here](../single-server/concepts-planned-maintenance-notification.md#to-receive-planned-maintenance-notification).
- Check the automigration notification on the Azure portal by following steps [here](../single-server/concepts-planned-maintenance-notification.md#check-planned-maintenance-notification-from-azure-portal).

**Q. How can I defer the scheduled migration of my Single server?​**

**A.** You can review the migration schedule by navigating to the Overview page of your Single Server instance. If you wish to defer the migration, you can defer by a month at the most by navigating to the Overview page of your single server instance on the Azure portal. You can reschedule the migration by selecting another migration window within a month. The migration details will be locked seven days before the scheduled migration window after which you're unable to reschedule. This automigration can be deferred monthly until 28 March, 2025.

**Q. How can I opt out of a scheduled automigration of my Single server?​**

**A.** If you wish to opt out of the automigration, you can raise a support ticket for this purpose.

**Q. What post-migration steps should I follow if my Single server uses VNet rules?​**

**A.** VNet rules are not supported on Flexible server. Refer to [this section](#handling-vnet-rules-in-flexible-server)

**Q. Do I need to re-configure Long-term retention backups on Flexible server?​**

**A.** Yes. Please refer to [this section](#long-term-retention-backup)

**Q. What username and connection string would be supported for the migrated Flexible Server? ​​**

**A.** Both username formats - username@server_name (Single Server format) and username (Flexible Server format) are supported for the migrated Flexible Server, and hence you aren't required to update them to maintain your application continuity post migration. Additionally, both connection string formats (Single and Flexible server format) are also supported for the migrated Flexible Server.

**Q. I see a pricing difference on my potential move from postgresql Basic Single Server to postgresql Flexible Server??​**

**A.** Few servers might see a minor price revision after migration as the minimum storage limit on both offerings is different (5 GiB on Single Server and 32 GiB on Flexible Server). Storage cost for Flexible Server is marginally higher than Single Server. Any price increase is offset through better throughput and performance compared to Single Server. For more information on Flexible server pricing refer to this [document](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/)

**Q. What happens if I do not migrate or my server is not auto migrated by March 28th, 2025??​**

**A.** After the retirement deadline of March 28, 2025, all existing single servers that have not migrated will be force migrated to Flexible server. Servers with add-on features such as CMK or Private endpoint will require more actions by the user post-migration to ensure normal operation. There are no extensions to the retirement date.

## Related content

- [Manage an Azure Database for postgresql - Flexible Server using the Azure portal.](../flexible-server/how-to-manage-server-portal.md)
