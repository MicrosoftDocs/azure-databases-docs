---
title: Extensions and modules
description: Learn about extensions and modules in an Azure Database for PostgreSQL flexible server instance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 10/14/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
# customer intent: As a user, I want to learn what are extensions and modules in an Azure Database for PostgreSQL flexible server instance.
---

# Extensions and modules

Extensions and modules in PostgreSQL are powerful tools that allow users to extend the functionality of the database system. They can range from simple SQL objects to complex binary libraries, providing extra features and capabilities that aren't available in the core PostgreSQL distribution.

## Extensions

To define an extension, it's at least required one **script file** that contains the SQL commands to create the objects distributed by the extension, and one **control file** that specifies a few basic properties of the extension itself.

When extensions are created, installed, or loaded in a database, they deploy a set of bundle objects that aim to extend the functionality of the engine. Those objects can be functions, operators, roles, data types, access methods, and other database object types.

When extensions are dropped, uninstalled, or unloaded from a database, all the objects that were created by the extension are removed. An exception to that case is when there are other objects in the database with dependencies on any of the objects defined by the extension.

The implementation of the functionality provided by those objects distributed by the extension can be written in SQL or PL/pgSQL. But it can also be implemented in a separate shared library (binary) file, which is the result of compiling the source code (typically written in C or Rust) that implements the functionality.

In PostgreSQL, extensions are managed through the `CREATE EXTENSION`, `ALTER EXTENSION`, `DROP EXTENSION`, and `COMMENT ON EXTENSION` commands.

- `CREATE EXTENSION` creates, installs, or loads an extension into the database in which the command is executed.
- `ALTER EXTENSION` updates the extension to a newer version.
- `DROP EXTENSION` drops, uninstalls, or unloads an extension from the database in which the command is executed.
- `COMMENT ON EXTENSION` stores a comment about the extension as a database object.

When the server is started, it defines an area of memory that all backend processes can access, to cooperatively run any workloads. In PostgreSQL jargon, that area of memory is referred to as **shared memory**.

Some extensions that implement functionality using shared libraries, nned to access that shared memory area from the code built in those libraries. Those extensions have one more requirement, which is that their shared library files must be loaded by the main engine process, as soon as the server starts. For those libraries, you need to follow the instructions in [load libraries](how-to-load-libraries.md).

## Modules

Although not considered extensions as such, because they don't have a **control file** and a **script file** to deploy bundled SQL objects in a database, another form of extensibility in PostgreSQL consists on implementing functionality in standalone shared binary library files.

These files can also be loaded in memory when the server starts and can implement code that, typically, detours the natural execution path of PostgreSQL to alter the default functioning of the engine. Such behavioral alterations normally aim to amplify some limited functionality of the engine.

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
