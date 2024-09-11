---
title: Security terminology glossary
titleSuffix: Azure Cosmos DB for Table
description: Explore common glossary terminology used when describing how to managed role-based access control within Azure Cosmos DB for Table.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: glossary
ms.date: 09/11/2024
ai-usage: ai-assisted
---

# Security glossary for Azure Cosmos DB for Table

[!INCLUDE[Table](../../includes/appliesto-table.md)]

:::image type="complex" source="media/glossary/map.svg" border="false" alt-text="Diagram of the current location ('Concepts') in the sequence of the deployment guide.":::
Diagram of the sequence of the deployment guide including these locations, in order: Overview, Concepts, Prepare, Role-based access control, and Solution. The 'Concepts' location is currently highlighted.
:::image-end:::

This article includes a glossary of common terminology used in this security guide.

## Role-based access control

Role-based access control refers to a method to manage access to resources in Azure. This method is based on specific [identities](#identityprincipal) being assigned [roles](#role) that manage what level of access they have to one or more resources. Role-based access control provides a flexible system of fine-grained access management that ensures identities only have the [least privileged](#least-privilege) level of access they need to perform their task.

For more information, see [TODO](about:blank).

## Identity/Principal

Identities refer to objects within Microsoft Entra that represents some entity that may need a level of access to your system. In the context of Azure and Microsoft Entra, identities could refer to one of the following types of entities:

| | Description |
| --- | --- |
| **Workload identities** | |
| **Human identities** | |
| **Managed identities** | |
| **Service principals** | |
| **Device identities** | |

For more information, see [TODO](about:blank).

## Role

TODO

For more information, see [TODO](about:blank).

## Definition

TODO

For more information, see [TODO](about:blank).

## Assignment

TODO

For more information, see [TODO](about:blank).

## Scope

TODO

For more information, see [TODO](about:blank).

## Least privilege

The concept of "least privilege" refers to an operational best practice to ensure that all users only have the minimal level of access they need to perform their task or job. For example, an application that reads data from a database would only need read access to the data store. If that application had read and write access to the data store, a few things could happen including, but not limited to:

- The application could errantly destroy data
- An unauthorized user could get access to the application's credentials and modify data

Following the practice of least privilege ensures that any potential data breaches are limited in scope. This practice maximises operational security while allowing users to remain effective.

For more information, see [TODO](about:blank).

## Control plane

TODO

For more information, see [TODO](about:blank).

## Data plane

TODO

For more information, see [TODO](about:blank).

## Actions

TODO

For more information, see [TODO](about:blank).

## Portable authentication

TODO

For more information, see [TODO](about:blank).

## Unique identifier

TODO

For more information, see [TODO](about:blank).

## Next step

> [!div class="nextstepaction"]
> [Get signed in account's identity](how-to-get-signed-in-identity.md)
