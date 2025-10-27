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
### hot_standby

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Allows connections and queries during recovery. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [hot_standby](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-HOT-STANDBY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### hot_standby_feedback

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Enables/disables the option whether hot standby needs to send feedback to the primary or upstream standby about queries currently executing on the standby. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [hot_standby_feedback](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-HOT-STANDBY-FEEDBACK) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_standby_archive_delay

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Sets the maximum delay before canceling queries that conflict when a hot standby server is processing archived WAL data. |
| Data type | integer |
| Default value | `30000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [max_standby_archive_delay](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-MAX-STANDBY-ARCHIVE-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_standby_streaming_delay

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Sets the maximum delay before canceling queries that conflict when a hot standby server is processing streamed WAL data. |
| Data type | integer |
| Default value | `30000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [max_standby_streaming_delay](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-MAX-STANDBY-STREAMING-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_receiver_status_interval

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Sets the maximum interval between WAL receiver status reports to the primary. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `0-2147483` |
| Parameter type | dynamic |
| Documentation | [wal_receiver_status_interval](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-WAL-RECEIVER-STATUS-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_receiver_timeout

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Sets the maximum wait time to receive data from the primary. |
| Data type | integer |
| Default value | `60000` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [wal_receiver_timeout](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-WAL-RECEIVER-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_retrieve_retry_interval

| Attribute | Value |
| --- | --- |
| Category | Replication / Standby Servers |
| Description | Sets the time to wait before retrying to retrieve WAL after a failed attempt. |
| Data type | integer |
| Default value | `5000` |
| Allowed values | `5000` |
| Parameter type | read-only |
| Documentation | [wal_retrieve_retry_interval](https://www.postgresql.org/docs/11/runtime-config-replication.html#GUC-WAL-RETRIEVE-RETRY-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



