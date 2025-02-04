---
title: Extensions
description: Learn about extensions in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/04/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
#customer intent: As a user, I want to learn what are extensions in an Azure Database for PostgreSQL flexible server.
---

# Extensions

Extensions in PostgreSQL are powerful tools that allow users to extend the functionality of the database system. They can range from simple SQL objects to complex binary libraries, providing additional features and capabilities that are not available in the core PostgreSQL distribution.

## How extensions work

When extensions are created (installed) in a database, they deploy a set of bundle objects that aim to extend the functionality of the engine. Those objects can be functions, operators, roles, data types, access methods, and other database object types.

When extensions are dropped (uninstalled) from a database, it's checked if there are no dependencies on any of the objects defined by the extension and, only if that's the case, all the objects that were created by the extension are removed.

To define an extension, it's at least required one **script file**, that contains the SQL commands to create the extension's objects, and one **control file**, that specifies a few basic properties of the extension itself. 

The implementation of the functionality provided by those extension's objects can be written in SQL or PL/pgSQL, or it can be implemented in a separate shared library file (a binary file), which is the result of compiling the source code (typically written in C or Rust) that actually implements the functionality.

In PostgreSQL, when the server is started, it defines an are of memory to which all backend processes can access, to cooperatively run any workloads. In PostgreSQL jargon, that are of memory is referred as **shared memory**. Some extensions that implement functionality using shared libraries, require accessing that shared memory from the code built in those librarires. Those extensions have the additional requirement that their shared library files are loaded by the main engine process, as soon as the server starts. For those libraries, you need to follow the instructions in [load libraries](how-to-load-libraries.md).

Although not considered extensions as such, because they don't have a **control file** and a **script file** to deploy bundled SQL objects in a database, another form of extensibility in PostgreSQL consist of implementing functionality in standalone shared library files. These files can also be loaded in memory when the server starts, and they can implement code that typically detours the natural execution path of PostgreSQL, and alters the default functioning of the engine. Such behavioral alterations, normally aim to amplify some limited functionality of the engine.

## Related content

- [Allow extensions](how-to-allow-extensions.md)
- [Special considerations with extensions](concepts-extensions-considerations.md)
- [List of extensions by name](concepts-extensions-versions.md)
