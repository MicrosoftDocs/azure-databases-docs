---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### vacuum_cost_delay

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | the amount of time (in milliseconds) that the vacuum process will sleep when the cost limit has been exceeded. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_delay](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-VACUUM-COST-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_limit

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | The accumulated cost that will cause the vacuuming process to sleep. |
| Data type | integer |
| Default value | `200` |
| Allowed values | `1-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_limit](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-VACUUM-COST-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_dirty

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | The estimated cost charged when vacuum modifies a block that was previously clean. |
| Data type | integer |
| Default value | `20` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_dirty](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-DIRTY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_hit

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | The estimated cost for vacuuming a buffer found in the shared buffer cache. |
| Data type | integer |
| Default value | `1` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_hit](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-HIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_miss

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | The estimated cost for vacuuming a buffer that must be read from disk. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_miss](https://www.postgresql.org/docs/12/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-MISS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



