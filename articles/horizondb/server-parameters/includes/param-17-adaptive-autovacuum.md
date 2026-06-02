---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: include
ms.custom:
  - automatically generated
---

### adaptive_autovacuum.open_transaction_threshold

| Attribute | Value |
| --- | --- |
| Category | Adaptive Autovacuum |
| Description | Specifies the timeout, in seconds, before an orphan transaction is rolled back and before a long running transaction is terminated. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483` |
| Parameter type | static |
| Documentation | |
[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]

### adaptive_autovacuum.optimize_configurations

| Attribute | Value |
| --- | --- |
| Category | Adaptive Autovacuum |
| Description | Configures server parameter tuning as disabled ('OFF') or enabled to tune and update autovacuum server parameters. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | static |
| Documentation | [adaptive_autovacuum.optimize_configurations](https://www.postgresql.org/docs/current/runtime-config-vacuum.html) |
[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]
