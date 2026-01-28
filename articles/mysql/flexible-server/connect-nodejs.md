---
title: "Quickstart: Connect Using Node.js"
description: This quickstart provides several Node.js code samples you can use to connect and query data from Azure Database for MySQL - Flexible Server.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: quickstart
ms.custom:
  - mvc
  - devx-track-js
  - mode-api
  - linux-related-content
  - sfi-image-nochange
ms.devlang: javascript
---

# Quickstart: Use Node.js to connect and query data in Azure Database for MySQL - Flexible Server

In this quickstart, you connect to Azure Database for MySQL Flexible Server by using Node.js. You then use SQL statements to query, insert, update, and delete data in the database from Mac, Linux, and Windows platforms.

This article assumes that you're familiar with developing using Node.js, but you're new to working with Azure Database for MySQL Flexible Server.

## Prerequisites

This quickstart uses the resources created in either of these guides as a starting point:

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)

> [!IMPORTANT]
> Add the IP address you're connecting from to the server's firewall rules using [Azure portal](security-how-to-manage-firewall-portal.md) or [Azure CLI](security-how-to-manage-firewall-cli.md).

## Install Node.js and the MySQL connector

Depending on your platform, follow the instructions in the appropriate section to install [Node.js](https://nodejs.org/en). Use npm to install the [`mysql2`](https://www.npmjs.com/package/mysql2) package and its dependencies into your project folder.

### [Windows](#tab/windows)

1. Visit the [Node.js downloads page](https://nodejs.org/en/download/package-manager), and then select your desired Windows installer option.
1. Make a local project folder such as `nodejsmysql`.
1. Open the command prompt, and then change directory into the project folder, such as `cd c:\nodejsmysql\`
1. Run the NPM tool to install `mysql2` library into the project folder.

   ```console
   cd c:\nodejsmysql\
   "C:\Program Files\nodejs\npm" install mysql2
   "C:\Program Files\nodejs\npm" list
   ```

1. Verify the installation by checking the `npm list` output text. The version number might vary as new patches are released.

### [Linux (Ubuntu/Debian)](#tab/ubuntu)

1. Run the following commands to install **Node.js** and **npm** the package manager for Node.js.

   ```bash
    # Using Ubuntu
    sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # Using Debian, as root
    sudo curl -sL https://deb.nodesource.com/setup_14.x | bash -
    sudo apt-get install -y nodejs
   ```

1. Run the following commands to create a project folder `mysqlnodejs` and install the mysql2 package into that folder.

   ```bash
   mkdir nodejsmysql
   cd nodejsmysql
   npm install --save mysql2
   npm list
   ```

1. Verify the installation by checking npm list output text. The version number might vary as new patches are released.

### [Linux (RHEL)](#tab/rhel)

1. Run the following commands to install **Node.js** and **npm** the package manager for Node.js.

   **RHEL 7.x**

   ```bash
   sudo yum install -y rh-nodejs8
   scl enable rh-nodejs8 bash
  ```

   **RHEL 8.x**

   ```bash
    sudo yum install -y nodejs
   ```

1. Run the following commands to create a project folder `mysqlnodejs` and install the mysql2 package into that folder.

   ```bash
   mkdir nodejsmysql
   cd nodejsmysql
   npm install --save mysql2
   npm list
   ```

1. Verify the installation by checking npm list output text. The version number might vary as new patches are released.

### [Linux (SUSE)](#tab/sles)

1. Run the following commands to install **Node.js** and **npm** the package manager for Node.js.

   ```bash
   sudo zypper install nodejs
   ```

1. Run the following commands to create a project folder `mysqlnodejs` and install the mysql2 package into that folder.

   ```bash
   mkdir nodejsmysql
   cd nodejsmysql
   npm install --save mysql2
   npm list
   ```

1. Verify the installation by checking npm list output text. The version number might vary as new patches are released.

### [macOS](#tab/mac)

1. Visit the [Node.js downloads page](https://nodejs.org/en/download/package-manager), and then select your macOS installer.

1. Run the following commands to create a project folder `mysqlnodejs` and install the mysql2 package into that folder.

   ```bash
   mkdir nodejsmysql
   cd nodejsmysql
   npm install --save mysql2
   npm list
   ```

1. Verify the installation by checking the `npm list` output text. The version number might vary as new patches are released.

---

## Get connection information

Get the connection information needed to connect to the Azure Database for MySQL Flexible Server instance. You need the fully qualified server name and sign in credentials.

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. From the left-hand menu in Azure portal, select **All resources**, and then search for the server you created (such as **mydemoserver**).
1. Select the server name.
1. From the server's **Overview** panel, make a note of the **Server name** and **Server admin login name**. If you forget your password, you can also reset the password from this panel.

## Run the code samples

1. Paste the JavaScript code into new text files, and then save it into a project folder with file extension .js (such as C:\nodejsmysql\createtable.js or /home/username/nodejsmysql/createtable.js).
1. Replace `host`, `user`, `password`, and `database` config options in the code with the values that you specified when you created the MySQL Flexible Server and database.
1. **Obtain TLS certificate**: To use encrypted connections with your client applications, you need to follow the instruction in [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

Save the certificate file to your preferred location.

1. In the `ssl` config option, replace the `ca-cert` filename with the path to this local file. This will allow the application to connect securely to the database over SSL.
1. Open the command prompt or bash shell, and then change directory into your project folder `cd nodejsmysql`.
1. To run the application, enter the node command followed by the file name, such as `node createtable.js`.
1. On Windows, if the node application isn't in your environment variable path, you might need to use the full path to launch the node application, such as `"C:\Program Files\nodejs\node.exe" createtable.js`

## Connect, create table, and insert data

Use the following code to connect and load the data by using **CREATE TABLE** and **INSERT INTO** SQL statements.

The [mysql.createConnection()](https://github.com/sidorares/node-mysql2#first-query) method is used to interface with the Azure Database for MySQL Flexible Server instance. The [connect()](https://github.com/sidorares/node-mysql2#first-query) function is used to establish the connection to the server. The [query()](https://github.com/sidorares/node-mysql2#first-query) function is used to execute the SQL query against MySQL database.

```sql
const mysql = require('mysql2');
const fs = require('fs');

var config =
{
    host: 'your_server_name.mysql.database.azure.com',
    user: 'your_admin_name',
    password: 'your_admin_password',
    database: 'quickstartdb',
    port: 3306,
    ssl: {ca: fs.readFileSync("your_path_to_ca_cert_file_DigiCertGlobalRootCA.crt.pem")}
};

const conn = new mysql.createConnection(config);

conn.connect(
    function (err) {
    if (err) {
        console.log("!!! Cannot connect !!! Error:");
        throw err;
    }
    else
    {
        console.log("Connection established.");
        queryDatabase();
    }
});

function queryDatabase()
{
    conn.query('DROP TABLE IF EXISTS inventory;',
        function (err, results, fields) {
            if (err) throw err;
            console.log('Dropped inventory table if existed.');
        }
    )
    conn.query('CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);',
        function (err, results, fields) {
            if (err) throw err;
            console.log('Created inventory table.');
        }
    )
    conn.query('INSERT INTO inventory (name, quantity) VALUES (?, ?);', ['banana', 150],
        function (err, results, fields) {
            if (err) throw err;
            else console.log('Inserted ' + results.affectedRows + ' row(s).');
        }
    )
    conn.query('INSERT INTO inventory (name, quantity) VALUES (?, ?);', ['orange', 250],
        function (err, results, fields) {
            if (err) throw err;
            console.log('Inserted ' + results.affectedRows + ' row(s).');
        }
    )
    conn.query('INSERT INTO inventory (name, quantity) VALUES (?, ?);', ['apple', 100],
        function (err, results, fields) {
            if (err) throw err;
            console.log('Inserted ' + results.affectedRows + ' row(s).');
        }
    )
    conn.end(function (err) {
        if (err) throw err;
        else  console.log('Done.')
    });
};
```

## Read data

Use the following code to connect and read the data by using a **SELECT** SQL statement.

The [mysql.createConnection()](https://github.com/sidorares/node-mysql2#first-query) method is used to interface with the Azure Database for MySQL Flexible Server instance. The [connect()](https://github.com/sidorares/node-mysql2#first-query) method is used to establish the connection to the server. The [query()](https://github.com/sidorares/node-mysql2#first-query) method is used to execute the SQL query against MySQL database. The results array is used to hold the results of the query.

```sql
const mysql = require('mysql2');
const fs = require('fs');

var config =
{
    host: 'your_server_name.mysql.database.azure.com',
    user: 'your_admin_name',
    password: 'your_admin_password',
    database: 'quickstartdb',
    port: 3306,
    ssl: {ca: fs.readFileSync("your_path_to_ca_cert_file_DigiCertGlobalRootCA.crt.pem")}
};

const conn = new mysql.createConnection(config);

conn.connect(
    function (err) {
        if (err) {
            console.log("!!! Cannot connect !!! Error:");
            throw err;
        }
        else {
            console.log("Connection established.");
            readData();
        }
    });

function readData(){
    conn.query('SELECT * FROM inventory',
        function (err, results, fields) {
            if (err) throw err;
            else console.log('Selected ' + results.length + ' row(s).');
            for (i = 0; i < results.length; i++) {
                console.log('Row: ' + JSON.stringify(results[i]));
            }
            console.log('Done.');
        })
    conn.end(
        function (err) {
            if (err) throw err;
            else  console.log('Closing connection.')
    });
};
```

## Update data

Use the following code to connect and update the data by using an **UPDATE** SQL statement.

The [mysql.createConnection()](https://github.com/sidorares/node-mysql2#first-query) method is used to interface with the Azure Database for MySQL Flexible Server instance. The [connect()](https://github.com/sidorares/node-mysql2#first-query) method is used to establish the connection to the server. The [query()](https://github.com/sidorares/node-mysql2#first-query) method is used to execute the SQL query against MySQL database.

```sql
const mysql = require('mysql2');
const fs = require('fs');

var config =
{
    host: 'your_server_name.mysql.database.azure.com',
    user: 'your_admin_name',
    password: 'your_admin_password',
    database: 'quickstartdb',
    port: 3306,
    ssl: {ca: fs.readFileSync("your_path_to_ca_cert_file_DigiCertGlobalRootCA.crt.pem")}
};

const conn = new mysql.createConnection(config);

conn.connect(
    function (err) {
        if (err) {
            console.log("!!! Cannot connect !!! Error:");
            throw err;
        }
        else {
            console.log("Connection established.");
            updateData();
        }
    });

function updateData(){
       conn.query('UPDATE inventory SET quantity = ? WHERE name = ?', [75, 'banana'],
            function (err, results, fields) {
                if (err) throw err;
                else console.log('Updated ' + results.affectedRows + ' row(s).');
           })
       conn.end(
           function (err) {
                if (err) throw err;
                else  console.log('Done.')
        });
};
```

## Delete data

Use the following code to connect and delete data by using a **DELETE** SQL statement.

The [mysql.createConnection()](https://github.com/sidorares/node-mysql2#first-query) method is used to interface with the Azure Database for MySQL Flexible Server instance. The [connect()](https://github.com/sidorares/node-mysql2#first-query) method is used to establish the connection to the server. The [query()](https://github.com/sidorares/node-mysql2#first-query) method is used to execute the SQL query against MySQL database.

```sql
const mysql = require('mysql2');
const fs = require('fs');

var config =
{
    host: 'your_server_name.mysql.database.azure.com',
    user: 'your_admin_name',
    password: 'your_admin_password',
    database: 'quickstartdb',
    port: 3306,
    ssl: {ca: fs.readFileSync("your_path_to_ca_cert_file_DigiCertGlobalRootCA.crt.pem")}
};

const conn = new mysql.createConnection(config);

conn.connect(
    function (err) {
        if (err) {
            console.log("!!! Cannot connect !!! Error:");
            throw err;
        }
        else {
            console.log("Connection established.");
            deleteData();
        }
    });

function deleteData(){
       conn.query('DELETE FROM inventory WHERE name = ?', ['orange'],
            function (err, results, fields) {
                if (err) throw err;
                else console.log('Deleted ' + results.affectedRows + ' row(s).');
           })
       conn.end(
           function (err) {
                if (err) throw err;
                else  console.log('Done.')
        });
};
```

## Clean up resources

To clean up all resources used during this quickstart, delete the resource group using the following command:

```azurecli-interactive
az group delete \
    --name $AZ_RESOURCE_GROUP \
    --yes
```

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](security-tls-how-to-connect.md)
- [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](security-how-to-manage-firewall-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
