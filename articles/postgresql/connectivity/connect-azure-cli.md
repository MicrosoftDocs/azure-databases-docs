---
title: "Quickstart: Connect and Query by Using Azure CLI in Azure Database for PostgreSQL Flexible Server"
description: This quickstart provides several ways to connect by using Azure CLI with an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to connect to my Azure Database for PostgreSQL flexible server using Azure CLI, so that I can verify my connection works from my development environment.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: quickstart
---

# Quickstart: Connect and query by using Azure CLI with Azure Database for PostgreSQL flexible server

This quickstart shows how to connect to an Azure Database for PostgreSQL flexible server by using Azure CLI with `az postgres flexible-server connect`. It also shows how to execute a single query or SQL file by using the `az postgres flexible-server execute` command. This command helps you test connectivity to your database server and run queries. You can also run multiple queries by using the interactive mode. 

## Prerequisites
- An Azure account with an active subscription. If you don't have one, [get a free trial](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Install the latest version of [Azure CLI](/cli/azure/install-azure-cli).
- Sign in by using Azure CLI with the `az login` command.
- (optional) Turn on an experimental parameter persistence by using `az config param-persist on`. Parameter persistence helps you use local context without having to repeat numerous arguments like resource group or location.

## Create Azure Database for PostgreSQL instance

First, create a managed Azure Database for PostgreSQL flexible server. In [Azure Cloud Shell](https://shell.azure.com/), run the following script. Make a note of the **server name**, **username**, and **password** generated from this command.

```azurecli-interactive
az postgres flexible-server create --public-access <your-ip-address>
```

To customize the command, provide more arguments. See all arguments for [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create).

## View all the arguments
You can view all the arguments for this command by using the `--help` argument. 

```azurecli-interactive
az postgres flexible-server connect --help
```

## Test database server connection
You can test and validate the connection to the database from your development environment by using the [az postgres flexible-server connect](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-connect) command.

```azurecli-interactive
az postgres flexible-server connect \
    -n <servername> -u <username> -p "<password>" -d <databasename>
```
**Example:** 
```azurecli-interactive
az postgres flexible-server connect \
    -n server372060240 -u starchylapwing9 -p "dbpassword" -d postgres
```
You see similar output if the connection is successful.

```output
Successfully connected to server372060240.
```

If the connection fails, check the following points:
- Ensure your server administrator user name and password are correct.
- Ensure you configured the firewall rule for your client machine.
- If your server is configured with private access by using virtual networking, make sure your client machine is in the same virtual network.

## Run multiple queries by using interactive mode
You can run multiple queries by using the **interactive** mode. To enable interactive mode, run the following command.

```azurecli-interactive
az postgres flexible-server connect \
    -n <servername> -u <username> -p "<password>" -d <databasename> \
    --interactive
```

**Example:**

```azurecli-interactive
az postgres flexible-server connect \
    -n server372060240 -u starchylapwing9 -p "dbpassword" -d postgres --interactive
```

You see the **psql** shell experience similar to the following output:

```output
Password for starchylapwing9:
Server: PostgreSQL 13.14
Version: 4.0.1
Home: http://pgcli.com
postgres> SELECT 1;
+----------+
| ?column? |
|----------|
| 1        |
+----------+
SELECT 1
Time: 0.167s
postgres>
```

## Execute single queries
Use [az postgres flexible-server execute](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-execute) to run single queries against a Postgres database.

```azurecli-interactive
az postgres flexible-server execute \
    -n <servername> -u <username> -p "<password>" -d <databasename> \
    -q <querytext> --output table
```

**Example:** 
```azurecli-interactive
az postgres flexible-server execute \
    -n server372060240 -u starchylapwing9 -p "dbpassword" -d postgres \
    -q "SELECT 1" --output table
```

You see an output as shown in the following example:

```output
Successfully connected to server372060240.
Ran Database Query: 'SELECT 1'
Retrieving first 30 rows of query output, if applicable.
Closed the connection to server372060240
?column?
----------
1
```

## Run SQL file
Use the [az postgres flexible-server execute](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-execute) command with the `--file-path` argument, `-f`, to execute a SQL file.

```azurecli-interactive
az postgres flexible-server execute \
    -n <server-name> -u <username> -p "<password>" -d <database-name> \
    --file-path "<file-path>"
```

**Example:** 
Prepare a `test.sql` file. You can use the following test script with simple `SELECT` queries:

```sql
SELECT 1;
SELECT 2;
SELECT 3;
```

Save the content to the `test.sql` file in the current directory. Then, run the following command to execute the file.


```azurecli-interactive
az postgres flexible-server execute \
    -n server372060240 -u starchylapwing9 -p "dbpassword" -d postgres \
    -f "test.sql"
```

You see an output as shown in the following example:

```output
Running sql file 'test.sql'...
Successfully executed the file.
Closed the connection to server372060240
```

## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](../configure-maintain/how-to-manage-server-portal.md).
- [Quickstart: Use Python to connect and query data from an Azure Database for PostgreSQL](connect-python.md).
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL](connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL](connect-csharp.md).
- [Quickstart: Use Go language to connect and query data from an Azure Database for PostgreSQL](connect-go.md).
- [Quickstart: Use PHP to connect and query data from an Azure Database for PostgreSQL](connect-php.md).
- [Quickstart: Import data from Azure Database for PostgreSQL in Power BI](../integration/connect-with-power-bi-desktop.md).
