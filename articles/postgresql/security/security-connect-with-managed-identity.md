---
title: Connect with Managed Identity
description: Learn about how to connect and authenticate using managed identity for authentication with an Azure Database for PostgreSQL flexible server instance.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - devx-track-csharp
  - devx-track-extended-java
  - devx-track-python
  - sfi-ropc-nochange
  - horz-security
---

# Connect with managed identity to Azure Database for PostgreSQL 

You can use both system-assigned and user-assigned managed identities to authenticate to an Azure Database for PostgreSQL flexible server instance. This article shows you how to use a system-assigned managed identity for an Azure Virtual Machine (VM) to access an Azure Database for PostgreSQL flexible server instance. Managed Identities are automatically managed by Azure and enable you to authenticate to services that support Microsoft Entra authentication without needing to insert credentials into your code.

You learn how to:
- Grant your VM access to an Azure Database for PostgreSQL flexible server instance.
- Create a user in the database that represents the VM's system-assigned identity.
- Get an access token using the VM identity and use it to query an Azure Database for PostgreSQL flexible server instance.
- Implement the token retrieval in a C# example application.

## Prerequisites

- If you're not familiar with the managed identities for Azure resources feature, see this [overview](/azure/active-directory/managed-identities-azure-resources/overview). If you don't have an Azure account, [sign up for a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you continue.
- To do the required resource creation and role management, your account needs "Owner" permissions at the appropriate scope (your subscription or resource group). If you need assistance with a role assignment, see [Assign Azure roles to manage access to your Azure subscription resources](/azure/role-based-access-control/role-assignments-portal).
- You need an Azure VM (for example, running Ubuntu Linux) that you'd like to use to access your database using Managed Identity
- You need an Azure Database for PostgreSQL flexible server instance that has [Microsoft Entra authentication](../security/security-entra-configure.md) configured
- To follow the C# example, first, complete the guide on how to [Connect with C#](../connectivity/connect-csharp.md)

## Create a system-assigned managed identity for your VM

Use [az vm identity assign](/cli/azure/vm/identity/) with the `identity assign` command enables the system-assigned identity to an existing VM:

```azurecli-interactive
az vm identity assign -g myResourceGroup -n myVm
```

Retrieve the application ID for the system-assigned managed identity, which you need in the next few steps:

```azurecli-interactive
# Get the client ID (application ID) of the system-assigned managed identity

az ad sp list --display-name vm-name --query [*].appId --out tsv
```

## Create an Azure Database for PostgreSQL  user for your Managed Identity

Now, connect as the Microsoft Entra administrator user to your Azure Database for PostgreSQL flexible server database, and run the following SQL statements, replacing `<identity_name>` with the name of the resources for which you created a system-assigned managed identity:

Note **pgaadauth_create_principal** must be run on the Postgres database.

```sql
select * from pgaadauth_create_principal('<identity_name>', false, false);
```

Success looks like:

```sql
    pgaadauth_create_principal
-----------------------------------
 Created role for "<identity_name>"
(1 row)
```

For more information on managing Microsoft Entra ID enabled database roles, see [Manage Microsoft Entra roles in Azure Database for PostgreSQL](../security/security-manage-entra-users.md).

The managed identity now has access when authenticating with the identity name as a role name and the Microsoft Entra token as a password.

> [!NOTE]  
> If the managed identity is not valid, an error is returned: `ERROR:   Could not validate AAD user <ObjectId> because its name is not found in the tenant. [...]`.
>
> If you see an error like "No function matches...", make sure you're connecting to the `postgres` database, not a different database that you also created.

## Retrieve the access token from the Azure Instance Metadata service

Your application can now retrieve an access token from the Azure Instance Metadata service and use it for authenticating with the database.

This token retrieval is done by making an `HTTP` request to `http://169.254.169.254/metadata/identity/oauth2/token` and passing the following parameters:

- `api-version` = `2018-02-01`
- `resource` = `https://ossrdbms-aad.database.windows.net`
- `client_id` = `CLIENT_ID` (that you retrieved earlier)

You get back a JSON result containing an `access_token` field - this long text value is the Managed Identity access token you should use as the password when connecting to the database.

For testing purposes, you can run the following commands in your shell.

> [!NOTE]  
> Note you need `curl`, `jq`, and the `psql` client installed.

```bash
# Retrieve the access token

export PGPASSWORD=`curl -s 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fossrdbms-aad.database.windows.net&client_id=CLIENT_ID' -H Metadata:true | jq -r .access_token`

# Connect to the database

psql -h SERVER --user USER DBNAME
```

You're now connected to the database you configured earlier.

## Connect using Managed Identity

This section shows how to get an access token using the VM's user-assigned managed identity and use it to call an Azure Database for PostgreSQL flexible server instance. Azure Database for PostgreSQL natively supports Microsoft Entra authentication, so it can directly accept access tokens obtained using managed identities for Azure resources. When creating a connection to an Azure Database for PostgreSQL, you pass the access token in the password field.

## Connect using Managed Identity in Python

For a Python code example, refer to the [Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL](../connectivity/connect-python.md)

## Connect using Managed Identity in Java

For a Java code example, refer to the [Quickstart: Use Java and JDBC with Azure Database for PostgreSQL](../connectivity/connect-java.md)

## Connect using Managed Identity in C#

Here's a .NET code example of opening a connection to an Azure Database for PostgreSQL flexible server instance using an access token. This code must run on the VM to use the system-assigned managed identity to obtain an access token from Microsoft Entra ID. Replace the values of HOST, USER (with `<identity_name>`), and `DATABASE`.

```csharp
using Azure.Identity;
using Npgsql;
using System;

class Program
{
    static void Main(string[] args)
    {
        try
        {
            // Obtain an access token using the system-assigned managed identity
            var tokenCredential = new DefaultAzureCredential();
            var accessToken = tokenCredential.GetToken(
                new Azure.Core.TokenRequestContext(new[] { "https://ossrdbms-aad.database.windows.net/.default" })
            );

            // Build the connection string
            string host = "your-server-name.postgres.database.azure.com"; // Replace with your flexible server's host
            string database = "your-database-name";                      // Replace with your database name
            string user = "<identity_name>";                             // Replace with your identity name (e.g., "myManagedIdentity")

            var connectionString = $"Host={host};Database={database};Username={user};Password={accessToken.Token};SSL Mode=Require;Trust Server Certificate=true";

            // Open a connection to the database
            using var connection = new NpgsqlConnection(connectionString);
            connection.Open();

            Console.WriteLine("Connection successful!");

            // Optional: Perform a simple query
            using var command = new NpgsqlCommand("SELECT version();", connection);
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                Console.WriteLine($"PostgreSQL version: {reader.GetString(0)}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}
```

You must fill in the following placeholders:

- HOST: Replace your-server-name.postgres.database.azure.com with your instance's hostname.
- USER: Replace <identity_name> with the name of your managed identity.
- `DATABASE`: Replace your-database-name with the name of your Azure Database for PostgreSQL instance.
- Microsoft Entra Authentication: The code uses the system-assigned managed identity of the VM to fetch an access token from Microsoft Entra ID.

When run, this command gives an output like this:

```output
Getting access token from Azure AD...
Opening connection using access token...

Connected!

Postgres version: PostgreSQL 11.11, compiled by Visual C++ build 1800, 64-bit
```

## Related content

- [Microsoft Entra authentication in Azure Database for PostgreSQL](../security/security-entra-concepts.md)
