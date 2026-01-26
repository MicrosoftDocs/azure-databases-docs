---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### cluster_name

| Attribute | Value |
| --- | --- |
| Category | Process Title |
| Description | Sets the name of the cluster, which is included in the process title. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [cluster_name](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-CLUSTER-NAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### update_process_title

| Attribute | Value |
| --- | --- |
| Category | Process Title |
| Description | Updates the process title to show the active SQL command. Enables updating of the process title every time a new SQL command is received by the server. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [update_process_title](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-UPDATE-PROCESS-TITLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



