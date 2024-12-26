---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### hot_standby

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Allows connections and queries during recovery.                                                                                                             |
| Data type      | boolean   |
| Default value  | `on`          |
| Allowed values | `on`            |
| Parameter type | read-only      |
| Documentation  | [hot_standby](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-HOT-STANDBY)                                     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### hot_standby_feedback

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Enables/disables the option whether hot standby needs to send feedback to the primary or upstream standby about queries currently executing on the standby. |
| Data type      | boolean   |
| Default value  | `off`         |
| Allowed values | `on,off`        |
| Parameter type | dynamic        |
| Documentation  | [hot_standby_feedback](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-HOT-STANDBY-FEEDBACK)                   |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_standby_archive_delay

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the maximum delay before canceling queries that conflict when a hot standby server is processing archived WAL data.                                    |
| Data type      | integer   |
| Default value  | `30000`       |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic        |
| Documentation  | [max_standby_archive_delay](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-MAX-STANDBY-ARCHIVE-DELAY)         |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_standby_streaming_delay

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the maximum delay before canceling queries that conflict when a hot standby server is processing streamed WAL data.                                    |
| Data type      | integer   |
| Default value  | `30000`       |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic        |
| Documentation  | [max_standby_streaming_delay](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-MAX-STANDBY-STREAMING-DELAY)     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### primary_conninfo

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the connection string to be used to connect to the sending server.                                                                                     |
| Data type      | string    |
| Default value  |               |
| Allowed values |                 |
| Parameter type | read-only      |
| Documentation  | [primary_conninfo](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-PRIMARY-CONNINFO)                           |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### primary_slot_name

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the name of the replication slot to use on the sending server.                                                                                         |
| Data type      | string    |
| Default value  |               |
| Allowed values |                 |
| Parameter type | read-only      |
| Documentation  | [primary_slot_name](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-PRIMARY-SLOT-NAME)                         |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recovery_min_apply_delay

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the minimum delay for applying changes during recovery.                                                                                                |
| Data type      | integer   |
| Default value  | `0`           |
| Allowed values | `0`             |
| Parameter type | read-only      |
| Documentation  | [recovery_min_apply_delay](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-RECOVERY-MIN-APPLY-DELAY)           |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_receiver_create_temp_slot

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets whether a WAL receiver should create a temporary replication slot if no permanent slot is configured.                                                  |
| Data type      | boolean   |
| Default value  | `off`         |
| Allowed values | `off`           |
| Parameter type | read-only      |
| Documentation  | [wal_receiver_create_temp_slot](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-WAL-RECEIVER-CREATE-TEMP-SLOT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_receiver_status_interval

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the maximum interval between WAL receiver status reports to the primary.                                                                               |
| Data type      | integer   |
| Default value  | `10`          |
| Allowed values | `0-2147483`     |
| Parameter type | dynamic        |
| Documentation  | [wal_receiver_status_interval](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-WAL-RECEIVER-STATUS-INTERVAL)   |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_receiver_timeout

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the maximum wait time to receive data from the sending server.                                                                                         |
| Data type      | integer   |
| Default value  | `60000`       |
| Allowed values | `60000`         |
| Parameter type | read-only      |
| Documentation  | [wal_receiver_timeout](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-WAL-RECEIVER-TIMEOUT)                   |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_retrieve_retry_interval

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Replication / Standby Servers |
| Description    | Sets the time to wait before retrying to retrieve WAL after a failed attempt.                                                                               |
| Data type      | integer   |
| Default value  | `5000`        |
| Allowed values | `5000`          |
| Parameter type | read-only      |
| Documentation  | [wal_retrieve_retry_interval](https://www.postgresql.org/docs/16/runtime-config-replication.html#GUC-WAL-RETRIEVE-RETRY-INTERVAL)     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



