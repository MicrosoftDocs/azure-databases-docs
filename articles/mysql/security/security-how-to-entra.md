---
title: Set up Microsoft Entra Authentication
description: Learn how to set up Microsoft Entra authentication for Azure Database for MySQL - Flexible Server.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 07/17/2026
ms.service: azure-database-mysql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
  - has-azure-ad-ps-ref
  - sfi-image-nochange
  - sfi-ropc-nochange
---

# Set up Microsoft Entra authentication for Azure Database for MySQL - Flexible Server

This tutorial shows you how to set up Microsoft Entra authentication for Azure Database for MySQL Flexible Server.

In this tutorial, you learn how to:

- Configure the Microsoft Entra admin.
- Connect to Azure Database for MySQL Flexible Server by using Microsoft Entra ID.

## Prerequisites

- An Azure account with an active subscription.
- If you don't have an Azure subscription, create an [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).

<a id="configure-the-azure-ad-admin"></a>

## Configure the Microsoft Entra Admin

To create a Microsoft Entra Admin user, follow these steps:

- In the Azure portal, select the instance of Azure Database for MySQL Flexible Server that you want to enable for Microsoft Entra ID.
- Under the Security pane, select **Authentication**:
  :::image type="content" source="media/how-to-azure-ad/Azure-ad-configuration.jpg" alt-text="Diagram of how to configure Microsoft Entra authentication.":::

- Choose from three types of authentication:
  - **MySQL authentication only** - By default, MySQL uses the built-in `mysql_native_password` authentication plugin, which performs authentication by using the native password hashing method.
  - **Microsoft Entra authentication only** - Only allows authentication by using a Microsoft Entra account. Disables `mysql_native_password` authentication and turns *ON* the server parameter `aad_auth_only`.
  - **MySQL and Microsoft Entra authentication** - Allows authentication by using a native MySQL password or a Microsoft Entra account. Turns *OFF* the server parameter `aad_auth_only`.
- **Select Identity** - Select or add a user-assigned managed identity. To allow the UAMI to read from Microsoft Graph as the server identity, it needs the following permissions. Alternatively, give the user-assigned managed identity the [Directory Readers](/azure/active-directory/roles/permissions-reference#directory-readers) role.
  - [User.Read.All](/graph/permissions-reference#user-permissions): Allows access to Microsoft Entra user information.
  - [GroupMember.Read.All](/graph/permissions-reference#group-permissions): Allows access to Microsoft Entra group information.
  - [Application.Read.ALL](/graph/permissions-reference#application-resource-permissions): Allows access to Microsoft Entra service principal (application) information.

> [!IMPORTANT]  
> Only a user with at least the [Privileged Role Administrator](/azure/active-directory/roles/permissions-reference#privileged-role-administrator) role can grant these permissions.

- Select a valid Microsoft Entra user or a Microsoft Entra group in your tenant to be **Microsoft Entra administrator** for your database server.

  > [!NOTE]  
  > You can create only one Microsoft Entra admin per MySQL server. Selecting another admin overwrites the existing Microsoft Entra admin configured for the server.

### Grant permissions to user-assigned managed identity

The following sample PowerShell script grants the necessary permissions for a UMI. This sample assigns permissions to the UMI `umiservertest`.

To run the script, sign in as a user with a Privileged Role Administrator role.

The script grants the `User.Read.All`, `GroupMember.Read.All`, and `Application.Read.ALL` permissions to a UMI to access [Microsoft Graph](/graph/auth/auth-concepts#microsoft-graph-permissions).

```powershell
# Script to assign permissions to the UMI "umiservertest"

import-module Az.Resources
import-module Microsoft.Entra
$tenantId = '<tenantId>' # Your Azure AD tenant ID

Connect-Entra -TenantID $tenantId
# Log in as a user with a "Privileged Role Administrator" role
# Script to assign permissions to an existing UMI
# The following Microsoft Graph permissions are required:
#   User.Read.All
#   GroupMember.Read.All
#   Application.Read.ALL

# Search for Microsoft Graph
$AAD_SP = Get-AzADServicePrincipal -DisplayNameStartsWith "Microsoft Graph"
$AAD_SP
# Use Microsoft Graph; in this example, this is the first element $AAD_SP[0]

#Output

#ObjectId                             AppId                                DisplayName
#--------                             -----                                -----------
#44444444-4444-4444-4444-444444444444 00000003-0000-0000-c000-000000000000 Microsoft Graph
#44444444-4444-4444-4444-444444444444 0bf30f3b-4a52-48df-9a82-234910c4a086 Microsoft Graph #Change

$MSIName = "<managedIdentity>";  # Name of your user-assigned
$MSI = Get-AzADServicePrincipal -DisplayNameStartsWith $MSIName
if($MSI.Count -gt 1)
{
Write-Output "More than 1 principal found, please find your principal and copy the right object ID. Now use the syntax $MSI = Get-AzureADServicePrincipal -ObjectId <your_object_id>"

# Choose the right UMI

Exit
}

# If you have more UMIs with similar names, you have to use the proper $MSI[ ]array number

# Assign the app roles

$AAD_AppRole = $AAD_SP.AppRole | Where-Object {$_.Value -eq "User.Read.All"}
New-AzADServicePrincipalAppRoleAssignment -ServicePrincipalId $MSI.Id -ResourceId $AAD_SP.Id -AppRoleId $AAD_AppRole.Id
$AAD_AppRole = $AAD_SP.AppRole | Where-Object {$_.Value -eq "GroupMember.Read.All"}
New-AzADServicePrincipalAppRoleAssignment -ServicePrincipalId $MSI.Id -ResourceId $AAD_SP.Id -AppRoleId $AAD_AppRole.Id
$AAD_AppRole = $AAD_SP.AppRole | Where-Object {$_.Value -eq "Application.Read.All"}
New-AzADServicePrincipalAppRoleAssignment -ServicePrincipalId $MSI.Id -ResourceId $AAD_SP.Id -AppRoleId $AAD_AppRole.Id
```

In the final steps of the script, if you have more UMIs with similar names, you must use the proper `$MSI[ ]array` number. An example is `$AAD_SP.ObjectId[0]`.

### Check permissions for user-assigned managed identity

To check permissions for a UMI, go to the [Azure portal](https://portal.azure.com). In the **Microsoft Entra ID** resource, go to **Enterprise applications**. Select **All Applications** for **Application type**, and search for the UMI that you created.

Select the UMI, and go to the **Permissions** settings under **Security**.

When you grant the permissions to the UMI, they apply to all servers you create with the UMI assigned as a server identity.

<a id="connect-to-azure-database-for-mysql---flexible-server-using-azure-ad"></a>

## Connect to Azure Database for MySQL Flexible Server using Microsoft Entra ID

<a id="1---authenticate-with-azure-ad"></a>

### 1 - Authenticate with Microsoft Entra ID

Start by authenticating with Microsoft Entra ID by using the Azure CLI tool.
*(This step isn't required in Azure Cloud Shell.)*

- Sign in to your Azure account by using the [az login](/cli/azure/reference-index#az-login) command. Note the ID property, which refers to the Subscription ID for your Azure account:

  ```azurecli-interactive
  az login
  ```

The command launches a browser window to the Microsoft Entra authentication page. It requires you to provide your Microsoft Entra user ID and password.

- If you have multiple subscriptions, choose the appropriate subscription by using the `az account set` command:

  ```azurecli-interactive
  az account set --subscription \<subscription id\>
  ```

<a id="2---retrieve-azure-ad-access-token"></a>

### 2 - Retrieve Microsoft Entra access token

Invoke the Azure CLI tool to acquire an access token for the Microsoft Entra authenticated user from step 1 to access Azure Database for MySQL Flexible Server.

- Azure CLI example to acquire access token:

  ```azurecli-interactive
  az account get-access-token --resource https://ossrdbms-aad.database.windows.net
  ```

- Azure PowerShell example to acquire access token:

  ```powershell
  $accessToken = Get-AzAccessToken -ResourceUrl https://ossrdbms-aad.database.windows.net
  $accessToken.Token | out-file C:\temp\MySQLAccessToken.txt
  ```

Microsoft Entra returns an access token:

```json
{
  "accessToken": "TOKEN",
  "expiresOn": "...",
  "subscription": "...",
  "tenant": "...",
  "tokenType": "Bearer"
}
```

The token is a Base 64 string that encodes all the information about the authenticated user and is targeted to the Azure Database for MySQL service.

The access token validity is anywhere between 5 minutes to 60 minutes. Get the access token before initiating the sign-in to Azure Database for MySQL Flexible Server.

- Use the following PowerShell command to see the token validity.

```powershell
    $accessToken.ExpiresOn.DateTime
  ```

### 3 - Use a token as a password for logging in with MySQL

Use the access token as the MySQL user password when connecting.

## Connect to Azure Database for MySQL Flexible Server by using MySQL CLI

When you use the CLI, use this shorthand to connect:

**Example (Linux/macOS):**

```powershell
mysql -h mydb.mysql.database.azure.com \
  --user user@tenant.onmicrosoft.com \
  --enable-cleartext-plugin \
  --password=`az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken`
```

**Example (PowerShell):**

```powershell
mysql -h mydb.mysql.database.azure.com \
  --user user@tenant.onmicrosoft.com \
  --enable-cleartext-plugin \
  --password=$(az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken)

mysql -h mydb.mysql.database.azure.com \
  --user user@tenant.onmicrosoft.com \
  --enable-cleartext-plugin \
  --password=$((Get-AzAccessToken -ResourceUrl https://ossrdbms-aad.database.windows.net).Token)
```

## Connect to Azure Database for MySQL Flexible Server by using MySQL Workbench

- Launch MySQL Workbench and select the Database option, and then select **Connect to database**.
- In the hostname field, enter the MySQL FQDN, such as `mysql.database.azure.com`.
- In the username field, enter the MySQL Microsoft Entra administrator name. For example, `user@tenant.onmicrosoft.com`.
- In the password field, select **Store in Vault** and paste the access token from the file, such as `C:\temp\MySQLAccessToken.txt`.
- Select the advanced tab and ensure that you check **Enable Cleartext Authentication Plugin**.
- Select **OK** to connect to the database.

## Important considerations when connecting

- `user@tenant.onmicrosoft.com` is the name of the Microsoft Entra user or group you connect as
- Use the exact spelling for the Microsoft Entra user or group name
- Microsoft Entra user and group names are case sensitive
- When connecting as a group, use only the group name (for example, `GroupName`)
- If the name contains spaces, use `\` before each space to escape it

> [!NOTE]  
> For the `enable-cleartext-plugin` setting, use a similar configuration with other clients to make sure the token gets sent to the server without being hashed.

You're now authenticated to your MySQL flexible server by using Microsoft Entra authentication.

<a id="other-azure-ad-admin-commands"></a>

## Other Microsoft Entra admin commands

- Manage server Active Directory administrator

  ```azurecli-interactive
  az mysql flexible-server ad-admin
  ```

- Create an Active Directory administrator

  ```azurecli-interactive
  az mysql flexible-server ad-admin create
  ```

  *Example: Create Active Directory administrator with user `john@contoso.com`, administrator ID `00000000-0000-0000-0000-000000000000`, and identity `test-identity`*

  ```azurecli-interactive
  az mysql flexible-server ad-admin create -g testgroup -s testsvr -u john@contoso.com -i 00000000-0000-0000-0000-000000000000 --identity test-identity
  ```

- Delete an Active Directory administrator

  ```azurecli-interactive
  az mysql flexible-server ad-admin delete
  ```

  *Example: Delete Active Directory administrator*

  ```azurecli-interactive
  az mysql flexible-server ad-admin delete -g testgroup -s testsvr
  ```

- List all Active Directory administrators

  ```azurecli-interactive
  az mysql flexible-server ad-admin list
  ```

  *Example: List Active Directory administrators*

  ```azurecli-interactive
  az mysql flexible-server ad-admin list -g testgroup -s testsvr
  ```

- Get an Active Directory administrator

  ```azurecli-interactive
  az mysql flexible-server ad-admin show
  ```

  *Example: Get Active Directory administrator*

  ```azurecli-interactive
  az mysql flexible-server ad-admin show -g testgroup -s testsvr
  ```

- Wait for the Active Directory administrator to satisfy certain conditions

  ```azurecli-interactive
  az mysql flexible-server ad-admin wait
  ```

  *Examples:*

  - *Wait until the Active Directory administrator exists*

    ```azurecli-interactive
    az mysql flexible-server ad-admin wait -g testgroup -s testsvr --exists
    ```

  - *Wait for the Active Directory administrator to be deleted*

    ```azurecli-interactive
    az mysql flexible-server ad-admin wait -g testgroup -s testsvr -deleted
    ```

<a id="create-azure-ad-users-in-azure-database-for-mysql"></a>

## Create Microsoft Entra users in Azure Database for MySQL

To add a Microsoft Entra user to your Azure Database for MySQL database, complete the following steps after connecting:

1. Ensure that the Microsoft Entra user `<user>@yourtenant.onmicrosoft.com` is a valid user in the Microsoft Entra tenant.
1. Sign in to your Azure Database for MySQL instance as the Microsoft Entra admin user.
1. Create user `<user>@yourtenant.onmicrosoft.com` in Azure Database for MySQL.

*Example:*

```sql
CREATE AADUSER 'user1@yourtenant.onmicrosoft.com';
```

For user names that exceed 32 characters, use an alias instead of the full user name.

*Example:*

```sql
CREATE AADUSER 'userWithLongName@yourtenant.onmicrosoft.com' as 'userDefinedShortName';
```

> [!NOTE]  
> 1. MySQL ignores leading and trailing spaces, so the user name shouldn't have any leading or trailing spaces.
> 1. Authenticating a user through Microsoft Entra ID doesn't give the user any permissions to access objects within the Azure Database for MySQL database. You must grant the user the required permissions manually.

<a id="create-azure-ad-groups-in-azure-database-for-mysql"></a>

## Create Microsoft Entra groups in Azure Database for MySQL

To enable a Microsoft Entra group for access to your database, use the same mechanism as for users, but specify the group name:

*Example:*

```sql
CREATE AADUSER 'Prod_DB_Readonly';
```

When logging in, group members use their personal access tokens but sign in with the group name specified as the username.

## Compatibility with application drivers

Most drivers are supported. However, make sure to use the settings for sending the password in clear text, so the token goes without modification.

- C/C++
  - libmysqlclient: Supported
  - mysql-connector-c++: Supported

- Java
  - Connector/J (mysql-connector-java): Supported, must use the `useSSL` setting

- Python
  - Connector/Python: Supported

- Ruby
  - mysql2: Supported

- .NET
  - mysql-connector-net: Supported, need to add plugin for mysql_clear_password
  - mysql-net/MySqlConnector: Supported

- Node.js
  - mysqljs: Not supported (doesn't send the token in clear text without patch)
  - node-mysql2: Supported

- Perl
  - DBD::mysql: Supported
  - Net::MySQL: Not supported

- Go
  - go-sql-driver: Supported, add `?tls=true&allowCleartextPasswords=true` to connection string

- PHP

  - `mysqli` extension: Supported

  - PDO_MYSQL driver: Supported

## Next step

> [!div class="nextstepaction"]
> [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](security-entra-authentication.md)

## Related content

- [Secure your Azure Database for MySQL Server](security-overview.md)
- [Create users in Azure Database for MySQL flexible server](security-how-to-create-users.md)
- [Connect to Azure Database for MySQL flexible server with encrypted connections](security-tls-how-to-connect.md)
