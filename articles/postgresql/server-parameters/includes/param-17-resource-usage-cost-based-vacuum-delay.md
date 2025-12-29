---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### vacuum_cost_delay

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | Vacuum cost delay in milliseconds. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_delay](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-VACUUM-COST-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_limit

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | Vacuum cost amount available before napping. |
| Data type | integer |
| Default value | `200` |
| Allowed values | `1-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_limit](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-VACUUM-COST-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_dirty

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | Vacuum cost for a page dirtied by vacuum. |
| Data type | integer |
| Default value | `20` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_dirty](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-DIRTY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_hit

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | Vacuum cost for a page found in the buffer cache. |
| Data type | integer |
| Default value | `1` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_hit](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-HIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_cost_page_miss

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Cost-Based Vacuum Delay |
| Description | Vacuum cost for a page not found in the buffer cache. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `0-10000` |
| Parameter type | dynamic |
| Documentation | [vacuum_cost_page_miss](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-VACUUM-COST-PAGE-MISS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



