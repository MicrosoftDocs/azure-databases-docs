---
title: "Quickstart: Connect with PHP - Flexible Server"
description: This quickstart provides a PHP code sample you can use to connect and query data from Azure Database for PostgreSQL.
author: agapovm
ms.author: maximagapov
ms.reviewer: maghan
ms.date: 10/12/2024
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.devlang: php
ms.custom: sfi-ropc-nochange
---

# Quickstart: Use PHP to connect and query data in Azure Database for PostgreSQL 

This quickstart demonstrates connecting to an Azure Database for PostgreSQL using a [PHP](https://www.php.net/) application. It shows how to use SQL statements to query, insert, update, and delete data in the database. The steps in this article assume that you're familiar with developing using PHP and are new to working with Azure Database for PostgreSQL.

## Prerequisites

This quickstart uses the resources created in the [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md) as a starting point.

## Install PHP

Install PHP on your server, or create an Azure [web app](/azure/app-service/overview) that includes PHP.

### Windows

- Download [PHP 7.1.4 nonthread safe (x64) version](https://windows.php.net/download#php-7.1)
- Install PHP and refer to the [PHP manual](https://secure.php.net/manual/install.windows.php) for further configuration
- The code uses the **pgsql** class (ext/php_pgsql.dll) that is included in the PHP installation.
- Enabled the **pgsql** extension by editing the php.ini configuration file, typically located at `C:\Program Files\PHP\v7.1\php.ini`. The configuration file should contain a line with the text `extension=php_pgsql.so`. If it isn't shown, add the text and save the file. If the text is present but commented with a semicolon prefix, uncomment the text by removing the semicolon.

### Linux (Ubuntu)

- Download [PHP 7.1.4 nonthread safe (x64) version](https://secure.php.net/downloads.php)
- Install PHP and refer to the [PHP manual](https://secure.php.net/manual/install.unix.php) for further configuration
- The code uses the **pgsql** class (php_pgsql.so). Install it by running `sudo apt-get install php-pgsql`.
- Enabled the **pgsql** extension by editing the `/etc/php/7.0/mods-available/pgsql.ini` configuration file. The configuration file should contain a line with the text `extension=php_pgsql.so`. If it isn't shown, add the text and save the file. If the text is present but commented with a semicolon prefix, uncomment the text by removing the semicolon.

### macOS

- Download [PHP 7.1.4 version](https://secure.php.net/downloads.php)
- Install PHP and refer to the [PHP manual](https://secure.php.net/manual/install.macosx.php) for further configuration

## Get connection information

Get the connection information needed to connect to the Azure Database for PostgreSQL. You need the fully qualified server name and login credentials.

1. Log in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in the Azure portal, select **All resources**, then search for your created server (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.


## Connect and create a table

Use the following code to connect and create a table using **CREATE TABLE** SQL statement, followed by **INSERT INTO** SQL statements to add rows to the table.

The code call method [pg_connect()](https://secure.php.net/manual/en/function.pg-connect.php) is used to connect to the Azure Database for PostgreSQL. Then, it calls the method -  
[pg_query()](https://secure.php.net/manual/en/function.pg-query.php) - several times to run several commands, and [pg_last_error()](https://secure.php.net/manual/en/function.pg-last-error.php) to check the details if an error occurred each time. Then, it calls method [pg_close()](https://secure.php.net/manual/en/function.pg-close.php) to close the connection.

Replace the `$host`, `$database`, `$user`, and `$password` parameters with your values.

```php
<?php
    // Initialize connection variables.
 $host = "mydemoserver.postgres.database.azure.com";
 $database = "mypgsqldb";
 $user = "mylogin@mydemoserver";
 $password = "<server_admin_password>";

    // Initialize connection object.
 $connection = pg_connect("host=$host dbname=$database user=$user password=$password")
        or die("Failed to create connection to database: ". pg_last_error(). "<br/>");
    print "Successfully created a connection to the database.<br/>";

    // Drop the previous table of the same name if one exists.
 $query = "DROP TABLE IF EXISTS inventory;";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). "<br/>");
    print "Finished dropping table (if existed).<br/>";

    // Create table.
 $query = "CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). "<br/>");
    print "Finished creating table.<br/>";

    // Insert some data into the table.
 $name = '\'banana\'';
 $quantity = 150;
 $query = "INSERT INTO inventory (name, quantity) VALUES ($name, $quantity);";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). "<br/>");

 $name = '\'orange\'';
 $quantity = 154;
 $query = "INSERT INTO inventory (name, quantity) VALUES ($name, $quantity);";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). "<br/>");

 $name = '\'apple\'';
 $quantity = 100;
 $query = "INSERT INTO inventory (name, quantity) VALUES ($name, $quantity);";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error()). "<br/>";

    print "Inserted 3 rows of data.<br/>";

    // Closing connection
    pg_close($connection);
?>
```

## Read data

Use the following code to connect and read the data using a **SELECT** SQL statement.

The code call method [pg_connect()](https://secure.php.net/manual/en/function.pg-connect.php) is used to connect to the Azure Database for PostgreSQL. Then it calls method [pg_query()](https://secure.php.net/manual/en/function.pg-query.php) to run the SELECT command, keeping the results in a result set, and [pg_last_error()](https://secure.php.net/manual/en/function.pg-last-error.php) to check the details if an error occurred. To read the result set, method [pg_fetch_row()](https://secure.php.net/manual/en/function.pg-fetch-row.php) is called in a loop, once per row, and the row data is retrieved in an array `$row`, with one data value per column in each array position. To free the result set, method [pg_free_result()](https://secure.php.net/manual/en/function.pg-free-result.php) is called. Then it calls method [pg_close()](https://secure.php.net/manual/en/function.pg-close.php) to close the connection.

Replace the `$host`, `$database`, `$user`, and `$password` parameters with your values.

```php
<?php
    // Initialize connection variables.
 $host = "mydemoserver.postgres.database.azure.com";
 $database = "mypgsqldb";
 $user = "mylogin@mydemoserver";
 $password = "<server_admin_password>";

    // Initialize connection object.
 $connection = pg_connect("host=$host dbname=$database user=$user password=$password")
                or die("Failed to create connection to database: ". pg_last_error(). "<br/>");

    print "Successfully created a connection to the database. <br/>";

    // Perform some SQL queries over the connection.
 $query = "SELECT * from inventory";
 $result_set = pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). "<br/>");
    while ($row = pg_fetch_row($result_set))
 {
        print "Data row = ($row[0], $row[1], $row[2]). <br/>";
 }

    // Free result_set
    pg_free_result($result_set);

    // Closing connection
    pg_close($connection);
?>
```

## Update data

Use the following code to connect and update the data using a **UPDATE** SQL statement.

The code call method [pg_connect()](https://secure.php.net/manual/en/function.pg-connect.php) is used to connect to the Azure Database for PostgreSQL. Then it calls method [pg_query()](https://secure.php.net/manual/en/function.pg-query.php) to run a command, and [pg_last_error()](https://secure.php.net/manual/en/function.pg-last-error.php) to check the details if an error occurred. Then it calls method [pg_close()](https://secure.php.net/manual/en/function.pg-close.php) to close the connection.

Replace the `$host`, `$database`, `$user`, and `$password` parameters with your values.

```php
<?php
    // Initialize connection variables.
 $host = "mydemoserver.postgres.database.azure.com";
 $database = "mypgsqldb";
 $user = "mylogin@mydemoserver";
 $password = "<server_admin_password>";

    // Initialize connection object.
 $connection = pg_connect("host=$host dbname=$database user=$user password=$password")
                or die("Failed to create connection to database: ". pg_last_error(). ".<br/>");

    Print "Successfully created a connection to the database. <br/>";

    // Modify some data in a table.
 $new_quantity = 200;
 $name = '\'banana\'';
 $query = "UPDATE inventory SET quantity = $new_quantity WHERE name = $name;";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). ".<br/>");
    print "Updated 1 row of data. </br>";

    // Closing connection
    pg_close($connection);
?>
```

## Delete data

Use the following code to connect and read the data using a **DELETE** SQL statement.

The code call method [pg_connect()](https://secure.php.net/manual/en/function.pg-connect.php) is used to connect to the Azure Database for PostgreSQL. Then it calls method [pg_query()](https://secure.php.net/manual/en/function.pg-query.php) to run a command, and [pg_last_error()](https://secure.php.net/manual/en/function.pg-last-error.php) to check the details if an error occurred. Then it calls method [pg_close()](https://secure.php.net/manual/en/function.pg-close.php) to close the connection.

Replace the `$host`, `$database`, `$user`, and `$password` parameters with your values.

```php
<?php
    // Initialize connection variables.
 $host = "mydemoserver.postgres.database.azure.com";
 $database = "mypgsqldb";
 $user = "mylogin@mydemoserver";
 $password = "<server_admin_password>";

    // Initialize connection object.
 $connection = pg_connect("host=$host dbname=$database user=$user password=$password")
            or die("Failed to create connection to database: ". pg_last_error(). ". </br>");

    print "Successfully created a connection to the database. <br/>";

    // Delete some data from a table.
 $name = '\'orange\'';
 $query = "DELETE FROM inventory WHERE name = $name;";
    pg_query($connection, $query)
        or die("Encountered an error when executing given sql statement: ". pg_last_error(). ". <br/>");
    print "Deleted 1 row of data. <br/>";

    // Closing connection
    pg_close($connection);
?>
```

## Clean up resources

To clean up all resources used during this quickstart, delete the resource group using the following command:

```azurecli-interactive
az group delete \
 --name $AZ_RESOURCE_GROUP \
 --yes
```

## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](../configure-maintain/how-to-manage-server-portal.md).
- [Quickstart: Use Python to connect and query data from an Azure Database for PostgreSQL](connect-python.md).
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL](connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL](connect-csharp.md).
- [Quickstart: Use Go language to connect and query data from an Azure Database for PostgreSQL](connect-go.md).
- [Quickstart: Use Azure CLI to connect and query data from an Azure Database for PostgreSQL](connect-azure-cli.md).
- [Quickstart: Import data from Azure Database for PostgreSQL in Power BI](../integration/connect-with-power-bi-desktop.md).
