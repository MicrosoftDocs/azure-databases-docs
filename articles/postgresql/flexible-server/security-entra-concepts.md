---
title: Microsoft Entra Authentication
description: Learn about the concepts of Microsoft Entra ID for authentication with Azure Database for PostgreSQL.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Microsoft Entra authentication in Azure Database for PostgreSQL

Microsoft Entra authentication is a mechanism of connecting to Azure Database for PostgreSQL by using identities defined in Microsoft Entra ID. With Microsoft Entra authentication, you can manage database user identities and other Microsoft services in a central location, which simplifies permission management.

Benefits of using Microsoft Entra ID include:

- Authentication of users across Azure services in a uniform way.
- Management of password policies and password rotation in a single place.
- Support for multiple forms of authentication, which can eliminate the need to store passwords.
- The ability of customers to manage database permissions by using external (Microsoft Entra ID) groups.
- The use of PostgreSQL database roles to authenticate identities at the database level.
- Support of token-based authentication for applications that connect to Azure Database for PostgreSQL.

<a id="how-azure-ad-works-in-flexible-server"></a>

## How Microsoft Entra ID works in Azure Database for PostgreSQL

The following high-level diagram summarizes how authentication works when you use Microsoft Entra authentication with Azure Database for PostgreSQL. The arrows indicate communication pathways.

:::image type="content" source="media/security-entra-concepts/authentication-flow.png" alt-text="Screenshot of authentication concepts.":::

1. Your application can request a token from the Azure Instance Metadata Service identity endpoint.
1. When you use the client ID and certificate, a call is made to Microsoft Entra ID to request an access token.
1. A JSON Web Token (JWT) access token is returned by Microsoft Entra ID. Your application sends the access token on a call to your server.
1. The server validates the token with Microsoft Entra ID.

For the steps to configure Microsoft Entra ID with Azure Database for PostgreSQL, see [Configure and sign in with Microsoft Entra ID for Azure Database for PostgreSQL](how-to-configure-sign-in-azure-ad-authentication.md).

## Differences between a PostgreSQL administrator and a Microsoft Entra administrator

When you turn on Microsoft Entra authentication for your Microsoft Entra principal as a Microsoft Entra administrator, the account:

- Gets the same privileges as the original PostgreSQL administrator.
- Can manage other Microsoft Entra roles on the server.

The PostgreSQL administrator can create only local password-based users. But the Microsoft Entra administrator has the authority to manage both Microsoft Entra users and local password-based users.

The Microsoft Entra administrator can be a Microsoft Entra user, Microsoft Entra group, service principal, or managed identity. Using a group account as an administrator enhances manageability. It permits the centralized addition and removal of group members in Microsoft Entra ID without changing the users or permissions within the Azure Database for PostgreSQL instance.

You can configure multiple Microsoft Entra administrators concurrently. You can deactivate password authentication to an Azure Database for PostgreSQL instance for enhanced auditing and compliance requirements.

:::image type="content" source="media/security-entra-concepts/admin-structure.png" alt-text="Screenshot of admin structure for Entra ID.":::

Microsoft Entra administrators that you create via the Azure portal, an API, or SQL have the same permissions as the regular admin user that you created during server provisioning. You manage database permissions for nonadmin Microsoft Entra roles similarly to regular roles.

<a id="connect-using-azure-ad-identities"></a>

## Connection with Microsoft Entra identities

Microsoft Entra authentication supports the following methods for connecting to a database by using Microsoft Entra identities:

- Microsoft Entra password authentication
- Microsoft Entra integrated authentication
- Microsoft Entra universal with multifactor authentication
- Active Directory application certificates or client secrets
- [Managed identity](how-to-connect-with-managed-identity.md)

After you authenticate against Active Directory, you retrieve a token. This token acts as your password for signing in.

To configure Microsoft Entra ID with Azure Database for PostgreSQL, follow the steps in [Configure and sign in with Microsoft Entra ID for Azure Database for PostgreSQL](how-to-configure-sign-in-azure-ad-authentication.md).

## Other considerations

When you use Microsoft Entra authentication with Azure Database for PostgreSQL, keep the following points in mind:

- To have Microsoft Entra principals assume ownership of the user databases within any deployment procedure, add explicit dependencies within your deployment (Terraform or Azure Resource Manager) module to ensure that Microsoft Entra authentication is turned on before you create any user databases.
- You can configure multiple Microsoft Entra principals (user, group, service principal, or managed identity) as Microsoft Entra administrators for an Azure Database for PostgreSQL instance at any time.
- Only a Microsoft Entra administrator for PostgreSQL can initially connect to the Azure Database for PostgreSQL instance by using a Microsoft Entra account. The Active Directory administrator can configure subsequent Microsoft Entra database users.
- If you delete a Microsoft Entra principal from Microsoft Entra ID, it remains as a PostgreSQL role but can no longer acquire a new access token. In this case, although the matching role still exists in the database, it can't authenticate to the server. Database administrators need to transfer ownership and drop roles manually.

> [!NOTE]  
> The deleted Microsoft Entra user can still sign in until the token expires (up to 60 minutes from token issuing). If you also remove the user from Azure Database for PostgreSQL, this access is revoked immediately.

- Azure Database for PostgreSQL matches access tokens to the database role by using the user's unique Microsoft Entra user ID, as opposed to using the username. If you delete a Microsoft Entra user and create a new user with the same name, Azure Database for PostgreSQL considers that a different user. Therefore, if you delete a user from Microsoft Entra ID and add a new user with the same name, the new user can't connect with the existing role.

## Frequently asked questions

- **What authentication modes are available in Azure Database for PostgreSQL?**

    Azure Database for PostgreSQL supports three authentication modes: PostgreSQL authentication only, Microsoft Entra authentication only, and both PostgreSQL and Microsoft Entra authentication.
    
- **Can I configure multiple Microsoft Entra administrators on my server?**

    Yes. You can configure multiple Microsoft Entra administrators on your server. During provisioning, you can set only a single Microsoft Entra administrator. After the server is created, you can set as many Microsoft Entra administrators as you want by going to the **Authentication** pane.        

- **Is a Microsoft Entra administrator just a Microsoft Entra user?**

    No. A Microsoft Entra administrator can be a user, group, service principal, or managed identity.
    
- **Can a Microsoft Entra administrator create local password-based users?**

    Yes. A Microsoft Entra administrator can manage both Microsoft Entra users and local password-based users.
    
- **What happens when I enable Microsoft Entra authentication on my server?**

    When you set Microsoft Entra authentication at the server level, the PGAadAuth extension is enabled and the server restarts.
    
- **How do I sign in by using Microsoft Entra authentication?**

    You can use client tools like psql or pgAdmin to sign in to your server. Use your Microsoft Entra user ID as the username and your Microsoft Entra token as your password.
    
- **How do I generate my token?**

    Use `az login` to generate the token. For more information, see [Retrieve the Microsoft Entra access token](how-to-configure-sign-in-azure-ad-authentication.md).
    
- **What's the difference between group authentication and individual authentication?**

    The only difference between signing in as a Microsoft Entra group member and signing in as an individual Microsoft Entra user lies in the username. Signing in as an individual user requires an individual Microsoft Entra user ID. Signing in as a group member requires the group name. In both scenarios, you use the same individual Microsoft Entra token as the password.
    
- **What's the token lifetime?**

    User tokens are valid for up to 1 hour. Tokens for system-assigned managed identities are valid for up to 24 hours.
    
## Related content

- [Use Microsoft Entra ID in Azure Database for PostgreSQL](how-to-configure-sign-in-azure-ad-authentication.md)
- [Manage Microsoft Entra roles in Azure Database for PostgreSQL](how-to-manage-azure-ad-users.md)
