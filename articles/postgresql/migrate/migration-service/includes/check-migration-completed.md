---
title: "Check The Migration When Completed (Online)"
description: Check the migration when completed (online).
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-postgresql
ms.topic: include
---
After completing the databases, you need to manually validate the data between source and target and verify that all the objects in the target database are successfully created.

After migration, you can perform the following tasks:

- Verify the data on your flexible server and ensure it's an exact copy of the source instance.

- Post verification, enable the high availability option on your flexible server as needed.

- Change the SKU of the flexible server to match the application needs. This change needs a database server restart.

- If you change any server parameters from their default values in the source instance, copy those server parameter values in the flexible server.

- Copy other server settings, such as tags, alerts, and firewall rules (if applicable), from the source instance to the flexible server.

- Make changes to your application to point the connection strings to a flexible server.

- Monitor the database performance closely to see if it requires performance tuning.
