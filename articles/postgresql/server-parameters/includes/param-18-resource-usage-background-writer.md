---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 02/02/2026
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### bgwriter_delay

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Background Writer |
| Description | Background writer sleep time between rounds. |
| Data type | integer |
| Default value | `20` |
| Allowed values | `10-10000` |
| Parameter type | dynamic |
| Documentation | [bgwriter_delay](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-BGWRITER-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### bgwriter_flush_after

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Background Writer |
| Description | Number of pages after which previously performed writes are flushed to disk. |
| Data type | integer |
| Default value | `64` |
| Allowed values | `0-256` |
| Parameter type | dynamic |
| Documentation | [bgwriter_flush_after](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-BGWRITER-FLUSH-AFTER) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### bgwriter_lru_maxpages

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Background Writer |
| Description | Background writer maximum number of LRU pages to flush per round. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `0-1073741823` |
| Parameter type | dynamic |
| Documentation | [bgwriter_lru_maxpages](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-BGWRITER-LRU-MAXPAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### bgwriter_lru_multiplier

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Background Writer |
| Description | Multiple of the average buffer usage to free per round. |
| Data type | numeric |
| Default value | `2` |
| Allowed values | `0-10` |
| Parameter type | dynamic |
| Documentation | [bgwriter_lru_multiplier](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-BGWRITER-LRU-MULTIPLIER) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



