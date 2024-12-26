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
### block_size

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the size of a disk block.                                |
| Data type      | integer   |
| Default value  | `8192`        |
| Allowed values | `8192`         |
| Parameter type | read-only      |
| Documentation  | [block_size](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-BLOCK-SIZE)                       |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### data_checksums

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows whether data checksums are turned on for this cluster.   |
| Data type      | boolean   |
| Default value  | `on`          |
| Allowed values | `on`           |
| Parameter type | read-only      |
| Documentation  | [data_checksums](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-DATA-CHECKSUMS)               |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### data_directory_mode

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Mode of the data directory.                                    |
| Data type      | integer   |
| Default value  | `0700`        |
| Allowed values | `0700`         |
| Parameter type | read-only      |
| Documentation  | [data_directory_mode](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-DATA-DIRECTORY-MODE)     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### debug_assertions

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows whether the running server has assertion checks enabled. |
| Data type      | boolean   |
| Default value  | `off`         |
| Allowed values | `off`          |
| Parameter type | read-only      |
| Documentation  |                                                                                                                  |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### integer_datetimes

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Datetimes are integer based.                                   |
| Data type      | boolean   |
| Default value  | `on`          |
| Allowed values | `on`           |
| Parameter type | read-only      |
| Documentation  | [integer_datetimes](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-INTEGER-DATETIMES)         |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### lc_collate

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the collation order locale.                              |
| Data type      | string    |
| Default value  | `en_US.utf8`  |
| Allowed values | `en_US.utf8`   |
| Parameter type | read-only      |
| Documentation  | [lc_collate](https://www.postgresql.org/docs/13/locale.html)                                                     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### lc_ctype

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the character classification and case conversion locale. |
| Data type      | string    |
| Default value  | `en_US.utf8`  |
| Allowed values | `en_US.utf8`   |
| Parameter type | read-only      |
| Documentation  | [lc_ctype](https://www.postgresql.org/docs/13/locale.html)                                                       |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_function_args

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the maximum number of function arguments.                |
| Data type      | integer   |
| Default value  | `100`         |
| Allowed values | `100`          |
| Parameter type | read-only      |
| Documentation  | [max_function_args](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-MAX-FUNCTION-ARGS)         |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_identifier_length

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the maximum identifier length.                           |
| Data type      | integer   |
| Default value  | `63`          |
| Allowed values | `63`           |
| Parameter type | read-only      |
| Documentation  | [max_identifier_length](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-MAX-IDENTIFIER-LENGTH) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_index_keys

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the maximum number of index keys.                        |
| Data type      | integer   |
| Default value  | `32`          |
| Allowed values | `32`           |
| Parameter type | read-only      |
| Documentation  | [max_index_keys](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-MAX-INDEX-KEYS)               |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### segment_size

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the number of pages per disk file.                       |
| Data type      | integer   |
| Default value  | `131072`      |
| Allowed values | `131072`       |
| Parameter type | read-only      |
| Documentation  | [segment_size](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-SEGMENT-SIZE)                   |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### server_encoding

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Sets the server (database) character set encoding.             |
| Data type      | string    |
| Default value  | `UTF8`        |
| Allowed values | `UTF8`         |
| Parameter type | read-only      |
| Documentation  | [server_encoding](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-SERVER-ENCODING)             |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### server_version

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the server version.                                      |
| Data type      | string    |
| Default value  | `13.16`       |
| Allowed values | `13.16`        |
| Parameter type | read-only      |
| Documentation  | [server_version](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-SERVER-VERSION)               |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### server_version_num

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the server version as an integer.                        |
| Data type      | integer   |
| Default value  | `130016`      |
| Allowed values | `130016`       |
| Parameter type | read-only      |
| Documentation  | [server_version_num](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-SERVER-VERSION-NUM)       |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_library

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Name of the SSL library.                                       |
| Data type      | string    |
| Default value  | `OpenSSL`     |
| Allowed values | `OpenSSL`      |
| Parameter type | read-only      |
| Documentation  | [ssl_library](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-SSL-LIBRARY)                     |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_block_size

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the block size in the write ahead log.                   |
| Data type      | integer   |
| Default value  | `8192`        |
| Allowed values | `8192`         |
| Parameter type | read-only      |
| Documentation  | [wal_block_size](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-WAL-BLOCK-SIZE)               |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_segment_size

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Preset Options |
| Description    | Shows the size of write ahead log segments.                    |
| Data type      | integer   |
| Default value  | `16777216`    |
| Allowed values | `16777216`     |
| Parameter type | read-only      |
| Documentation  | [wal_segment_size](https://www.postgresql.org/docs/13/runtime-config-preset.html#GUC-WAL-SEGMENT-SIZE)           |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



