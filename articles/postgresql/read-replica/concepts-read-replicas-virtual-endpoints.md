---
title: Virtual Endpoints in Azure Database for PostgreSQL Flexible Server
description: This article describes the virtual endpoints for read replica feature in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand what virtual endpoints are in Azure Database for PostgreSQL flexible server, so that I can keep my application connection strings consistent after a role change.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: concept-article
---

# Virtual endpoints in Azure Database for PostgreSQL flexible server

Virtual endpoints are read-write and read-only listener endpoints that stay consistent regardless of the current role of the Azure Database for PostgreSQL flexible server. This consistency means you don't need to update your application's connection string after you perform the **promote to primary server** action. The endpoints automatically point to the correct server following a role change.

You perform all operations involving virtual endpoints, whether adding, editing, or removing, in the context of the primary server. In the Azure portal, you manage these endpoints under the primary server page. Similarly, when using tools like the CLI, REST API, or other utilities, commands and actions target the primary server for endpoint management.

Virtual endpoints offer two distinct types of connection points:

**Writer endpoint (read/write)**: This endpoint always points to the current primary server. It ensures that write operations are directed to the correct server, irrespective of any promote operations users trigger. This endpoint can't be changed to point to a [replica](concepts-read-replicas.md).


**Read-only endpoint**: You can configure this endpoint to point either to a read replica or the primary server. However, it can only target one server at a time. It doesn't support load balancing between multiple servers. You can adjust the target server for this endpoint anytime, whether before or after promotion.

> [!NOTE]  
> You can create only one writer and one read-only endpoint per primary server and one of its replicas.

### Virtual endpoints and promote behavior

When you trigger a promote action, these endpoints behave in predictable ways.
The following sections explain how these endpoints react to both [Promote to primary server](concepts-read-replicas-promote.md) and **Promote to independent server** scenarios.

| **Virtual endpoint** | **Original target** | **Behavior when "Promote to primary server" is triggered** | **Behavior when "Promote to independent server" is triggered** |
| --- | --- | --- | --- |
| <b> Writer endpoint | Primary | Points to the new primary server. | Remains unchanged. |
| <b> Read-Only endpoint | Replica | Points to the new replica (former primary). | Points to the primary server. |
| <b> Read-Only endpoint | Primary | Not supported. | Remains unchanged. |
#### Behavior when "Promote to primary server" is triggered

- **Writer endpoint**: This endpoint updates to point to the new primary server, reflecting the role switch.
- **Read-only endpoint**
  * **If read-only endpoint points to replica**: After the promote action, the read-only endpoint points to the new replica (the former primary).
  * **If read-only endpoint points to primary**: For the promotion to function correctly, the read-only endpoint must point to the server intended for promotion. Pointing to the primary server isn't supported. You must reconfigure the endpoint to point to the replica before promotion.

#### Behavior when "Promote to the independent server and remove from replication" is triggered

- **Writer endpoint**: This endpoint remains unchanged. It continues to direct traffic to the server, holding the primary role.
- **Read-only endpoint**
  * **If read-only endpoint points to replica**: The read-only endpoint redirects from the promoted replica to point to the primary server.
  * **If read-only endpoint points to primary**: The read-only endpoint remains unchanged, continuing to point to the same server.

### Use virtual endpoints for consistent hostname during point-in-time recovery (PITR) or snapshot restore

This section explains how to use virtual endpoints in an Azure Database for PostgreSQL flexible server to maintain a consistent hostname during point-in-time recovery (PITR) or snapshot restore, ensuring application connection strings remain unchanged. Follow these steps:

1. **Add virtual endpoint to primary server:**
    - Browse to your primary server in the Azure portal.
    - Go to the **Replication** tab. Under **Virtual endpoints**, select **Add virtual endpoint**.
    - Configure the virtual endpoint with a consistent hostname, such as `mydb-virtual-endpoint.postgres.database.azure.com`.
    - Save the configuration.
    - Update your application to use this virtual endpoint in the connection string.

1. **Perform point-in-time restore (PITR) or snapshot restore:**
    - Initiate recovery:
        - Go to the **Backups** section of your primary server.
        - Choose the appropriate restore option (`PITR` or `snapshot`) and specify the desired point in time.
    - Update virtual endpoint:
        - After the new server is created, go back to the old primary server **Replication** tab.
        - Remove the virtual endpoint from the original primary server. The original primary server must be in the `succeeded` state to remove the virtual endpoint.
        - Add the same virtual endpoint to the newly created server.

1. **Validation:**
    - Ensure that your application connects by using the virtual endpoint and verify the database operations after recovery.

## Related content

- [Create virtual endpoints for read replicas with Terraform](../read-replica/how-to-create-read-replica.md)
- [Read replicas in Azure Database for PostgreSQL](concepts-read-replicas.md).
- [Geo-replication in Azure Database for PostgreSQL](concepts-read-replicas-geo.md).
- [Promote read replicas in Azure Database for PostgreSQL](concepts-read-replicas-promote.md).
- [Create a read replica](how-to-create-read-replica.md).
- [Replication across Azure regions and virtual networks with private networking](../network/concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking).
