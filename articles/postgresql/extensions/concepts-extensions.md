---
title: Extensions
description: Learn about extensions in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/10/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
#customer intent: As a user, I want to learn what are extensions in an Azure Database for PostgreSQL flexible server.
---

# Extensions

Extensions in PostgreSQL are powerful tools that allow users to extend the functionality of the database system. They can range from simple SQL objects to complex binary libraries, providing extra features and capabilities that aren't available in the core PostgreSQL distribution.

> [!NOTE]
> Third-party extensions and extensibility modules offered in Azure Database for PostgreSQL - Flexible Server, are open-source licensed code. We don't offer any third-party extensions or extension versions with premium or proprietary licensing models. 

## How extensions work

When extensions are created (installed) in a database, they deploy a set of bundle objects that aim to extend the functionality of the engine. Those objects can be functions, operators, roles, data types, access methods, and other database object types.

When extensions are dropped (uninstalled) from a database, if there are no dependencies on any of the objects defined by the extension, all the objects that were created by the extension are removed.

To define an extension, it's at least required one **script file**, that contains the SQL commands to create the extension's objects, and one **control file**, that specifies a few basic properties of the extension itself. 

The implementation of the functionality provided by those extension's objects can be written in SQL or PL/pgSQL. It can also be implemented in a separate shared library file (a binary file), which is the result of compiling the source code (typically written in C or Rust) that actually implements the functionality.

In PostgreSQL, when the server is started, it defines an area of memory to which all backend processes can access, to cooperatively run any workloads. In PostgreSQL jargon, that area of memory is referred as **shared memory**. Some extensions that implement functionality using shared libraries, require accessing that shared memory from the code built in those libraries. Those extensions have one more requirement, which is that their shared library files are loaded by the main engine process, as soon as the server starts. For those libraries, you need to follow the instructions in [load libraries](how-to-load-libraries.md).

## Modules as another form of extensibility

Although not considered extensions as such, because they don't have a **control file** and a **script file** to deploy bundled SQL objects in a database, another form of extensibility in PostgreSQL consist of implementing functionality in standalone shared library files. These files can also be loaded in memory when the server starts, and they can implement code that typically detours the natural execution path of PostgreSQL, and alters the default functioning of the engine. Such behavioral alterations normally aim to amplify some limited functionality of the engine.

Using these modules, PostgreSQL supports the following forms of extensibility:

 - [Archive Modules](https://www.postgresql.org/docs/current/archive-modules.html): PostgreSQL provides infrastructure to create custom modules for continuous archiving.
 - [Logical Decoding Output Plugins](https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html): Output plugins transform the data from the write-ahead log's internal representation into the format the consumer of a replication slot desires.
 - [Pluggable JIT providers](https://www.postgresql.org/docs/current/jit-extensibility.html): PostgreSQL provides a JIT implementation based on LLVM. The interface to the JIT provider is pluggable and the provider can be changed without recompiling (although currently, the build process only provides inlining support data for LLVM).
 - [Base Backups Sinks](https://www.postgresql.org/docs/16/basebackup-to-shell.html): Taking a base backup produces one archive per tablespace directory, plus a backup manifest unless that feature has been disabled. The
 backup process puts those archives and manifest someplace, possibly after postprocessing them in some way. Base backup sinks are objects to which those archives, and the manifest if present, can be sent. Base backups sinks can be chained.
 - Hooking Modules: These are modules that implement functions which they register with the database engine, so that they're called at very specific points. For example, after the raw parse tree has been transformed into a query tree. Or when the postmaster process has finished initializing shared memory, so that these custom modules can set up their own shared memory allocations. Or at the different phases the query executor takes a query through (Start, Run, Finish, End).

## Related content

- [Allow extensions](how-to-allow-extensions.md).
- [Special considerations with extensions](concepts-extensions-considerations.md).
- [List of extensions by name](concepts-extensions-versions.md).
