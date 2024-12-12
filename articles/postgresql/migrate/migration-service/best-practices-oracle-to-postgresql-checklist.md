---
title: Best practices to migrate from Oracle into Flexible Server
description: Best practices for migration from Oracle into Azure Database for PostgreSQL.
author: jaredmeade
ms.author: jaredmeade
ms.reviewer: tbd
ms.date: 12/11/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual

---

# Best practices for seamless migration into Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The following questions are intended to help you identify and record the compute resources required to maintain operational database performance.  This information is critical when planning your migration as well as discussing migration plans with your selected migration partner(s).

## 1. Workload Consistency

| Question | Answer |
| :------------------- | :--- |
| Does my database environment utilization change throughout the *day*? | |
| &nbsp; &nbsp; If Yes, which time(s) of *day* does activity peak? | |
| &nbsp; &nbsp; How long is the sustained peak activity period? | |
| Does my database environment utilization change throughout the *week*? | |
| &nbsp; &nbsp; If Yes, which day(s) of the *week* does activity peak? | |
| &nbsp; &nbsp; How long is the sustained peak activity period? | |
| Does my database environment utilization change throughout the *month*? | |
| &nbsp; &nbsp; If Yes, which times(s) of the *month* does activity peak? | |
| &nbsp; &nbsp; How long is the sustained peak activity period? | |
| Does my database environment utilization change throughout the *year*? | |
| &nbsp; &nbsp; If Yes, which month(s) of the *year* does activity peak? | |
| &nbsp; &nbsp; How long is the sustained peak activity period? | |

## 2. Workload Type

| Question | Answer |
| :-------------------| :--- |
| Is my workload read-intensive, write-intensive, or hybrid of both? | |
| Are there any inbound or outbound linked database connection dependencies? | |
| Does my database use any file system mounts for data operations? | |
| How many dependent client applications are connected to my database? | |

## 3. Peak Operational Periods
During peak operational periods…

| Question | Answer |
| :------------------- | :--- |
| How many cores are being utilized? | |
| What is the percentage of core utilization? | |
| What is the maximum amount of memory used by SGA? | |
| What is the maximum amount of memory used by PGA? | |
| What are the maximum IOPS required? | |
| What are the maximum storage throughput speeds? | |
| What is the maximum required network speed? | |
| What is the maximum number of concurrent active database connections? | |

To learn more about identifying the ideal software and/or partner solutions for your migration, and discussing these answers with experienced migration partners, see our [Oracle to Azure Postgres Migration Playbook](../../../../flexible-server/LINK_TO_PLAYBOOK_PDF.)