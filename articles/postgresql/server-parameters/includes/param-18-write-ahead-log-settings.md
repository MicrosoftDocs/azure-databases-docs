---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### commit_delay

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Sets the delay in microseconds between transaction commit and flushing WAL to disk. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-100000` |
| Parameter type | dynamic |
| Documentation | [commit_delay](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-COMMIT-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### commit_siblings

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Sets the minimum number of concurrent open transactions required before performing \"commit_delay\". |
| Data type | integer |
| Default value | `5` |
| Allowed values | `0-1000` |
| Parameter type | dynamic |
| Documentation | [commit_siblings](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-COMMIT-SIBLINGS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### fsync

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Forces synchronization of updates to disk. The server will use the fsync() system call in several places to make sure that updates are physically written to disk. This ensures that a database cluster will recover to a consistent state after an operating system or hardware crash. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [fsync](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-FSYNC) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### full_page_writes

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Writes full pages to WAL when first modified after a checkpoint. A page write in process during an operating system crash might be only partially written to disk. During recovery, the row changes stored in WAL are not enough to recover. This option writes pages when first modified after a checkpoint to WAL so full recovery is possible. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [full_page_writes](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-FULL-PAGE-WRITES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### synchronous_commit

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Sets the current transaction's synchronization level. |
| Data type | enumeration |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [synchronous_commit](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_buffers

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Sets the number of disk-page buffers in shared memory for WAL. Specify -1 to have this value determined as a fraction of shared_buffers. |
| Data type | integer |
| Default value | Depends on resources (vCores, RAM, or disk space) allocated to the server. |
| Allowed values | `-1-262143` |
| Parameter type | static |
| Documentation | [wal_buffers](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-BUFFERS) |


[!INCLUDE [server-parameters-azure-notes-wal-buffers](./server-parameters-azure-notes-wal-buffers.md)]



### wal_compression

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Compresses full-page writes written in WAL file. |
| Data type | enumeration |
| Default value | `zstd` |
| Allowed values | `pglz,lz4,zstd,on,off` |
| Parameter type | dynamic |
| Documentation | [wal_compression](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-COMPRESSION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_init_zero

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Writes zeroes to new WAL files before first use. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [wal_init_zero](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-INIT-ZERO) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_level

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Sets the level of information written to the WAL. |
| Data type | enumeration |
| Default value | `replica` |
| Allowed values | `replica,logical` |
| Parameter type | static |
| Documentation | [wal_level](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-LEVEL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_log_hints

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Writes full pages to WAL when first modified after a checkpoint, even for a non-critical modification. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [wal_log_hints](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-LOG-HINTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_recycle

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Recycles WAL files by renaming them. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [wal_recycle](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-RECYCLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_skip_threshold

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Minimum size of new file to fsync instead of writing WAL. |
| Data type | integer |
| Default value | `2048` |
| Allowed values | `2048` |
| Parameter type | read-only |
| Documentation | [wal_skip_threshold](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-SKIP-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_summary_keep_time

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Time for which WAL summary files should be kept. |
| Data type | integer |
| Default value | `14400` |
| Allowed values | `14400` |
| Parameter type | read-only |
| Documentation | [wal_summary_keep_time](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-SUMMARY-KEEP-TIME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_sync_method

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Selects the method used for forcing WAL updates to disk. |
| Data type | enumeration |
| Default value | `fdatasync` |
| Allowed values | `fdatasync` |
| Parameter type | read-only |
| Documentation | [wal_sync_method](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-SYNC-METHOD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_writer_delay

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Time between WAL flushes performed in the WAL writer. |
| Data type | integer |
| Default value | `200` |
| Allowed values | `1-10000` |
| Parameter type | dynamic |
| Documentation | [wal_writer_delay](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-WRITER-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_writer_flush_after

| Attribute | Value |
| --- | --- |
| Category | Write-Ahead Log / Settings |
| Description | Amount of WAL written out by WAL writer that triggers a flush. |
| Data type | integer |
| Default value | `128` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [wal_writer_flush_after](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-WRITER-FLUSH-AFTER) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



