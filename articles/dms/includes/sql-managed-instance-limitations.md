---
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/28/2025
ms.service: azure-database-migration-service
ms.topic: include
ms.collection:
  - sql-migration-content
---

- If migrating a single database, the database backups must be placed in a flat-file structure inside a database folder (including the container root folder), and the folders can't be nested. Nested folders aren't supported.

- If migrating multiple databases using the same Azure Blob Storage container, you must place backup files for different databases in separate folders inside the container.

- Overwriting existing databases using Database Migration Service (DMS) in your target Azure SQL Managed Instance isn't supported.

- DMS doesn't support configuring high availability and disaster recovery on your target to match the source topology.

- The following server objects aren't supported:

  - SQL Server Agent jobs
  - Credentials
  - SQL Server Integration Services (SSIS) packages
  - Server audit

- You can't use an existing self-hosted integration runtime created from Azure Data Factory for database migrations with DMS. Initially, the self-hosted integration runtime should be created using the Azure SQL migration extension in Azure Data Studio and can be reused for further database migrations.

- A single Log Replay Service (LRS) job (created by DMS) can run for a maximum of 30 days. When this period expires, the job is automatically canceled thus your target database gets automatically deleted.

- If you receive the following error: `Memory-optimized filegroup must be empty in order to be restored on General Purpose tier of SQL Database Managed Instance`, this issue is by design. SQL Server In-Memory OLTP isn't supported on the General Purpose tier of Azure SQL Managed Instance. To continue migration, one way is to upgrade to Business Critical tier, which supports In-Memory OLTP. Another way is to make sure the source database isn't using it while the Azure SQL Managed Instance is General Purpose.
