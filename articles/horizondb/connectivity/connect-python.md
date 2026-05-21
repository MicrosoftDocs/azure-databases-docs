---
title: "Quickstart: Use Python to Connect and Query Data in Azure HorizonDB"
description: This quickstart provides several Python code samples you can use to connect and query data from an Azure HorizonDB cluster.
author: scoriani
ms.author: scoriani
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: quickstart
ms.custom:
  - mvc
  - mode-api
  - devx-track-python
  - passwordless-python
  - sfi-ropc-blocked
ms.devlang: "python"
---

# Quickstart: Use Python to connect and query data in Azure HorizonDB

In this quickstart, you connect to an Azure HorizonDB instance by using Python. You then use SQL statements to query, insert, update, and delete data in the database from macOS, Ubuntu Linux, and Windows platforms.

The steps in this article include PostgreSQL authentication.

PostgreSQL authentication uses accounts stored in PostgreSQL and you need to manage the rotation of the passwords by yourself.

This article assumes that you're familiar with developing using Python, but you're new to working with Azure HorizonDB.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure HorizonDB cluster. To create Azure HorizonDB cluster, refer to [Create an Azure HorizonDB cluster](../configure-maintain/quickstart-create-cluster.md).
- [Python](https://www.python.org/downloads/) 3.8+.
- Latest [pip](https://pip.pypa.io/en/stable/installing/) package installer.

## Add firewall rules for your client workstation

- If you created your Azure HorizonDB cluster with *Public access (allowed IP addresses)*, you can add your local IP address to the list of firewall rules on your cluster. Refer to [Networking in Azure HorizonDB](../network/how-to-networking.md).

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

Install the [psycopg](https://pypi.org/project/psycopg/) module, which enables connecting to and querying a PostgreSQL database.

```bash
# Recommended: install the binary wheel that bundles a compatible libpq wrapper (Windows/macOS)
python -m pip install "psycopg[binary]"

# Linux alternative (if you prefer building against system libpq):
sudo apt-get update
sudo apt-get install -y libpq-dev build-essential python3-dev
python -m pip install psycopg
```

## Add authentication code

In this section, you add authentication code to your working directory and perform any additional steps required for authentication and authorization with your cluster instance.

Before you add the authentication code, make sure the required packages for each example are installed.

Required packages (examples in this article):

- Password example: `psycopg` (recommended: `python -m pip install "psycopg[binary]"`)

Optional: create a `requirements.txt` with these entries and install with `python -m pip install -r requirements.txt` for reproducible installs.

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

   1. From the left-hand menu in Azure portal, select **All resources**, and then search for the cluster you have created.

   1. Select the cluster name.

   1. In the resource menu, select **Overview**.

      :::image type="content" source="media/connect-python/overview.png" alt-text="Screenshot showing the Overview page." lightbox="media/connect-python/overview.png":::

   1. Copy the value shown as **Endpoint**.

      :::image type="content" source="media/connect-python/endpoint-administrator-login.png" alt-text="Screenshot showing the values of Endpoint and Administrator login in the Overview page." lightbox="media/connect-python/endpoint-administrator-login.png":::

   1. If you forget the password of the administrator login, you can reset it using the **Reset password** button.

      :::image type="content" source="media/connect-python/reset-password.png" alt-text="Screenshot showing the Reset password button in the Overview page." lightbox="media/connect-python/reset-password.png":::

1. Set environment variables for the connection URI elements:

   ### [Windows](#tab/cmd)

   ```cmd
   set DBHOST=<cluster-name>
   set DBNAME=<database-name>
   set DBUSER=<username>
   set DBPASSWORD=<password>
   set SSLMODE=require
   ```

   ### [macOS/Linux](#tab/bash)

   ```bash
   export DBHOST=<cluster-name>
   export DBNAME=<database-name>
   export DBUSER=<username>
   export DBPASSWORD=<password>
   export SSLMODE=require
   ```

---

## How to run the Python examples

For each code example in this article:

1. Create a new file in a text editor.

1. Add the code example to the file.

1. Save the file in your project folder with a *.py* extension, such as *postgres-insert.py*. For Windows, make sure UTF-8 encoding is selected when you save the file.

1. In your project folder type `python` followed by the filename, for example `python postgres-insert.py`.

## Create a table and insert data

The following code example connects to your Azure HorizonDB cluster using the `psycopg.connect` function, and loads data with a SQL `INSERT` statement. The `cursor.execute` function executes the SQL query against the database.

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

The following code example connects to your Azure HorizonDB cluster and uses cursor.execute with the SQL `SELECT` statement to read data. This function accepts a query and returns a result set to iterate over by using cursor.fetchall().

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

The following code example connects to your Azure HorizonDB cluster and uses cursor.execute with the SQL `UPDATE` statement to update data.

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

The following code example connects to your Azure HorizonDB cluster and uses cursor.execute with the SQL `DELETE` statement to delete an inventory item that you previously inserted.

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

- [Quickstart: Use Java and JDBC in Azure HorizonDB](connect-java.md)
- [Quickstart: Use .NET (C#) to connect and query data in Azure HorizonDB](connect-csharp.md)
- [Quickstart: Use Go language to connect and query data in Azure HorizonDB](connect-go.md)
- [Quickstart: Use PHP to connect and query data in Azure HorizonDB](connect-php.md)
- [Quickstart: Connect and query with Azure CLI in Azure HorizonDB](connect-azure-cli.md)
- [Quickstart: Import data in Power BI in Azure HorizonDB](../integration/connect-with-power-bi-desktop.md)
