---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### compute_query_id

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Statistics / Monitoring |
| Description    | Enables in-core computation of query identifiers.                           |
| Data type      | enumeration |
| Default value  | `auto`        |
| Allowed values | `auto`         |
| Parameter type | read-only      |
| Documentation  | [compute_query_id](https://www.postgresql.org/docs/15/runtime-config-statistics.html#GUC-COMPUTE-QUERY-ID)     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_executor_stats

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Statistics / Monitoring |
| Description    | Writes executor performance statistics to the server log.                   |
| Data type      | boolean     |
| Default value  | `off`         |
| Allowed values | `off`          |
| Parameter type | read-only      |
| Documentation  | [log_executor_stats](https://www.postgresql.org/docs/15/runtime-config-statistics.html#id-1.6.7.12.3.2.2.4.3)  |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_parser_stats

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Statistics / Monitoring |
| Description    | Writes parser performance statistics to the server log.                     |
| Data type      | boolean     |
| Default value  | `off`         |
| Allowed values | `off`          |
| Parameter type | read-only      |
| Documentation  | [log_parser_stats](https://www.postgresql.org/docs/15/runtime-config-statistics.html#id-1.6.7.12.3.2.2.4.3)    |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_planner_stats

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Statistics / Monitoring |
| Description    | Writes planner performance statistics to the server log.                    |
| Data type      | boolean     |
| Default value  | `off`         |
| Allowed values | `off`          |
| Parameter type | read-only      |
| Documentation  | [log_planner_stats](https://www.postgresql.org/docs/15/runtime-config-statistics.html#id-1.6.7.12.3.2.2.4.3)   |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_statement_stats

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Statistics / Monitoring |
| Description    | For each query, writes cumulative performance statistics to the server log. |
| Data type      | boolean     |
| Default value  | `off`         |
| Allowed values | `on,off`       |
| Parameter type | dynamic        |
| Documentation  | [log_statement_stats](https://www.postgresql.org/docs/15/runtime-config-statistics.html#id-1.6.7.12.3.2.2.4.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



