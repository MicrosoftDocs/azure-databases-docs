---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### azure.migration_copy_with_binary

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set to on, this parameter will enable the use of the binary format for copying data during migration. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_copy_with_binary](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_analyze

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set to on, this parameter will skip the analyze phase (`vacuumdb --analyze-only`) during the migration. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_analyze](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_extensions

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set to on, this parameter will skip the migration of extensions. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_extensions](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_large_objects

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set to on, this parameter will skip the migration of large objects such as BLOBs. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_large_objects](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_role_user

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set to on, this parameter will exclude user roles from the migration process. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_role_user](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_table_split_size

| Attribute | Value |
| --- | --- |
| Category | Migration |
| Description | When set, this parameter specifies the size at which tables will be partitioned during migration. |
| Data type | integer |
| Default value | `20480` |
| Allowed values | `1-204800` |
| Parameter type | dynamic |
| Documentation | [azure.migration_table_split_size](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



