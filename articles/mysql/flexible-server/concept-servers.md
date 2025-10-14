---
title: Server Concepts in Azure Database for MySQL - Flexible Server
description: This topic provides considerations and guidelines for working with Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Server concepts in Azure Database for MySQL - Flexible Server

This article provides considerations and guidelines for working with Azure Database for MySQL - Flexible Server.

## What is Azure Database for MySQL - Flexible Server?

Azure Database for MySQL - Flexible Server is a fully managed database service that runs the community version of MySQL. In general, the service provides flexibility and configuration customizations based on user requirements.

It's the same MySQL server construct that you might be familiar with in the on-premises world. Specifically, the flexible server is managed, provides out-of-the-box performance, improves server manageability and control, and exposes access and features at the server level.

An Azure Database for MySQL - Flexible Server instance:

- Is created within an Azure subscription.
- Is the parent resource for databases.
- Allows MySQL configuration exposed through server parameters.
- Performs automated backups and supports point-in-time restores.
- Provides a namespace for databases.
- Is a container with strong lifetime semantics: deleting a server deletes the contained databases.
- Collocates resources in a region.
- Supports customer-provided server maintenance schedules.
- Supports the ability to deploy flexible servers in a zone-redundant setup for improved high availability.
- Provides a virtual network integration for database server access.
- Provides a way to save costs by pausing when it's not in use.
- Provides the scope for management policies that apply to its databases; for example, sign-in, firewall, users, roles, and configurations.
- Supports the major versions MySQL 5.7 and MySQL 8.0. For more information, see [Connect to a gateway node to a specific MySQL version](./../concepts-supported-versions.md).

Within an Azure Database for MySQL - Flexible Server instance, you can create one or multiple databases. You can create a single database per server to use all the resources, or you can create multiple databases to share the resources. The pricing is structured per server, based on the configuration of compute tier, vCores, and storage (in gigabytes). For more information, see [Azure Database for MySQL - Flexible Server service tiers](./concepts-compute-storage.md).

## Stop and start a server

With Azure Database for MySQL - Flexible Server, you can stop the server when it's not in use and start the server when you resume activity. The purpose is to save costs on the database servers and pay for the resource only when it's in use. This ability becomes even more important for dev/test workloads and when you're using the server for only part of the day.

When you stop the server, all active connections are dropped. Later, when you want to bring the server back online, you can use either the [Stop/Start an Azure Database for MySQL - Flexible Server instance](how-to-stop-start-server-portal.md) or the Azure CLI.

When the server is in the stopped state, the server's compute isn't billed. However, storage continues to be billed because the server's storage remains to ensure that data files are available when you start the server again.

> [!IMPORTANT]  
> When you stop the server, it remains in that state for the next 30 days. If you don't manually start the server during that time, it's automatically started at the end of 30 days. You can chose to stop the server again if you're not using it.

During the time that the server is stopped, you can't perform any management operations on it. Operations that aren't supported on stopped servers include changing the pricing tier, number of vCores, storage size or I/O operations, backup retention day, server tag, server password, server parameters, storage autogrow, geo-redundant backup, high availability, and user identity. These operations appear as inactive in the Azure portal.

To change any configuration settings on a stopped server, you need to [start the server](how-to-stop-start-server-portal.md). For more information, see the [stop/start limitations](./concepts-limitations.md#stopstart-operations).

## Manage a server

You can manage the creation, deletion, server parameter configuration (*my.cnf*), scaling, networking, security, high availability, backup and restore, and monitoring of your Azure Database for MySQL - Flexible Server instance by using the [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) or the [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md).

In addition, the following stored procedures are available in Azure Database for MySQL - Flexible Server to perform certain required database administration tasks, because the server doesn't support `SUPER` user privileges.

| Stored procedure name | Input parameters | Output parameters | Usage note |
| --- | --- | --- | --- |
| *mysql.az_kill* | `processlist_id` | Not applicable | Equivalent to the [`KILL CONNECTION`](https://dev.mysql.com/doc/refman/8.0/en/kill.html) command. Terminates the connection associated with the provided `processlist_id` value after terminating any statement that the connection is executing. |
| *mysql.az_kill_query* | `processlist_id` | Not applicable | Equivalent to the [`KILL QUERY`](https://dev.mysql.com/doc/refman/8.0/en/kill.html) command. Terminates the statement that the connection is currently executing. Leaves the connection itself alive. |
| *mysql.az_load_timezone* | Not applicable | Not applicable | Loads [time zone tables](../single-server/how-to-server-parameters.md#working-with-the-time-zone-parameter) to allow the `time_zone` parameter to be set to named values (for example, `US/Pacific`). |

## Related content

- [creating a server](quickstart-create-server-portal.md)
- [monitoring and alerts](how-to-alert-on-metric.md)
