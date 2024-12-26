---
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 09/18/2024
ms.service: azure-database-migration-service
ms.topic: include
ms.collection:
  - sql-migration-content
---

- [Download and install Azure Data Studio](/azure-data-studio/download-azure-data-studio).
- [Install the Azure SQL Migration extension](/azure-data-studio/extensions/azure-sql-migration-extension) from Azure Data Studio Marketplace.
- Have an Azure account that's assigned to one of the following built-in roles:

  - Contributor for the target instance of Azure SQL Database
  - Reader role for the Azure resource group that contains the target instance of Azure SQL Database
  - Owner or Contributor role for the Azure subscription (required if you create a new instance of Azure Database Migration Service)

  As an alternative to using one of these built-in roles, you can [assign a custom role](/data-migration/sql-server/database/custom-roles).

  > [!IMPORTANT]  
  > An Azure account is required only when you configure the migration steps. An Azure account isn't required for the assessment or to view Azure recommendations in the migration wizard in Azure Data Studio.

- Create a target instance of [Azure SQL Database](/azure/azure-sql/database/single-database-create-quickstart).

- Make sure that the SQL Server login that connects to the source SQL Server instance is a member of the db_datareader role and that the login for the target SQL Server instance is a member of the db_owner role.

- Migrate the database schema from source to target by using the [SQL Server dacpac extension](/azure-data-studio/extensions/sql-server-dacpac-extension) or the [SQL Database Projects extension](/azure-data-studio/extensions/sql-database-project-extension) in Azure Data Studio.

- If you're using Azure Database Migration Service for the first time, make sure that the Microsoft.DataMigration [resource provider is registered in your subscription](../quickstart-create-data-migration-service-portal.md#register-the-resource-provider).
