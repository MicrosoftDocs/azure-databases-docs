---
title: Managed identity in Azure Database for PostgreSQL - Flexible Server
description: Learn about Managed identity in Azure Database for PostgreSQL - Flexible Server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 12/18/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - mvc
  - mode-other
ms.devlang: python
---

# Managed identity in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

A common challenge for developers is the management of secrets, credentials, certificates, and keys used to secure communication between services. Managed identities eliminate the need for developers to manage these credentials.

While developers can securely store the secrets in Azure Key Vault, services need a way to access Azure Key Vault. Managed identities provide an automatically managed identity in Microsoft Entra ID for applications to use when connecting to resources that support Microsoft Entra authentication. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials.

Here are some of the benefits of using managed identities:

- You don't need to manage credentials. Credentials aren't even accessible to you.
- You can use managed identities to authenticate to any resource that supports Microsoft Entra authentication including your own applications.
- Managed identities can be used at no extra cost.

## Types of managed identities available in Azure

There are two types of managed identities:

- **System-assigned**: Some Azure resource types, such as Azure Database for PostgreSQL - Flexible Server, allow you to enable a managed identity directly on the resource. They're referred to as system-assigned managed identities. When you enable a system-assigned managed identity: 
    - A service principal of a special type is created in Microsoft Entra ID for the identity. The service principal is tied to the lifecycle of that Azure resource. When the Azure resource is deleted, Azure automatically deletes the service principal for you.
    - By design, only that Azure resource can use this identity to request tokens from Microsoft Entra ID.
    - You can authorize the service principal associated to the managed identity to have access to one or more services.
    - The name assigned to the service principal associated to the managed identity is always the same as the name of the Azure resource for which it's created.    

- **User-assigned**: Some Azure resource types also support the assignment of managed identities created by the user as independent resources. The lifecycle of these identities is independent from the lifecycle of the resources to which they are assigned. They can be assigned to multiple resources. When you enable a user-assigned managed identity:
    - A service principal of a special type is created in Microsoft Entra ID for the identity. The service principal is managed separately from the resources that use it. 
    - Multiple resources can utilize user-assigned identities.
    - You authorize the managed identity to have access to one or more services.

> [!NOTE]
> Azure Database for PostgreSQL - Flexible Server doesn't support the use of user-assigned managed identities.

## Enable the system-assigned managed identity on your instance

## [Portal](#tab/portal-enable)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/concepts-identity/server-search.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/concepts-identity/server-search.png":::

2. In the resource menu, under **Security**, select **Identity**. Then, in the **System assigned managed identity** section, select the **On** option. Select **Save**.

    :::image type="content" source="./media/concepts-identity/identity.png" alt-text="Screenshot that shows how to enable the system-assigned managed identity on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/concepts-identity/identity.png":::

3. When the process completes, a notification informs you that the system assigned managed identity is enabled.

    :::image type="content" source="./media/concepts-identity/notification.png" alt-text="Screenshot that shows the notification informing that the system-assigned managed identity is enabled." lightbox="./media/concepts-identity/notification.png":::

## [ARM template](#tab/arm-enable)

Here is the ARM template to enable system assigned managed identity. You can use the 2023-06-01-preview or the latest available API.

```json
{
    "resources": [
        {
            "apiVersion": "2023-06-01-preview",
            "identity": {
                "type": "SystemAssigned"
            },
            "location": "Region name",
            "name": "flexible server name",
            "type": "Microsoft.DBforPostgreSQL/flexibleServers"
        }
    ]
}
  ```

To disable system assigned managed identity change the type to **None**
 
```json
{
    "resources": [
        {
            "apiVersion": "2023-06-01-preview",
            "identity": {
                "type": "None"
            },
            "location": "Region Name",
            "name": "flexible server name",
            "type": "Microsoft.DBforPostgreSQL/flexibleServers"
        }
    ]
}
 ```

---

## Verify the system assigned managed identity

You can verify the managed identity created by going to **Enterprise Applications** 

1. Choose  **Application Type == Managed Identity**

2. Provide your flexible server name in **Search by application name or Identity** as shown in the screenshot.

![Screenshot verifying system assigned managed identity.](media/concepts-Identity/verify-managed-identity.png)


[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Firewall rules in Azure Database for PostgreSQL - Flexible Server](concepts-firewall-rules.md).
- [Public access and private endpoints in Azure Database for PostgreSQL - Flexible Server](concepts-networking-public.md).
- [Virtual network integration in Azure Database for PostgreSQL - Flexible Server](concepts-networking-private.md).
