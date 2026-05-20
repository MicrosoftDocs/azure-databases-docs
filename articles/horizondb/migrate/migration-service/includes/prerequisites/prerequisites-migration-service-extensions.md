---
title: "Prerequisites for the Migration Service: Enable Extensions"
description: Get prerequisite information for enabling extensions for the migration service in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: include
---

To ensure a successful migration by using the migration service in Azure HorizonDB, you might need to verify extensions to your source PostgreSQL instance. Extensions provide functionality and features that might be required for your application. Make sure that you verify the extensions on the source PostgreSQL instance before you initiate the migration process.

In the target instance of Azure HorizonDB, enable supported extensions that are identified in the source PostgreSQL instance.

For more information, see [Extensions and modules in Azure HorizonDB](../../../../extensions/concepts-extensions.md).
