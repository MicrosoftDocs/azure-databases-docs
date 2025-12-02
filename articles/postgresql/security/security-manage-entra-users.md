---
title: Manage Microsoft Entra Users
description: This article describes how you can manage Microsoft Entra ID enabled roles to interact with an Azure Database for PostgreSQL flexible server instance.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 10/06/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - devx-track-arm-template
  - sfi-image-nochange
---

# Manage Microsoft Entra roles in Azure Database for PostgreSQL

This article describes how to create Microsoft Entra ID-enabled database roles within an Azure Database for PostgreSQL flexible server instance.

To learn about how to create and manage Azure subscription users and their privileges, see the [Azure role-based access control (Azure RBAC) article](/azure/role-based-access-control/built-in-roles) or review [how to customize roles](/azure/role-based-access-control/custom-roles).

> [!NOTE]  
> This guide assumes you already enabled Microsoft Entra authentication on your Azure Database for PostgreSQL flexible server instance.

## Create or delete Microsoft Entra administrators using Azure portal or Azure Resource Manager (ARM) API

1. Open the **Authentication** page for your Azure Database for PostgreSQL flexible server instance in the Azure portal.
1. To add an administrator, select **Add Microsoft Entra Admin** and select a user, group, application, or a managed identity from the current Microsoft Entra tenant.
1. To remove an administrator, select the **Delete** icon for the administrator you want to remove.
1. Select **Save** and wait for the provisioning operation to complete.

> [!NOTE]  
> Support for Microsoft Entra Administrators management via Azure SDK, az cli, and Azure PowerShell is coming soon.

## Manage Microsoft Entra roles using SQL

After you create the first Microsoft Entra administrator from the Azure portal or API, you can use the administrator role to manage Microsoft Entra roles in your Azure Database for PostgreSQL flexible server instance.

For the best experience with Microsoft Entra integration in Azure Database for PostgreSQL, we recommend getting familiar with [Microsoft identity platform](/azure/active-directory/develop/v2-overview).

### Principal types

Azure Database for PostgreSQL internally stores the mapping between PostgreSQL database roles and unique identifiers of Microsoft Entra objects.
Each PostgreSQL database role can be mapped to one of the following Microsoft Entra object types:

- **User** - Including tenant local and guest users.
- **Service Principal** - Including [Applications and Managed identities](/azure/active-directory/develop/app-objects-and-service-principals)
- **Group** - When a PostgreSQL role is linked to a Microsoft Entra group, any user or service principal member of this group can connect to the Azure Database for PostgreSQL flexible server instance with the group role.

### List Microsoft Entra roles using SQL

```sql
select * from pg_catalog.pgaadauth_list_principals(isAdminValue boolean)
```

#### Arguments

##### `isAdminValue`

`boolean` - When `true`, returns admin users. When `false`, returns all Microsoft Entra users, including Microsoft Entra admins and nonadmins.

#### Return type

`TABLE(rolename name, principalType text, objectId text, tenantId text, isMfa integer, isAdmin integer)` - A table with the following schema:
- `rolename` - The name of the role in PostgreSQL.
- `principalType` - The type of principal in Microsoft Entra ID. It can be `user`, `group`, or `service`.
- `objectId` - The identifier of the object in Microsoft Entra ID for this principal.
- `tenantId` - The identifier of the tenant hosting this principal in Microsoft Entra ID.
- `isMfa` - Returns a value of `1` if the user/role has MFA enforced.
- `isAdmin` - Returns a value of `1` if the user/role is an administrator in PostgreSQL.

## Create a user or role with a Microsoft Entra principal name

```sql
select * from pg_catalog.pgaadauth_create_principal(roleName text, isAdmin boolean, isMfa boolean)
```

#### Arguments

##### `roleName`

`text` name of the role to create. This name **must match the name of the Microsoft Entra principal**.
- For **users**, use the User Principal Name from the profile. For guest users, include the full name in their home domain with the #EXT# tag.
- For **groups** and **service principals**, use the display name. The name must be unique in the tenant.

##### `isAdmin`

`boolean` when `true`, creates a PostgreSQL admin user (member of the `azure_pg_admin` role and with CREATEROLE and CREATEDB permissions). When `false`, creates a regular PostgreSQL user.

##### `isMfa`

`boolean` when `true`, enforces multifactor authentication for this PostgreSQL user.

> [!IMPORTANT]  
> The `isMfa` flag tests the `mfa` claim in the Microsoft Entra ID token, but it doesn't impact the token acquisition flow. For example, if the tenant of the principal isn't configured for multifactor authentication, it prevents the use of the feature. And if the tenant requires multifactor authentication for all tokens, it makes this flag useless.

#### Return type

`text` single value that consists of a string "Created role for ***roleName***", where ***roleName*** is the argument you pass for the **roleName** parameter.

## Drop a role with a Microsoft Entra principal name

You can drop a role that corresponds to a Microsoft Entra ID principal in three ways:

- The Azure portal
- The Azure Resource Manager (ARM) API
- By executing the following SQL statement:

   ```sql
   DROP ROLE rolename;
   ```

> [!NOTE]  
> The Azure portal displays only admin roles. To drop a nonadmin role, use either the Azure Resource Manager (ARM) API or the SQL statement.

## Create a role using the Microsoft Entra ID object identifier

```sql
select * from pg_catalog.pgaadauth_create_principal_with_oid(roleName text, objectId text, objectType text, isAdmin boolean, isMfa boolean)
```

#### Arguments

##### `roleName`

`text` name of the role to create.

##### `objectId`

`text` unique object identifier of the Microsoft Entra object.
- For **users**, **groups**, and **managed identities**, find the `objectId` by searching for the object name in [Microsoft Entra ID](https://ms.portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade) page in Azure portal. [See this guide as an example](/partner-center/find-ids-and-domain-names).
- For **groups** and **service principals**, use the display name. The name must be unique in the tenant.
- For **applications**, use the objectId of the corresponding **Service Principal**. In Azure portal, find the required objectId on [Enterprise Applications](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/EnterpriseApps) page.

##### `objectType`

`text` type of Microsoft Entra object to link to this role. It can be `user`, `group`, or `service`.

##### `isAdmin`

`boolean` when `true`, creates a PostgreSQL admin user (member of the `azure_pg_admin` role and with CREATEROLE and CREATEDB permissions). When `false`, creates a regular PostgreSQL user.

##### `isMfa`

`boolean` when `true`, enforces multifactor authentication for this PostgreSQL user.

> [!IMPORTANT]  
> The `isMfa` flag tests the `mfa` claim in the Microsoft Entra ID token, but it doesn't impact the token acquisition flow. For example, if the tenant of the principal isn't configured for multifactor authentication, it prevents the use of the feature. And if the tenant requires multifactor authentication for all tokens, it makes this flag useless.

#### Return type

`text` single value that consists of a string "Created role for ***roleName***", where ***roleName*** is the argument you pass for the **roleName** parameter.

## Enable Microsoft Entra authentication for an existing PostgreSQL role using SQL

Azure Database for PostgreSQL uses security labels associated with database roles to store their corresponding Microsoft Entra ID mapping.

Use the following SQL to assign the required security label and map it to a Microsoft Entra object:

```sql
SECURITY LABEL for "pgaadauth" on role "<roleName>" is 'aadauth,oid=<objectId>,type=<objectType>,admin';
```

#### Arguments

##### `roleName`

`text` name of an existing PostgreSQL role to enable Microsoft Entra authentication.

##### `objectId`

`text` unique object identifier of the Microsoft Entra object.

##### `objectType`

`text` set to `user`, `group`, or `service` (for applications or managed identities connecting under their own service credentials).

##### `admin`

`text` set to present or absent. If present in the security label, users or roles can manage other Microsoft Entra ID roles.

## Related content

- [Microsoft Entra authentication in Azure Database for PostgreSQL](../security/security-entra-concepts.md)
