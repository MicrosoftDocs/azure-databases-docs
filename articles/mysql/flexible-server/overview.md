---
title: Azure Database for MySQL - Flexible Server Overview
description: Learn about the Flexible Server deployment model for Azure Database for MySQL.
author: deepthiprasad
ms.author: deprasa
ms.reviewer: maghan
ms.date: 02/20/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - mvc
  - references_regions
---

# What is Azure Database for MySQL - Flexible Server?

This article provides an overview and introduction to the core concepts of the Flexible Server deployment model. For information on the appropriate deployment option for your workload, see [Choose the right MySQL Server option in Azure](../select-right-deployment-type.md).

Azure Database for MySQL - Flexible Server is a fully managed, production-ready relational database service in the Microsoft Cloud. It's based on the [MySQL Community Edition](https://www.mysql.com/products/community/) (available under the GPLv2 license) database engine, versions 5.6 (retired), 5.7, and 8.0. The service gives you granular control and flexibility over database management functions and configuration settings. It's generally available in various [Azure regions](#azure-regions).

Azure Database for MySQL - Flexible Server delivers:

- Zone-redundant and Local-redundant high availability (HA).
- The ability to schedule maintenance windows.
- Data protection by using automatic backups and point-in-time restore for up to 35 days.
- Automated patching and maintenance for the underlying hardware, operating system, and database engine to help keep the service secure and up to date.
- Predictable performance, by using inclusive pay-as-you-go pricing.
- Elastic scaling within seconds.
- Cost optimization controls with the low-cost Burstable compute tier and the ability to stop and start the server.
- Enterprise-grade security, compliance, and privacy to help protect sensitive data at rest and in motion.
- Monitoring and automation to simplify management for large-scale deployments.
- Multiple ways to get support.

These capabilities require no extra cost and almost no administration. They allow you to focus on rapid app development and accelerate your time to market rather than allocating time and resources to managing virtual machines and infrastructure. In addition, you can continue to develop your application with the open-source tools and platform of your choice to deliver the speed and efficiency that your business demands without learning new skills.

Azure Database for MySQL - Flexible Server also supports reserved instances. If your production workloads have predictable compute capacity requirements, using reserved instances can help you save costs.

For the latest updates on Azure Database for MySQL - Flexible Server, refer to [What's new in Azure Database for MySQL](whats-new.md).

:::image type="content" source="media/overview/1-azure-db-for-mysql-conceptual-diagram.png" alt-text="Diagram that shows the relationship between Azure database services and MySQL.":::

## Architecture overview

The Flexible Server deployment option offers three compute tiers have different compute and memory capacities to support your database workloads:

- The *Burstable* tier is best suited for low-cost development workloads and low-concurrency workloads that don't need full compute capacity continuously.
- The *General Purpose* and *Memory-Optimized* tiers are better suited for production workloads that require high concurrency, scale, and predictable performance.

You can build your first app on a Burstable tier at a low cost and then adjust the scale to meet the needs of your solution. For details, see [Azure Database for MySQL - Flexible Server service tiers](concepts-compute-storage.md).

When you use a Flexible Server architecture, you can opt for high availability within a single availability zone or across multiple availability zones. Flexible servers are best suited for:

- Ease of deployment, simplified scaling, and low database-management overhead for backups, high availability, security, and monitoring.
- Application developments that require a community version of MySQL with better control and customizations.
- Production workloads with Local-redundant or zone-redundant high availability, along with managed maintenance windows.
- A simplified development experience.

:::image type="content" source="media/overview/1-flexible-server-conceptual-diagram.png" alt-text="Diagram of a Flexible Server architecture." lightbox="media/overview/1-flexible-server-conceptual-diagram.png":::

## Free 12-month offer

With an [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn), you can use Azure Database for MySQL - Flexible Server for free for 12 months. The offer includes monthly limits of up to:

- 750 hours of use for a Burstable Standard_B1ms virtual machine. That's enough hours to run a database instance continuously each month.
- 32 GB of storage and 32 GB of backup storage.

You can use this offer to develop and deploy Azure database applications for flexible servers. To learn how to create and use Azure Database for MySQL - Flexible Server instances for free by using an Azure free account, refer to [this tutorial](how-to-deploy-on-azure-free-account.md).

## High availability within and across availability zones

Azure Database for MySQL - Flexible Server allows configuring high availability with automatic failover. The high-availability solution helps ensure that committed data isn't lost due to failures, and it helps improve overall uptime for your application.

When you configure high availability, a flexible server automatically provisions and manages a standby replica. You're billed for the provisioned compute and storage for the primary and secondary replica.

There are two high-availability architectural models:

- **Zone-redundant high availability**: This option offers complete isolation and requires you to configure infrastructure redundancy across multiple availability zones. It provides the highest level of availability against any infrastructure failure in an availability zone and where latency across availability zones is acceptable.

  Zone-redundant HA is available in a [subset of Azure regions](#azure-regions) that support multiple availability zones and zone-redundant premium file shares.

- **Local-redundant high availability**: This option offers infrastructure redundancy with lower network latency because both primary and standby servers are in the same availability zone. It provides high availability without requiring you to configure application redundancy across zones.

  Local-redundant HA is available in [all Azure regions](#azure-regions) where you can create Azure Database for MySQL - Flexible Server instances.

For more information, see [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md).

## Automated patching with a managed maintenance window

The service performs automated patching of the underlying hardware, operating system, and database engine. The patching includes security and software updates. For the MySQL engine, the planned maintenance release also includes minor version upgrades.

You can configure the patching schedule to be system managed or define your own custom schedule. During the maintenance schedule, the patch is applied, and the server might require a restart. With a custom schedule, you can make your patching cycle predictable and choose a maintenance window that has a minimum impact on the business. The service follows a monthly release schedule for continuous integration and release.

For more information, see [Scheduled maintenance in Azure Database for MySQL - Flexible Server](concepts-maintenance.md).

## Automatic backups

The Azure Database for MySQL - Flexible Server service automatically creates server backups and stores them in user-configured locally redundant or geo-redundant storage. You can use backups to restore your server to any point in time within the backup retention period.

You can configure a retention period of 1 to 35 days. The default is seven days. All backups are encrypted through AES 256-bit encryption.

For more information, see [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md).

## Network isolation

To connect to Azure Database for MySQL - Flexible Server, you have two networking options:

- **Private access (virtual network integration)**: You can deploy your Azure Database for MySQL - Flexible Server instance into an [Azure virtual network](/azure/virtual-network/virtual-networks-overview). Resources in a virtual network can communicate through private IP addresses.

  Choose virtual network integration if you want the following capabilities:

  - Connect from Azure resources in the same virtual network to your Azure Database for MySQL - Flexible Server instance by using private IP addresses.
  - Use a virtual private network (VPN) or Azure ExpressRoute to connect from non-Azure resources to your Azure Database for MySQL - Flexible Server instance.
  - Avoid a public endpoint.

- **Public access (allowed IP addresses)**: You can deploy your Azure Database for MySQL - Flexible Server instance with a public endpoint. The public endpoint is a publicly resolvable DNS address. You choose a range of IP addresses to give permission to access your server. These types of permissions are called *firewall rules*.

For more information, see [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md).

## Fast adjustments to performance and scale

You can build your first app on a small database for a few dollars a month and then seamlessly adjust the scale to meet the needs of your solution. The storage scaling is online and supports the *storage autogrow* feature of Azure Database for MySQL - Flexible Server.

With Azure Database for MySQL - Flexible Server, you can provision additional input/output operations per second (IOPS) above the complimentary IOPS limit independent of storage. By using this feature, you can increase or decrease the amount of provisioned IOPS based on your workload requirements at any time. Dynamic scalability enables your database to respond to rapidly changing resource requirements transparently. You pay for only the resources that you consume.

For more information, see [Azure Database for MySQL - Flexible Server service tiers](concepts-compute-storage.md).

## Ability to scale out your read workload with read replicas

MySQL is a popular database engine for running internet-scale web and mobile applications. Microsoft customers use it for online education, video streaming, digital payment solutions, e-commerce platforms, gaming services, news portals, and government and healthcare websites. These services are required to serve and scale as the web or mobile application's traffic increases.

The application is typically developed in Java or PHP and is either:

- Migrated to run on [Azure virtual machine scale sets](/azure/virtual-machine-scale-sets/overview) or [Azure App Service](/azure/app-service/overview)
- Containerized to run on [Azure Kubernetes Service (AKS)](/azure/aks/intro-kubernetes)

Using a virtual machine scale set with App Service or AKS as the underlying infrastructure simplifies application scaling by instantaneously provisioning new virtual machines and replicating the stateless components of applications to cater to the requests. But often, the database ends up being a bottleneck as a centralized stateful component.

The *read replica* feature allows you to replicate data from an Azure Database for MySQL - Flexible Server instance to a read-only server. You can replicate from the source server to *up to 10 replicas*.

Replicas are updated asynchronously via the MySQL engine's native [binary log (binlog) file position-based replication technology](https://dev.mysql.com/doc/refman/5.7/en/replication-features.html). You can use a load-balancer proxy solution like [ProxySQL](https://techcommunity.microsoft.com/blog/adformysql/load-balance-read-replicas-using-proxysql-in-azure-database-for-mysql/880042) to seamlessly scale out your application workload to read replicas without any application refactoring cost.

For more information, see [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md).

## Hybrid or multicloud data synchronization with data-in replication

You can use the *data-in replication* feature to synchronize data from an external MySQL server into Azure Database for MySQL - Flexible Server. The external server can be on-premises, in virtual machines, in Azure Database for MySQL - Single Server, or in a database service hosted by other cloud providers.

Data-in replication is position-based on the binlog file. The main scenarios to consider about using the feature are:

- Hybrid data synchronization
- Multicloud synchronization
- [Minimal-downtime migration to Azure Database for MySQL - Flexible Server](../../mysql/howto-migrate-single-flexible-minimum-downtime.md)

For more information, see [Replicate data into Azure Database for MySQL - Flexible Server](concepts-data-in-replication.md).

## On-demand server stop/start

With Azure Database for MySQL - Flexible Server, you can stop and start servers on demand to optimize costs. The compute tier billing stops immediately when the server is stopped. This functionality can help you save costs during development, testing, and time-bound predictable production workloads. The server remains in the stopped state for 30 days unless you restart it sooner.

For more information, see [Server concepts in Azure Database for MySQL - Flexible Server](concept-servers.md).

## Enterprise-grade security, compliance, and privacy

Azure Database for MySQL - Flexible Server uses the FIPS 140-2 validated cryptographic module for storage encryption of data at rest. Data (including backups) and temporary files created while you run queries are encrypted.

The service uses the AES 256-bit cipher included in Azure storage encryption, and the keys can be system managed (default). You can also use customer-managed keys stored in an Azure key vault or a managed hardware security module for data encryption at rest. For more information, see [Data encryption with customer managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md).

Azure Database for MySQL - Flexible Server encrypts data in motion with Transport Layer Security (TLS) enforced by default. Azure Database for MySQL - Flexible Server supports encrypted connections that use TLS 1.2. All incoming connections that use TLS 1.0 and TLS 1.1 are denied. You can turn off TLS enforcement by setting the `require_secure_transport` server parameter and then setting the minimum `tls_version` value for your server. For more information, see [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md).

Azure Database for MySQL - Flexible Server allows full private access to the servers through [virtual network](/azure/virtual-network/virtual-networks-overview) integration. Servers in a virtual network can be reached and connected only through private IP addresses. With virtual network integration, public access is denied and servers can't be reached through public endpoints. For more information, see [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md).

<a id="monitoring-and-alerting"></a>

## Monitor and alerting

Azure Database for MySQL - Flexible Server has built-in performance monitoring and alerting features. All Azure metrics have a one-minute frequency. Each metric provides 30 days of history.

You can configure alerts on the metrics. Azure Database for MySQL - Flexible Server exposes host server metrics to monitor resource utilization and allows configuring slow query logs. By using these tools, you can quickly optimize your workloads and configure your server for the best performance.

In Azure Database for MySQL - Flexible Server, you can visualize slow query and audit log data by using Azure Monitor workbooks. With workbooks, you get a flexible canvas for analyzing data and creating rich visual reports within the Azure portal. Azure Database for MySQL - Flexible Server provides three workbook templates: Server Overview, [Tutorial: Configure audit logs by using Azure Database for MySQL - Flexible Server](tutorial-configure-audit.md), and [Tutorial: Query Performance Insight for Azure Database for MySQL - Flexible Server](tutorial-query-performance-insights.md).

The Query Performance Insight workbook helps you spend less time troubleshooting database performance by providing such information as:

- Top long-running queries and their trends.
- Query details: view the query text and the execution history with minimum, maximum, average, and standard deviation query time.
- Resource utilization (CPU, memory, and storage).

In addition, you can use community monitoring tools like [Percona Monitoring and Management](https://techcommunity.microsoft.com/blog/adformysql/monitor-azure-database-for-mysql-using-percona-monitoring-and-management-pmm/2568545) and integrate them with Azure Database for MySQL - Flexible Server.

For more information, see [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md).

## Migration

Azure Database for MySQL - Flexible Server runs the community version of MySQL. This design allows full application compatibility and requires minimal refactoring costs to migrate existing applications developed on the MySQL engine to Azure Database for MySQL - Flexible Server. You can migrate to Azure Database for MySQL - Flexible Server by using the following options.

### Offline migrations

Use Azure Database Migration Service when network bandwidth between the source and Azure is good (for example: a high-speed ExpressRoute connection). For step-by-step instructions, see [Tutorial: Migrate MySQL to Azure Database for MySQL offline using DMS](../../DMS/tutorial-mysql-azure-mysql-offline-portal.md).

Use mydumper and myloader to use compression settings to efficiently move data over low-speed networks (such as the public internet). For step-by-step instructions, see [Migrate large databases to Azure Database for MySQL using mydumper/myloader](../../mysql/concepts-migrate-mydumper-myloader.md).

### Online or minimal-downtime migrations

Use data-in replication with mydumper/myloader-consistent backup and restore for initial seeding. For step-by-step instructions, see [Migrate Azure Database for MySQL - Single Server to Azure Database for MySQL - Flexible Server with open-source tools](../../mysql/howto-migrate-single-flexible-minimum-downtime.md).

To migrate from Azure Database for MySQL - Single Server to Azure Database for MySQL - Flexible Server in five easy steps, refer to [this blog](https://techcommunity.microsoft.com/blog/adformysql/migrate-from-azure-database-for-mysql---single-server-to-flexible-server-in-5-ea/2674057).

For more information, see [Select the right tools for migration to Azure Database for MySQL](../../mysql/how-to-decide-on-right-migration-tools.md).

## Azure regions

One advantage of running your workload in Azure is its global reach. Azure Database for MySQL - Flexible Server is currently available in the following Azure regions:

| Region | Availability | Local-redundant HA | Zone-redundant HA | Geo-redundant backup |
| --- | --- | --- | --- | --- |
| Australia Central | Yes | Yes | No | No |
| Australia East | Yes | Yes | Yes | Yes |
| Australia Southeast | Yes | Yes | No | Yes |
| Brazil South | Yes | Yes | Yes | Yes |
| Canada Central | Yes | Yes | Yes | Yes |
| Canada East | Yes | Yes | No | Yes |
| Central India | Yes | Yes | Yes | Yes |
| Central US | Yes | Yes | Yes | Yes |
| Chile Central | Yes | Yes | Yes | Yes |
| China East 2 | Yes | Yes | No | Yes |
| China East 3 | Yes | Yes | No | Yes |
| China North 2 | Yes | Yes | No | Yes |
| China North 3 | Yes | Yes | Yes | Yes |
| East Asia (Hong Kong SAR) | Yes | Yes | Yes | Yes |
| East US | Yes | Yes | Yes | Yes |
| East US 2 | Yes | Yes | Yes | Yes |
| France Central | Yes | Yes | Yes | Yes |
| France South | Yes | Yes | No | Yes |
| Germany West Central | Yes | Yes | Yes | Yes |
| Germany North | Yes | Yes | No | Yes |
| Indonesia Central | Yes | Yes | No | No |
| Israel Central | Yes | Yes | Yes | No |
| Italy North | Yes | Yes | Yes | No |
| Japan East | Yes | Yes | Yes | Yes |
| Japan West | Yes | Yes | No | Yes |
| Jio India West | Yes | Yes | No | No |
| Korea Central | Yes | Yes | Yes | Yes |
| Korea South | Yes | Yes | No | Yes |
| Malaysia West | Yes | Yes | Yes | Yes |
| Mexico Central | Yes | Yes | Yes | No |
| New Zealand North | Yes | Yes | Yes | No |
| North Central US | Yes | Yes | No | Yes |
| North Europe | Yes | Yes | Yes | Yes |
| Norway East | Yes | Yes | Yes | Yes |
| Norway West | Yes | Yes | No | No |
| Poland Central | Yes | Yes | Yes | No |
| Qatar Central | Yes | Yes | Yes | No |
| South Africa North | Yes | Yes | Yes | Yes |
| South Africa West | Yes | Yes | No | Yes |
| South Central US | Yes | Yes | Yes | Yes |
| South India | Yes | Yes | No | Yes |
| Southeast Asia | Yes | Yes | Yes | Yes |
| Spain Central | Yes | Yes | No | No |
| Sweden Central | Yes | Yes | Yes | No |
| Switzerland North | Yes | Yes | Yes | Yes |
| Switzerland West | Yes | Yes | No | Yes |
| Taiwan North | Yes | Yes | No | No |
| Taiwan Northwest | Yes | Yes | No | No |
| UAE Central | Yes | Yes | No | Yes |
| UAE North | Yes | Yes | Yes | Yes |
| UK South | Yes | Yes | Yes | Yes |
| UK West | Yes | Yes | No | Yes |
| USGov Virginia | Yes | Yes |Yes| No |
| USGov Arizona | Yes | Yes | No | Yes |
| USGov Texas | Yes | Yes | No | Yes |
| West Central US | Yes | Yes | No | Yes |
| West Europe | Yes | Yes | Yes | Yes |
| West US | Yes | Yes | No | Yes |
| West US 2 | Yes | Yes | Yes | Yes |
| West US 3 | Yes | Yes | Yes | Yes |

## Feedback and support

For any questions or suggestions that you might have about working with Azure Database for MySQL - Flexible Server, consider the following points of contact:

- To contact Azure support, [file a request in the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To provide feedback or to request new features, [post an idea via community feedback](https://feedback.azure.com/d365community/forum/47b1e71d-ee24-ec11-b6e6-000d3a4f0da0).

## Related content

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)
- [Manage Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-server-portal.md)
- [Quickstart: Use Python to connect and query data in Azure Database for MySQL - Flexible Server](connect-python.md)
- [Use PHP with Azure Database for MySQL - Flexible Server](connect-php.md)
