---
title: "Quickstart: Connect Using Go"
description: This quickstart provides several Go code samples you can use to connect and query data from Azure Database for MySQL.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc,
  - mode-api
  - devx-track-go
  - linux-related-content
  - sfi-ropc-nochange
ms.devlang: golang
---

# Quickstart: Use Go language to connect and query data in Azure Database for MySQL

This quickstart demonstrates how to connect to an Azure Database for MySQL from Windows, Ubuntu Linux, and Apple macOS platforms using the [Go](https://go.dev/) language. It shows how to use SQL statements to query, insert, update, and delete data in the database. This topic assumes that you're familiar with development using Go and that you're new to working with Azure Database for MySQL.

## Prerequisites

This quickstart uses the resources created in either of these guides as a starting point:

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)

> [!IMPORTANT]  
> We recommend you use a server with **Public access (allowed IP addresses)** enabled for this quickstart. Using a server with **Private access (virtual network integration)** enabled to complete this quickstart might involve extra steps that aren't covered.
>
> Ensure the IP addresses you're connecting from are added the server's firewall rules using [Azure portal](security-how-to-manage-firewall-portal.md) or [Azure CLI](security-how-to-manage-firewall-cli.md).

## Install Go and MySQL connector

Install [Go](https://go.dev/doc/install) and the [go-sql-driver for MySQL](https://github.com/go-sql-driver/mysql#installation) on your own computer. Depending on your platform, follow the steps in the appropriate section:

### [Windows](#tab/windows)

1. [Download](https://go.dev/dl/) and install Go for Microsoft Windows according to the [installation instructions](https://go.dev/doc/install).
1. Launch the command prompt from the start menu.
1. Make a folder for your project, such as `mkdir %USERPROFILE%\go\src\mysqlgo`.
1. Change directory into the project folder, such as `cd %USERPROFILE%\go\src\mysqlgo`.
1. Set the environment variable for GOPATH to point to the source code directory: `set GOPATH=%USERPROFILE%\go`.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init mysqlgo`.
   - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
   - For test command-line apps the `<module_path>` might not refer to an actual location.
1. Install the [go-sql-driver for mysql](https://github.com/go-sql-driver/mysql#installation) by running the `go get github.com/go-sql-driver/mysql` command.

   In summary, install Go, then run these commands in the command prompt:

   ```cmd
   mkdir  %USERPROFILE%\go\src\mysqlgo
   cd %USERPROFILE%\go\src\mysqlgo
   set GOPATH=%USERPROFILE%\go
   go mod init mysqlgo
   go get github.com/go-sql-driver/mysql
   ```

### [Linux (Ubuntu)](#tab/ubuntu)

1. Launch the Bash shell.
1. Install Go by running `sudo apt-get install golang-go`.
1. Make a folder for your project in your home directory, such as `mkdir -p ~/go/src/mysqlgo/`.
1. Change directory into the folder, such as `cd ~/go/src/mysqlgo/`.
1. Set the GOPATH environment variable to point to a valid source directory, such as your current home directory's go folder. At the Bash shell, run `export GOPATH=~/go` to add the `Go` directory as the GOPATH for the current shell session.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init mysqlgo`.
   - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
   - When you're creating a command-line app as a test and won't publish the app, the `<module_path>` doesn't need to refer to an actual location. For example, `mysqlgo`.
1. Install the [go-sql-driver for mysql](https://github.com/go-sql-driver/mysql#installation) by running the `go get github.com/go-sql-driver/mysql` command.

   In summary, run these bash commands:

   ```bash
   sudo apt-get install golang-go git -y
   mkdir -p ~/go/src/mysqlgo/
   cd ~/go/src/mysqlgo/
   export GOPATH=~/go/
   go mod init mysqlgo
   go get github.com/go-sql-driver/mysql
   ```

### [Apple macOS](#tab/macos)

1. Download and install Go according to the [installation instructions](https://go.dev/doc/install) matching your platform.
1. Launch the Bash shell.
1. Make a folder for your project in your home directory, such as `mkdir -p ~/go/src/mysqlgo/`.
1. Change directory into the folder, such as `cd ~/go/src/mysqlgo/`.
1. Set the GOPATH environment variable to point to a valid source directory, such as your current home directory's go folder. At the Bash shell, run `export GOPATH=~/go` to add the go directory as the GOPATH for the current shell session.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init mysqlgo`.
   - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
   - When you're creating a command-line app as a test and won't publish the app, the `<module_path>` doesn't need to refer to an actual location. For example, `mysqlgo`.
1. Install the [go-sql-driver for mysql](https://github.com/go-sql-driver/mysql#installation) by running the `go get github.com/go-sql-driver/mysql` command.

   In summary, install Go, then run these bash commands:

   ```bash
   mkdir -p ~/go/src/mysqlgo/
   cd ~/go/src/mysqlgo/
   export GOPATH=~/go/
   go mod init mysqlgo
   go get github.com/go-sql-driver/mysql
   ```

---

## Get connection information

Get the connection information needed to connect to the Azure Database for MySQL. You need the fully qualified server name and login credentials.

1. Log in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.

## Build and run Go code

1. To write Golang code, you can use a simple text editor, such as Notepad in Microsoft Windows, [`vi`](https://manpages.ubuntu.com/manpages/jammy/man1/nvi.1.html) or [Nano](https://www.nano-editor.org/) in Ubuntu, or TextEdit in macOS. If you prefer a richer Interactive Development Environment (IDE), try [`GoLand`](https://www.jetbrains.com/go/) by `JetBrains`, [Visual Studio Code](https://code.visualstudio.com/) by Microsoft, or [Atom](https://github.blog/news-insights/product-news/sunsetting-atom).
1. Paste the Go code into text files, and then save them into your project folder with file extension \*.go (such as Windows path `%USERPROFILE%\go\src\mysqlgo\createtable.go` or Linux path `~/go/src/mysqlgo/createtable.go`).
1. Locate the `host`, `database`, `user`, and `password` constants in the code, and then replace the example values with your own values. A database named *flexibleserverdb* is created when you create your Azure Database for MySQL server instance. You can use that database or another one.
1. Launch the command prompt or Bash shell. Change directory into your project folder. For example, on Windows `cd %USERPROFILE%\go\src\mysqlgo\`. On Linux `cd ~/go/src/mysqlgo/`. Some of the IDE editors mentioned offer debug and runtime capabilities without requiring shell commands.
1. Compile the application and run it with the command `go run createtable.go`.
1. Alternatively, to build the code into a native application, `go build createtable.go`, then launch `createtable.exe` to run the application.

## Connect, create table, and insert data

Use the following code to connect to the server, create a table, and load the data by using an **INSERT** SQL statement.

The code imports three packages: the [sql package](https://pkg.go.dev/database/sql), the [go sql driver for mysql](https://github.com/go-sql-driver/mysql#installation) as a driver to communicate with the Azure Database for MySQL, and the [fmt package](https://pkg.go.dev/fmt) for printed input and output on the command line.

The code calls method [`sql.Open()`](http://go-database-sql.org/accessing.html) to connect to Azure Database for MySQL, and it checks the connection by using method [`db.Ping()`](https://pkg.go.dev/database/sql#DB.Ping). A [database handle](https://pkg.go.dev/database/sql#DB) is used throughout, holding the connection pool for the database server. The code calls the [`Exec()`](https://pkg.go.dev/database/sql#DB.Exec) method several times to run several DDL commands. The code also uses [`Prepare()`](http://go-database-sql.org/prepared.html) and Exec() to run prepared statements with different parameters to insert three rows. Each time, a custom checkError() method is used to check if an error occurred and panic to exit.

Replace the `host`, `database`, `user`, and `password` constants with your own values.

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

const (
    host     = "mydemoserver.mysql.database.azure.com"
    database = "flexibleserverdb"
    user     = "myadmin"
    password = "yourpassword"
)

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {

    // Initialize connection string.
    var connectionString = fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?allowNativePasswords=true&tls=true", user, password, host, database)

    // Initialize connection object.
    db, err := sql.Open("mysql", connectionString)
    checkError(err)
    defer db.Close()

    err = db.Ping()
    checkError(err)
    fmt.Println("Successfully created connection to database.")

    // Drop previous table of same name if one exists.
    _, err = db.Exec("DROP TABLE IF EXISTS inventory;")
    checkError(err)
    fmt.Println("Finished dropping table (if existed).")

    // Create table.
    _, err = db.Exec("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    checkError(err)
    fmt.Println("Finished creating table.")

    // Insert some data into table.
    sqlStatement, err := db.Prepare("INSERT INTO inventory (name, quantity) VALUES (?, ?);")
    res, err := sqlStatement.Exec("banana", 150)
    checkError(err)
    rowCount, err := res.RowsAffected()
    fmt.Printf("Inserted %d row(s) of data.\n", rowCount)

    res, err = sqlStatement.Exec("orange", 154)
    checkError(err)
    rowCount, err = res.RowsAffected()
    fmt.Printf("Inserted %d row(s) of data.\n", rowCount)

    res, err = sqlStatement.Exec("apple", 100)
    checkError(err)
    rowCount, err = res.RowsAffected()
    fmt.Printf("Inserted %d row(s) of data.\n", rowCount)
    fmt.Println("Done.")
}
```

## Read data

Use the following code to connect and read the data by using a **SELECT** SQL statement.

The code imports three packages: the [sql package](https://pkg.go.dev/database/sql), the [go sql driver for mysql](https://github.com/go-sql-driver/mysql#installation) as a driver to communicate with the Azure Database for MySQL, and the [fmt package](https://pkg.go.dev/fmt) for printed input and output on the command line.

The code calls method [sql.Open()](http://go-database-sql.org/accessing.html) to connect to Azure Database for MySQL, and checks the connection using method [db.Ping()](https://pkg.go.dev/database/sql#DB.Ping). A [database handle](https://pkg.go.dev/database/sql#DB) is used throughout, holding the connection pool for the database server. The code calls the [Query()](https://pkg.go.dev/database/sql#DB.Query) method to run the select command. Then it runs [Next()](https://pkg.go.dev/database/sql#Rows.Next) to iterate through the result set and [Scan()](https://pkg.go.dev/database/sql#Rows.Scan) to parse the column values, saving the value into variables. Each time a custom checkError() method is used to check if an error occurred and panic to exit.

Replace the `host`, `database`, `user`, and `password` constants with your own values.

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

const (
    host     = "mydemoserver.mysql.database.azure.com"
    database = "flexibleserverdb"
    user     = "myadmin"
    password = "yourpassword"
)

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {

    // Initialize connection string.
    var connectionString = fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?allowNativePasswords=true&tls=true", user, password, host, database)

    // Initialize connection object.
    db, err := sql.Open("mysql", connectionString)
    checkError(err)
    defer db.Close()

    err = db.Ping()
    checkError(err)
    fmt.Println("Successfully created connection to database.")

    // Variables for printing column data when scanned.
    var (
        id       int
        name     string
        quantity int
    )

    // Read some data from the table.
    rows, err := db.Query("SELECT id, name, quantity from inventory;")
    checkError(err)
    defer rows.Close()
    fmt.Println("Reading data:")
    for rows.Next() {
        err := rows.Scan(&id, &name, &quantity)
        checkError(err)
        fmt.Printf("Data row = (%d, %s, %d)\n", id, name, quantity)
    }
    err = rows.Err()
    checkError(err)
    fmt.Println("Done.")
}
```

## Update data

Use the following code to connect and update the data using a **UPDATE** SQL statement.

The code imports three packages: the [sql package](https://pkg.go.dev/database/sql), the [go sql driver for mysql](https://github.com/go-sql-driver/mysql#installation) as a driver to communicate with the Azure Database for MySQL, and the [fmt package](https://pkg.go.dev/fmt) for printed input and output on the command line.

The code calls method [sql.Open()](http://go-database-sql.org/accessing.html) to connect to Azure Database for MySQL, and checks the connection using method [db.Ping()](https://pkg.go.dev/database/sql#DB.Ping). A [database handle](https://pkg.go.dev/database/sql#DB) is used throughout, holding the connection pool for the database server. The code calls the [Exec()](https://pkg.go.dev/database/sql#DB.Exec) method to run the update command. Each time a custom checkError() method is used to check if an error occurred and panic to exit.

Replace the `host`, `database`, `user`, and `password` constants with your own values.

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

const (
    host     = "mydemoserver.mysql.database.azure.com"
    database = "flexibleserverdb"
    user     = "myadmin"
    password = "yourpassword"
)

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {

    // Initialize connection string.
    var connectionString = fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?allowNativePasswords=true&tls=true", user, password, host, database)

    // Initialize connection object.
    db, err := sql.Open("mysql", connectionString)
    checkError(err)
    defer db.Close()

    err = db.Ping()
    checkError(err)
    fmt.Println("Successfully created connection to database.")

    // Modify some data in table.
    rows, err := db.Exec("UPDATE inventory SET quantity = ? WHERE name = ?", 200, "banana")
    checkError(err)
    rowCount, err := rows.RowsAffected()
    fmt.Printf("Updated %d row(s) of data.\n", rowCount)
    fmt.Println("Done.")
}
```

## Delete data

Use the following code to connect and remove data using a **DELETE** SQL statement.

The code imports three packages: the [sql package](https://pkg.go.dev/database/sql), the [go sql driver for mysql](https://github.com/go-sql-driver/mysql#installation) as a driver to communicate with the Azure Database for MySQL, and the [fmt package](https://pkg.go.dev/fmt) for printed input and output on the command line.

The code calls method [sql.Open()](http://go-database-sql.org/accessing.html) to connect to Azure Database for MySQL, and checks the connection using method [db.Ping()](https://pkg.go.dev/database/sql#DB.Ping). A [database handle](https://pkg.go.dev/database/sql#DB) is used throughout, holding the connection pool for the database server. The code calls the [Exec()](https://pkg.go.dev/database/sql#DB.Exec) method to run the delete command. Each time a custom checkError() method is used to check if an error occurred and panic to exit.

Replace the `host`, `database`, `user`, and `password` constants with your own values.

```go
package main

import (
    "database/sql"
    "fmt"
    _ "github.com/go-sql-driver/mysql"
)

const (
    host     = "mydemoserver.mysql.database.azure.com"
    database = "flexibleserverdb"
    user     = "myadmin"
    password = "yourpassword"
)

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {

    // Initialize connection string.
    var connectionString = fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?allowNativePasswords=true&tls=true", user, password, host, database)

    // Initialize connection object.
    db, err := sql.Open("mysql", connectionString)
    checkError(err)
    defer db.Close()

    err = db.Ping()
    checkError(err)
    fmt.Println("Successfully created connection to database.")

    // Modify some data in table.
    rows, err := db.Exec("DELETE FROM inventory WHERE name = ?", "orange")
    checkError(err)
    rowCount, err := rows.RowsAffected()
    fmt.Printf("Deleted %d row(s) of data.\n", rowCount)
    fmt.Println("Done.")
}
```

## Clean up resources

To clean up all resources used during this quickstart, delete the resource group using the following command:

```azurecli-interactive
az group delete \
    --name $AZ_RESOURCE_GROUP \
    --yes
```

## Next step

> [!div class="nextstepaction"]
> [Migrate your Azure Database for MySQL - Flexible Server database by using import and export](concepts-migrate-import-export.md)
