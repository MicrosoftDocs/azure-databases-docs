---
title: Possible Errors When Managing Extensions in Azure HorizonDB
description: This article describes possible errors that can be seen when managing extensions in an Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: troubleshooting
# customer intent: As a user, I want to learn how to troubleshoot possible errors that might occur while managing extensions in an Azure HorizonDB.
---

# Possible errors when managing extensions in Azure HorizonDB

## Extension "%s" isn't allow-listed for "azure_pg_admin" users in Azure HorizonDB

This error occurs when you run a `CREATE EXTENSION` or `DROP EXTENSION` command referring to an extension that isn't [allowlisted](how-to-allow-extensions.md), or an extension that isn't supported yet on the instance of Azure Database for flexible server on which you're running the command.

## Only members of "azure_pg_admin" are allowed to use CREATE EXTENSION

This error occurs when the user that runs a `CREATE EXTENSION` command isn't a member of `azure_pg_admin` role.

## Only members of "azure_pg_admin" are allowed to use DROP EXTENSION

This error occurs when the user that runs a `DROP EXTENSION` command isn't a member of `azure_pg_admin` role.

## SET SCHEMA clause for ALTER EXTENSION isn't supported.

This error occurs when the user tries to use the `SET SCHEMA` clause of the `ALTER EXTENSION` command. The use of this clause would move the referred extension's objects into another schema, as long as the extension is relocatable. However, the use of this clause for the `ALTER EXTENSION` command isn't supported in an Azure HorizonDB instance. The only supported way to move the objects created by an extension in an Azure HorizonDB instance to a specific schema is at creation time. Use the `WITH SCHEMA` clause of `CREATE EXTENSION`.

## Related content

- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
- [Allow extensions in Azure HorizonDB](how-to-allow-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB](concepts-extensions-by-engine.md)
