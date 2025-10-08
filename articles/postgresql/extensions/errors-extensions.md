---
title: Possible errors when managing extensions
description: This article describes possible errors that can be seen when managing extensions in an Azure Database for PostgreSQL flexible server instance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/17/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to troubleshoot possible errors that might occur while managing extensions in an Azure Database for PostgreSQL flexible server instance.
---

# Possible errors when managing extensions


## Extension "%s" is not allow-listed for "azure_pg_admin" users in Azure Database for PostgreSQL

This error occurs when you run a `CREATE EXTENSION` or `DROP EXTENSION` command referring to an extension that isn't [allowlisted](how-to-allow-extensions.md), or an extension that isn't supported yet on the instance of Azure Database for flexible server on which you're running the command.

## Only members of "azure_pg_admin" are allowed to use CREATE EXTENSION

This error occurs when the user that runs a `CREATE EXTENSION` command isn't a member of `azure_pg_admin` role.

## Only members of "azure_pg_admin" are allowed to use DROP EXTENSION

This error occurs when the user that runs a `DROP EXTENSION` command isn't a member of `azure_pg_admin` role.

## SET SCHEMA clause for ALTER EXTENSION is not supported.

This error occurs when the user tries to use the `SET SCHEMA` clause of the `ALTER EXTENSION` command. The use of this clause would move the referred extension's objects into another schema, as long as the extension is relocatable. However, the use of this clause for the `ALTER EXTENSION` command isn't supported in an Azure Database for PostgreSQL flexible server instance. The only supported way to move the objects created by an extension in an Azure Database for PostgreSQL flexible server instance to a specific schema is at creation time. Use the `WITH SCHEMA` clause of `CREATE EXTENSION`.

## Related content

- [Extensions](concepts-extensions.md)
- [Allow extensions](how-to-allow-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
