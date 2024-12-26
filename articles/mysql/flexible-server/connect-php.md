---
title: "Quickstart: Connect Using PHP"
description: This quickstart provides several PHP code samples you can use to connect and query data from Azure Database for MySQL - Flexible Server.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-other
---

# Use PHP with Azure Database for MySQL - Flexible Server

This quickstart demonstrates how to connect to Azure Database for MySQL flexible server using a [PHP](https://www.php.net/) application. It shows how to use SQL statements to query, insert, update, and delete data in the database. This article assumes that you're familiar with development using PHP and that you're new to working with Azure Database for MySQL flexible server.

## Prerequisites

This quickstart uses the resources created in either of these guides as a starting point:

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)

<a id="preparing-your-client-workstation"></a>

## Prepare your client workstation

1. If you created your flexible server with *Private access (virtual network Integration)*, you'll need to connect to your server from a resource within the same virtual network as your server. You can create a virtual machine and add it to the virtual network created with your flexible server. Refer to [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md).

1. If you created your flexible server with *Public access (allowed IP addresses)*, you can add your local IP address to the list of firewall rules on your server. Refer to [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](how-to-manage-firewall-cli.md).

### Install PHP

Install PHP on your own server, or create an Azure [web app](/azure/app-service/overview) that includes PHP. Refer to [create and manage firewall rules](how-to-manage-firewall-portal.md) to learn how to create firewall rules.

#### [macOS](#tab/macos)

1. Download [PHP 7.1.4 version](https://www.php.net/downloads.php).
1. Install PHP and refer to the [PHP manual](https://www.php.net/manual/en/install.macosx.php) for further configuration.

#### [Linux](#tab/linux)

1. Download [PHP 7.1.4 nonthread safe (x64) version](https://www.php.net/downloads.php).
1. Install PHP and refer to the [PHP manual](https://www.php.net/manual/en/install.unix.php) for further configuration.

#### [Windows](#tab/windows)

1. Download [PHP 7.1.4 nonthread safe (x64) version](https://windows.php.net/download#php-7.1).
1. Install PHP and refer to the [PHP manual](https://www.php.net/manual/en/install.windows.php) for further configuration.

---

## Get connection information

Get the connection information needed to connect to the Azure Database for MySQL flexible server instance. You need the fully qualified server name and sign in credentials.

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you have created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.
<!------>

<a id="connecting-to-flexible-server-using-tlsssl-in-php"></a>

## Connect to flexible server using TLS/SSL in PHP

To establish an encrypted connection to your flexible server over TLS/SSL from your application, refer to the following code samples. You can download the certificate needed to communicate over TLS/SSL from [https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem)

```powershell
$conn = mysqli_init();
mysqli_ssl_set($conn,NULL,NULL, "/var/www/html/DigiCertGlobalRootCA.crt.pem", NULL, NULL);
mysqli_real_connect($conn, 'mydemoserver.mysql.database.azure.com', 'myadmin', 'yourpassword', 'quickstartdb', 3306, MYSQLI_CLIENT_SSL);
if (mysqli_connect_errno($conn)) {
die('Failed to connect to MySQL: '.mysqli_connect_error());
}
```

## Connect and create a table

Use the following code to connect and create a table by using **CREATE TABLE** SQL statement.

The code uses the **MySQL Improved extension** (mysqli) class included in PHP. The code calls methods [mysqli_init](https://www.php.net/manual/en/mysqli.init.php) and [mysqli_real_connect](https://www.php.net/manual/en/mysqli.real-connect.php) to connect to MySQL. Then it calls method [mysqli_query](https://www.php.net/manual/en/mysqli.query.php) to run the query. Then it calls method [mysqli_close](https://www.php.net/manual/en/mysqli.close.php) to close the connection.

Replace the host, username, password, and db_name parameters with your own values.

```php
<?php
$host = 'mydemoserver.mysql.database.azure.com';
$username = 'myadmin';
$password = 'your_password';
$db_name = 'your_database';

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
die('Failed to connect to MySQL: '.mysqli_connect_error());
}

// Run the create table query
if (mysqli_query($conn, '
CREATE TABLE Products (
`Id` INT NOT NULL AUTO_INCREMENT ,
`ProductName` VARCHAR(200) NOT NULL ,
`Color` VARCHAR(50) NOT NULL ,
`Price` DOUBLE NOT NULL ,
PRIMARY KEY (`Id`)
);
')) {
printf("Table created\n");
}

//Close the connection
mysqli_close($conn);
?>
```

## Insert data

Use the following code to connect and insert data by using an **INSERT** SQL statement.

The code uses the **MySQL Improved extension** (mysqli) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared insert statement, then binds the parameters for each inserted column value using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

Replace the host, username, password, and db_name parameters with your own values.

```php
<?php
$host = 'mydemoserver.mysql.database.azure.com';
$username = 'myadmin';
$password = 'your_password';
$db_name = 'your_database';

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {f
die('Failed to connect to MySQL: '.mysqli_connect_error());
}

//Create an Insert prepared statement and run it
$product_name = 'BrandNewProduct';
$product_color = 'Blue';
$product_price = 15.5;
if ($stmt = mysqli_prepare($conn, "INSERT INTO Products (ProductName, Color, Price) VALUES (?, ?, ?)")) {
mysqli_stmt_bind_param($stmt, 'ssd', $product_name, $product_color, $product_price);
mysqli_stmt_execute($stmt);
printf("Insert: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));
mysqli_stmt_close($stmt);
}

// Close the connection
mysqli_close($conn);
?>
```

## Read data

Use the following code to connect and read the data by using a **SELECT** SQL statement. The code uses the **MySQL Improved extension** (mysqli) class included in PHP. The code uses method [mysqli_query](https://www.php.net/manual/en/mysqli.query.php) perform the sql query and method [mysqli_fetch_assoc](https://www.php.net/manual/en/mysqli-result.fetch-assoc.php) to fetch the resulting rows.

Replace the host, username, password, and db_name parameters with your own values.

```php
<?php
$host = 'mydemoserver.mysql.database.azure.com';
$username = 'myadmin';
$password = 'your_password';
$db_name = 'your_database';

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
die('Failed to connect to MySQL: '.mysqli_connect_error());
}

//Run the Select query
printf("Reading data from table: \n");
$res = mysqli_query($conn, 'SELECT * FROM Products');
while ($row = mysqli_fetch_assoc($res)) {
var_dump($row);
}

//Close the connection
mysqli_close($conn);
?>
```

## Update data

Use the following code to connect and update the data by using an **UPDATE** SQL statement.

The code uses the **MySQL Improved extension** (mysqli) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared update statement, then binds the parameters for each updated column value using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

Replace the host, username, password, and db_name parameters with your own values.

```php
<?php
$host = 'mydemoserver.mysql.database.azure.com';
$username = 'myadmin';
$password = 'your_password';
$db_name = 'your_database';

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
die('Failed to connect to MySQL: '.mysqli_connect_error());
}

//Run the Update statement
$product_name = 'BrandNewProduct';
$new_product_price = 15.1;
if ($stmt = mysqli_prepare($conn, "UPDATE Products SET Price = ? WHERE ProductName = ?")) {
mysqli_stmt_bind_param($stmt, 'ds', $new_product_price, $product_name);
mysqli_stmt_execute($stmt);
printf("Update: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));

//Close the connection
mysqli_stmt_close($stmt);
}

mysqli_close($conn);
?>
```

## Delete data

Use the following code to connect and read the data by using a **DELETE** SQL statement.

The code uses the **MySQL Improved extension** (mysqli) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared delete statement, then binds the parameters for the where clause in the statement using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

Replace the host, username, password, and db_name parameters with your own values.

```php
<?php
$host = 'mydemoserver.mysql.database.azure.com';
$username = 'myadmin';
$password = 'your_password';
$db_name = 'your_database';

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
die('Failed to connect to MySQL: '.mysqli_connect_error());
}

//Run the Delete statement
$product_name = 'BrandNewProduct';
if ($stmt = mysqli_prepare($conn, "DELETE FROM Products WHERE ProductName = ?")) {
mysqli_stmt_bind_param($stmt, 's', $product_name);
mysqli_stmt_execute($stmt);
printf("Delete: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));
mysqli_stmt_close($stmt);
}

//Close the connection
mysqli_close($conn);
?>
```

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
- [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-firewall-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
