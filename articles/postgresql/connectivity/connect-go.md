---
title: 'Quickstart: Connect using Go'
description: This quickstart provides a Go programming language sample you can use to connect and query data from an Azure Database for PostgreSQL flexible server instance.
author: agapovm
ms.author: maximagapov
ms.reviewer: maghan
ms.date: 09/04/2024
ms.service: azure-database-postgresql
ms.topic: quickstart
ms.custom:
- mvc
- mode-api
- devx-track-go
- sfi-ropc-blocked
ms.devlang: golang
---

# Quickstart: Use Go language to connect and query data in Azure Database for PostgreSQL 

This quickstart demonstrates how to connect to an Azure Database for PostgreSQL using code written in the [Go](https://go.dev/) language (golang). It shows how to use SQL statements to query, insert, update, and delete data in the database. This article assumes you are familiar with development using Go, but that you are new to working with Azure Database for PostgreSQL.

## Prerequisites

This quickstart uses the resources created in the [Create an Azure Database for PostgreSQL](../configure-maintain/quickstart-create-server.md) as a starting point.

> [!IMPORTANT]
> We recommend you use a server with **Public access (allowed IP addresses)** enabled for this quickstart. Using a server with **Private access (VNet Integration)** enabled to complete this quickstart might involve extra steps that aren't covered.
>
> Ensure the IP address you're connecting from has been added the server's firewall rules using the [Azure portal](../network/how-to-networking.md) or [Azure CLI](../network/how-to-networking.md).

## Install Go and pq connector

Install [Go](https://go.dev/doc/install) and the [Pure Go Postgres driver (pq)](https://github.com/lib/pq) on your own machine. Depending on your platform, follow the appropriate steps:

### [Windows](#tab/windows)

1. [Download](https://go.dev/dl/) and install Go for Microsoft Windows according to the [installation instructions](https://go.dev/doc/install).
1. Launch the command prompt from the start menu.
1. Make a folder for your project, such as `mkdir  %USERPROFILE%\go\src\postgresqlgo`.
1. Change directory into the project folder, such as `cd %USERPROFILE%\go\src\postgresqlgo`.
1. Set the environment variable for GOPATH to point to the source code directory. `set GOPATH=%USERPROFILE%\go`.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init postgresqlgo`.
    - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
    - When you're creating a command-line app as a test and won't publish the app, the `<module_path>` doesn't need to refer to an actual location. For example, `postgresqlgo`.
1. Install the [Pure Go Postgres driver (pq)](https://github.com/lib/pq) by running the `go get github.com/lib/pq` command.

   In summary, install Go, then run these commands in the command prompt:

   ```cmd
   mkdir  %USERPROFILE%\go\src\postgresqlgo
   cd %USERPROFILE%\go\src\postgresqlgo
   set GOPATH=%USERPROFILE%\go
   go mod init postgresqlgo
   go get github.com/lib/pq
   ```

### [Linux (Ubuntu)](#tab/ubuntu)

1. Launch the Bash shell.
1. Install Go by running `sudo apt-get install golang-go`.
1. Make a folder for your project in your home directory, such as `mkdir -p ~/go/src/postgresqlgo/`.
1. Change directory into the folder, such as `cd ~/go/src/postgresqlgo/`.
1. Set the GOPATH environment variable to point to a valid source directory, such as your current home directory's go folder. At the bash shell, run `export GOPATH=~/go` to add the go directory as the GOPATH for the current shell session.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init postgresqlgo`.
    - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
    - When you're creating a command-line app as a test and won't publish the app, the `<module_path>` doesn't need to refer to an actual location. For example, `postgresqlgo`.
1. Install the [Pure Go Postgres driver (pq)](https://github.com/lib/pq) by running the `go get github.com/lib/pq` command.

   In summary, run these bash commands:

   ```bash
   sudo apt-get install golang-go
   mkdir -p ~/go/src/postgresqlgo/
   cd ~/go/src/postgresqlgo/
   export GOPATH=~/go/
   go mod init postgresqlgo
   go get github.com/lib/pq
   ```

### [Apple macOS](#tab/macos)

1. Download and install Go according to the [installation instructions](https://go.dev/doc/install)  matching your platform.
1. Launch the Bash shell.
1. Make a folder for your project in your home directory, such as `mkdir -p ~/go/src/postgresqlgo/`.
1. Change directory into the folder, such as `cd ~/go/src/postgresqlgo/`.
1. Set the GOPATH environment variable to point to a valid source directory, such as your current home directory's go folder. At the bash shell, run `export GOPATH=~/go` to add the go directory as the GOPATH for the current shell session.
1. Run [go mod init](https://go.dev/ref/mod#go-mod-init) to create a module in the current directory. For example: `go mod init postgresqlgo`.
    - The `<module_path>` parameter is generally a location in a GitHub repo - such as `github.com/<your_github_account_name>/<directory>`.
    - When you're creating a command-line app as a test and won't publish the app, the `<module_path>` doesn't need to refer to an actual location. For example, `postgresqlgo`.
1. Install the [Pure Go Postgres driver (pq)](https://github.com/lib/pq) by running the `go get github.com/lib/pq` command.

   In summary, install Go, then run these bash commands:

   ```bash
   mkdir -p ~/go/src/postgresqlgo/
   cd ~/go/src/postgresqlgo/
   export GOPATH=~/go/
   go mod init postgresqlgo
   go get github.com/lib/pq
   ```

---

## Get connection information

Get the connection information needed to connect to the Azure Database for PostgreSQL. You need the fully qualified server name and login credentials.

1. Log in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you have created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.

## Build and run Go code

1. To write Golang code, you can use a plain text editor, such as Notepad in Microsoft Windows, or [Nano](https://www.nano-editor.org/) in Ubuntu, or TextEdit in macOS. If you prefer a richer Interactive Development Environment (IDE) try [GoLand](https://www.jetbrains.com/go/) by Jetbrains, [Visual Studio Code](https://code.visualstudio.com/) by Microsoft, or [Atom](https://atom.io/).
1. Paste the Golang code from the following sections into text files, and save into your project folder with file extension \*.go, such as Windows path `%USERPROFILE%\go\src\postgresqlgo\createtable.go` or Linux path `~/go/src/postgresqlgo/createtable.go`.
1. Locate the `HOST`, `DATABASE`, `USER`, and `PASSWORD` constants in the code, and replace the example values with your own values. A database named *postgres* is created when you create your Azure Database for PostgreSQL server instance. You can use that database or another one that you've created. 
1. Launch the command prompt or bash shell. Change directory into your project folder. For example, on Windows `cd %USERPROFILE%\go\src\postgresqlgo\`. On Linux `cd ~/go/src/postgresqlgo/`. Some of the IDE environments mentioned offer debug and runtime capabilities without requiring shell commands.
1. Run the code by typing the command `go run createtable.go` to compile the application and run it. 
1. Alternatively, to build the code into a native application, `go build createtable.go`, then launch `createtable.exe` to run the application.

## Connect and create a table

Use the following code to connect and create a table using **CREATE TABLE** SQL statement, followed by **INSERT INTO** SQL statements to add rows into the table.

The code imports three packages: the [sql package](https://go.dev/pkg/database/sql/), the [pq package](https://godoc.org/github.com/lib/pq) as a driver to communicate with the PostgreSQL server, and the [fmt package](https://go.dev/pkg/fmt/) for printed input and output on the command line.

The code calls method [sql.Open()](https://godoc.org/github.com/lib/pq#Open) to connect to Azure Database for PostgreSQL database, and checks the connection using method [db.Ping()](https://go.dev/pkg/database/sql/#DB.Ping). A [database handle](https://go.dev/pkg/database/sql/#DB) is used throughout, holding the connection pool for the database server. The code calls the [Exec()](https://go.dev/pkg/database/sql/#DB.Exec) method several times to run several SQL commands. Each time a custom checkError() method checks if an error occurred and panic to exit if an error does occur.

Replace the `HOST`, `DATABASE`, `USER`, and `PASSWORD` parameters with your own values.

```go
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
)

const (
	// Initialize connection constants.
	HOST     = "mydemoserver.postgres.database.azure.com"
	DATABASE = "postgres"
	USER     = "mylogin"
	PASSWORD = "<server_admin_password>"
)

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	// Initialize connection string.
	var connectionString string = fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=require", HOST, USER, PASSWORD, DATABASE)

	// Initialize connection object.
	db, err := sql.Open("postgres", connectionString)
	checkError(err)

	err = db.Ping()
	checkError(err)
	fmt.Println("Successfully created connection to database")

	// Drop previous table of same name if one exists.
	_, err = db.Exec("DROP TABLE IF EXISTS inventory;")
	checkError(err)
	fmt.Println("Finished dropping table (if existed)")

	// Create table.
	_, err = db.Exec("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
	checkError(err)
	fmt.Println("Finished creating table")

	// Insert some data into table.
	sql_statement := "INSERT INTO inventory (name, quantity) VALUES ($1, $2);"
	_, err = db.Exec(sql_statement, "banana", 150)
	checkError(err)
	_, err = db.Exec(sql_statement, "orange", 154)
	checkError(err)
	_, err = db.Exec(sql_statement, "apple", 100)
	checkError(err)
	fmt.Println("Inserted 3 rows of data")
}
```

## Read data

Use the following code to connect and read the data using a **SELECT** SQL statement.

The code imports three packages: the [sql package](https://go.dev/pkg/database/sql/), the [pq package](https://godoc.org/github.com/lib/pq) as a driver to communicate with the PostgreSQL server, and the [fmt package](https://go.dev/pkg/fmt/) for printed input and output on the command line.

The code calls method [sql.Open()](https://godoc.org/github.com/lib/pq#Open) to connect to Azure Database for PostgreSQL database, and checks the connection using method [db.Ping()](https://go.dev/pkg/database/sql/#DB.Ping). A [database handle](https://go.dev/pkg/database/sql/#DB) is used throughout, holding the connection pool for the database server. The select query is run by calling method [db.Query()](https://go.dev/pkg/database/sql/#DB.Query), and the resulting rows are kept in a variable of type 
[rows](https://go.dev/pkg/database/sql/#Rows). The code reads the column data values in the current row using method [rows.Scan()](https://go.dev/pkg/database/sql/#Rows.Scan) and loops over the rows using the iterator [rows.Next()](https://go.dev/pkg/database/sql/#Rows.Next) until no more rows exist. Each row's column values are printed to the console out. Each time a custom checkError() method is used to check if an error occurred and panic to exit if an error does occur.

Replace the `HOST`, `DATABASE`, `USER`, and `PASSWORD` parameters with your own values.

```go
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
)

const (
	// Initialize connection constants.
	HOST     = "mydemoserver.postgres.database.azure.com"
	DATABASE = "postgres"
	USER     = "mylogin"
	PASSWORD = "<server_admin_password>"
)

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {

	// Initialize connection string.
	var connectionString string = fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=require", HOST, USER, PASSWORD, DATABASE)

	// Initialize connection object.
	db, err := sql.Open("postgres", connectionString)
	checkError(err)

	err = db.Ping()
	checkError(err)
	fmt.Println("Successfully created connection to database")

	// Read rows from table.
	var id int
	var name string
	var quantity int

	sql_statement := "SELECT * from inventory;"
	rows, err := db.Query(sql_statement)
	checkError(err)
	defer rows.Close()

	for rows.Next() {
		switch err := rows.Scan(&id, &name, &quantity); err {
		case sql.ErrNoRows:
			fmt.Println("No rows were returned")
		case nil:
			fmt.Printf("Data row = (%d, %s, %d)\n", id, name, quantity)
		default:
			checkError(err)
		}
	}
}
```

## Update data

Use the following code to connect and update the data using an **UPDATE** SQL statement.

The code imports three packages: the [sql package](https://go.dev/pkg/database/sql/), the [pq package](https://godoc.org/github.com/lib/pq) as a driver to communicate with the Postgres server, and the [fmt package](https://go.dev/pkg/fmt/) for printed input and output on the command line.

The code calls method [sql.Open()](https://godoc.org/github.com/lib/pq#Open) to connect to Azure Database for PostgreSQL database, and checks the connection using method [db.Ping()](https://go.dev/pkg/database/sql/#DB.Ping). A [database handle](https://go.dev/pkg/database/sql/#DB) is used throughout, holding the connection pool for the database server. The code calls the [Exec()](https://go.dev/pkg/database/sql/#DB.Exec) method to run the SQL statement that updates the table. A custom checkError() method is used to check if an error occurred and panic to exit if an error does occur.

Replace the `HOST`, `DATABASE`, `USER`, and `PASSWORD` parameters with your own values. 
```go
package main

import (
  "database/sql"
  _ "github.com/lib/pq"
  "fmt"
)

const (
	// Initialize connection constants.
	HOST     = "mydemoserver.postgres.database.azure.com"
	DATABASE = "postgres"
	USER     = "mylogin"
	PASSWORD = "<server_admin_password>"
)

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {

	// Initialize connection string.
	var connectionString string = 
		fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=require", HOST, USER, PASSWORD, DATABASE)

	// Initialize connection object.
	db, err := sql.Open("postgres", connectionString)
	checkError(err)

	err = db.Ping()
	checkError(err)
	fmt.Println("Successfully created connection to database")

	// Modify some data in table.
	sql_statement := "UPDATE inventory SET quantity = $2 WHERE name = $1;"
	_, err = db.Exec(sql_statement, "banana", 200)
	checkError(err)
	fmt.Println("Updated 1 row of data")
}
```

## Delete data

Use the following code to connect and delete the data using a **DELETE** SQL statement.

The code imports three packages: the [sql package](https://go.dev/pkg/database/sql/), the [pq package](https://godoc.org/github.com/lib/pq) as a driver to communicate with the Postgres server, and the [fmt package](https://go.dev/pkg/fmt/) for printed input and output on the command line.

The code calls method [sql.Open()](https://godoc.org/github.com/lib/pq#Open) to connect to Azure Database for PostgreSQL database, and checks the connection using method [db.Ping()](https://go.dev/pkg/database/sql/#DB.Ping). A [database handle](https://go.dev/pkg/database/sql/#DB) is used throughout, holding the connection pool for the database server. The code calls the [Exec()](https://go.dev/pkg/database/sql/#DB.Exec) method to run the SQL statement that deletes a row from the table. A custom checkError() method is used to check if an error occurred and panic to exit if an error does occur.

Replace the `HOST`, `DATABASE`, `USER`, and `PASSWORD` parameters with your own values. 
```go
package main

import (
  "database/sql"
  _ "github.com/lib/pq"
  "fmt"
)

const (
	// Initialize connection constants.
	HOST     = "mydemoserver.postgres.database.azure.com"
	DATABASE = "postgres"
	USER     = "mylogin"
	PASSWORD = "<server_admin_password>"
)

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {

	// Initialize connection string.
	var connectionString string = 
		fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=require", HOST, USER, PASSWORD, DATABASE)

	// Initialize connection object.
	db, err := sql.Open("postgres", connectionString)
	checkError(err)

	err = db.Ping()
	checkError(err)
	fmt.Println("Successfully created connection to database")

	// Delete some data from table.
	sql_statement := "DELETE FROM inventory WHERE name = $1;"
	_, err = db.Exec(sql_statement, "orange")
	checkError(err)
	fmt.Println("Deleted 1 row of data")
}
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
- [Quickstart: Use Python to connect and query data in Azure Database for PostgreSQL](connect-python.md).
- [Quickstart: Use Java to connect and query data from an Azure Database for PostgreSQL](connect-java.md).
- [Quickstart: Use .NET (C#) to connect and query data from an Azure Database for PostgreSQL](connect-csharp.md).
- [Quickstart: Use PHP to connect and query data from an Azure Database for PostgreSQL](connect-php.md).
- [Quickstart: Use Azure CLI to connect and query data from an Azure Database for PostgreSQL](connect-azure-cli.md).
- [Quickstart: Import data from Azure Database for PostgreSQL in Power BI](../integration/connect-with-power-bi-desktop.md).
