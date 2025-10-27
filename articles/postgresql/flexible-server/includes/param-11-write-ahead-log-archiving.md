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
### archive_command

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Sets the shell command that will be called to archive a WAL file. |
| Data type | string |
| Default value | `BlobLogUpload.sh %f %p` |
| Allowed values | `BlobLogUpload.sh %f %p` |
| Parameter type | read-only |
| Documentation | [archive_command](https://www.postgresql.org/docs/11/runtime-config-wal.html#GUC-ARCHIVE-COMMAND) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### archive_mode

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Allows archiving of WAL files using archive_command. |
| Data type | enumeration |
| Default value | `always` |
| Allowed values | `always` |
| Parameter type | read-only |
| Documentation | [archive_mode](https://www.postgresql.org/docs/11/runtime-config-wal.html#GUC-ARCHIVE-MODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### archive_timeout

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Archiving |
| Description | Forces a switch to the next WAL file if a new file has not been started within N seconds. |
| Data type | integer |
| Default value | `300` |
| Allowed values | `300` |
| Parameter type | read-only |
| Documentation | [archive_timeout](https://www.postgresql.org/docs/11/runtime-config-wal.html#GUC-ARCHIVE-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



