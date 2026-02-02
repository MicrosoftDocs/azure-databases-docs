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
### authentication_timeout

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Sets the maximum allowed time to complete client authentication. |
| Data type | integer |
| Default value | `30` |
| Allowed values | `30` |
| Parameter type | read-only |
| Documentation | [authentication_timeout](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-AUTHENTICATION-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### gss_accept_delegation

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Sets whether GSSAPI delegation should be accepted from the client. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [gss_accept_delegation](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-GSS-ACCEPT-DELEGATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### krb_caseins_users

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Sets whether Kerberos and GSSAPI user names should be treated as case-insensitive. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [krb_caseins_users](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-KRB-CASEINS-USERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### krb_server_keyfile

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Sets the location of the Kerberos server key file. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [krb_server_keyfile](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-KRB-SERVER-KEYFILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### password_encryption

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Chooses the algorithm for encrypting passwords. |
| Data type | enumeration |
| Default value | `scram-sha-256` |
| Allowed values | `md5,scram-sha-256` |
| Parameter type | dynamic |
| Documentation | [password_encryption](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### scram_iterations

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / Authentication |
| Description | Sets the iteration count for SCRAM secret generation. |
| Data type | integer |
| Default value | `4096` |
| Allowed values | `4096` |
| Parameter type | read-only |
| Documentation | [scram_iterations](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-SCRAM-ITERATIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



