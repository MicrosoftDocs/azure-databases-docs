---
title: "Prerequisites for the Migration Service: Enable Extensions"
description: Get prerequisite information for enabling extensions for the migration service in Azure Database for PostgreSQL.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/16/2025
ms.service: azure-database-postgresql
ms.topic: include
---

To ensure a successful migration by using the migration service in Azure Database for PostgreSQL, you might need to verify extensions to your source PostgreSQL instance. Extensions provide functionality and features that might be required for your application. Make sure that you verify the extensions on the source PostgreSQL instance before you initiate the migration process.

In the target instance of Azure Database for PostgreSQL flexible server, enable supported extensions that are identified in the source PostgreSQL instance.

For more information, see [Extensions and modules](../../../../extensions/concepts-extensions.md).
