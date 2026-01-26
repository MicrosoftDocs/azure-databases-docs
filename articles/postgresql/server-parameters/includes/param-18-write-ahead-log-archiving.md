---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/26/2026
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### archive_command

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Sets the shell command that will be called to archive a WAL file. This is used only if \"archive_library\" is not set. |
| Data type | string |
| Default value | `BlobLogUpload.sh %f %p` |
| Allowed values | `BlobLogUpload.sh %f %p` |
| Parameter type | read-only |
| Documentation | [archive_command](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-ARCHIVE-COMMAND) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### archive_library

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Sets the library that will be called to archive a WAL file. An empty string indicates that \"archive_command\" should be used. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [archive_library](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-ARCHIVE-LIBRARY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### archive_mode

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Allows archiving of WAL files using \"archive_command\". |
| Data type | enumeration |
| Default value | `always` |
| Allowed values | `always` |
| Parameter type | read-only |
| Documentation | [archive_mode](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-ARCHIVE-MODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### archive_timeout

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Sets the amount of time to wait before forcing a switch to the next WAL file. |
| Data type | integer |
| Default value | `300` |
| Allowed values | `300` |
| Parameter type | read-only |
| Documentation | [archive_timeout](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-ARCHIVE-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



