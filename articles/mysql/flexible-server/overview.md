---
title: Azure Database for MySQL flexible server
description: Get an overview of Azure Database for MySQL flexible server, a fully managed MySQL service with high availability, automated backups, scaling, and enterprise-grade security.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - references_regions
ai-usage: ai-assisted
---

# What is Azure Database for MySQL flexible server?

Azure Database for MySQL flexible server is a fully managed, production-ready relational database service in the Microsoft Cloud. It's based on the [MySQL Community Edition](https://www.mysql.com/products/community/) (available under the GPLv2 license) database engine, versions 5.7, 8.0, and 8.4. The service gives you granular control and flexibility over database management functions and configuration settings. It's generally available in various [Azure regions](#azure-regions).

Azure Database for MySQL flexible server delivers:

- Zone-redundant and local-redundant high availability (HA).
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

Azure Database for MySQL flexible server also supports reserved instances. If your production workloads have predictable compute capacity requirements, reserved instances can help you save costs.

For the latest updates on Azure Database for MySQL flexible server, see [What's new in Azure Database for MySQL?](whats-new.md)

:::image type="content" source="media/overview/azure-db-for-mysql-conceptual-diagram.png" alt-text="Diagram that shows the relationship between Azure database services and MySQL." lightbox="media/overview/azure-db-for-mysql-conceptual-diagram.png":::

## Architecture overview

The flexible server deployment option offers three compute tiers that have different compute and memory capacities to support your database workloads:

- The *Burstable* tier is best suited for low-cost development workloads and low-concurrency workloads that don't need full compute capacity continuously.
- The *General Purpose* and *Memory-Optimized* tiers are better suited for production workloads that require high concurrency, scale, and predictable performance.

You can build your first app on a Burstable tier at a low cost and then adjust the scale to meet the needs of your solution. For details, see [Azure Database for MySQL flexible server service tiers](concepts-compute-storage.md).

When you use a flexible server architecture, you can opt for high availability within a single availability zone or across multiple availability zones. Flexible servers are best suited for:

- Ease of deployment, simplified scaling, and low database-management overhead for backups, high availability, security, and monitoring.
- Application developments that require a community version of MySQL with better control and customizations.
- Production workloads with local-redundant or zone-redundant high availability, along with managed maintenance windows.
- A simplified development experience.

:::image type="content" source="media/overview/flexible-server-conceptual-diagram.png" alt-text="Diagram of a flexible server architecture." lightbox="media/overview/flexible-server-conceptual-diagram.png":::

## Free 12-month offer

With an [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn), you can use Azure Database for MySQL flexible server for free for 12 months. The offer includes monthly limits of up to:

- 750 hours of use for a Burstable Standard_B1ms virtual machine. That's enough hours to run a database instance continuously each month.
- 32 GB of storage and 32 GB of backup storage.

Use this offer to develop and deploy Azure database applications for flexible servers. To learn how to create and use Azure Database for MySQL flexible server for free by using an Azure free account, see [Deploy Azure Database for MySQL flexible server on an Azure free account](how-to-deploy-on-azure-free-account.md).

## High availability within and across availability zones

Azure Database for MySQL flexible server enables you to configure high availability with automatic failover. This high-availability solution helps ensure that committed data isn't lost due to failures, and it helps improve overall uptime for your application.

When you configure high availability, a flexible server automatically provisions and manages a standby replica. You pay for the provisioned compute and storage for the primary and secondary replica.

Two high-availability architectural models are available:

- **Zone-redundant high availability**: This option offers complete isolation and requires you to configure infrastructure redundancy across multiple availability zones. It provides the highest level of availability against any infrastructure failure in an availability zone and where latency across availability zones is acceptable.

  A [subset of Azure regions](#azure-regions) that support multiple availability zones and zone-redundant premium file shares offer zone-redundant HA.

- **Local-redundant high availability**: This option offers infrastructure redundancy with lower network latency because both primary and standby servers are in the same availability zone. It provides high availability without requiring you to configure application redundancy across zones.

  You can enable local-redundant HA in all regions where Azure Database for MySQL flexible server instances are available.

For more information, see [High availability in Azure Database for MySQL](concepts-high-availability.md).

## Automated patching with a managed maintenance window

The service performs automated patching of the underlying hardware, operating system, and database engine. The patching process includes security and software updates. For the MySQL engine, the planned maintenance release also includes minor version upgrades.

You can configure the patching schedule to be system managed or define your own custom schedule. During the maintenance schedule, the patch is applied, and the server might require a restart. By using a custom schedule, you can make your patching cycle predictable and choose a maintenance window that has a minimum impact on the business. The service follows a monthly release schedule for continuous integration and release.

For more information, see [Scheduled maintenance in Azure Database for MySQL](concepts-maintenance.md).

## Automatic backups

The Azure Database for MySQL flexible server service automatically creates server backups and stores them in user-configured locally redundant or geo-redundant storage. Use backups to restore your server to any point in time within the backup retention period.

You can configure a retention period of 1 to 35 days. The default is seven days. All backups are encrypted through AES 256-bit encryption.

For more information, see [Backup and restore in Azure Database for MySQL](concepts-backup-restore.md).

## Network isolation

To connect to Azure Database for MySQL flexible server, you have two networking options:

- **Private access (virtual network integration)**: Deploy your Azure Database for MySQL flexible server into an [Azure virtual network](/azure/virtual-network/virtual-networks-overview). Resources in a virtual network can communicate through private IP addresses.

  Choose virtual network integration if you want the following capabilities:

  - Connect from Azure resources in the same virtual network to your Azure Database for MySQL flexible server by using private IP addresses.
  - Use a virtual private network (VPN) or Azure ExpressRoute to connect from non-Azure resources to your Azure Database for MySQL flexible server.
  - Avoid a public endpoint.

- **Public access (allowed IP addresses)**: Deploy your Azure Database for MySQL flexible server with a public endpoint. The public endpoint is a publicly resolvable DNS address. Choose a range of IP addresses to give permission to access your server. These types of permissions are called *firewall rules*.

For more information, see [Connectivity and networking concepts for Azure Database for MySQL flexible server](concepts-networking.md).

## Fast adjustments to performance and scale

You can build your first app on a small database for a few dollars a month and then seamlessly adjust the scale to meet the needs of your solution. The storage scaling is online and supports the *storage autogrow* feature of Azure Database for MySQL flexible server.

With Azure Database for MySQL flexible server, you can provision additional input/output operations per second (IOPS) above the complimentary IOPS limit independent of storage. By using this feature, you can increase or decrease the amount of provisioned IOPS based on your workload requirements at any time. Dynamic scalability enables your database to respond to rapidly changing resource requirements transparently. You pay for only the resources that you consume.

For more information, see [Azure Database for MySQL flexible server service tiers](concepts-compute-storage.md).

## Ability to scale out your read workload with read replicas

MySQL is a popular database engine for running internet-scale web and mobile applications. Microsoft customers use it for online education, video streaming, digital payment solutions, e-commerce platforms, gaming services, news portals, and government and healthcare websites. These services are required to serve and scale as the web or mobile application's traffic increases.

The application is typically developed in Java or PHP and is either:

- Migrated to run on [Azure virtual machine scale sets](/azure/virtual-machine-scale-sets/overview) or [Azure App Service](/azure/app-service/overview)
- Containerized to run on [Azure Kubernetes Service (AKS)](/azure/aks/intro-kubernetes)

A virtual machine scale set with App Service or AKS as the underlying infrastructure simplifies application scaling by instantaneously provisioning new virtual machines and replicating the stateless components of applications to cater to the requests. But often, the database ends up being a bottleneck as a centralized stateful component.

The *read replica* feature allows you to replicate data from an Azure Database for MySQL flexible server to a read-only server. You can replicate from the source server to *up to 10 replicas*.

Replicas are updated asynchronously via the MySQL engine's native [binary log (binlog) file position-based replication technology](https://dev.mysql.com/doc/refman/5.7/en/replication-features.html). You can use a load-balancer proxy solution like [ProxySQL](https://techcommunity.microsoft.com/blog/adformysql/load-balance-read-replicas-using-proxysql-in-azure-database-for-mysql/880042) to seamlessly scale out your application workload to read replicas without any application refactoring cost.

For more information, see [Read replicas in Azure Database for MySQL](concepts-read-replicas.md).

## Hybrid or multicloud data synchronization with data-in replication

Use the *data-in replication* feature to synchronize data from an external MySQL server into Azure Database for MySQL flexible server. The external server can be on-premises, in virtual machines, or in a database service hosted by other cloud providers.

Data-in replication is position-based on the binlog file. Consider the following main scenarios for using the feature:

- Hybrid data synchronization
- Multicloud synchronization

For more information, see [Replicate data into Azure Database for MySQL flexible server](concepts-data-in-replication.md).

## On-demand server stop and start

With Azure Database for MySQL flexible server, you can stop and start servers on demand to optimize costs. The compute tier billing stops immediately when the server stops. This functionality can help you save costs during development, testing, and time-bound predictable production workloads. The server stays in the stopped state for 30 days unless you restart it sooner.

For more information, see [Server concepts in Azure Database for MySQL flexible server](concept-servers.md).

## Enterprise-grade security, compliance, and privacy

Azure Database for MySQL flexible server uses the FIPS 140-2 validated cryptographic module for storage encryption of data at rest. Data (including backups) and temporary files created while you run queries are encrypted.

The service uses the AES 256-bit cipher included in Azure storage encryption, and the keys can be system managed (default). You can also use customer-managed keys stored in an Azure key vault or a managed hardware security module for data encryption at rest. For more information, see [Data encryption with customer managed keys for Azure Database for MySQL](security-customer-managed-key.md).

Azure Database for MySQL flexible server encrypts data in motion with Transport Layer Security (TLS) enforced by default. The service supports encrypted connections that use TLS 1.2 (default) and TLS 1.3 (recommended on MySQL 8.0 and later). All incoming connections that use TLS 1.0 and TLS 1.1 are denied. You can turn off TLS enforcement by setting the `require_secure_transport` server parameter and then setting the minimum `tls_version` value for your server. For more information, see [Connect to Azure Database for MySQL flexible server with encrypted connections](security-tls-how-to-connect.md).

Azure Database for MySQL flexible server allows full private access to the servers through [virtual network](/azure/virtual-network/virtual-networks-overview) integration. You can reach and connect to servers in a virtual network only through private IP addresses. By using virtual network integration, you deny public access and can't reach servers through public endpoints. For more information, see [Connectivity and networking concepts for Azure Database for MySQL flexible server](concepts-networking.md).

<a id="monitoring-and-alerting"></a>

## Monitor and alert

Azure Database for MySQL flexible server has built-in performance monitoring and alerting features. All Azure metrics have a one-minute frequency. Each metric provides 30 days of history.

You can configure alerts on the metrics. Azure Database for MySQL flexible server exposes host server metrics to monitor resource utilization and allows configuring slow query logs. By using these tools, you can quickly optimize your workloads and configure your server for the best performance.

In Azure Database for MySQL flexible server, you can visualize slow query and audit log data by using Azure Monitor workbooks. With workbooks, you get a flexible canvas for analyzing data and creating rich visual reports within the Azure portal. Azure Database for MySQL flexible server provides three workbook templates: Server Overview, [Tutorial: Configure audit logs by using Azure Database for MySQL flexible server](tutorial-configure-audit.md), and [Tutorial: Query Performance Insight for Azure Database for MySQL](tutorial-query-performance-insights.md).

The Query Performance Insight workbook helps you spend less time troubleshooting database performance by providing such information as:

- Top long-running queries and their trends.
- Query details: view the query text and the execution history with minimum, maximum, average, and standard deviation query time.
- Resource utilization (CPU, memory, and storage).

In addition, you can use community monitoring tools like [Percona Monitoring and Management](https://techcommunity.microsoft.com/blog/adformysql/monitor-azure-database-for-mysql-using-percona-monitoring-and-management-pmm/2568545) and integrate them with Azure Database for MySQL flexible server.

For more information, see [Monitor Azure Database for MySQL flexible server](concepts-monitoring.md).

## Migration

Azure Database for MySQL flexible server runs the community version of MySQL. This design choice ensures full application compatibility and requires minimal refactoring costs to migrate existing applications developed on the MySQL engine to Azure Database for MySQL flexible server. You can migrate to Azure Database for MySQL flexible server by using the following options.

### Offline migrations

Use Azure Database Migration Service when network bandwidth between the source and Azure is good (for example: a high-speed ExpressRoute connection). For step-by-step instructions, see [Tutorial: Migrate MySQL to Azure Database for MySQL offline using DMS](../../dms/tutorial-mysql-azure-mysql-offline-portal.md).

Use compression settings in **mydumper** and **myloader** tools to efficiently move data over low-speed networks (such as the public internet). For step-by-step instructions, see [Migrate large databases to Azure Database for MySQL using mydumper/myloader](../../mysql/concepts-migrate-mydumper-myloader.md).

### Online or minimal-downtime migrations

For online or minimal-downtime migration, consider using community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) with [data-in replication](concepts-data-in-replication.md) to keep a flexible server in sync with an external MySQL source while you cut over. For more information, see [Migrate Azure Database for MySQL - Single Server to Azure Database for MySQL - Flexible Server with open-source tools](../../mysql/howto-migrate-single-flexible-minimum-downtime.md).

## Azure regions

One advantage of running your workload in Azure is its global reach. Azure Database for MySQL flexible server is currently available in the following Azure regions:

> [!NOTE]
> For Zone-redundant HA, due to zonal capacity constraints that can vary dynamically across regions, check the Azure portal experience for the latest support status. Availability might change based on current capacity and quota allocation in specific zones for your subscription.

| Region | Availability | Local-redundant HA | Zone-redundant HA | Geo-redundant backup |
| --- | --- | --- | --- | --- |
| Australia Central | Yes | Yes | No | No |
| Australia East | Yes | Yes | Yes | Yes |
| Australia Southeast | Yes | Yes | No | Yes |
| Austria East | Yes | Yes | No | Yes |
| Belgium Central | Yes | Yes | No | Yes |
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
| Denmark East | Yes | Yes | Yes | Yes |
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
| Japan West | Yes | Yes | Yes | Yes |
| Jio India West | Yes | Yes | No | No |
| Korea Central | Yes | Yes | Yes | Yes |
| Korea South | Yes | Yes | No | Yes |
| Malaysia West | Yes | Yes | Yes | Yes |
| Mexico Central | Yes | Yes | Yes | No |
| New Zealand North | Yes | Yes | Yes | No |
| North Central US | Yes | Yes | Yes | Yes |
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
| Spain Central | Yes | Yes | Yes | Yes |
| Sweden Central | Yes | Yes | Yes | No |
| Switzerland North | Yes | Yes | Yes | Yes |
| Switzerland West | Yes | Yes | No | Yes |
| Taiwan North | Yes | Yes | No | No |
| Taiwan Northwest | Yes | Yes | No | No |
| UAE Central | Yes | Yes | No | Yes |
| UAE North | Yes | Yes | Yes | Yes |
| UK South | Yes | Yes | Yes | Yes |
| UK West | Yes | Yes | No | Yes |
| USGov Virginia | Yes | Yes | Yes | No |
| USGov Arizona | Yes | Yes | Yes | Yes |
| USGov Texas | Yes | Yes | No | Yes |
| West Central US | Yes | Yes | No | Yes |
| West Europe | Yes | Yes | Yes | Yes |
| West US | Yes | Yes | No | Yes |
| West US 2 | Yes | Yes | Yes | Yes |
| West US 3 | Yes | Yes | Yes | Yes |

## Feedback and support

For questions or suggestions about working with Azure Database for MySQL flexible server, consider the following points of contact:

- To contact Azure support, [file a request in the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To provide feedback or to request new features, [post an idea via community feedback](https://feedback.azure.com/d365community/forum/47b1e71d-ee24-ec11-b6e6-000d3a4f0da0).

## Related content

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL flexible server by using the Azure CLI](quickstart-create-server-cli.md)
- [Manage Azure Database for MySQL using the Azure portal](how-to-manage-server-portal.md)
- [Quickstart: Use Python to connect and query data in Azure Database for MySQL flexible server](connect-python.md)
- [Use PHP with Azure Database for MySQL flexible server](connect-php.md)
