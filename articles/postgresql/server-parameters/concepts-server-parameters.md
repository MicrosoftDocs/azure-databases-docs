---
title: Server Parameters
description: Learn about the server parameters for an Azure Database for PostgreSQL flexible server instance.
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: concept-article
---

# Server parameters in Azure Database for PostgreSQL 

Azure Database for PostgreSQL provides a set of configurable parameters for each server.

These parameters can correspond to:

- **Database engine**: parameters defined by the PostgreSQL database engine or by binary libraries that implement functionality of extensions. Some examples of database engine built-in parameters are `autovacuum_max_workers`, `DateStyle`, `client_min_messages`, `password_encryption`, `max_connections`, `geqo`, `from_collapse_limit`, `cpu_tuple_cost`, `cpu_tuple_cost`, `max_standby_streaming_delay`, `log_connections`, `log_min_duration_statement`, `max_parallel_workers`, `bgwriter_delay`, and `shared_buffers`. Some examples of parameters defined by extensions are `pg_qs.max_query_text_length` (pg_qs extension, implementing functionality for [query store](../monitor/concepts-query-store.md)), `pg_stat_statements.max` ([pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) extension), `pgaudit.log_catalog` ([pgaudit](https://github.com/pgaudit/pgaudit) extension), and `cron.database_name` ([cron](https://github.com/citusdata/pg_cron) extension).
- **Non-database engine**: parameters that control some built-in functionality, which is core to the Azure Database for PostgreSQL service, but is not part of the database engine or any of its extensions. Some examples of these are `metrics.collector_database_activity` (controls whether or not the service should collect the list of metrics which are considered [enhanced metrics](../monitor/concepts-monitoring.md#enhanced-metrics) and aren't collected by default), `pgbouncer.enabled` (allows the user to activate the instance of [PgBouncer](../connectivity/concepts-pgbouncer.md) which is built into the service), `index_tuning.analysis_interval` (sets the frequency at which [automatic index tuning](../monitor/concepts-index-tuning.md) should wake up to produce recommendations)

## Customize parameters

Both, **database engine** and **non-database engine** parameters can be configured at the server level. For more information, see [set the value of one or more server parameters](how-to-server-parameters-set-value.md).

> [!NOTE]
> Because Azure Database for PostgreSQL is a managed database service, users don't have host or operating system access to view or modify configuration files such as *postgresql.conf*. The content of the files is automatically updated based on parameter changes that you make.

**Database engine** parameters can also be configured at more granular scopes. These adjustments override globally set values. Their scope and duration depend on the level at which you make them:

* **Database level**: Use the `ALTER DATABASE` command for database-specific configurations.
* **Role or user level**: Use the `ALTER USER` command for user-centric settings.
* **Function, procedure level**: When you're defining a function or procedure, you can specify or alter the configuration parameters that are used when the function is called.
* **Table level**: As an example, you can modify parameters related to autovacuum at this level.
* **Session level**: For the life of an individual database session, you can adjust specific parameters. PostgreSQL facilitates this adjustment with the following SQL commands:

  * Use the `SET` command to make session-specific adjustments. These changes serve as the default settings during the current session. Access to these changes might require specific `SET` privileges, and the limitations for modifiable and read-only parameters described earlier don't apply. The corresponding SQL function is `set_config(setting_name, new_value, is_local)`.
  * Use the `SHOW` command to examine existing parameter settings. Its SQL function equivalent is `current_setting(setting_name text)`.


## Work with time zone parameters
If you plan to work with date and time data in PostgreSQL, make sure that you set the correct time zone for your location. All timezone-aware dates and times are stored internally in PostgreSQL in UTC. They're converted to local time in the zone specified by the **TimeZone** server parameter before being displayed to the client. This parameter can be edited on **Server parameters** page. 
PostgreSQL allows you to specify time zones in three different forms:

- A full time zone name, for example America/New_York. The recognized time zone names are listed in the [**pg_timezone_names**](https://www.postgresql.org/docs/9.2/view-pg-timezone-names.html) view.  
   Example to query this view in psql and get list of time zone names:
   <pre>select name FROM pg_timezone_names LIMIT 20;</pre>

   You should see result set like:

   <pre>
            name
        -----------------------
        GMT0
        Iceland
        Factory
        NZ-CHAT
        America/Panama
        America/Fort_Nelson
        America/Pangnirtung
        America/Belem
        America/Coral_Harbour
        America/Guayaquil
        America/Marigot
        America/Barbados
        America/Porto_Velho
        America/Bogota
        America/Menominee
        America/Martinique
        America/Asuncion
        America/Toronto
        America/Tortola
        America/Managua
        (20 rows)
    </pre>
   
- A time zone abbreviation, for example PST. Such a specification merely defines a particular offset from UTC, in contrast to full time zone names which can imply a set of daylight savings transition-date rules as well. The recognized abbreviations are listed in the [**pg_timezone_abbrevs view**](https://www.postgresql.org/docs/current/view-pg-timezone-abbrevs.html)
   Example to query this view in psql and get list of time zone abbreviations:

   <pre> select abbrev from pg_timezone_abbrevs limit 20;</pre>

    You should see result set like:

     <pre>
        abbrev|
        ------+
        ACDT  |
        ACSST |
        ACST  |
        ACT   |
        ACWST |
        ADT   |
        AEDT  |
        AESST |
        AEST  |
        AFT   |
        AKDT  |
        AKST  |
        ALMST |
        ALMT  |
        AMST  |
        AMT   |
        ANAST |
        ANAT  |
        ARST  |
        ART   |
    </pre>

- In addition to the timezone names and abbreviations PostgreSQL accepts POSIX-style time zone specifications of the form STDoffset or STDoffsetDST. STD is a zone abbreviation. Offset is a numeric offset in hours west from UTC. DST is an optional daylight-savings zone abbreviation, assumed to stand for one hour ahead of the given offset.

## Supported server parameters

[!INCLUDE [server-parameters-table](includes/server-parameters-table.md)]


## Related content

- [Configure server parameters](how-to-server-parameters-list-all.md).
