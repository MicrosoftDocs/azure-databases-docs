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
### bonjour

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Enables advertising the server via Bonjour. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [bonjour](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-BONJOUR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### bonjour_name

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the Bonjour service name. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [bonjour_name](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-BONJOUR-NAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### listen_addresses

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the host name or IP address(es) to listen to. |
| Data type | string |
| Default value | `*` |
| Allowed values | `*` |
| Parameter type | read-only |
| Documentation | [listen_addresses](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-LISTEN-ADDRESSES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_connections

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the maximum number of concurrent connections to the database server. |
| Data type | integer |
| Default value | Depends on resources (vCores, RAM, or disk space) allocated to the server. |
| Allowed values | `25-5000` |
| Parameter type | static |
| Documentation | [max_connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-MAX-CONNECTIONS) |


[!INCLUDE [server-parameters-azure-notes-max-connections](./server-parameters-azure-notes-max-connections.md)]



### port

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the TCP port the server listens on. |
| Data type | integer |
| Default value | `5432` |
| Allowed values | `5432` |
| Parameter type | read-only |
| Documentation | [port](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PORT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### reserved_connections

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the number of connections slots reserved for replication users and super users. |
| Data type | integer |
| Default value | `5` |
| Allowed values | `5` |
| Parameter type | read-only |
| Documentation | [reserved_connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-RESERVED-CONNECTIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### superuser_reserved_connections

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the number of connection slots reserved for superusers. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `10` |
| Parameter type | read-only |
| Documentation | [superuser_reserved_connections](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-SUPERUSER-RESERVED-CONNECTIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### unix_socket_directories

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the directories where Unix-domain sockets will be created. |
| Data type | string |
| Default value | `/tmp,/tmp/tuning_sockets` |
| Allowed values | `/tmp,/tmp/tuning_sockets` |
| Parameter type | read-only |
| Documentation | [unix_socket_directories](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-UNIX-SOCKET-DIRECTORIES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### unix_socket_group

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the owning group of the Unix-domain socket. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [unix_socket_group](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-UNIX-SOCKET-GROUP) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### unix_socket_permissions

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Connection Settings |
| Description | Sets the access permissions of the Unix-domain socket. |
| Data type | integer |
| Default value | `0777` |
| Allowed values | `0777` |
| Parameter type | read-only |
| Documentation | [unix_socket_permissions](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-UNIX-SOCKET-PERMISSIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



