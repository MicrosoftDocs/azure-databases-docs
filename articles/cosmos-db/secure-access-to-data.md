---
title: Learn how to secure access to data in Azure Cosmos DB
description: Learn about access control concepts in Azure Cosmos DB, including primary keys, read-only keys, users, and permissions.
author: iriaosara
ms.author: iriaosara
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 09/26/2024
ms.custom: devx-track-csharp, subject-rbac-steps
---

# Secure access to data in Azure Cosmos DB

[!INCLUDE[NoSQL](includes/appliesto-nosql.md)]

This article provides an overview of data access control in Azure Cosmos DB.

Azure Cosmos DB provides three ways to control access to your data.

| Access control type | Characteristics |
|---|---|
| [Primary/secondary keys](#primarysecondary-keys) | Shared secret allowing any management or data operation. It comes in both read-write and read-only variants. |
| [Role-based access control (RBAC)](#role-based-access-control) | Fine-grained, role-based permission model using Microsoft Entra identities for authentication. |

## Primary/secondary keys

Primary/secondary keys provide access to all the administrative resources for the database account. Each account consists of two keys: a primary key and secondary key. The purpose of dual keys is to let you regenerate, or roll, keys, providing continuous access to your account and data. To learn more about primary/secondary keys, see [Overview of database security in Azure Cosmos DB](database-security.md#primary-keys).

To see your account keys, on the left menu select **Keys**. Then, select the **View** icon at the right of each key. Select the **Copy** button to copy the selected key. You can hide them afterwards by selecting the same icon per key, which updates the icon to a **Hide** button.

:::image type="content" source="./media/database-security/view-account-key.png" alt-text="Screenshot of the View account key for Azure Cosmos DB.":::

### Key rotation and regeneration

> [!NOTE]
> The following section describes the steps to rotate and regenerate keys for the API for NoSQL. If you're using a different API, see the [API for MongoDB](database-security.md?tabs=mongo-api), [API for Cassandra](database-security.md?tabs=cassandra-api), [API for Gremlin](database-security.md?tabs=gremlin-api), or [API for Table](database-security.md?tabs=table-api) sections.
>
> To monitor your account for key updates and key regeneration, see [Monitor your Azure Cosmos DB account for key updates and key regeneration](monitor-account-key-updates.md).

The process of key rotation and regeneration is simple. First, make sure that *your application is consistently using either the primary key or the secondary key* to access your Azure Cosmos DB account. Then, follow the steps in the next section.

# [If your application is currently using the primary key](#tab/using-primary-key)

1. Go to your Azure Cosmos DB account in the Azure portal.

1. Select **Keys** on the left menu and then select **Regenerate Secondary Key** from the ellipsis on the right of your secondary key.

    :::image type="content" source="./media/database-security/regenerate-secondary-key.png" alt-text="Screenshot that shows the Azure portal showing how to regenerate the secondary key." border="true":::

1. Validate that the new secondary key works consistently against your Azure Cosmos DB account. Key regeneration can take anywhere from one minute to multiple hours depending on the size of the Azure Cosmos DB account.

1. Replace your primary key with the secondary key in your application.

1. Go back to the Azure portal and trigger the regeneration of the primary key.

    :::image type="content" source="./media/database-security/regenerate-primary-key.png" alt-text="Screenshot that shows the Azure portal showing how to regenerate the primary key." border="true":::

# [If your application is currently using the secondary key](#tab/using-secondary-key)

1. Go to your Azure Cosmos DB account in the Azure portal.

1. Select **Keys** on the left menu and then select **Regenerate Primary Key** from the ellipsis on the right of your primary key.

    :::image type="content" source="./media/database-security/regenerate-primary-key.png" alt-text="Screenshot that shows the Azure portal showing how to regenerate the primary key." border="true":::

1. Validate that the new primary key works consistently against your Azure Cosmos DB account. Key regeneration can take anywhere from one minute to multiple hours depending on the size of the Azure Cosmos DB account.

1. Replace your secondary key with the primary key in your application.

1. Go back to the Azure portal and trigger the regeneration of the secondary key.

    :::image type="content" source="./media/database-security/regenerate-secondary-key.png" alt-text="Screenshot that shows the Azure portal showing how to regenerate the secondary key." border="true":::

---

### Code sample to use a primary key

The following code sample illustrates how to use an Azure Cosmos DB account endpoint and primary key to instantiate a `CosmosClient`:

```csharp
// Read the Azure Cosmos DB endpointUrl and authorization keys from config.
// These values are available from the Azure portal on the Azure Cosmos DB account blade under "Keys".
// Keep these values in a safe and secure location. Together they provide Administrative access to your Azure Cosmos DB account.

private static readonly string endpointUrl = ConfigurationManager.AppSettings["EndPointUrl"];
private static readonly string authorizationKey = ConfigurationManager.AppSettings["AuthorizationKey"];

CosmosClient client = new CosmosClient(endpointUrl, authorizationKey);
```

## Role-based access control

Azure Cosmos DB exposes a built-in RBAC system that lets you:

- Authenticate your data requests with a Microsoft Entra identity.
- Authorize your data requests with a fine-grained, role-based permission model.

Azure Cosmos DB RBAC is the ideal access control method in situations where:

- You don't want to use a shared secret like the primary key and prefer to rely on a token-based authentication mechanism.
- You want to use Microsoft Entra identities to authenticate your requests.
- You need a fine-grained permission model to tightly restrict which database operations your identities are allowed to perform.
- You want to materialize your access control policies as "roles" that you can assign to multiple identities.

To learn more about Azure Cosmos DB RBAC, see [Configure role-based access control for your Azure Cosmos DB account](nosql/security/index.md).

For information and sample code to configure RBAC for the Azure Cosmos DB for MongoDB, see [Configure role-based access control for your Azure Cosmos DB for MongoDB](mongodb/security/index.md).

## Add users and assign roles

To add Azure Cosmos DB account reader access to your user account, have a subscription owner perform the following steps in the Azure portal.

1. Open the Azure portal and select your Azure Cosmos DB account.

1. Select **Access control (IAM)**.

1. Select **Add** > **Add role assignment** to open the **Add role assignment** page.

1. Assign the following role. For detailed steps, see [Assign Azure roles by using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

    | Setting | Value |
    | --- | --- |
    | Role | Cosmos DB Account Reader. |
    | Assign access to | User, group, or service principal. |
    | Members | The user, group, or application in your directory to which you want to grant access. |

    ![Screenshot that shows the Add role assignment page in the Azure portal.](~/reusable-content/ce-skilling/azure/media/role-based-access-control/add-role-assignment-page.png)

The entity can now read Azure Cosmos DB resources.

## Delete or export user data

As a database service, Azure Cosmos DB enables you to search, select, modify, and delete any data located in your database or containers. It's your responsibility to use the provided APIs and define logic required to find and erase any personal data if needed.

Each multi-model API (SQL, MongoDB, Gremlin, Cassandra, or Table) provides different language SDKs that contain methods to search and delete data based on custom predicates. You can also enable the [time to live (TTL)](time-to-live.md) feature to delete data automatically after a specified period, without incurring any more cost.

[!INCLUDE [GDPR-related guidance](~/reusable-content/ce-skilling/azure/includes/gdpr-dsr-and-stp-note.md)]

## Related content

- [Azure Cosmos DB database security](database-security.md)
- [Access control on Azure Cosmos DB resources](/rest/api/cosmos-db/access-control-on-cosmosdb-resources)
- [.NET SDK user management samples](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/UserManagement/UserManagementProgram.cs)
