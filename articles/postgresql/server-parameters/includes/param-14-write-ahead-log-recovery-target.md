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
### recovery_target

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Set to \"immediate\" to end recovery as soon as a consistent state is reached. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [recovery_target](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_action

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets the action to perform upon reaching the recovery target. |
| Data type | enumeration |
| Default value | `pause` |
| Allowed values | `pause` |
| Parameter type | read-only |
| Documentation | [recovery_target_action](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-ACTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_inclusive

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets whether to include or exclude transaction with recovery target. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [recovery_target_inclusive](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-INCLUSIVE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_lsn

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets the LSN of the write-ahead log location up to which recovery will proceed. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [recovery_target_lsn](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-LSN) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_name

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets the named restore point up to which recovery will proceed. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [recovery_target_name](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-NAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_time

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets the time stamp up to which recovery will proceed. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [recovery_target_time](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-TIME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_timeline

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Specifies the timeline to recover into. |
| Data type | string |
| Default value | `latest` |
| Allowed values | `latest` |
| Parameter type | read-only |
| Documentation | [recovery_target_timeline](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-TIMELINE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_target_xid

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Recovery Target |
| Description | Sets the transaction ID up to which recovery will proceed. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [recovery_target_xid](https://www.postgresql.org/docs/14/runtime-config-wal.html#GUC-RECOVERY-TARGET-XID) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



