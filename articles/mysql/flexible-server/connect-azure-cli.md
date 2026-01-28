---
title: "Quickstart: Connect Using Azure CLI"
description: This quickstart provides several ways to connect with and query Azure Database for MySQL - Flexible Server by using Azure CLI.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-api
  - devx-track-azurecli
  - ai-assistant-test
---

# Quickstart: Connect to Azure Database for MySQL - Flexible Server by using Azure CLI

This quickstart shows how to connect to Azure Database for MySQL Flexible Server by using Azure CLI with `az mysql flexible-server connect`. It also shows how to execute a single query or SQL file by using the `az mysql flexible-server execute` command. This command helps you test connectivity to your database server and run queries. You can also run multiple queries by using the interactive mode.

## Prerequisites

- An Azure account with an active subscription.

[!INCLUDE [flexible-server-free-trial-note](../includes/flexible-server-free-trial-note.md)]

- Install the latest version of [Azure CLI](/cli/azure/install-azure-cli) (2.20.0 or higher).
- Sign in by using Azure CLI with the `az login` command.
- Turn on parameter persistence by using `az config param-persist on`. Parameter persistence helps you use local context without repeating numerous arguments like resource group or location.

## Create a MySQL Flexible Server

First, create a managed Azure Database for MySQL Flexible Server instance. In [Azure Cloud Shell](https://portal.azure.com/#cloudshell), run the following script. Make a note of the **server name**, **username**, and **password** generated from this command.

```azurecli-interactive
az mysql flexible-server create --public-access <your-ip-address>
```

You can provide more arguments for this command to customize it. See all arguments for [az mysql flexible-server create](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-create).

## Create a database

Run the following command to create a database named `newdatabase` if you don't already have one.

```azurecli-interactive
az mysql flexible-server db create -d newdatabase
```

## View all the arguments

You can view all the arguments for this command by using the `--help` argument.

```azurecli-interactive
az mysql flexible-server connect --help
```

## Test database server connection

Run the following script to test and validate the connection to the database from your development environment.

```azurecli-interactive
az mysql flexible-server connect -n <servername> -u <username> -p <password> -d <databasename>
```

**Example**:

```azurecli-interactive
az mysql flexible-server connect -n mysqldemoserver1 -u dbuser -p "dbpassword" -d newdatabase
```

You should see the following output for successful connection:

```output
Command group 'mysql flexible-server' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Connecting to newdatabase database.
Successfully connected to mysqldemoserver1.
```

If the connection failed, try these solutions:

- Check if port 3306 is open on your client machine.
- Check if your server administrator user name and password are correct.
- Check if you configure a firewall rule for your client machine.
- If you configure your server with private access in virtual networking, make sure your client machine is in the same virtual network.

## Run multiple queries by using interactive mode

You can run multiple queries by using the **interactive** mode. To turn on interactive mode, run the following command:

```azurecli-interactive
az mysql flexible-server connect -n <server-name> -u <username> -p <password> --interactive
```

**Example**:

```azurecli-interactive
az mysql flexible-server connect -n mysqldemoserver1 -u dbuser -p "dbpassword" -d newdatabase --interactive
```

**MySQL** shell experience:

```sql
Command group 'mysql flexible-server' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Password:
mysql 5.7.29-log
mycli 1.22.2
Chat: https://gitter.im/dbcli/mycli
Mail: https://groups.google.com/forum/#!forum/mycli-users
Home: http://mycli.net
Thanks to the contributor - Martijn Engler
newdatabase> CREATE TABLE table1 (id int NOT NULL, val int,txt varchar(200));
Query OK, 0 rows affected
Time: 2.290s
newdatabase1> INSERT INTO table1 values (1,100,'text1');
Query OK, 1 row affected
Time: 0.199s
newdatabase1> SELECT * FROM table1;
+----+-----+-------+
| id | val | txt |
| +----+-----+-------+ |
| 1 | 100 | text1 |
| +----+-----+-------+ |
| 1 row in set |
| Time: 0.149s |
| newdatabase>exit; |
Goodbye!
```

## Run single query

Run the following command to execute a single query by using the `--querytext` argument, `-q`.

```azurecli-interactive
az mysql flexible-server execute -n <server-name> -u <username> -p "<password>" -d <database-name> --querytext "<query text>"
```

**Example**:

```azurecli-interactive
az mysql flexible-server execute -n mysqldemoserver1 -u dbuser -p "dbpassword" -d newdatabase -q "select * from table1;" --output table
```

Output:

```output
Command group 'mysql flexible-server' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Successfully connected to mysqldemoserver1.
Ran Database Query: 'select * from table1;'
Retrieving first 30 rows of query output, if applicable.
Closed the connection to mysqldemoserver1
Txt    Val
-----  -----
test   200
test   200
test   200
test   200
test   200
test   200
test   200
```

## Run SQL file

You can run a SQL file by using the `-q` command with the `--file-path` argument.

```azurecli-interactive
az mysql flexible-server execute -n <server-name> -u <username> -p "<password>" -d <database-name> --file-path "<file-path>"
```

**Example**:

```azurecli-interactive
az mysql flexible-server execute -n mysqldemoserver -u dbuser -p "dbpassword" -d flexibleserverdb -f "./test.sql"
```

Output:

```output
Command group 'mysql flexible-server' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Running sql file '.\test.sql'...
Successfully executed the file.
Closed the connection to mysqldemoserver.
```

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](security-tls-how-to-connect.md)
- [Manage Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-server-cli.md)
