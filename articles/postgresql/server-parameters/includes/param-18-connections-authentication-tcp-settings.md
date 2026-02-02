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
### client_connection_check_interval

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Sets the time interval between checks for disconnection while running queries. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [client_connection_check_interval](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-CLIENT-CONNECTION-CHECK-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_count

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Maximum number of TCP keepalive retransmits. Number of consecutive keepalive retransmits that can be lost before a connection is considered dead. A value of 0 uses the system default. |
| Data type | integer |
| Default value | `9` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_count](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-TCP-KEEPALIVES-COUNT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_idle

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Time between issuing TCP keepalives. A value of 0 uses the system default. |
| Data type | integer |
| Default value | `120` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_idle](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-TCP-KEEPALIVES-IDLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_interval

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Time between TCP keepalive retransmits. A value of 0 uses the system default. |
| Data type | integer |
| Default value | `30` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_interval](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-TCP-KEEPALIVES-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_user_timeout

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | TCP user timeout. A value of 0 uses the system default. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_user_timeout](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-TCP-USER-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



