---
title: Extensions and Modules in Azure HorizonDB
description: Learn about extensions and modules in an Azure HorizonDB.
#customer intent: As a user, I want to learn what extensions and modules are in Azure HorizonDB, so that I can extend the functionality of my PostgreSQL database.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: concept-article
---

# Extensions and modules in Azure HorizonDB (Preview)

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

Some extensions that implement functionality by using shared libraries need to access that shared memory area from the code built in those libraries. Those extensions have one more requirement, which is that their shared library files must be loaded by the main engine process, as soon as the database engine starts. For those libraries, follow the instructions in [load libraries](how-to-load-libraries.md).

## Modules

Although they're not considered extensions because they don't have a **control file** and a **script file** to deploy bundled SQL objects in a database, another form of extensibility in PostgreSQL is implementing functionality in standalone shared binary library files.

You can load these files in memory when the database engine starts. They can implement code that typically detours the natural execution path of PostgreSQL to alter the default functioning of the engine. Such behavioral alterations normally aim to amplify some limited functionality of the engine.

Azure HorizonDB supports the following modules:

- auto_explain
- pg_failover_slots
- pg_partman_bgw
- wal2json

## Related content

- [Allow extensions in Azure HorizonDB (Preview)](how-to-allow-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB (Preview)](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB (Preview)](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB (Preview)](concepts-extensions-by-engine.md)
