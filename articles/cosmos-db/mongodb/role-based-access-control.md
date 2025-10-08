---
title: Role-Based Access Control
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn the fundamentals of role-based access control in Azure Cosmos DB for MongoDB to secure data access.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: concept-article
ms.date: 08/20/2025
appliesto:
  - ✅ MongoDB
---

# Role-based access control in Azure Cosmos DB for MongoDB

Azure Cosmos DB for MongoDB exposes a built-in role-based access control system that lets you authorize your data requests with a fine-grained, role-based permission model. Users and roles reside within a database and are managed using the Azure CLI, Azure PowerShell, or Azure Resource Manager (ARM).

## Core concepts

There's a set of core concepts you need to understand before working with role-based access control in Azure Cosmos DB for MongoDB.

### Resource

A resource is a collection or database to which we're applying access control rules.

### Privileges

Privileges are actions that can be performed on a specific resource. For example, "read access to collection xyz." Privileges are assigned to a specific role.

### Role

A role has one or more privileges. Roles are assigned to users (zero or more) to enable them to perform the actions defined in those privileges. Roles are stored within a single database.

### Diagnostic log auditing

Another column named `userId` appears in the `MongoRequests` table in the Azure portal's diagnostics feature. This column shows which user performed each data plan operation. The value in this column remains empty when role-based access control isn't enabled.

## Privileges

This list includes all of the privileges available for roles in Azure Cosmos DB for MongoDB.

- Query and Write
  - `find`
  - `insert`
  - `remove`
  - `update`
- Change Streams
  - `changeStream`
- Database Management
  - `createCollection`
  - `createIndex` 
  - `dropCollection`
  - `killCursors`
  - `killAnyCursor`
- Server Administration 
  - `dropDatabase`
  - `dropIndex`
  - `reIndex`
- Diagnostics
  - `collStats`
  - `dbStats`
  - `listDatabases`
  - `listCollections`
  - `listIndexes`

## Built-in Roles

These roles already exist on every database and don't need to be created.

| | `read` | `readWrite` | `dbAdmin` | `dbOwner` |
| --- | --- | --- | --- | --- |
| **`changeStream`** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **`collStats`** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **`listCollections`** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **`listIndexes`** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **`createCollection`** | ✖️ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **`createIndex`** | ✖️ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **`dropCollection`** | ✖️ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **`dbStats`** | ✖️ No | ✖️ No | ✅ Yes | ✅ Yes |
| **`dropDatabase`** | ✖️ No | ✖️ No | ✅ Yes | ✅ Yes |
| **`reIndex`** | ✖️ No | ✖️ No | ✅ Yes | ✅ Yes |
| **`find`** | ✅ Yes | ✅ Yes | ✖️ No | ✅ Yes |
| **`killCursors`** | ✅ Yes | ✅ Yes | ✖️ No | ✅ Yes |
| **`dropIndex`** | ✖️ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **`insert`** | ✖️ No | ✅ Yes | ✖️ No | ✅ Yes |
| **`remove`** | ✖️ No | ✅ Yes | ✖️ No | ✅ Yes |
| **`update`** | ✖️ No | ✅ Yes | ✖️ No | ✅ Yes |

## Related content

- [How to setup role-based access control](how-to-setup-rbac.md)
- [Frequently asked questions about role-based access control](faq.yml#role-based-access-control)
