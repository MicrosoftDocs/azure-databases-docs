---
title: Intelligent tuning
description: This article describes the intelligent tuning feature in Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: concept-article
---

# Intelligent tuning

Azure Database for PostgreSQL flexible server has an intelligent tuning feature designed to enhance performance automatically and help prevent problems. Intelligent tuning continuously monitors the Azure Database for PostgreSQL flexible server database's status and dynamically adapts the database to your workload.

This feature comprises two automatic tuning functions:

* **Autovacuum tuning**: This feature is deprecated and replaced with the newer [adaptive autovacuum](./concepts-adaptive-autovacuum.md).
* **Writes tuning**: This function monitors the volume and patterns of write operations, and it modifies parameters that affect write performance. These adjustments enhance both system performance and reliability, to proactively avert potential complications.

Learn how to [Configure intelligent tuning](how-to-configure-intelligent-tuning.md).

## Why intelligent tuning?

Tuning of write operations within the database is a critical part of maintaining the health and performance of an Azure Database for PostgreSQL flexible server. This task typically falls to database administrators. Constantly monitoring a database and fine-tuning write operations can be challenging and time-consuming. This task becomes increasingly complex when you're dealing with multiple databases.

This is where intelligent tuning steps in. Rather than manually overseeing and tuning your database, you can use intelligent tuning to automatically monitor and tune the database. You can then focus on other important tasks.

The writes tuning function observes the quantity and transactional patterns of write operations. It intelligently adjusts parameters such as `bgwriter_delay`, `checkpoint_completion_target`, `max_wal_size`, and `min_wal_size`. By doing so, it enhances system performance and reliability, even under high write loads.

When you use intelligent tuning, you can save valuable time and resources by relying on your Azure Database for PostgreSQL flexible server to maintain the optimal performance of your databases.

## How does intelligent tuning work?

Intelligent tuning is an ongoing monitoring and analysis process that not only learns about the characteristics of your workload but also tracks your current load and resource usage, such as CPU or IOPS. It doesn't disturb the normal operations of your application workload.

The process allows the database to dynamically adjust to your workload by discerning the current write performance, and checkpoint efficiency on your instance. With these insights, intelligent tuning deploys tuning actions that enhance your workload's performance and avoid potential pitfalls.

### Writes tuning

Intelligent tuning adjusts four parameters related to writes tuning: `bgwriter_delay`, `checkpoint_completion_target`, `max_wal_size`, and `min_wal_size`.

The `bgwriter_delay` parameter determines the frequency at which the background writer process is awakened to clean "dirty" buffers (buffers that are new or modified). The background writer process is one of three processes in an Azure Database for PostgreSQL flexible server that handle write operations. The other are the checkpointer process and back-end writes (standard client processes, such as application connections).

The background writer process's primary role is to alleviate the load from the main checkpointer process and decrease the strain of back-end writes. The `bgwriter_delay` parameter governs the frequency of background writer rounds. By adjusting this parameter, you can also optimize the performance of Data Manipulation Language (DML) queries.

The `checkpoint_completion_target` parameter is part of the second write mechanism that an Azure Database for PostgreSQL flexible server instance supports, specifically the checkpointer process. Checkpoints occur at constant intervals that `checkpoint_timeout` defines (unless forced by exceeding the configured space). To avoid overloading the I/O system with a surge of page writes, writing dirty buffers during a checkpoint is spread out over a period of time. The `checkpoint_completion_target` parameter controls this duration by using `checkpoint_timeout` to specify the duration as a fraction of the checkpoint interval.

The default value of `checkpoint_completion_target` is 0.9 (since PostgreSQL 14). This value generally works best, because it spreads the I/O load over the maximum time period. In rare instances, checkpoints might not finish in time because of unexpected fluctuations in the number of needed Write-Ahead Logging (WAL) segments. Potential impact on performance is the reason why `checkpoint_completion_target` is a target metric for intelligent tuning.

## Limitations and known issues

* Intelligent tuning makes optimizations only in specific ranges. It's possible that the feature doesn't make any changes.
* Intelligent tuning doesn't adjust `ANALYZE` settings.

## Related content

- [Configure intelligent tuning](how-to-configure-intelligent-tuning.md).
- [Troubleshooting for Azure Database for PostgreSQL](../troubleshoot/concepts-troubleshooting-guides.md).
- [Autovacuum tuning in Azure Database for PostgreSQL](../troubleshoot/how-to-autovacuum-tuning.md).
- [Troubleshoot high IOPS utilization in Azure Database for PostgreSQL](../troubleshoot/how-to-high-io-utilization.md).
- [Best practices to bulk upload data to Azure Database for PostgreSQL](../troubleshoot/how-to-bulk-load-data.md).
- [Troubleshoot high CPU utilization in an Azure Database for PostgreSQL](../troubleshoot/how-to-high-cpu-utilization.md).
- [Query Performance Insight in Azure Database for PostgreSQL](concepts-query-performance-insight.md).
