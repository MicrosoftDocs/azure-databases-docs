---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/18/2026
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### pgms_stats.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Internal Use Only: This parameter is used as a feature override switch. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pgms_wait_sampling.history_period

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Set the frequency, in milliseconds, at which wait events are sampled. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-600000` |
| Parameter type | dynamic |
| Documentation | [pgms_wait_sampling.history_period](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pgms_wait_sampling.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, wait sampling will be disabled despite the value set for pgms_wait_sampling.query_capture_mode. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pgms_wait_sampling.is_enabled_fs](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pgms_wait_sampling.query_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Selects which statements are tracked by the pgms_wait_sampling extension. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `all,none` |
| Parameter type | dynamic |
| Documentation | [pgms_wait_sampling.query_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.interval_length_minutes

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Sets the query_store capture interval in minutes for pg_qs - this is the frequency of data persistence. |
| Data type | integer |
| Default value | `15` |
| Allowed values | `1-30` |
| Parameter type | dynamic |
| Documentation | [pg_qs.interval_length_minutes](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, Query Store will be disabled despite the value set for pg_qs.query_capture_mode. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pg_qs.is_enabled_fs](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.max_plan_size

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Sets the maximum number of bytes that will be saved for query plan text for pg_qs; longer plans will be truncated. |
| Data type | integer |
| Default value | `7500` |
| Allowed values | `100-10000` |
| Parameter type | dynamic |
| Documentation | [pg_qs.max_plan_size](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.max_query_text_length

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Sets the maximum query text length that will be saved; longer queries will be truncated. |
| Data type | integer |
| Default value | `6000` |
| Allowed values | `100-10000` |
| Parameter type | dynamic |
| Documentation | [pg_qs.max_query_text_length](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.parameters_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Whether and when to capture query positional parameters. |
| Data type | enumeration |
| Default value | `capture_parameterless_only` |
| Allowed values | `capture_parameterless_only,capture_first_sample` |
| Parameter type | dynamic |
| Documentation | [pg_qs.parameters_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.query_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Sets query capture mode for query store. None disables any capturing. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `top,all,none` |
| Parameter type | dynamic |
| Documentation | [pg_qs.query_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.retention_period_in_days

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Sets the retention period window in days for pg_qs - after this time data will be deleted. |
| Data type | integer |
| Default value | `7` |
| Allowed values | `1-30` |
| Parameter type | dynamic |
| Documentation | [pg_qs.retention_period_in_days](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.store_query_plans

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Turns saving query plans on or off for pg_qs |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_qs.store_query_plans](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



### pg_qs.track_utility

| Attribute | Value |
| --- | --- |
| Category | Query Store |
| Description | Selects whether utility commands are tracked by pg_qs. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_qs.track_utility](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [parameters-azure-notes-void](./parameters-azure-notes-void.md)]



