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
### client_connection_check_interval

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Sets the time interval between checks for disconnection while running queries. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [client_connection_check_interval](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-CLIENT-CONNECTION-CHECK-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_count

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Specifies the number of TCP keepalives that can be lost before the server's connection to the client is considered dead. |
| Data type | integer |
| Default value | `9` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_count](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-TCP-KEEPALIVES-COUNT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_idle

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Specifies the number of seconds of inactivity after which TCP should send a keepalive message to the client. |
| Data type | integer |
| Default value | `120` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_idle](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-TCP-KEEPALIVES-IDLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_keepalives_interval

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Specifies the number of seconds after which a TCP keepalive message that is not acknowledged by the client should be retransmitted. |
| Data type | integer |
| Default value | `30` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_keepalives_interval](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-TCP-KEEPALIVES-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### tcp_user_timeout

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / TCP Settings |
| Description | Specifies the amount of time that transmitted data may remain unacknowledged before the TCP connection is forcibly closed. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [tcp_user_timeout](https://www.postgresql.org/docs/14/runtime-config-connection.html#GUC-TCP-USER-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



