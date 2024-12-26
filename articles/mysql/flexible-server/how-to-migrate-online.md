---
title: Minimal-Downtime Migration
description: This article describes how to perform a minimal-downtime migration of a MySQL database to Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Minimal-downtime migration to Azure Database for MySQL - Flexible Server

You can perform MySQL migrations to Azure Database for MySQL Flexible Server with minimal downtime by using Data-in replication, which limits the amount of downtime that is incurred by the application.

You can also refer to [Database Migration Guide](https://github.com/Azure/azure-mysql/tree/master/MigrationGuide) for detailed information and use cases about migrating databases to Azure Database for MySQL Flexible Server. This guide provides guidance that will lead the successful planning and execution of a MySQL migration to Azure.

## Overview

Using Data-in replication, you can configure the source as your primary and the target as your replica, so that there's continuous synching of any new transactions to Azure while the application remains running. After the data catches up on the target Azure side, you stop the application for a brief moment (minimum downtime), wait for the last batch of data (from the time you stop the application until the application is effectively unavailable to take any new traffic) to catch up in the target, and then update your connection string to point to Azure. When you're finished, your application will be live on Azure!

## Next step

> [!div class="nextstepaction"]
> [Database Migration Guide](https://github.com/Azure/azure-mysql/tree/master/MigrationGuide)
