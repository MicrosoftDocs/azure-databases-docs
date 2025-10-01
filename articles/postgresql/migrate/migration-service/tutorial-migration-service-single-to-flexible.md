---
title: "Migrate To Azure Database For Postgresql Flexible Server From Single Server"
titleSuffix: "Migrate from Single Server to flexible server."
description: "Learn about migrating your Single Server databases to Azure Database for PostgreSQL flexible server by using the Azure portal or CLI commands."
author: hariramt
ms.author: hariramt
ms.reviewer: maghan, adityaduvuri
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: migration-guide
ms.topic: tutorial
ms.custom:
  - devx-track-azurecli
# CustomerIntent: As a user, I want to learn how to migrate my Single Server databases to Azure Database for PostgreSQL flexible server using the Azure portal, so that I can take advantage of the flexibility and scalability offered by the flexible server.
---

# Tutorial: Migrate from Azure Database for PostgreSQL - Single Server to flexible server with the migration service

Using the Azure portal, you can migrate an Azure Database for PostgreSQL flexible server – Single Server to Azure Database for PostgreSQL flexible server. In this tutorial, we perform migration of a sample database from an Azure Database for PostgreSQL single server to a PostgreSQL flexible server using the Azure portal.

> [!div class="checklist"]
>  
> - Configure your Azure Database for PostgreSQL flexible server
> - Configure the migration task
> - Monitor the migration
> - Cancel the migration
> - Post migration

#### [Portal](#tab/portal)

[!INCLUDE [postgresql-single-server-portal-migrate](includes/single-server/postgresql-single-server-portal-migrate.md)]

#### [CLI](#tab/cli)

[!INCLUDE [postgresql-single-server-cli-migrate](includes/single-server/postgresql-single-server-cli-migrate.md)]

---

## Check the migration once complete

After a successful migration, ensure you can log in to your flexible server using the same credentials as on the single server. If you're encountering authentication errors on your flexible server after migrating from a single server, it might be due to the flexible server's VM being [FIPS-compliant](/compliance/regulatory/offering-FIPS-140-2) or using a different password encryption algorithm (SCRAM-SHA-256) compared to the single server's MD5 encryption. To mitigate this issue, follow these steps:

1) Change the password_encryption [server parameter on your flexible server](../../flexible-server/how-to-configure-server-parameters-using-portal.md) from SCRAM-SHA-256 to MD5.
2) Reinitiate the migration from your single server to the flexible server.
3) If authentication issues persist, delete the existing flexible server and [provision a new one](../../flexible-server/quickstart-create-server.md). Repeat steps 1 and 2 to resolve the issue.

This should resolve the authentication errors.

After migration, you can perform the following tasks:

- Verify the data on your flexible server and ensure it's an exact copy of the source instance.

- Post verification, enable the high availability option on your flexible server as needed.

- Change the SKU of the flexible server to match the application needs. This change needs a database server restart.

- If you change any server parameters from their default values in the source instance, copy those server parameter values in the flexible server.

- Copy other server settings like tags, alerts, and firewall rules (if applicable) from the source instance to the flexible server.

- Make changes to your application to point the connection strings to a flexible server.

- Monitor the database performance closely to see if it requires performance tuning.

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Best practices](best-practices-migration-service-postgresql.md)
- [Known Issues and limitations](concepts-known-issues-migration-service.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)
