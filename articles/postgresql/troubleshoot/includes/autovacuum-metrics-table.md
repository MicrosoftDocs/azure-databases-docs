---
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 2/4/2025
ms.service: azure-database-postgresql
ms.topic: include

---

Autovacuum metrics can be used to monitor and tune autovacuum performance for Azure Database for PostgreSQL flexible server. Each metric is emitted at a *30-minute* interval and has up to *93 days* of retention. You can create alerts for specific metrics, and you can split and filter metrics data by using the `DatabaseName` dimension.

#### How to enable autovacuum metrics

- Autovacuum metrics are disabled by default.
- To enable these metrics, set the server parameter `metrics.autovacuum_diagnostics` to `ON`.
- This parameter is dynamic, so an instance restart isn't required.

#### List of autovacuum metrics

|Display name                           |Metric ID                        |Unit   |Description                                                                                               |Dimension   |Default enabled|
|---------------------------------------|---------------------------------|-------|-----------------------------------------------------------------------------------------------------------|------------|---------------|
|**Analyze Counter User Tables**        |`analyze_count_user_tables`      |Count  |Number of times user-only tables have been manually analyzed in this database.                             |DatabaseName|No             |
|**AutoAnalyze Counter User Tables**    |`autoanalyze_count_user_tables`  |Count  |Number of times user-only tables have been analyzed by the autovacuum daemon in this database.             |DatabaseName|No             |
|**AutoVacuum Counter User Tables**     |`autovacuum_count_user_tables`   |Count  |Number of times user-only tables have been vacuumed by the autovacuum daemon in this database.             |DatabaseName|No             |
|**Bloat Percent (Preview)**            |`bloat_percent`                  |Percent|Estimated bloat percentage for user only tables.                                                           |DatabaseName|No             |
|**Estimated Dead Rows User Tables**    |`n_dead_tup_user_tables`         |Count  |Estimated number of dead rows for user-only tables in this database.                                       |DatabaseName|No             |
|**Estimated Live Rows User Tables**    |`n_live_tup_user_tables`         |Count  |Estimated number of live rows for user-only tables in this database.                                       |DatabaseName|No             |
|**Estimated Modifications User Tables**|`n_mod_since_analyze_user_tables`|Count  |Estimated number of rows that were modified since user-only tables were last analyzed.                     |DatabaseName|No             |
|**User Tables Analyzed**               |`tables_analyzed_user_tables`    |Count  |Number of user-only tables that have been analyzed in this database.                                       |DatabaseName|No             |
|**User Tables AutoAnalyzed**           |`tables_autoanalyzed_user_tables`|Count  |Number of user-only tables that have been analyzed by the autovacuum daemon in this database.              |DatabaseName|No             |
|**User Tables AutoVacuumed**           |`tables_autovacuumed_user_tables`|Count  |Number of user-only tables that have been vacuumed by the autovacuum daemon in this database.              |DatabaseName|No             |
|**User Tables Counter**                |`tables_counter_user_tables`     |Count  |Number of user-only tables in this database.                                                               |DatabaseName|No             |
|**User Tables Vacuumed**               |`tables_vacuumed_user_tables`    |Count  |Number of user-only tables that have been vacuumed in this database.                                       |DatabaseName|No             |
|**Vacuum Counter User Tables**         |`vacuum_count_user_tables`       |Count  |Number of times user-only tables have been manually vacuumed in this database (not counting `VACUUM FULL`).|DatabaseName|No             |

#### Considerations for using autovacuum metrics

- Autovacuum metrics that use the DatabaseName dimension have a *30-database* limit.
- On the *Burstable* SKU, the limit is 10 databases for metrics that use the DatabaseName dimension.
- The DatabaseName dimension limit is applied on the OID column, which reflects the order of creation for the database.