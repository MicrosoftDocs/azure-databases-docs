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
### array_nulls

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Enable input of NULL elements in arrays. When turned on, unquoted NULL in an array input value means a null value; otherwise it is taken literally. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [array_nulls](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-ARRAY-NULLS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### backslash_quote

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Sets whether \"\\'\" is allowed in string literals. |
| Data type | enumeration |
| Default value | `safe_encoding` |
| Allowed values | `safe_encoding,on,off` |
| Parameter type | dynamic |
| Documentation | [backslash_quote](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-BACKSLASH-QUOTE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### escape_string_warning

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Warn about backslash escapes in ordinary string literals. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [escape_string_warning](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-ESCAPE-STRING-WARNING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### lo_compat_privileges

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Enables backward compatibility mode for privilege checks on large objects. Skips privilege checks when reading or modifying large objects, for compatibility with PostgreSQL releases prior to 9.0. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [lo_compat_privileges](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-LO-COMPAT-PRIVILEGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### quote_all_identifiers

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | When generating SQL fragments, quote all identifiers. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [quote_all_identifiers](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-QUOTE-ALL-IDENTIFIERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### standard_conforming_strings

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Causes '...' strings to treat backslashes literally. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [standard_conforming_strings](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-STANDARD-CONFORMING-STRINGS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### synchronize_seqscans

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Previous PostgreSQL Versions |
| Description | Enable synchronized sequential scans. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [synchronize_seqscans](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-SYNCHRONIZE-SEQSCANS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



