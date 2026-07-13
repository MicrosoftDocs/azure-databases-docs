---
title: Extensions and modules in Azure Database for PostgreSQL Flexible Server
description: Learn about extensions and modules in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn what are extensions and modules in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
---

# Extensions and modules in Azure Database for PostgreSQL flexible server

Extensions and modules in PostgreSQL are powerful tools that you can use to extend the functionality of the database system. They range from simple SQL objects to complex binary libraries, and they provide extra features and capabilities that aren't available in the core PostgreSQL distribution.

## Extensions

To define an extension, you need at least one **script file** that contains the SQL commands to create the objects distributed by the extension, and one **control file** that specifies a basic properties of the extension itself.

When you create, install, or load extensions in a database, they deploy a set of bundle objects that aim to extend the functionality of the engine. Those objects can be functions, operators, roles, data types, access methods, and other database object types.

When you drop, uninstall, or unload extensions from a database, the process removes all the objects that the extension created. An exception to that case is when there are other objects in the database with dependencies on any of the objects defined by the extension.

You can write the implementation of the functionality provided by those objects distributed by the extension in SQL or PL/pgSQL. But you can also implement it in a separate shared library (binary) file, which is the result of compiling the source code (typically written in C or Rust) that implements the functionality.

In PostgreSQL, you manage extensions through the `CREATE EXTENSION`, `ALTER EXTENSION`, `DROP EXTENSION`, and `COMMENT ON EXTENSION` commands.

- `CREATE EXTENSION` creates, installs, or loads an extension into the database in which you execute the command.
- `ALTER EXTENSION` updates the extension to a newer version.
- `DROP EXTENSION` drops, uninstalls, or unloads an extension from the database in which you execute the command.
- `COMMENT ON EXTENSION` stores a comment about the extension as a database object.

When the server starts, it defines an area of memory that all backend processes can access, to cooperatively run any workloads. In PostgreSQL jargon, that area of memory is referred to as **shared memory**.

Some extensions that implement functionality by using shared libraries need to access that shared memory area from the code built in those libraries. Those extensions have one more requirement, which is that their shared library files must be loaded by the main engine process, as soon as the server starts. For those libraries, follow the instructions in [load libraries](how-to-load-libraries.md).

## Modules

Although they're not considered extensions because they don't have a **control file** and a **script file** to deploy bundled SQL objects in a database, another form of extensibility in PostgreSQL is implementing functionality in standalone shared binary library files.

You can load these files in memory when the server starts. They can implement code that typically detours the natural execution path of PostgreSQL to alter the default functioning of the engine. Such behavioral alterations normally aim to amplify some limited functionality of the engine.

Azure Database for PostgreSQL supports the following modules:

- auto_explain
- pg_failover_slots
- pg_partman_bgw
- wal2json

## Related content

- [Allow extensions](how-to-allow-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
