---
title: Use Microsoft Entra ID and native PostgreSQL roles for authentication with Azure Cosmos DB for PostgreSQL
description: Learn how to set up Microsoft Entra ID and add native PostgreSQL roles for authentication with Azure Cosmos DB for PostgreSQL
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: how-to
ms.date: 04/12/2025
ms.custom: sfi-ropc-blocked
appliesto:
  - ✅ PostgreSQL
---

# Use Microsoft Entra ID and native PostgreSQL roles for authentication with Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

In this article, you configure authentication methods for Azure Cosmos DB for PostgreSQL. You manage Microsoft Entra ID admin users and native PostgreSQL roles for authentication with Azure Cosmos DB for PostgreSQL. You also learn how to use a Microsoft Entra ID token with Azure Cosmos DB for PostgreSQL.

An Azure Cosmos DB for PostgreSQL cluster is created with one built-in native PostgreSQL role named 'citus'. You can add more native PostgreSQL roles after cluster provisioning is completed.

You can also configure Microsoft Entra ID (formerly Azure Active Directory) authentication for Azure Cosmos DB for PostgreSQL. You can enable Microsoft Entra ID authentication in addition or instead of the native PostgreSQL authentication on your cluster. You can change authentication methods enabled on cluster at any point after the cluster is provisioned. When Microsoft Entra ID authentication is enabled, you can add multiple Microsoft Entra ID users to an Azure Cosmos DB for PostgreSQL cluster and make any of them administrators. Microsoft Entra ID user can be a user or a service principal.

## Choose authentication method
You need to use Azure portal to configure authentication methods on an Azure Cosmos DB for PostgreSQL cluster.

Complete the following items on your Azure Cosmos DB for PostgreSQL cluster to enable or disable Microsoft Entra ID authentication and native PostgreSQL authentication.

1. On the cluster page, under the **Cluster management** heading, choose **Authentication** to open authentication management options.
1. In **Authentication methods** section, choose **PostgreSQL authentication only**, **Microsoft Entra ID authentication**, or **PostgreSQL and Microsoft Entra ID authentication** as the authentication method based on your requirements.

Once done proceed with [configuring Microsoft Entra ID authentication](#configure-azure-active-directory-authentication) or [adding native PostgreSQL roles](#configure-native-postgresql-authentication) on the same **Authentication** page.

<a name='configure-azure-active-directory-authentication'></a>

## Configure Microsoft Entra ID authentication

### Prerequisites

Users need to be allowed to sign in to Azure Cosmos DB for PostgreSQL in the Microsoft Entra ID tenant. These steps should be performed once for the Microsoft Entra ID tenant that is going to be used for authentication on Azure Cosmos DB for PostgreSQL clusters.

> [!IMPORTANT]
> Microsoft Entra ID tenant administrator permissions are needed to make the change. See [guidance for troubleshooting permissions](/entra/identity/enterprise-apps/add-application-portal-configure#prerequisites).

# [Azure portal](#tab/portal)

1. Search for 'Microsoft Entra ID' in [Azure portal](https://portal.azure.com/).
1. Open 'Microsoft Entra ID' service.
1. On the **Overview** page of Microsoft Entra ID service in the **Overview** section, search for 'b4fa09d8-5da5-4352-83d9-05c2a44cf431' application ID.
1. Choose 'Azure Cosmos DB for PostgreSQL AAD Authentication' enterprise application in the search results.
1. In the **Azure Cosmos DB for PostgreSQL AAD Authentication** enterprise application, choose **Properties** page.
1. Set **Enabled for users to sign-in?** to **Yes** and save the change.

# [Azure CLI](#tab/cli)

```azurecli
az ad sp update --id b4fa09d8-5da5-4352-83d9-05c2a44cf431 --set accountEnabled=true
```
---

> [!NOTE]
> Editing enterprise application's properties such as "Enabled for users to sign-in" requires permissions granted to a role with privileges to update enterprise application properties. Roles, such as **Enterprise application owner**, must have the *"update enterprise application properties"* permission. For more information, see [Microsoft Entra least privileged roles by task - Enterprise applications](/entra/identity/role-based-access-control/delegate-by-task#enterprise-applications).

### Add Microsoft Entra ID admins to Azure Cosmos DB for PostgreSQL cluster

To add or remove Microsoft Entra ID roles on cluster, follow these steps on **Authentication** page:

1. In **Microsoft Entra ID authentication** section, select **Add Microsoft Entra ID admins**.
1. In **Select Microsoft Entra ID Admins** panel, select one or more valid Microsoft Entra ID user or enterprise application in the current AD tenant to be a Microsoft Entra ID administrator on your Azure Cosmos DB for PostgreSQL cluster.
1. Use **Select** to confirm your choice.
1. In the **Authentication** page, select **Save** in the toolbar to save changes or proceed with adding native PostgreSQL roles.

## Configure native PostgreSQL authentication

To add Postgres roles on cluster, follow these steps on **Authentication** page:

1. In **PostgreSQL authentication** section, select **Add PostgreSQL role**.
1. Enter the role name and password. Select **Save**.
1. In the **Authentication** page, select **Save** in the toolbar to save changes or proceed with adding Microsoft Entra ID admin users.

The native PostgreSQL user is created on the coordinator node of the cluster, and propagated to all the worker nodes. Roles created through the Azure portal have the LOGIN attribute, which means they’re true users who can sign in to the database.

<a name='connect-to-azure-cosmos-for-postgresql-by-using-azure-ad-authentication'></a>

## Connect to Azure Cosmos for PostgreSQL by using Microsoft Entra ID authentication

Microsoft Entra ID integration works with standard PostgreSQL client tools like **psql**, which aren't Microsoft Entra ID aware and support only specifying the username and password when you're connecting to PostgreSQL. In such cases, the Microsoft Entra ID token is passed as the password.

We tested the following clients:

- **psql command line**: Use the `PGPASSWORD` variable to pass the token.
- **Other libpq-based clients**: Examples include common application frameworks and object-relational mappers (ORMs).
- **pgAdmin**: Clear **Connect now** at server creation.

Use the following procedures to authenticate with Microsoft Entra ID as an Azure Cosmos DB for PostgreSQL user. You can follow along in [Azure Cloud Shell](/azure/cloud-shell/get-started), on an Azure virtual machine, or on your local machine.

### Sign in to the user's Azure subscription

Start by authenticating with Microsoft Entra ID by using the Azure CLI. This step isn't required in Azure Cloud Shell.

```azurecli
az login
```

The command opens a browser window to the Microsoft Entra ID authentication page. It requires you to give your Microsoft Entra ID user name and password.

The user account name you use to authenticate (for example, user@tenant.onmicrosoft.com) is the one the access token will be generated for in the next step.

<a name='retrieve-the-azure-ad-access-token'></a>

### Retrieve the Microsoft Entra ID access token

Use the Azure CLI to acquire an access token for the Microsoft Entra ID authenticated user to access Azure Cosmos for PostgreSQL. Here's an example:

```azurecli-interactive
az account get-access-token --resource https://token.postgres.cosmos.azure.com
```

After authentication is successful, Microsoft Entra ID returns an access token for current Azure subscription:

```json
{
  "accessToken": "[TOKEN]",
  "expiresOn": "[expiration_date_and_time]",
  "subscription": "[subscription_id]",
  "tenant": "[tenant_id]",
  "tokenType": "Bearer"
}
```

The TOKEN is a Base64 string. It encodes all the information about the authenticated user and is associated with the Azure Cosmos DB for PostgreSQL service. The token is valid for at least 5 minutes with the maximum of 90 minutes. The **expiresOn** defines actual token expiration time.

### Use a token as a password for signing in with client psql

When connecting, it's best to use the access token as the PostgreSQL user password.

While using the psql command-line client, the access token needs to be passed through the `PGPASSWORD` environment variable. The reason is that the access token exceeds the password length that psql can accept directly.

Here's a Windows example:

```cmd
set PGPASSWORD=<TOKEN value from the previous step>
```

```powerShell
$env:PGPASSWORD='<TOKEN value from the previous step>'
```

Here's a Linux/macOS example:

```bash
export PGPASSWORD=<TOKEN value from the previous step>
```

You can also combine the previous two steps together using command substitution. The token retrieval can be encapsulated into a variable and passed directly as a value for `PGPASSWORD` environment variable:

```bash
export PGPASSWORD=$(az account get-access-token --resource https://token.postgres.cosmos.azure.com --query "[accessToken]" -o tsv)
```


> [!NOTE]
> Make sure PGPASSWORD variable is set to the Microsoft Entra ID access token for your
> subscription for Microsoft Entra ID authentication. If you need to do Postgres role authentication
> from the same session you can set PGPASSWORD to the Postgres role password
> or clear the PGPASSWORD variable value to enter the password interactively.
> Authentication would fail with the wrong value in PGPASSWORD.

Now you can initiate a connection with Azure Cosmos DB for PostgreSQL using the Microsoft Entra ID user account that the access token was generated for. You would do it as you usually would with the user account as the user and without 'password' parameter in the command line:

```sql
psql "host=mycluster.[uniqueID].postgres.cosmos.azure.com user=user@tenant.onmicrosoft.com dbname=[db_name] sslmode=require"
```

### Use a token as a password for signing in with PgAdmin

To connect by using a Microsoft Entra ID token with PgAdmin, follow these steps:

1. Clear the **Connect now** option at server creation.
1. Enter your server details on the **Connection** tab and save.
    1. Make sure a valid Microsoft Entra ID user is specified in **Username**.
1. From the pgAdmin **Object** menu, select **Connect Server**.
1. Enter the Microsoft Entra ID token password when you're prompted.

Here are some essential considerations when you're connecting:

- `user@tenant.onmicrosoft.com` is the name of the Microsoft Entra ID user.
- Be sure to use the exact way the Azure user is spelled. Microsoft Entra ID user names are case-sensitive.
- If the name contains spaces, use a backslash (`\`) before each space to escape it.
- The access token's validity is 5 minutes to 90 minutes. You should get the access token before initiating the sign-in to Azure Cosmos for PostgreSQL.

You're now authenticated to your Azure Cosmos for PostgreSQL server through Microsoft Entra ID authentication.

## Manage native PostgreSQL roles

When native PostgreSQL authentication is enabled on cluster, you can add and delete Postgres roles in addition to built-in 'citus' role. You can also reset password and modify Postgres privileges for native roles.

### How to delete a native PostgreSQL user role or change their password

To update a user, visit the **Authentication** page for your cluster,
and select the ellipses **...** next to the user. The ellipses open a menu
to delete the user or reset their password.

The `citus` role is privileged and can't be deleted. However, `citus` role would be *disabled*, if 'Microsoft Entra ID authentication only' authentication method is selected for the cluster.

## How to modify privileges for user roles

New user roles are commonly used to provide database access with restricted
privileges. To modify user privileges, use standard PostgreSQL commands, using
a tool such as PgAdmin or psql. For more information, see [Connect to a cluster](quickstart-connect-psql.md).

For example, to allow PostgreSQL `db_user` to read `mytable`, grant the permission:

```sql
GRANT SELECT ON mytable TO db_user;
```

To grant the same permissions to Microsoft Entra ID role `user@tenant.onmicrosoft.com` use the following command:

```sql
GRANT SELECT ON mytable TO "user@tenant.onmicrosoft.com";
```

Azure Cosmos DB for PostgreSQL propagates single-table GRANT statements through the entire
cluster, applying them on all worker nodes. It also propagates GRANTs that are
system-wide (for example, for all tables in a schema):

```sql
-- applies to the coordinator node and propagates to worker nodes for Postgres role db_user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_user;
```

Or for Microsoft Entra ID role

```sql
-- applies to the coordinator node and propagates to worker nodes for Azure AD role user@tenant.onmicrosoft.com
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "user@tenant.onmicrosoft.com";
```


## Next steps

- Learn about [authentication in Azure Cosmos DB for PostgreSQL](./concepts-authentication.md)
- Check out [Microsoft Entra ID limits and limitations in Azure Cosmos DB for PostgreSQL](./reference-limits.md#azure-active-directory-authentication)
- Review [Microsoft Entra ID fundamentals](/entra/fundamentals/whatis)
- [Learn more about SQL GRANT in PostgreSQL](https://www.postgresql.org/docs/current/sql-grant.html)
