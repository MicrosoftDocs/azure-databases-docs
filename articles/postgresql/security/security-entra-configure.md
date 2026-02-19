---
title: Use Microsoft Entra ID Authentication
description: Learn how to set up Microsoft Entra ID for authentication for your Azure Database for PostgreSQL flexible server instance.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 02/19/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
  - sfi-image-nochange
  - sfi-ropc-blocked
---

# How to use Microsoft Entra ID for authentication with Azure Database for PostgreSQL

In this article, you configure Microsoft Entra ID access for authentication with Azure Database for PostgreSQL. You also learn how to use a Microsoft Entra token with an Azure Database for PostgreSQL flexible server instance.

You can configure Microsoft Entra authentication for an Azure Database for PostgreSQL flexible server instance either during server provisioning or later. Only Microsoft Entra administrator users can create or enable users for Microsoft Entra ID-based authentication. Don't use the Microsoft Entra administrator for regular database operations because that role has elevated user permissions, such as `CREATEDB`.

You can have multiple Microsoft Entra admin users with Azure Database for PostgreSQL. Microsoft Entra admin users can be a user, a group, or service principal.

## Prerequisites

- You need an Azure account with an active subscription. [Create an account for free](/pricing/purchase-options/azure-account?cid=msft_learn).

### Configure network requirements

Microsoft Entra ID is a multitenant application. It needs outbound connectivity for operations like adding Microsoft Entra admin groups.

Networking requirements vary by topology:

- **Public access (allowed IP addresses)**: No extra outbound rules required.
- **Private access (virtual network integration)**:
  - Add an outbound NSG rule that allows traffic to the `AzureActiveDirectory` service tag only.
  - If you use a route table, add a route with destination `AzureActiveDirectory` and next hop `Internet`.
  - If you use a proxy, allow only HTTPS traffic to the `AzureActiveDirectory` service tag.
- **Custom DNS**:
  - Ensure these hostnames resolve publicly: `login.microsoftonline.com` (authentication) and `graph.microsoft.com` (Microsoft Graph API).
  - If resolution fails, admin assignment and token acquisition operations fail.

To set the Microsoft Entra admin during server provisioning, follow these steps:

1. In the Azure portal, during server provisioning, select either **PostgreSQL and Microsoft Entra authentication** or **Microsoft Entra authentication only** as the authentication method.
1. On the **Set admin** tab, select a valid Microsoft Entra user, group, service principal, or managed identity in the customer tenant to be the Microsoft Entra administrator.

You can optionally add a local PostgreSQL admin account if you prefer using the **PostgreSQL and Microsoft Entra authentication** method.

> [!NOTE]  
> You can add only one Microsoft Entra admin during server provisioning. You can add multiple Microsoft Entra admin users after the server is created.

To set the Microsoft Entra administrator after server creation, follow these steps:

1. In the Azure portal, select the instance of Azure Database for PostgreSQL flexible server that you want to enable for Microsoft Entra ID.
1. Under **Security**, select **Authentication**. Then choose either **PostgreSQL and Microsoft Entra authentication** or **Microsoft Entra authentication only** as the authentication method, based on your requirements.
1. Select **Add Microsoft Entra Admins**. Then select a valid Microsoft Entra user, group, service principal, or managed identity in the customer tenant to be a Microsoft Entra administrator.
1. Select **Save**.

> [!IMPORTANT]  
> When you set the administrator, you add a new user to your Azure Database for PostgreSQL flexible server instance with full administrator permissions.

## Connect to Azure Database for PostgreSQL by using Microsoft Entra ID

Microsoft Entra integration works with standard PostgreSQL tools like psql, which aren't Microsoft Entra aware and support only specifying the username and password when you're connecting to PostgreSQL.

Tested clients include:

- **PostgreSQL for Visual Studio Code extension**: Use the **AUTHENTICATION TYPE** to set the authentication method to **Entra Auth**.
- **psql command line**: Use the `PGPASSWORD` variable to pass the token.
- **Other libpq-based clients**: Examples include common application frameworks and object-relational mappers (ORMs).
- **PgAdmin**: Clear **Connect now** at server creation.

## Authenticate with Microsoft Entra ID

Use the following procedures to authenticate with Microsoft Entra ID as an Azure Database for PostgreSQL flexible server instance user.

You can follow along by using:

- Azure Cloud Shell
- Azure virtual machine
- Your local machine

### Sign in to Azure

Start by authenticating with Microsoft Entra ID by using the Azure CLI. This step isn't required in Azure Cloud Shell.

```azurecli-interactive
az login
```

The command opens a browser window to the Microsoft Entra authentication page. It requires you to provide your Microsoft Entra user ID and password.

### Retrieve a Microsoft Entra access token

Use the Azure CLI to get an access token for the Microsoft Entra authenticated user to access Azure Database for PostgreSQL. Here's an example of the public cloud:

```azurecli-interactive
az account get-access-token --resource https://ossrdbms-aad.database.windows.net
```

Specify the resource value as shown in the preceding example. For other clouds, you can look up the resource value by using the following command:

```azurecli-interactive
az cloud show
```

For Azure CLI version 2.0.71 and later, you can specify the command in the following convenient version for all clouds:

```azurecli-interactive
az account get-access-token --resource-type oss-rdbms
```

After authentication is successful, Microsoft Entra ID returns an access token:

```json
{
  "accessToken": "TOKEN",
  "expiresOn": "...",
  "subscription": "...",
  "tenant": "...",
  "tokenType": "Bearer"
}
```

The token is a Base64 string. It encodes all the information about the authenticated user and is targeted to the Azure Database for PostgreSQL service.

### Use a token as a password for signing in with client psql

When connecting, use the access token as the PostgreSQL user password.

When you use the psql command-line client, you need to pass the access token through the `PGPASSWORD` environment variable. The access token is longer than the password length that psql can accept directly.

Here's a Windows example:

```cmd
set PGPASSWORD=<copy/pasted TOKEN value from step 2>
```

```powershell
$env:PGPASSWORD='<copy/pasted TOKEN value from step 2>'
```

Here's a Linux or macOS example:

```bash
export PGPASSWORD=<copy/pasted TOKEN value from step 2>
```

You can also combine steps 2 and 3 together by using command substitution. You can put the token retrieval into a variable and pass it directly as the value for the `PGPASSWORD` environment variable:

```bash
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query "[accessToken]" -o tsv)
```

Now connect to Azure Database for PostgreSQL:

```sql
psql "host=mydb.postgres... user=user@tenant.onmicrosoft.com dbname=postgres sslmode=require"
```

### Use a token as a password for signing in by using PgAdmin

To connect by using a Microsoft Entra token with PgAdmin, follow these steps:

1. Open PgAdmin and select **Register** > **Server**.
1. On the **General** tab, enter a connection name and clear **Connect now**.
1. On the **Connection** tab, enter host details. Set **Username** to your Microsoft Entra UPN (for example, `user@tenant.onmicrosoft.com`). Save.
1. In the tree, select the server and choose **Connect Server**.
1. When prompted, paste the access token as the password.

Here are some essential considerations when you're connecting:

- `user@tenant.onmicrosoft.com` is the userPrincipalName of the Microsoft Entra user.
- Be sure to use the exact way the Azure user is spelled. Microsoft Entra user and group names are case-sensitive.
- If the name contains spaces, use a backslash (`\`) before each space to escape it.
  You can use the Azure CLI to get the signed in user and set the value for `PGUSER` environment variable:

  ```bash
  export PGUSER=$(az ad signed-in-user show --query "[userPrincipalName]" -o tsv | sed 's/ /\\ /g')
  ```

- The access token is valid for 5 to 60 minutes. Get the access token before initiating the sign-in to Azure Database for PostgreSQL.

You're now authenticated to your Azure Database for PostgreSQL server through Microsoft Entra authentication.

## Authenticate with Microsoft Entra ID as a group member

This section shows how to connect by using a Microsoft Entra group. You must be a member of the group and the group must be created (mapped) in the database.

### Create a group principal

Create the group principal (role) in the database (replace the display name as needed):

```sql
select * from  pgaadauth_create_principal('Prod DB Readonly', false, false).
```

If you disable group sync, members can sign in by using their access tokens and specify the group name as username.

If you enable group sync (via pgaadauth.enable_group_sync server parameter set to "ON"), members should sign in by using their individual Microsoft Entra ID credentials, but they can still sign in by using the group name as the username.

- Group logins remain available for compatibility reasons but you can disable them by using: `ALTER ROLE "ROLE_NAME" NOLOGIN;`
- Don't delete the group role to maintain syncing.
- Groups autosync every 30 minutes.
- You can trigger manual sync by using: `SELECT * FROM pgaadauth_sync_roles_for_group_members();` (`pgaadauth.enable_group_sync` param must be "ON").
- Changes to group metadata like group name aren't synced.
- Group membership changes are synced.

> [!NOTE]  
> Managed identities and service principals are supported as group members.

### Sign in to Azure

Authenticate with Microsoft Entra ID by using the Azure CLI. This step isn't required in Azure Cloud Shell. The user needs to be a member of the Microsoft Entra group.

```azurecli-interactive
az login
```

### Retrieve a Microsoft Entra access token

Use the Azure CLI to get an access token for the Microsoft Entra authenticated user to access Azure Database for PostgreSQL. Here's an example of the public cloud:

```azurecli-interactive
az account get-access-token --resource https://ossrdbms-aad.database.windows.net
```

You must specify the initial resource value exactly as shown. For other clouds, you can look up the resource value by using the following command:

```azurecli-interactive
az cloud show
```

For Azure CLI version 2.0.71 and later, you can specify the command in the following convenient version for all clouds:

```azurecli-interactive
az account get-access-token --resource-type oss-rdbms
```

After authentication is successful, Microsoft Entra ID returns an access token:

```json
{
  "accessToken": "TOKEN",
  "expiresOn": "...",
  "subscription": "...",
  "tenant": "...",
  "tokenType": "Bearer"
}
```

### Use a token as a password for signing in with psql or PgAdmin

These considerations are essential when you're connecting as a group member:

- The group name must exactly match the Microsoft Entra group display name (case-sensitive).
- Use only the group name, not a member alias.
- Escape spaces where required (for example, `Prod\ DB\ Readonly`).
- Token validity is 5–60 minutes. Acquire it just before connecting; don't store tokens in scripts.

> [!TIP]  
> If authentication fails, verify the database role exists (for example, with `\du`) and confirm the `pgaadauth.enable_group_sync` setting.

You're now authenticated to your PostgreSQL server through Microsoft Entra authentication.

## Related content

- [Microsoft Entra authentication with Azure Database for PostgreSQL](../security/security-entra-concepts.md)
- [Manage Microsoft Entra roles in Azure Database for PostgreSQL](../security/security-manage-entra-users.md)
