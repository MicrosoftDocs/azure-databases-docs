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
### ssl

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Enables SSL connections. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [ssl](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_ca_file

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Location of the SSL certificate authority file. |
| Data type | string |
| Default value | `/datadrive/certs/ca.pem` |
| Allowed values | `/datadrive/certs/ca.pem` |
| Parameter type | read-only |
| Documentation | [ssl_ca_file](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-CA-FILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_cert_file

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Location of the SSL server certificate file. |
| Data type | string |
| Default value | `/datadrive/certs/cert.pem` |
| Allowed values | `/datadrive/certs/cert.pem` |
| Parameter type | read-only |
| Documentation | [ssl_cert_file](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-CERT-FILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_ciphers

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Sets the list of allowed SSL ciphers. |
| Data type | string |
| Default value | `ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256` |
| Allowed values | `ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256` |
| Parameter type | read-only |
| Documentation | [ssl_ciphers](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-CIPHERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_crl_file

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Location of the SSL certificate revocation list file. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [ssl_crl_file](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-CRL-FILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_dh_params_file

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Location of the SSL DH parameters file. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [ssl_dh_params_file](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-DH-PARAMS-FILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_ecdh_curve

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Sets the curve to use for ECDH. |
| Data type | string |
| Default value | `prime256v1` |
| Allowed values | `prime256v1` |
| Parameter type | read-only |
| Documentation | [ssl_ecdh_curve](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-ECDH-CURVE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_key_file

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Location of the SSL server private key file. |
| Data type | string |
| Default value | `/datadrive/certs/key.pem` |
| Allowed values | `/datadrive/certs/key.pem` |
| Parameter type | read-only |
| Documentation | [ssl_key_file](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-KEY-FILE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_max_protocol_version

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Sets the maximum SSL/TLS protocol version to use. |
| Data type | enumeration |
| Default value | |
| Allowed values | `TLSv1.2,TLSv1.3` |
| Parameter type | dynamic |
| Documentation | [ssl_max_protocol_version](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-MAX-PROTOCOL-VERSION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_min_protocol_version

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Sets the minimum SSL/TLS protocol version to use. |
| Data type | enumeration |
| Default value | `TLSv1.2` |
| Allowed values | `TLSv1.2,TLSv1.3` |
| Parameter type | dynamic |
| Documentation | [ssl_min_protocol_version](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-MIN-PROTOCOL-VERSION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_passphrase_command

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Command to obtain passphrases for SSL. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [ssl_passphrase_command](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-PASSPHRASE-COMMAND) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_passphrase_command_supports_reload

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Also use ssl_passphrase_command during server reload. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [ssl_passphrase_command_supports_reload](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-PASSPHRASE-COMMAND-SUPPORTS-RELOAD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_prefer_server_ciphers

| Attribute | Value |
| --- | --- |
| Category | Connections and Authentication / SSL |
| Description | Give priority to server ciphersuite order. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [ssl_prefer_server_ciphers](https://www.postgresql.org/docs/13/runtime-config-connection.html#GUC-SSL-PREFER-SERVER-CIPHERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



