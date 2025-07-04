---
title: Handle transient connectivity errors
description: Learn how to handle transient connectivity errors for Azure Database for PostgreSQL flexible server.
author: olmoloce
ms.author: olmoloce
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Handling transient connectivity errors in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes how to handle transient errors connecting to Azure Database for PostgreSQL flexible server.

## Transient errors

A transient error, also known as a transient fault, is an error that resolves itself. Most typically these errors manifest as a connection to the database server being dropped. Also new connections to a server can't be opened. Transient errors can occur, for example,  when hardware or network failure happens. Another reason could be a new version of a PaaS service that is being rolled out. The system automatically mitigates most of these events in less than 60 seconds. A best practice for designing and developing applications in the cloud is to expect transient errors. Assume they can happen in any component at any time and to have the appropriate logic in place to handle these situations.

## Handling transient errors

Transient errors should be handled using retry logic. Situations that must be considered:

* An error occurs when you try to open a connection
* An idle connection is dropped on the server side. When you try to issue a command, it can't be executed
* An active connection that currently is executing a command is dropped.

The first and second cases are fairly straight forward to handle. Try to open the connection again. Once the system mitigates the transient error, you succeed to connect. You can use your Azure Database for PostgreSQL flexible server instance again. We recommend having waits before retrying the connection. Back off if the initial retries fail. This way the system can use all resources available to overcome the error situation. A good pattern to follow is:

* Wait for 5 seconds before your first retry.
* For each following retry, increase the wait exponentially, up to 60 seconds.
* Set a max number of retries at which point your application considers the operation failed.

When a connection with an active transaction fails, it's more difficult to handle the recovery correctly. There are two cases: If the transaction was read-only in nature, it's safe to reopen the connection and to retry the transaction. If however if the transaction was also writing to the database, you must determine if the transaction was rolled back, or if it succeeded before the transient error happened. In that case, you might not have received the commit acknowledgment from the database server.

One way of doing this, is to generate a unique ID on the client that is used for all the retries. You pass this unique ID as part of the transaction to the server and to store it in a column with a unique constraint. This way you can safely retry the transaction. It succeeds if the previous transaction was rolled back and the client generated unique ID doesn't yet exist in the system. It fails indicating a duplicate key violation if the unique ID was previously stored because the previous transaction completed successfully.

When your program communicates with Azure Database for PostgreSQL flexible server through third-party middleware, ask the vendor whether the middleware contains retry logic for transient errors.

Make sure to test your retry logic. For example, try to execute your code while scaling up or down the compute resources of your Azure Database for PostgreSQL flexible server instance. Your application should handle the brief downtime that is encountered during this operation without any problems.
