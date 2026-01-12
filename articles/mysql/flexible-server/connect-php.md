---
title: "Quickstart: Connect Using PHP"
description: This quickstart provides several PHP code samples you can use to connect and query data from Azure Database for MySQL - Flexible Server.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-other
---

# Use PHP with Azure Database for MySQL - Flexible Server

This quickstart demonstrates how to connect to Azure Database for MySQL Flexible Server using a [PHP](https://www.php.net/) application. It shows how to use SQL statements to query, insert, update, and delete data in the database. This article assumes that you're familiar with development using PHP and that you're new to working with Azure Database for MySQL Flexible Server.

## Prerequisites

This quickstart uses the resources created in either of these guides as a starting point:

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)

<a id="preparing-your-client-workstation"></a>

## Prepare your client workstation

- If you created your flexible server with *Private access (virtual network Integration)*, you need to connect to your server from a resource within the same virtual network as your server. You can create a virtual machine and add it to the virtual network created with your flexible server. Refer to [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md).
- If you created your flexible server with *Public access (allowed IP addresses)*, you can add your local IP address to the list of firewall rules on your server. Refer to [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](security-how-to-manage-firewall-cli.md).

### Install PHP

Install PHP on your own server, or create an Azure [web app](/azure/app-service/overview) that includes PHP. For more information, see [create and manage firewall rules](security-how-to-manage-firewall-portal.md).

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

Get the connection information needed to connect to the Azure Database for MySQL Flexible Server instance. You need the fully qualified server name and sign in credentials.

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you created (in the following examples, replace `<server>` with a valid value).

1. Select the server name.

1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.

<a id="connecting-to-flexible-server-using-tlsssl-in-php"></a>

## Connect to flexible server using TLS/SSL in PHP

To establish an encrypted connection to your flexible server over TLS/SSL from your application, refer to the following code samples. You can download the certificate needed to communicate over TLS/SSL from [https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem).

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$conn = mysqli_init();
mysqli_ssl_set(
    $conn,
    null,
    null,
    "/var/www/html/DigiCertGlobalRootCA.crt.pem",
    null,
    null
);
mysqli_real_connect(
    $conn,
    "<server>.mysql.database.azure.com",
    "<username>",
    "<password>",
    "<database>",
    3306,
    MYSQLI_CLIENT_SSL
);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}
?>
```

## Connect and create a table

Use the following code to connect and create a table by using `CREATE TABLE` SQL statement.

The code uses the **MySQL Improved extension** (`mysqli`) class included in PHP. The code calls methods [mysqli_init](https://www.php.net/manual/en/mysqli.init.php) and [mysqli_real_connect](https://www.php.net/manual/en/mysqli.real-connect.php) to connect to MySQL. Then it calls method [mysqli_query](https://www.php.net/manual/en/mysqli.query.php) to run the query. Then it calls method [mysqli_close](https://www.php.net/manual/en/mysqli.close.php) to close the connection.

You can also connect to Azure Database for MySQL using the object-oriented interface provided by the `mysqli` extension.

#### [Procedural](#tab/procedural-create-table)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}

// Run the create table query
if (
    mysqli_query(
        $conn,
        '
CREATE TABLE Products (
`Id` INT NOT NULL AUTO_INCREMENT ,
`ProductName` VARCHAR(200) NOT NULL ,
`Color` VARCHAR(50) NOT NULL ,
`Price` DOUBLE NOT NULL ,
PRIMARY KEY (`Id`)
);
'
    )
) {
    printf("Table created\n");
}

//Close the connection
mysqli_close($conn);
?>
```

#### [Object oriented](#tab/object-oriented-create-table)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();

$conn = new mysqli($host, $username, $password, $db_name, 3306);

if ($conn->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
} else {
    $query = "CREATE TABLE Products (
        Id INT NOT NULL AUTO_INCREMENT,
        ProductName VARCHAR(200) NOT NULL,
        Color VARCHAR(50) NOT NULL,
        Price DOUBLE NOT NULL,
        PRIMARY KEY (Id)
    )";

    if ($conn->query($query) === true) {
        echo "Table created successfully. <br/>";
    } else {
        echo "Error creating table: " . $conn->error;
    }
}
$stmt->close();
$conn->close();
?>
```

---

## Insert data

Use the following code to connect and insert data by using an `INSERT` SQL statement.

The code uses the **MySQL Improved extension** (`mysqli`) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared insert statement, then binds the parameters for each inserted column value using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

You can also connect to Azure Database for MySQL using the object-oriented interface provided by the `mysqli` extension.

#### [Procedural](#tab/procedural-insert)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}

//Create an Insert prepared statement and run it
$product_name = "BrandNewProduct";
$product_color = "Blue";
$product_price = 15.5;
if (
    $stmt = mysqli_prepare(
        $conn,
        "INSERT INTO Products (ProductName, Color, Price) VALUES (?, ?, ?)"
    )
) {
    mysqli_stmt_bind_param(
        $stmt,
        "ssd",
        $product_name,
        $product_color,
        $product_price
    );
    mysqli_stmt_execute($stmt);
    printf("Insert: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));
    mysqli_stmt_close($stmt);
}

// Close the connection
mysqli_close($conn);
?>
```

#### [Object oriented](#tab/object-oriented-insert)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();

$conn = new mysqli($host, $username, $password, $db_name, 3306);

if ($conn->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
} else {
    echo "Connected to MySQL successfully.  <br/>";
    $product_name = "BrandNewProduct";
    $product_color = "Blue";
    $product_price = 15.5;

    $query =
        "INSERT INTO Products (ProductName, Color, Price) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($query);

    $stmt->bind_param("ssd", $product_name, $product_color, $product_price);

    if ($stmt->execute()) {
        echo "registration successful <br/>";
        printf("Insert: Affected %d rows\n", $stmt->affected_rows);
    } else {
        echo "registration failed";
    }
}
$stmt->close();
$conn->close();
?>
```

---

## Read data

Use the following code to connect and read the data by using a `SELECT` SQL statement. The code uses the **MySQL Improved extension** (`mysqli`) class included in PHP. The code uses method [mysqli_query](https://www.php.net/manual/en/mysqli.query.php) perform the sql query and method [mysqli_fetch_assoc](https://www.php.net/manual/en/mysqli-result.fetch-assoc.php) to fetch the resulting rows.

You can also connect to Azure Database for MySQL using the object-oriented interface provided by the `mysqli` extension.

#### [Procedural](#tab/procedural-read)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}

//Run the Select query
printf("Reading data from table: \n");
$res = mysqli_query($conn, "SELECT * FROM Products");
while ($row = mysqli_fetch_assoc($res)) {
    var_dump($row);
}

//Close the connection
mysqli_close($conn);
?>
```

#### [Object oriented](#tab/object-oriented-read)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();

$conn = new mysqli($host, $username, $password, $db_name, 3306);

if ($conn->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
} else {
    $query = "SELECT * FROM Products";
    $stmt = $conn->query($query);

    if ($stmt->num_rows > 0) {
        // output data of each row
        while ($row = $stmt->fetch_assoc()) {
            echo "id: " .
                $row["Id"] .
                " - ProductName: " .
                $row["ProductName"] .
                " -Color " .
                $row["Color"] .
                " -Price " .
                $row["Price"] .
                "<br>";
        }
    } else {
        echo "0 results";
    }
}
$stmt->close();
$conn->close();
?>
```

---

## Update data

Use the following code to connect and update the data by using an `UPDATE` SQL statement.

The code uses the **MySQL Improved extension** (`mysqli`) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared update statement, then binds the parameters for each updated column value using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

You can also connect to Azure Database for MySQL using the object-oriented interface provided by the `mysqli` extension.

#### [Procedural](#tab/procedural-update)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}

//Run the Update statement
$product_name = "BrandNewProduct";
$new_product_price = 15.1;
if (
    $stmt = mysqli_prepare(
        $conn,
        "UPDATE Products SET Price = ? WHERE ProductName = ?"
    )
) {
    mysqli_stmt_bind_param($stmt, "ds", $new_product_price, $product_name);
    mysqli_stmt_execute($stmt);
    printf("Update: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));

    //Close the connection
    mysqli_stmt_close($stmt);
}

mysqli_close($conn);

?>
```

#### [Object oriented](#tab/object-oriented-update)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();

$conn = new mysqli($host, $username, $password, $db_name, 3306);

if ($conn->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
} else {
    $product_name = "BrandNewProduct";
    $new_product_price = 15.1;

    $query = "UPDATE Products SET Price = ? WHERE ProductName = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ds", $new_product_price, $product_name);
    if ($stmt->execute()) {
        echo "update successful <br/>";
        printf("Updated: Affected %d rows\n", $stmt->affected_rows);
    } else {
        echo "registration failed";
    }
}
$stmt->close();
$conn->close();
?>
```

---

## Delete data

Use the following code to connect and read the data by using a `DELETE` SQL statement.

The code uses the **MySQL Improved extension** (`mysqli`) class included in PHP. The code uses method [mysqli_prepare](https://www.php.net/manual/en/mysqli.prepare.php) to create a prepared delete statement, then binds the parameters for the where clause in the statement using method [mysqli_stmt_bind_param](https://www.php.net/manual/en/mysqli-stmt.bind-param.php). The code runs the statement by using method [mysqli_stmt_execute](https://www.php.net/manual/en/mysqli-stmt.execute.php) and afterwards closes the statement by using method [mysqli_stmt_close](https://www.php.net/manual/en/mysqli-stmt.close.php).

You can also connect to Azure Database for MySQL using the object-oriented interface provided by the `mysqli` extension.

#### [Procedural](#tab/procedural-delete)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();
mysqli_real_connect($conn, $host, $username, $password, $db_name, 3306);
if (mysqli_connect_errno($conn)) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}

//Run the Delete statement
$product_name = "BrandNewProduct";
if (
    $stmt = mysqli_prepare($conn, "DELETE FROM Products WHERE ProductName = ?")
) {
    mysqli_stmt_bind_param($stmt, "s", $product_name);
    mysqli_stmt_execute($stmt);
    printf("Delete: Affected %d rows\n", mysqli_stmt_affected_rows($stmt));
    mysqli_stmt_close($stmt);
}

//Close the connection
mysqli_close($conn);
?>
```

#### [Object oriented](#tab/object-oriented-delete)

Replace the `$host`, `$username`, `$password`, and `$db_name` parameters with your own values.

```php
<?php
$host = "<server>.mysql.database.azure.com";
$username = "<username>";
$password = "<password>";
$db_name = "<database>";

//Establishes the connection
$conn = mysqli_init();

$conn = new mysqli($host, $username, $password, $db_name, 3306);

if ($conn->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
} else {
    $product_name = "BrandNewProduct";

    $query = "DELETE FROM Products WHERE ProductName = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("s", $product_name);

    if ($stmt->execute()) {
        echo "Delete successful <br/>";
        printf("Delete: Affected %d rows\n", $stmt->affected_rows);
    } else {
        echo "Delete failed";
    }
}
$stmt->close();
$conn->close();
?>
```

---

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](security-tls-how-to-connect.md)
- [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](security-how-to-manage-firewall-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
