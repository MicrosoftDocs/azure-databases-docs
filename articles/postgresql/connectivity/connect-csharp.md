---
title: "Quickstart: Connect with C#"
description: "This quickstart provides a C# (.NET) code sample you can use to connect and query data from an Azure Database for PostgreSQL flexible server instance."
author: agapovm
ms.author: maximagapov
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: connectivity
ms.topic: quickstart
ms.custom:
- mvc
- devcenter
- devx-track-csharp
- mode-other
- devx-track-dotnet
- sfi-image-nochange
- sfi-ropc-nochange
ms.devlang: csharp
---

# Quickstart: Use .NET (C#) to connect and query data in Azure Database for PostgreSQL 

This quickstart demonstrates how to connect to an Azure Database for PostgreSQL flexible server instance using a C# application. It shows how to use SQL statements to query, insert, update, and delete data in the database. The steps in this article assume that you are familiar with developing using C#, and that you are new to working with Azure Database for PostgreSQL.

## Prerequisites

For this quickstart you need:

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).
- [Create an Azure Database for PostgreSQL flexible server](../configure-maintain/quickstart-create-server.md) instance, if you do not have one.
- Use the empty *postgres* database available on the server or create a [new database](../configure-maintain/quickstart-create-server.md#connect-using-psql).
- Install the [.NET SDK for your platform](https://dotnet.microsoft.com/download) (Windows, Ubuntu Linux, or macOS) for your platform.
- Install [Visual Studio](https://www.visualstudio.com/downloads/) to build your project.
- Install [Npgsql](https://www.nuget.org/packages/Npgsql/) NuGet package in Visual Studio.

## Get connection information

Get the connection information needed to connect to the Azure Database for PostgreSQL flexible server instance. You need the fully qualified server name and login credentials.

Using the [Azure portal](https://portal.azure.com/):

1. From the left-hand menu in Azure portal, click **All resources**, and then search for the server you have created.

2. Click the server name.

3. In the resource menu, select **Overview**.

    :::image type="content" source="media/connect/overview.png" alt-text="Screenshot showing the Overview page." lightbox="media/connect/overview.png":::

4. Copy the values shown as **Endpoint** and **Administrator login**.

    :::image type="content" source="media/connect/endpoint-administrator-login.png" alt-text="Screenshot showing the values of Endpoint and Administrator login in the Overview page." lightbox="media/connect/endpoint-administrator-login.png":::

5. If you forget the password of the administrator login, you can reset it using the **Reset password** button.

    :::image type="content" source="media/connect/reset-password.png" alt-text="Screenshot showing the Reset password button in the Overview page." lightbox="media/connect/reset-password.png":::

## Step 1: Connect and insert data

Use the following code to connect and load the data using **CREATE TABLE** and  **INSERT INTO** SQL statements. The code uses NpgsqlCommand class with method:
- [Open()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_Open) to establish a connection to the Azure Database for PostgreSQL flexible server database.
- [CreateCommand()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_CreateCommand) sets the CommandText property.
- [ExecuteNonQuery()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlCommand.html#Npgsql_NpgsqlCommand_ExecuteNonQuery) method to run the database commands.

> [!IMPORTANT]
> Replace the Host, DBName, User, and Password parameters with the values that you specified when you created the server and database.

```csharp
using System;
using Npgsql;

namespace Driver
{
    public class AzurePostgresCreate
    {
        // Obtain connection string information from the portal
        //
        private static string Host = "mydemoserver.postgres.database.azure.com";
        private static string User = "mylogin";
        private static string  DBname = "postgres";
        private static string Password = "<server_admin_password>";
        private static string Port = "5432";

        static void Main(string[] args)
        {
            // Build connection string using parameters from portal
            //
            string connString =
                String.Format(
                    "Server={0};Username={1};Database={2};Port={3};Password={4};SSLMode=Prefer",
                    Host,
                    User,
                    DBname,
                    Port,
                    Password);


            using (var conn = new NpgsqlConnection(connString))

            {
                Console.Out.WriteLine("Opening connection");
                conn.Open();

                using (var command = new NpgsqlCommand("DROP TABLE IF EXISTS inventory", conn))
                {
                    command.ExecuteNonQuery();
                    Console.Out.WriteLine("Finished dropping table (if existed)");

                }

                using (var command = new NpgsqlCommand("CREATE TABLE inventory(id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER)", conn))
                {
                    command.ExecuteNonQuery();
                    Console.Out.WriteLine("Finished creating table");
                }

                using (var command = new NpgsqlCommand("INSERT INTO inventory (name, quantity) VALUES (@n1, @q1), (@n2, @q2), (@n3, @q3)", conn))
                {
                    command.Parameters.AddWithValue("n1", "banana");
                    command.Parameters.AddWithValue("q1", 150);
                    command.Parameters.AddWithValue("n2", "orange");
                    command.Parameters.AddWithValue("q2", 154);
                    command.Parameters.AddWithValue("n3", "apple");
                    command.Parameters.AddWithValue("q3", 100);

                    int nRows = command.ExecuteNonQuery();
                    Console.Out.WriteLine(String.Format("Number of rows inserted={0}", nRows));
                }
            }

            Console.WriteLine("Press RETURN to exit");
            Console.ReadLine();
        }
    }
}
```

[Having any issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)

## Step 2: Read data

Use the following code to connect and read the data using a **SELECT** SQL statement. The code uses NpgsqlCommand class with method:
- [Open()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_Open) to establish a connection to PostgreSQL.
- [CreateCommand()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_CreateCommand) and [ExecuteReader()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlCommand.html#Npgsql_NpgsqlCommand_ExecuteReader) to run the database commands.
- [Read()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlDataReader.html#Npgsql_NpgsqlDataReader_Read) to advance to the record in the results.
- [GetInt32()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlDataReader.html#Npgsql_NpgsqlDataReader_GetInt32_System_Int32_) and [GetString()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlDataReader.html#Npgsql_NpgsqlDataReader_GetString_System_Int32_) to parse the values in the record.

> [!IMPORTANT]
> Replace the Host, DBName, User, and Password parameters with the values that you specified when you created the server and database.

```csharp
using System;
using Npgsql;

namespace Driver
{
    public class AzurePostgresRead
    {
        // Obtain connection string information from the portal
        //
        private static string Host = "mydemoserver.postgres.database.azure.com";
        private static string User = "mylogin";
        private static string  DBname = "postgres";
        private static string Password = "<server_admin_password>";
        private static string Port = "5432";

        static void Main(string[] args)
        {
            // Build connection string using parameters from portal
            //
            string connString =
                String.Format(
                    "Server={0}; User Id={1}; Database={2}; Port={3}; Password={4};SSLMode=Prefer",
                    Host,
                    User,
                    DBname,
                    Port,
                    Password);

            using (var conn = new NpgsqlConnection(connString))
            {

                Console.Out.WriteLine("Opening connection");
                conn.Open();


                using (var command = new NpgsqlCommand("SELECT * FROM inventory", conn))
                {

                    var reader = command.ExecuteReader();
                    while (reader.Read())
                    {
                        Console.WriteLine(
                            string.Format(
                                "Reading from table=({0}, {1}, {2})",
                                reader.GetInt32(0).ToString(),
                                reader.GetString(1),
                                reader.GetInt32(2).ToString()
                                )
                            );
                    }
                    reader.Close();
                }
            }

            Console.WriteLine("Press RETURN to exit");
            Console.ReadLine();
        }
    }
}
```
[Having any issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)


## Step 3: Update data

Use the following code to connect and update the data using an **UPDATE** SQL statement. The code uses NpgsqlCommand class with method:
- [Open()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_Open) to establish a connection to the Azure Database for PostgreSQL flexible server instance.
- [CreateCommand()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_CreateCommand), sets the CommandText property.
- [ExecuteNonQuery()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlCommand.html#Npgsql_NpgsqlCommand_ExecuteNonQuery) method to run the database commands.

> [!IMPORTANT]
> Replace the Host, DBName, User, and Password parameters with the values that you specified when you created the server and database.

```csharp
using System;
using Npgsql;

namespace Driver
{
    public class AzurePostgresUpdate
    {
        // Obtain connection string information from the portal
        //
        private static string Host = "mydemoserver.postgres.database.azure.com";
        private static string User = "mylogin";
        private static string  DBname = "postgres";
        private static string Password = "<server_admin_password>";
        private static string Port = "5432";

        static void Main(string[] args)
        {
            // Build connection string using parameters from portal
            //
            string connString =
                String.Format(
                    "Server={0}; User Id={1}; Database={2}; Port={3}; Password={4};SSLMode=Prefer",
                    Host,
                    User,
                    DBname,
                    Port,
                    Password);

            using (var conn = new NpgsqlConnection(connString))
            {

                Console.Out.WriteLine("Opening connection");
                conn.Open();

                using (var command = new NpgsqlCommand("UPDATE inventory SET quantity = @q WHERE name = @n", conn))
                {
                    command.Parameters.AddWithValue("n", "banana");
                    command.Parameters.AddWithValue("q", 200);
                    int nRows = command.ExecuteNonQuery();
                    Console.Out.WriteLine(String.Format("Number of rows updated={0}", nRows));
                }
            }

            Console.WriteLine("Press RETURN to exit");
            Console.ReadLine();
        }
    }
}


```

[Having any issues? Let us know.](https://github.com/MicrosoftDocs/azure-docs/issues)

## Step 4: Delete data

Use the following code to connect and delete data using a **DELETE** SQL statement.

The code uses NpgsqlCommand class with method [Open()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_Open) to establish a connection to the Azure Database for PostgreSQL flexible server database. Then, the code uses the [CreateCommand()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlConnection.html#Npgsql_NpgsqlConnection_CreateCommand) method, sets the CommandText property, and calls the method [ExecuteNonQuery()](https://www.npgsql.org/doc/api/Npgsql.NpgsqlCommand.html#Npgsql_NpgsqlCommand_ExecuteNonQuery) to run the database commands.

> [!IMPORTANT]
> Replace the Host, DBName, User, and Password parameters with the values that you specified when you created the server and database.

```csharp
using System;
using Npgsql;

namespace Driver
{
    public class AzurePostgresDelete
    {
        // Obtain connection string information from the portal
        //
        private static string Host = "mydemoserver.postgres.database.azure.com";
        private static string User = "mylogin@mydemoserver";
        private static string  DBname = "postgres";
        private static string Password = "<server_admin_password>";
        private static string Port = "5432";

        static void Main(string[] args)
        {
            // Build connection string using parameters from portal
            //
            string connString =
                String.Format(
                    "Server={0}; User Id={1}; Database={2}; Port={3}; Password={4};SSLMode=Prefer",
                    Host,
                    User,
                    DBname,
                    Port,
                    Password);

            using (var conn = new NpgsqlConnection(connString))
            {
                Console.Out.WriteLine("Opening connection");
                conn.Open();

                using (var command = new NpgsqlCommand("DELETE FROM inventory WHERE name = @n", conn))
                {
                    command.Parameters.AddWithValue("n", "orange");

                    int nRows = command.ExecuteNonQuery();
                    Console.Out.WriteLine(String.Format("Number of rows deleted={0}", nRows));
                }
            }

            Console.WriteLine("Press RETURN to exit");
            Console.ReadLine();
        }
    }
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
- [Quickstart: Use Java and JDBC with Azure Database for PostgreSQL](connect-java.md).
- [Quickstart: Use Go language to connect and query data in Azure Database for PostgreSQL](connect-go.md).
- [Quickstart: Use PHP to connect and query data in Azure Database for PostgreSQL](connect-php.md).
- [Quickstart: Connect and query with Azure CLI with Azure Database for PostgreSQL](connect-azure-cli.md).
- [Quickstart: Import data from Azure Database for PostgreSQL in Power BI](../integration/connect-with-power-bi-desktop.md).
