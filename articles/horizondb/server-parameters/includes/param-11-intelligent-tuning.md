---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### intelligent_tuning

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Enables intelligent tuning |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [intelligent_tuning](https://go.microsoft.com/fwlink/?linkid=2274150) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### intelligent_tuning.metric_targets

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Specifies which metrics will be adjusted by intelligent tuning. |
| Data type | set |
| Default value | `none` |
| Allowed values | `none,Storage-checkpoint_completion_target,Storage-min_wal_size,Storage-max_wal_size,Storage-bgwriter_delay,tuning-autovacuum,all` |
| Parameter type | dynamic |
| Documentation | [intelligent_tuning.metric_targets](https://go.microsoft.com/fwlink/?linkid=2274150) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logfiles.download_enable

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Enables or disables server logs functionality. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [logfiles.download_enable](https://go.microsoft.com/fwlink/?linkid=2274270) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logfiles.retention_days

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Sets the retention period window in days for server logs - after this time data will be deleted. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-7` |
| Parameter type | dynamic |
| Documentation | [logfiles.retention_days](https://go.microsoft.com/fwlink/?linkid=2274270) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



