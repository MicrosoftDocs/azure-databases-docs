---
title: Oracle to Azure Database for PostgreSQL Pre-Migration Checklist
description: Best practices for migration from Oracle into Azure Database for PostgreSQL.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: maghan
ms.date: 01/24/2025
ms.service: azure-database-postgresql
ms.subservice: migration
ms.topic: best-practice
ms.collection:
  - migration
  - onprem-to-azure
---

# Oracle To Azure Database for PostgreSQL Pre-Migration Checklist

The following questions are intended to help you identify and record the compute resources required to maintain operational database performance. This information is critical when planning your migration as well as discussing migration plans with your selected migration partner(s).

## Workload Consistency

| Question | Answer |
| :--- | :--- |
| Does my database environment utilization change throughout the *day*? | &nbsp; |
| &nbsp; &nbsp; If Yes, which time(s) of *day* does activity peak? | &nbsp; |
| &nbsp; &nbsp; How long is the sustained peak activity period? | &nbsp; |
| Does my database environment utilization change throughout the *week*? | &nbsp; |
| &nbsp; &nbsp; If Yes, which day(s) of the *week* does activity peak? | &nbsp; |
| &nbsp; &nbsp; How long is the sustained peak activity period? | &nbsp; |
| Does my database environment utilization change throughout the *month*? | &nbsp; |
| &nbsp; &nbsp; If Yes, which time(s) of the *month* does activity peak? | &nbsp; |
| &nbsp; &nbsp; How long is the sustained peak activity period? | &nbsp; |
| Does my database environment utilization change throughout the *year*? | &nbsp; |
| &nbsp; &nbsp; If Yes, which month(s) of the *year* does activity peak? | &nbsp; |
| &nbsp; &nbsp; How long is the sustained peak activity period? | &nbsp; |

## Workload Type

| Question | Answer |
| :--- | :--- |
| Is my workload read-intensive, write-intensive, or hybrid of both? | &nbsp; |
| Are there any inbound or outbound linked database connection dependencies? | &nbsp; |
| Does my database use any file system mounts for data operations? | &nbsp; |
| How many dependent client applications are connected to my database? | &nbsp; |

## Peak Operational Periods

During peak operational periods...

| Question | Answer |
| :--- | :--- |
| How many cores are being utilized? | &nbsp; |
| What is the percentage of core utilization? | &nbsp; |
| What is the maximum amount of memory used by SGA? | &nbsp; |
| What is the maximum amount of memory used by PGA? | &nbsp; |
| What are the maximum IOPS required? | &nbsp; |
| What are the maximum storage throughput speeds? | &nbsp; |
| What is the maximum required network speed? | &nbsp; |
| What is the maximum number of concurrent active database connections? | &nbsp; |

To discuss these answers with experienced migration partners and to learn more about identifying the ideal software and/or partner solutions for your migration, see our [Oracle to Azure Postgres Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)

## Related content

- [Azure Database for PostgreSQL Migration Partners](./partners-migration-postgresql.md)
- [Oracle to Azure PostgreSQL Migration Playbook](https://download.microsoft.com/download/8/f/c/8fc4fe39-7cb1-484a-aaa0-418704b90c0e/Oracle%20to%20Azure%20Postgres%20Migration%20Playbook.pdf)
- [Oracle to Azure PostgreSQL Migration Workarounds](https://github.com/Microsoft/DataMigrationTeam/blob/master/Whitepapers/Oracle%20to%20Azure%20Database%20for%20PostgreSQL%20Migration%20Workarounds.pdf)
- [Microsoft Partner Site](https://partner.microsoft.com)
