---
title: "Quickstart: Connect Using Python"
description: This quickstart provides several Python code samples you can use to connect and query data from an Azure Database for PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 08/27/2025
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-api
  - devx-track-python
  - passwordless-python
  - sfi-ropc-blocked
ms.devlang: python
---

# Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL

In this quickstart, you connect to an Azure Database for PostgreSQL flexible server instance by using Python. You then use SQL statements to query, insert, update, and delete data in the database from macOS, Ubuntu Linux, and Windows platforms.

The steps in this article include two authentication methods: Microsoft Entra authentication and PostgreSQL authentication. The **Passwordless** tab shows the Microsoft Entra authentication and the **Password** tab shows the PostgreSQL authentication.

Microsoft Entra authentication is a mechanism for connecting to Azure Database for PostgreSQL using identities defined in Microsoft Entra ID. With Microsoft Entra authentication, you can manage database user identities and other Microsoft services in a central location, which simplifies permission management. To learn more, see [Microsoft Entra authentication with Azure Database for PostgreSQL](../security/security-entra-concepts.md).

PostgreSQL authentication uses accounts stored in PostgreSQL. If you choose to use passwords as credentials for the accounts, these credentials are stored in the `user` table. Because these passwords are stored in PostgreSQL, you need to manage the rotation of the passwords by yourself.

This article assumes that you're familiar with developing using Python, but you're new to working with Azure Database for PostgreSQL.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Database for PostgreSQL flexible server instance. To create Azure Database for PostgreSQL flexible server instance, refer to [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md).
- [Python](https://www.python.org/downloads/) 3.8+.
- Latest [pip](https://pip.pypa.io/en/stable/installing/) package installer.

## Add firewall rules for your client workstation

- If you created your Azure Database for PostgreSQL flexible server instance with *Private access (virtual network Integration)*, you need to connect to your server from a resource within the same virtual network as your server. You can create a virtual machine and add it to the virtual network created with your Azure Database for PostgreSQL flexible server instance. Refer to [Networking](../network/how-to-networking.md).
- If you created your Azure Database for PostgreSQL flexible server instance with *Public access (allowed IP addresses)*, you can add your local IP address to the list of firewall rules on your server. Refer to [Networking](../network/how-to-networking.md).

## Configure Microsoft Entra integration on the server (passwordless only)

If you're following the steps for passwordless authentication, Microsoft Entra authentication must be configured for your server instance, and you must be assigned as a Microsoft Entra administrator on the server instance. Follow the steps in [Configure Microsoft Entra integration](../security/security-entra-configure.md) to ensure that Microsoft Entra authentication is configured and that you're assigned as a Microsoft Entra administrator on your server instance.

## Prepare your development environment

Change to a folder where you want to run the code and create and activate a [virtual environment](https://docs.python.org/3/tutorial/venv.html). A virtual environment is a self-contained directory for a particular version of Python plus the other packages needed for that application.

Run the following commands to create and activate a virtual environment:

### [Windows](#tab/cmd)

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
```

### [macOS/Linux](#tab/bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> [!NOTE]
> Ensure the virtual environment is activated before you run any `python -m pip instalL...` commands; using `python -m pip` (not a bare `pip`) ensures packages install into the same interpreter/venv you use to run the examples.

---

## Install the Python libraries

Install the Python libraries needed to run the code examples.

#### [Passwordless (Recommended)](#tab/passwordless)

Install the [azure-identity](https://pypi.org/project/azure-identity/) library, which provides Microsoft Entra token authentication support across the Azure SDK.

```bash
# Use the interpreter-bound pip to ensure installs go into the active venv/interpreter
python -m pip install --upgrade pip
python -m pip install azure-identity azure-keyvault-secrets
```

#### [Password](#tab/password)

Install the [psycopg](https://pypi.org/project/psycopg/) module, which enables connecting to and querying a PostgreSQL database.

```bash
# Recommended: install the binary wheel that bundles a compatible libpq wrapper (Windows/macOS)
python -m pip install "psycopg[binary]"

# Linux alternative (if you prefer building against system libpq):
sudo apt-get update
sudo apt-get install -y libpq-dev build-essential python3-dev
python -m pip install psycopg
```

---

## Add authentication code

In this section, you add authentication code to your working directory and perform any additional steps required for authentication and authorization with your server instance.

Before you add the authentication code, make sure the required packages for each example are installed.

Required packages (examples in this article):

- Passwordless example: `azure-identity`, `azure-keyvault-secrets` (if you use Key Vault)
- Password example: `psycopg` (recommended: `python -m pip install "psycopg[binary]"`)

Optional: create a `requirements.txt` with these entries and install with `python -m pip install -r requirements.txt` for reproducible installs.

#### [Passwordless (Recommended)](#tab/passwordless)

1. Copy the following code into an editor and save it in a file named *get_conn.py*.

   ```python
   import urllib.parse
   import os

   from azure.identity import DefaultAzureCredential

   # IMPORTANT! This code is for demonstration purposes only. It's not suitable for use in production.
   # For example, tokens issued by Microsoft Entra ID have a limited lifetime (24 hours by default).
   # In production code, you need to implement a token refresh policy.

   def get_connection_uri():

       # Read URI parameters from the environment
       dbhost = os.environ['DBHOST']
       dbname = os.environ['DBNAME']
       dbuser = urllib.parse.quote(os.environ['DBUSER'])
       sslmode = os.environ['SSLMODE']

       # Use passwordless authentication via DefaultAzureCredential.
       # IMPORTANT! This code is for demonstration purposes only. DefaultAzureCredential() is invoked on every call.
       # In practice, it's better to persist the credential across calls and reuse it so you can take advantage of token
       # caching and minimize round trips to the identity provider. To learn more, see:
       # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md
       credential = DefaultAzureCredential()

       # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
       # Note the requested scope parameter in the call to get_token, "https://ossrdbms-aad.database.windows.net/.default".
       password = credential.get_token("https://ossrdbms-aad.database.windows.net/.default").token

       db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}?sslmode={sslmode}"
       return db_uri
   ```

1. Get database connection information.

    1. In the [Azure portal](https://portal.azure.com/), search for and select your Azure Database for PostgreSQL flexible server instance name.
    1. On the server's **Overview** page, copy the fully qualified **Server name**. The fully qualified **Server name** is always of the form *\<my-server-name>.postgres.database.azure.com*.
    1. On the left menu, under **Security**, select **Authentication**. Make sure your account is listed under **Microsoft Entra Admins**. If it isn't, complete the steps in [Configure Microsoft Entra integration on the server (passwordless only)](#configure-microsoft-entra-integration-on-the-server-passwordless-only).

1. Set environment variables for the connection URI elements:

    ### [Windows](#tab/cmd)
    
    ```cmd
    set DBHOST=<server-name>
    set DBNAME=<database-name>
    set DBUSER=<username>
    set SSLMODE=require
    ```
    
    ### [macOS/Linux](#tab/bash)
    
    ```bash
    export DBHOST=<server-name>
    export DBNAME=<database-name>
    export DBUSER=<username>
    export SSLMODE=require
    ```

    Replace the following placeholder values in the commands:
    
    - `<server-name>` with the value you copied from the Azure portal.
    - `<username>` with your Azure user name; for example: `john@contoso.com`.
    - `<database-name>` with the name of your Azure Database for PostgreSQL flexible server database. A default database named *postgres* was automatically created when you created your server. You can use that database or create a new database by using SQL commands.

1. Sign in to Azure on your workstation. You can sign in using the Azure CLI, Azure PowerShell, or Azure Developer CLI.

    The authentication code uses [`DefaultAzureCredential`](/python/api/azure-identity/azure.identity.defaultazurecredential) to authenticate with Microsoft Entra ID and get a token that authorizes you to perform operations on your server instance. `DefaultAzureCredential` supports a chain of authentication credential types. Among the credentials supported are credentials that you're signed in to developer tools with like the Azure CLI, Azure PowerShell, or Azure Developer CLI.
    
#### [Password](#tab/password)

1. Copy the following code into an editor and save it in a file named *get_conn.py*.

   ```python
   import urllib.parse
   import os

   def get_connection_uri():

       # Read URI parameters from the environment
       dbhost = os.environ['DBHOST']
       dbname = os.environ['DBNAME']
       dbuser = urllib.parse.quote(os.environ['DBUSER'])
   password = os.environ['DBPASSWORD']
   sslmode = os.environ['SSLMODE']
   db_uri = f"host={dbhost} dbname={dbname} user={dbuser} password={password} sslmode={sslmode}"
       # Construct connection URI
       return db_uri
   ```

1. Get database connection information.

   Using the [Azure portal](https://portal.azure.com/):

   1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you have created.

   1. Select the server name.

   1. In the resource menu, select **Overview**.

      :::image type="content" source="media/connect-python/overview.png" alt-text="Screenshot showing the Overview page." lightbox="media/connect-python/overview.png":::

   1. Copy the values shown as **Endpoint** and **Administrator login**.

      :::image type="content" source="media/connect-python/endpoint-administrator-login.png" alt-text="Screenshot showing the values of Endpoint and Administrator login in the Overview page." lightbox="media/connect-python/endpoint-administrator-login.png":::

   1. If you forget the password of the administrator login, you can reset it using the **Reset password** button.

      :::image type="content" source="media/connect-python/reset-password.png" alt-text="Screenshot showing the Reset password button in the Overview page." lightbox="media/connect-python/reset-password.png":::

1. Set environment variables for the connection URI elements:

   ### [Windows](#tab/cmd)

   ```cmd
   set DBHOST=<server-name>
   set DBNAME=<database-name>
   set DBUSER=<username>
   set DBPASSWORD=<password>
   set SSLMODE=require
   ```

   ### [macOS/Linux](#tab/bash)

   ```bash
   export DBHOST=<server-name>
   export DBNAME=<database-name>
   export DBUSER=<username>
   export DBPASSWORD=<password>
   export SSLMODE=require
   ```

   ---

---

## How to run the Python examples

For each code example in this article:

1. Create a new file in a text editor.

1. Add the code example to the file.

1. Save the file in your project folder with a *.py* extension, such as *postgres-insert.py*. For Windows, make sure UTF-8 encoding is selected when you save the file.

1. In your project folder type `python` followed by the filename, for example `python postgres-insert.py`.

## Create a table and insert data

The following code example connects to your Azure Database for PostgreSQL flexible server database using the `psycopg.connect` function, and loads data with a SQL `INSERT` statement. The `cursor.execute` function executes the SQL query against the database.

```python
import psycopg
from get_conn import get_connection_uri

conn_string = get_connection_uri()

conn = psycopg.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS inventory;")
print("Finished dropping table (if existed)")

# Create a table
cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
print("Finished creating table")

# Insert some data into the table
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
print("Inserted 3 rows of data")

# Clean up
conn.commit()
cursor.close()
conn.close()
```

When the code runs successfully, it produces the following output:

```output
Connection established
Finished dropping table (if existed)
Finished creating table
Inserted 3 rows of data
```

## Read data

The following code example connects to your Azure Database for PostgreSQL flexible server database and uses cursor.execute with the SQL `SELECT` statement to read data. This function accepts a query and returns a result set to iterate over by using cursor.fetchall().

```python
import psycopg
from get_conn import get_connection_uri

conn_string = get_connection_uri()

conn = psycopg.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# Fetch all rows from table
cursor.execute("SELECT * FROM inventory;")
rows = cursor.fetchall()

# Print all rows
for row in rows:
    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

# Cleanup
conn.commit()
cursor.close()
conn.close()
```

When the code runs successfully, it produces the following output:

```output
Connection established
Data row = (1, banana, 150)
Data row = (2, orange, 154)
Data row = (3, apple, 100)
```

## Update data

The following code example connects to your Azure Database for PostgreSQL flexible server database and uses cursor.execute with the SQL `UPDATE` statement to update data.

```python
import psycopg
from get_conn import get_connection_uri

conn_string = get_connection_uri()

conn = psycopg.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# Update a data row in the table
cursor.execute("UPDATE inventory SET quantity = %s WHERE name = %s;", (200, "banana"))
print("Updated 1 row of data")

# Cleanup
conn.commit()
cursor.close()
conn.close()
```

## Delete data

The following code example connects to your Azure Database for PostgreSQL flexible server database and uses cursor.execute with the SQL `DELETE` statement to delete an inventory item that you previously inserted.

```python
import psycopg
from get_conn import get_connection_uri

conn_string = get_connection_uri()

conn = psycopg.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# Delete data row from table
cursor.execute("DELETE FROM inventory WHERE name = %s;", ("orange",))
print("Deleted 1 row of data")

# Cleanup
conn.commit()
cursor.close()
conn.close()
```

## Related content

- [Quickstart: Use Java and JDBC with Azure Database for PostgreSQL](connect-java.md)
- [Quickstart: Use .NET (C#) to connect and query data in Azure Database for PostgreSQL](connect-csharp.md)
- [Quickstart: Use Go language to connect and query data in Azure Database for PostgreSQL](connect-go.md)
- [Quickstart: Use PHP to connect and query data in Azure Database for PostgreSQL](connect-php.md)
- [Quickstart: Connect and query with Azure CLI with Azure Database for PostgreSQL](connect-azure-cli.md)
- [Quickstart: Import data from Azure Database for PostgreSQL in Power BI](../integration/connect-with-power-bi-desktop.md)
