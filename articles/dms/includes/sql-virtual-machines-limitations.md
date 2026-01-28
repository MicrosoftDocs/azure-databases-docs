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

- If migrating a single database, the database backups must be placed in a flat-file structure inside a database folder (including container root folder), and the folders can't be nested. Nested folders aren't supported.

- If migrating multiple databases using the same Azure Blob Storage container, you must place backup files for different databases in separate folders inside the container.

- Overwriting existing databases using Database Migration Service (DMS) in your target SQL Server on Azure Virtual Machine isn't supported.

- DMS doesn't support configuring high availability and disaster recovery on your target to match source topology.

- The following server objects aren't supported:
  - SQL Server Agent jobs
  - Credentials
  - SQL Server Integration Services (SSIS) packages
  - Server audit

- You can't use an existing self-hosted integration runtime created from Azure Data Factory for database migrations with DMS. Initially, the self-hosted integration runtime should be created using the Azure SQL migration extension in Azure Data Studio, and can be reused for further database migrations.

- A virtual machine (VM) with SQL Server 2008 and earlier as target versions aren't supported when migrating to SQL Server on Azure Virtual Machines.

- If you're using a VM with SQL Server 2012 or SQL Server 2014, you need to store your source database backup files on an Azure Blob Storage container instead of using the network share option. Store the backup files as page blobs, since block blobs are only supported in SQL Server 2016 and later versions.

- You must make sure the SQL Server IaaS Agent Extension in the target Azure Virtual Machine is in **Full mode** instead of Lightweight mode.

- SQL Server IaaS Agent Extension only supports management of Default Server Instance or Single Named Instance.

<!-- The number of databases you can migrate to a SQL server Azure Virtual Machine depends on the hardware specification and workload, but there's no enforced limit. -->

- You can migrate a maximum of 100 databases to the same Azure SQL Server Virtual Machine as the target using one or more migrations simultaneously. Moreover, once a migration with 100 databases finishes, you must wait for at least 30 minutes before starting a new migration to the same Azure SQL Server VM as the target. Also, every migration operation (start migration, cutover) for each database takes a few minutes sequentially. For example, to migrate 100 databases, it can take approximately 200 (2 x 100) minutes to create the migration queues and approximately 100 (1 x 100) minutes to cut over all 100 databases (excluding backup and restore timing). Therefore, the migration becomes slower as the number of databases increases.

  You should either schedule a longer migration window in advance based on rigorous migration testing or partitioning large number of databases into batches when migrating them to a SQL server Azure VM.

- Apart from configuring the networking/firewall of your Azure Storage Account to allow your VM to access backup files. You also need to configure the networking/firewall of your SQL Server on Azure VM to allow outbound connection to your storage account.

- You need to keep the power **on** for the target SQL Server on Azure VM while the SQL Migration is in progress. Also, when creating a new migration, failing over, or canceling the migration.

- **Error**: `Login failed for user 'NT Service\SQLIaaSExtensionQuery`.

  **Reason**: SQL Server instance is in single-user mode. One possible reason is the target SQL Server on Azure VM is in upgrade mode.

  **Solution**: Wait for the target SQL Server on Azure VM exit the upgrade mode and start migration again.

- **Error**: `Ext_RestoreSettingsError, message: Failed to create restore job.;Cannot create file 'F:\data\XXX.mdf' because it already exists`.

  **Solution**: Connect to the target SQL Server on Azure VM and delete the XXX.mdf file. Then, start migration again.
