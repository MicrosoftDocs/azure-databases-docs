---
title: How to optimize costs
description: This article provides a list of cost optimization recommendations.
#customer intent: As a user managing Azure Database for PostgreSQL flexible server, I want to reduce my monthly costs so that I can stay within my budget without sacrificing performance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
---

# How to optimize costs in Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL is a relational database service in the Microsoft cloud based on the [PostgreSQL Community Edition](https://www.postgresql.org/). It's a fully managed database as a service offering that can handle mission-critical workloads with predictable performance and dynamic scalability.

This article provides a list of recommendations for optimizing Azure Database for PostgreSQL flexible server cost. The list includes design considerations, a configuration checklist, and recommended database settings to help you optimize your workload.

>[!div class="checklist"]
> * Use reserved capacity pricing.
> * Scale compute up or down.
> * Use Azure Advisor recommendations.
> * Evaluate high availability (HA) and disaster recovery (DR) requirements.
> * Consolidate databases and servers.
> * Place test servers in cost-efficient regions.
> * Start and stop servers.
> * Archive old data for cold storage.

## 1. Use reserved capacity pricing

Azure Database for PostgreSQL reserved capacity pricing lets you commit to a specific capacity for **1-3** **years**, so you can save costs if you use Azure Database for PostgreSQL flexible servers. The cost savings compared to pay-as-you-go pricing can be significant, depending on the amount of capacity reserved and the length of the term. You can purchase reserved capacity in increments of vCores and storage. Reserved capacity covers costs for Azure Database for PostgreSQL flexible servers in the same region and applies to your Azure subscription. Reserved pricing for Azure Database for PostgreSQL offers cost savings up to 40% for one-year and up to 60% for three-year commitments, for customers who reserve capacity. For more details, see [Pricing Calculator | Microsoft Azure](https://azure.microsoft.com/pricing/calculator/). To learn more, see [What are Azure Reservations?](/azure/cost-management-billing/reservations/save-compute-costs-reservations)

## 2. Scale compute up or down

Scaling up or down the resources of an Azure Database for PostgreSQL flexible server can help you optimize costs. Adjust the vCores and storage as needed to only pay for necessary resources. You can scale through the Azure portal, Azure CLI, or Azure REST API. Scaling compute resources up or down can be done at any time and requires server restart. Monitor your database usage patterns and adjust the resources accordingly to optimize costs and ensure performance. For more details, see Compute and Storage options in Azure Database for PostgreSQL.

Configure nonprod environments conservatively - Configure idle dev, test, and stage environments to have cost-efficient versions. Choosing burstable versions is ideal for workloads that don't need continuous full capacity.

To learn more, see [Scale compute](../scale/how-to-scale-compute.md).

## 3. Use Azure Advisor recommendations

Azure Advisor is a free service that provides recommendations to help optimize your Azure resources. It analyzes your resource configuration and usage patterns and provides recommendations on how to improve the performance, security, high availability, and cost-effectiveness of your Azure resources. The recommendations cover various Azure services including compute, storage, networking, and databases.

For Azure Database for PostgreSQL, Azure Advisor can provide recommendations on how to improve the performance, availability, and cost-effectiveness of your database. For example, it can suggest scaling the database up or down, using read-replicas to offload read-intensive workloads, or switching to reserved capacity pricing to reduce costs. Azure Advisor can also recommend security best practices, such as enabling encryption at rest, or enabling network security rules to limit incoming traffic to the database.

You can access the recommendations provided by Azure Advisor through the Azure portal, where you can view and implement the recommendations with just a few clicks. Implementing Azure Advisor recommendations can help you optimize your Azure resources and reduce costs. To learn more, see [Azure Advisor for Azure Database for PostgreSQL](concepts-azure-advisor-recommendations.md).

## 4. Evaluate high availability (HA) and disaster recovery (DR) requirements

Azure Database for PostgreSQL flexible servers have **built-in** node and storage resiliency at no extra cost to you. Node resiliency allows your Azure Database for PostgreSQL flexible server to automatically failover to a healthy VM with no data loss (that is, RPO zero) and with no connection string changes except that your application must reconnect. Similarly, the data and transaction logs are stored in three synchronous copies, and it automatically detects storage corruption and takes the corrective action. For most Dev/Test workloads, and for many production workloads, this configuration should suffice. 

If your workload requires AZ resiliency and lower RTO, you can enable High Availability (HA) with in-zone or cross-AZ standby. This option doubles your deployment costs, but it also provides a higher SLA. To achieve geo-resiliency for your application, you can set up GeoBackup for a lower cost but with a higher RTO. Alternatively, you can set up GeoReadReplica for double the cost, which offers an RTO in minutes if there was a geo-disaster.

Evaluate the requirements of your full application stack and then choose the right configuration for the Azure Database for PostgreSQL flexible server. For example, if your application isn't AZ resilient, there's nothing to be gained by configuring an Azure Database for PostgreSQL flexible server in AZ resilient configuration.

To learn more, see [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server).

## 5. Consolidate databases and servers

Consolidating databases can save you money with Azure Database for PostgreSQL flexible servers. By consolidating multiple databases into a single Azure Database for PostgreSQL flexible server, you reduce the number of instances and lower the overall cost of running Azure Database for PostgreSQL. Follow these steps to consolidate your databases and save costs:

- Access your server: Identify the server that you can consolidate, considering the database's size, geo-region, configuration (CPU, memory, IOPS), performance requirements, workload type, and data consistency needs.
- Create a new Azure Database for PostgreSQL flexible server: Create a new Azure Database for PostgreSQL flexible server with enough vCPUs, memory, and storage to support the consolidated databases.
- Reuse an existing Azure Database for PostgreSQL flexible server: If you already have an existing server, make sure it has enough vCPUs, memory, and storage to support the consolidated databases.
- Migrate the databases: Migrate the databases to the new Azure Database for PostgreSQL flexible server. Use tools such as `pg_dump` and `pg_restore` to export and import databases.
- Monitor performance: Monitor the performance of the consolidated Azure Database for PostgreSQL flexible server and adjust the resources as needed to ensure optimal performance.

Consolidating databases helps you save costs by reducing the number of Azure Database for PostgreSQL flexible servers you need to run and by enabling you to use larger instances that are more cost-effective than smaller instances. Evaluate the impact of consolidation on your databases' performance and ensure that the consolidated Azure Database for PostgreSQL flexible server is appropriately sized to meet all database needs.

To learn more, see [Improve the performance of Azure applications by using Azure Advisor](/azure/advisor/advisor-reference-performance-recommendations#databases).

## 6. Place test servers in cost-efficient regions

Creating a test server in a cost-efficient Azure region can save you money with Azure Database for PostgreSQL flexible servers. By creating a test server in a region with lower cost of computing resources, you reduce the cost of running your test server and minimize the cost of running Azure Database for PostgreSQL. Follow these steps to create a test server in a cost-efficient Azure region:

1. Identify a cost-efficient region: Identify an Azure region with lower cost of computing resources.
1. Create a new Azure Database for PostgreSQL flexible server: Create a new Azure Database for PostgreSQL flexible server in the cost-efficient region with the right configuration for your test environment.
1. Migrate test data: Migrate the test data to the new Azure Database for PostgreSQL flexible server. Use tools such as `pg_dump` and `pg_restore` to export and import databases.
1. Monitor performance: Monitor the performance of the test server and adjust the resources as needed to ensure optimal performance.

By creating a test server in a cost-efficient Azure region, you reduce the cost of running your test server and minimize the cost of running Azure Database for PostgreSQL. Evaluate the impact of the region on your test server's performance and your organization's specific regional requirements. This evaluation ensures that network latency and data transfer costs are acceptable for your use case.

To learn more, see [Azure regions](/azure/architecture/framework/cost/design-regions).

## 7. Start and stop servers

Starting and stopping servers can help you save money when using Azure Database for PostgreSQL flexible servers. By running the server only when you need it, you reduce the cost of running Azure Database for PostgreSQL. Follow these steps to start and stop servers and save costs:

1. Identify the server: Identify the Azure Database for PostgreSQL flexible server that you want to start and stop.
1. Start the server: Start the Azure Database for PostgreSQL flexible server when you need it. You can start the server by using the Azure portal, Azure CLI, or Azure REST API.
1. Stop the server: Stop the Azure Database for PostgreSQL flexible server when you don't need it. You can stop the server by using the Azure portal, Azure CLI, or Azure REST API.
1. If a server is in a stopped (or idle) state for several continuous weeks, consider dropping the server after the required due diligence.

By starting and stopping the server as needed, you reduce the cost of running an Azure Database for PostgreSQL flexible server. To ensure smooth database performance, evaluate the impact of starting and stopping the server and have a reliable process in place for these actions as required. For more information, see [Stop compute of a server](how-to-stop-server.md) and [Start compute of a server](how-to-start-server.md).

## 8. Archive old data for cold storage

Archiving infrequently accessed data to Azure archive store (while still keeping access) can help reduce costs. Export data from your Azure Database for PostgreSQL flexible server to Azure Archived Storage and store it in a lower-cost storage tier. 

1. Set up Azure Blob Storage account and create a container for your database backups.
1. Use `pg_dump` to export the old data to a file.
1. Use the Azure CLI or PowerShell to upload the exported file to your Blob Storage container.
1. Set up a retention policy on the Blob Storage container to automatically delete old backups.
1. Modify the backup script to export the old data to Blob Storage instead of local storage.
1. Test the backup and restore process to ensure that the archived data can be restored if needed.

You can also use Azure Data Factory to automate this process.

For more information, see [Migrate your PostgreSQL database by using dump and restore](../migrate/how-to-migrate-using-dump-and-restore.md).

## Tradeoffs for cost

As you design your application database on Azure Database for PostgreSQL, consider tradeoffs between cost optimization and other aspects of the design, such as security, scalability, resilience, and operability.

**Cost vs reliability**
> Cost has a direct correlation with reliability.

**Cost vs performance efficiency**
> Boosting performance leads to higher cost.

**Cost vs security**
> Increasing security of the workload increases cost.

**Cost vs operational excellence**
> Investing in systems monitoring and automation might increase the cost initially but over time reduces cost.

## Related content

- [Overview of the cost optimization pillar](/azure/architecture/framework/cost/overview).
- [Tradeoffs for cost](/azure/architecture/framework/cost/tradeoffs).
- [Checklist - Optimize cost](/azure/architecture/framework/cost/optimize-checklist).
- [Checklist - Monitor cost](/azure/architecture/framework/cost/monitor-checklist).
