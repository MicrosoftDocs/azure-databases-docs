---
title: Microsoft Entra ID authentication for Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about the concepts of Microsoft Entra ID authentication with Azure Cosmos DB for MongoDB vCore.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 04/14/2025
appliesto:
  - ✅ MongoDB vCore
---

# Microsoft Entra ID authentication with Azure Cosmos DB for MongoDB vCore

Azure Cosmos DB for MongoDB vCore supports integration with Microsoft Entra ID and native DocumentDB authentication. Each Azure Cosmos DB for MongoDB vCore cluster is created with native DocumentDB authentication enabled and one built-in administrative user.

You can enable Microsoft Entra ID (formerly Azure Active Directory) authentication on a cluster in addition to the native DocumentDB authentication method or instead of it. You can configure authentication methods on each Azure Cosmos DB for MongoDB vCore cluster independently. If you need to change authentication method, you can do it at any time after cluster provisioning is completed. Changing authentication methods doesn't require cluster restart.

## Microsoft Entra ID authentication

[Microsoft Entra ID](/entra/fundamentals/whatis) authentication is a mechanism of connecting to Azure Cosmos DB  for MongoDB vCore using identities defined in Microsoft Entra ID. With Microsoft Entra ID authentication, you can manage database user identities and other Microsoft services in a central location, which simplifies permission management and identity services compliance enforcement.

Benefits of using Microsoft Entra ID include:

- Authentication of users across Azure services in a uniform way
- Management of password policies and password rotation in a single place
- Multiple forms of authentication supported by Microsoft Entra ID, which can eliminate the need to store passwords
- Support of token-based authentication for applications connecting to Azure Cosmos DB for MongoDB vCore clusters

Interoperability with MongoDB drivers is provided via [OpenID Connect (OIDC) support in Microsoft Entra ID](/entra/identity-platform/v2-protocols-oidc). OIDC is an authentication protocol based on the OAuth2 protocol used for authorization. OIDC uses the standardized message flows from OAuth2 to provide identity services. When a security principal needs to authenticate to the database on an Azure Cosmos DB for MongoDB vCore cluster via Entra ID, OIDC identification and Entra ID security token should be provided.

### Administrative and non-administrative access for Microsoft Entra ID principals

When Microsoft Entra ID authentication is enabled on an Azure Cosmos DB for MongoDB vCore cluster, you can add one or more Microsoft Entra ID principals as *administrator users* to that cluster. The Microsoft Entra ID administrator sign-in can be a Microsoft Entra ID user, a service principal, or a managed identity. Multiple Microsoft Entra ID administrators can be configured at any time. 

Additionally, one or more non-administrative Microsoft Entra ID urser can be added to a cluster at any time once Microsoft Entra ID authentication is enabled. Non-administrative users are often used for ongoing production tasks that don't require administrative privileges.

## Considerations

- Microsoft Entra ID can be the only authentication method enabled on a 
- Multiple Microsoft Entra ID principals (a user, service principal, or managed identity) can be configured as Microsoft Entra ID administrator for an Azure Cosmos DB for MongoDB vCore cluster at any time.
-  If a Microsoft Entra ID principal is deleted from Microsoft Entra ID service, it still remains as a PostgreSQL role on the cluster, but it's no longer able to acquire new access token. In this case, although the matching role still exists in the Postgres database it's unable to authenticate to the cluster nodes. Database administrators need to transfer ownership and drop such roles manually.

> [!NOTE]  
> Login with the deleted Microsoft Entra ID user can still be done till the token expires (up to 90 minutes from token issuing).  If you also remove the user from Azure Cosmos DB for PostgreSQL cluster this access will be revoked immediately.

- Azure Cosmos DB for PostgreSQL matches access tokens to the database role using the user’s unique Microsoft Entra ID user ID, as opposed to using the username. If a Microsoft Entra ID user is deleted and a new user is created with the same name, Azure Cosmos DB for PostgreSQL considers that a different user. Therefore, if a user is deleted from Microsoft Entra ID and a new user is added with the same name the new user would be unable to connect with the existing role.

## Next steps

- Check out [Microsoft Entra ID limits and limitations in Azure Cosmos DB for PostgreSQL](./reference-limits.md#microsoft-entra-id-authentication)
- [Learn how to configure authentication for Azure Cosmos DB for PostgreSQL clusters](./how-to-configure-authentication.md)
- Set up private network access to the cluster nodes, see [Manage private access](./howto-private-access.md)
- Set up public network access to the cluster nodes, see [Manage public access](./howto-manage-firewall-using-portal.md)



## Prerequisites

Users need to be allowed to sign in to Azure Cosmos DB for MongoDB vCore in the Microsoft Entra ID tenant. These steps should be performed **once** for the Microsoft Entra ID *tenant* that is going to be used for authentication on Azure Cosmos DB for MongoDB vCore clusters.

> [!IMPORTANT]
> Microsoft Entra ID tenant administrator permissions are needed to make the change. See [guidance for troubleshooting permissions](/entra/identity/enterprise-apps/add-application-portal-configure#prerequisites).

# [Azure portal](#tab/portal)

1. Search for 'Microsoft Entra ID' in [Azure portal](https://portal.azure.com/).
1. Open 'Microsoft Entra ID' service.
1. On the **Overview** page of Microsoft Entra ID service in the **Overview** section, search for 'b4fa09d8-5da5-4352-83d9-05c2a44cf431' application ID.
1. Choose 'Azure Cosmos DB for MongoDB vCore AAD Authentication' enterprise application in the search results.
1. In the **Azure Cosmos DB for MongoDB vCore AAD Authentication** enterprise application, choose **Properties** page.
1. Set **Enabled for users to sign-in?** to **Yes** and save the change.

# [Azure CLI](#tab/cli)

```azurecli
az ad sp update --id b4fa09d8-5da5-4352-83d9-05c2a44cf431 --set accountEnabled=true
```
---

> [!NOTE]
> Editing enterprise application's properties such as "Enabled for users to sign-in" requires permissions granted to a user with privileges to update enterprise application properties. users, such as **Enterprise application owner**, must have the *"update enterprise application properties"* permisssion. For more information, see [Microsoft Entra least privileged users by task - Enterprise applications](/entra/identity/user-based-access-control/delegate-by-task#enterprise-applications).

## Add Microsoft Entra ID administrative users to Azure Cosmos DB for MongoDB vCore cluster

To add or remove Microsoft Entra ID users with administative permissions on cluster, follow these steps in [Azure CLI](/cli/azure/get-started-with-azure-cli):

1. Enable Microsoft Entra ID authentication on cluster in addition to the native DocumentDB authentication:
```azurecli
az rest --method put --url https://eastus2euap.management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.DocumentDB/mongoClusters/<clusterName>?api-version=2025-04-01-preview --body "{'location': '<cluterRegion>', 'properties': {'authConfig': {'allowedModes': ['MicrosoftEntraID', 'NativeAuth'] } } }"
```

1. In **Select Microsoft Entra ID Admins** panel, select one or more valid Microsoft Entra ID user or enterprise application in the current AD tenant to be a Microsoft Entra ID administrator on your Azure Cosmos DB for MongoDB vCore cluster.
1. Use **Select** to confirm your choice.
1. In the **Authentication** page, select **Save** in the toolbar to save changes or proceed with adding native MongoDB users.


Go to Body and choose json: { "location": "cluter region", "properties": { "authConfig": { "allowedModes": ["MicrosoftEntraID", "NativeAuth"] } }

# Command format example
az rest --method put --url https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.ContainerRegistry/registries/<containerRegistryName>?api-version=2023-01-01-preview --body "{'location': '<locationName>', 'sku': {'name': '<skuName>'}, 'properties': {'adminUserEnabled': '<propertyValue>'}}"


## Configure native MongoDB authentication

To add MongoDB users on cluster, follow these steps on **Authentication** page:

1. In **MongoDB authentication** section, select **Add MongoDB user**.
1. Enter the user name and password. Select **Save**.
1. In the **Authentication** page, select **Save** in the toolbar to save changes or proceed with adding Microsoft Entra ID admin users.

The native MongoDB user is created on the coordinator node of the cluster, and propagated to all the worker nodes. users created through the Azure portal have the LOGIN attribute, which means they’re true users who can sign in to the database.

<a name='connect-to-azure-cosmos-for-MongoDB-by-using-azure-ad-authentication'></a>

## Connect to Azure Cosmos for MongoDB by using Microsoft Entra ID authentication

Microsoft Entra ID integration works with standard MongoDB client tools like **psql**, which aren't Microsoft Entra ID aware and support only specifying the username and password when you're connecting to MongoDB. In such cases, the Microsoft Entra ID token is passed as the password.

We tested the following clients:

- **psql command line**: Use the `PGPASSWORD` variable to pass the token.
- **Other libpq-based clients**: Examples include common application frameworks and object-relational mappers (ORMs).
- **pgAdmin**: Clear **Connect now** at server creation.

Use the following procedures to authenticate with Microsoft Entra ID as an Azure Cosmos DB for MongoDB vCore user. You can follow along in [Azure Cloud Shell](/azure/cloud-shell/get-started), on an Azure virtual machine, or on your local machine.

### Sign in to the user's Azure subscription

Start by authenticating with Microsoft Entra ID by using the Azure CLI. This step isn't required in Azure Cloud Shell.

```azurecli
az login
```

The command opens a browser window to the Microsoft Entra ID authentication page. It requires you to give your Microsoft Entra ID user name and password.

The user account name you use to authenticate (for example, user@tenant.onmicrosoft.com) is the one the access token will be generated for in the next step.

<a name='retrieve-the-azure-ad-access-token'></a>

### Retrieve the Microsoft Entra ID access token

Use the Azure CLI to acquire an access token for the Microsoft Entra ID authenticated user to access Azure Cosmos for MongoDB. Here's an example:

```azurecli-interactive
az account get-access-token --resource https://token.MongoDB.cosmos.azure.com
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

The TOKEN is a Base64 string. It encodes all the information about the authenticated user and is associated with the Azure Cosmos DB for MongoDB vCore service. The token is valid for at least 5 minutes with the maximum of 90 minutes. The **expiresOn** defines actual token expiration time.

### Use a token as a password for signing in with client psql

When connecting, it's best to use the access token as the MongoDB user password.

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
export PGPASSWORD=$(az account get-access-token --resource https://token.MongoDB.cosmos.azure.com --query "[accessToken]" -o tsv)
```


> [!NOTE]
> Make sure PGPASSWORD variable is set to the Microsoft Entra ID access token for your
> subscription for Microsoft Entra ID authentication. If you need to do MongoDB user authentication
> from the same session you can set PGPASSWORD to the MongoDB user password
> or clear the PGPASSWORD variable value to enter the password interactively.
> Authentication would fail with the wrong value in PGPASSWORD.

Now you can initiate a connection with Azure Cosmos DB for MongoDB vCore using the Microsoft Entra ID user account that the access token was generated for. You would do it as you usually would with the user account as the user and without 'password' parameter in the command line:

```sql
psql "host=mycluster.[uniqueID].MongoDB.cosmos.azure.com user=user@tenant.onmicrosoft.com dbname=[db_name] sslmode=require"
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
- Be sure to use the exact way the Azure user is spelled. Microsoft Entra ID user and group names are case-sensitive.
- If the name contains spaces, use a backslash (`\`) before each space to escape it.
- The access token's validity is 5 minutes to 90 minutes. You should get the access token before initiating the sign-in to Azure Cosmos for MongoDB.

You're now authenticated to your Azure Cosmos for MongoDB server through Microsoft Entra ID authentication.

## Manage native MongoDB users

When native MongoDB authentication is enabled on cluster, you can add and delete MongoDB users in addition to built-in 'citus' user. You can also reset password and modify MongoDB privileges for native users.

### How to delete a native MongoDB user user or change their password

To update a user, visit the **Authentication** page for your cluster,
and select the ellipses **...** next to the user. The ellipses open a menu
to delete the user or reset their password.

The `citus` user is privileged and can't be deleted. However, `citus` user would be *disabled*, if 'Microsoft Entra ID authentication only' authentication method is selected for the cluster.

## How to modify privileges for user users

New user users are commonly used to provide database access with restricted
privileges. To modify user privileges, use standard MongoDB commands, using
a tool such as PgAdmin or psql. For more information, see [Connect to a cluster](quickstart-connect-psql.md).

For example, to allow MongoDB `db_user` to read `mytable`, grant the permission:

```sql
GRANT SELECT ON mytable TO db_user;
```

To grant the same permissions to Microsoft Entra ID user `user@tenant.onmicrosoft.com` use the following command:

```sql
GRANT SELECT ON mytable TO "user@tenant.onmicrosoft.com";
```

Azure Cosmos DB for MongoDB vCore propagates single-table GRANT statements through the entire
cluster, applying them on all worker nodes. It also propagates GRANTs that are
system-wide (for example, for all tables in a schema):

```sql
-- applies to the coordinator node and propagates to worker nodes for MongoDB user db_user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_user;
```

Or for Microsoft Entra ID user

```sql
-- applies to the coordinator node and propagates to worker nodes for Azure AD user user@tenant.onmicrosoft.com
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "user@tenant.onmicrosoft.com";
```


## Next steps

- Learn about [authentication in Azure Cosmos DB for MongoDB vCore](./concepts-authentication.md)
- Check out [Microsoft Entra ID limits and limitations in Azure Cosmos DB for MongoDB vCore](./reference-limits.md#azure-active-directory-authentication)
- Review [Microsoft Entra ID fundamentals](/entra/fundamentals/whatis)
- [Learn more about SQL GRANT in MongoDB](https://www.MongoDB.org/docs/current/sql-grant.html)
