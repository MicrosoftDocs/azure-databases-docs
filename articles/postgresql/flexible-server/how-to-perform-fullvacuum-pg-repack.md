---
title: Optimize by using pg_repack
description: Perform full vacuum using pg_Repack extension.
author: sarat0681
ms.author: sbalijepalli
ms.reviewer: maghan
ms.date: 04/22/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Full vacuum using pg_repack in Azure Database for PostgreSQL 

In this article, you learn how to use `pg_repack` to remove bloat and improve your Azure Database for PostgreSQL flexible server performance. Bloat is the unnecessary data accumulating in tables and indexes due to frequent updates and deletes. Bloat can cause the database size to grow larger than expected, and it can severely affect the performance of some queries. Use `pg_repack` to reclaim the wasted space and reorganize the data more efficiently.

## What is pg_repack?

`pg_repack` is a PostgreSQL extension that removes bloat from tables and indexes and reorganizes them more efficiently. `pg_repack` works by creating a new copy of the target table or index, applying any changes that occurred during the process, and then swapping the old and new versions atomically. `pg_repack` doesn't require any downtime or exclusive access locks on the processed table or index, except for a brief period at the beginning and at the end of the operation. You can use `pg_repack` to optimize any table or index in your Azure Database for PostgreSQL flexible server databases.

## How to use pg_repack?

To use `pg_repack`, you need to install the extension in your Azure Database for PostgreSQL flexible server database and then run the `pg_repack` command, specifying the table name or index you want to optimize. The extension acquires locks on the table or index to prevent other operations from being performed while the optimization is in progress. It removes the bloat and reorganizes the data more efficiently.

## How full table repacking works

To perform a full table repacking, the extension follows these steps:

1.    Creates a log table to record changes made to the original table.
2.    Adds a trigger to the original table, logging INSERTs, UPDATEs, and DELETEs into the log table.
3.    Creates a new table containing all the rows in the original table.
4.    Builds indexes on the new table.
5.    Applies all changes recorded in the log table to the new table.
6.    Swaps the original and new tables, including indexes and toast tables.
7.    Drops the original table.

During these steps, `pg_repack` only holds an exclusive access lock for a short period, during the initial setup (steps 1 and 2) and again during the final swap-and-drop phase (steps 6 and 7). For the rest of the time, `pg_repack` only needs to hold a shared access lock on the original table, allowing INSERTs, UPDATEs, and DELETEs to proceed as usual.

## Limitations

`pg_repack` has some limitations that you should be aware of before using it:

-  The target table must have either a PRIMARY KEY or a UNIQUE index on a NOT NULL column for the operation to be successful.
-  While `pg_repack` is running, you aren't able to perform any Data Definition Language (DDL) commands on the target tables except for VACUUM or ANALYZE. To ensure these restrictions are enforced, `pg_repack` holds a shared access lock on the target table during a full table repacking.

## Setup

### Prerequisites

1. Configure the `pg_repack` extension by [allowlisting](../extensions/how-to-allow-extensions.md#allow-extensions) and [creating](../extensions/how-to-create-extensions.md) the extension.

### Build pg_repack client application

The use of this extension requires a client application which you can build and install on an instance of Ubuntu.

To install version 1.5.1 of `pg_repack`, run the following bash script on an Ubuntu machine.

```bash
# Create the file repository configuration
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# Import the repository signing key
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# Update the package lists
sudo apt-get update
# Install required packages to build the code
sudo apt-get install -y postgresql-server-dev-14 unzip make gcc libssl-dev liblz4-dev zlib1g-dev libreadline-dev libzstd-dev
# Download compressed version of build tree for version 1.5.1 of pg_repack
wget 'https://api.pgxn.org/dist/pg_repack/1.5.1/pg_repack-1.5.1.zip'
# Uncompress build tree
unzip pg_repack-1.5.1.zip
# Set current directory to where build tree was uncompressed
cd pg_repack-1.5.1
# Build code
sudo make
# Copy resulting binaries to /usr/local/bin
sudo cp bin/pg_repack /usr/local/bin
# Run pg_repack to check its version
pg_repack --version
```

## Use pg_repack

Example of how to run `pg_repack` on a table named info in a public schema within the Azure Database for PostgreSQL flexible server instance with endpoint pgserver.postgres.database.azure.com, username azureuser, and database foo using the following command.

1. Using the client of your preference, connect to the Azure Database for PostgreSQL flexible server instance. We use psql in this example.

    ```bash
        psql "host=<server>.postgres.database.azure.com port=5432 dbname=<database> user=<user> password=<password> sslmode=require"
    ```

2. Find the version of `pg_repack` extension installed in the database.

    ```sql
    SELECT installed_version FROM pg_available_extensions WHERE name = 'pg_repack';
    ```

3. The version of the extension must match the version of the client application, which you can check by running this command:

    ```bash
    azureuser@azureuser:~$ pg_repack --version
    ```

4. Run `pg_repack` client against a table called **info** which exists in database **foo**.

    ```bash
    pg_repack --host=<server>.postgres.database.azure.com --username=<user> --dbname=<database> --table=info --jobs=2 --no-kill-backend --no-superuser-check
    ```

### pg_repack options

Useful `pg_repack` options for production workloads:

- `-k`, `--no-superuser-check`: Skip the superuser checks in the client. This setting is helpful for using `pg_repack` on platforms that support running it as non-superusers, like Azure Database for PostgreSQL flexible server instances.

- `-j`, `--jobs`: Create the specified number of extra connections to Azure Database for PostgreSQL flexible server, and use these extra connections to parallelize the rebuild of indexes on each table. Parallel index builds are only supported for full-table repacks.

- `--index` or `--only` indexes options: If your Azure Database for PostgreSQL flexible server instance has extra cores and disk I/O available, the use of this option can be a useful way to speed up `pg_repack`.

- `-D`, `--no-kill-backend`: Instead of killing backend clients that are running blocking queries, skip the repacking of a table if the lock can't be acquired after waiting for the time specified in `--wait-timeout`. By default, `--wait-timeout` is set to 60 seconds. The default value for this parameter is `false`.

- `-E LEVEL`, `--elevel=LEVEL`: Choose the output message level from `DEBUG`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL`, and `PANIC`. The default is `INFO`.

To understand all the options, refer to the documentation of [pg_repack](https://reorg.github.io/pg_repack/).

## Frequently Asked Questions

### Is pg_repack an extension or a client-side executable like psql or pg_dump?

pg_repack is actually both. [pg_repack/lib](https://github.com/reorg/pg_repack/tree/master/lib) has the code for the extension, including the schema and SQL artifacts it creates, and the C library implementing the code of several of those functions.

On the other hand, [pg_repack/bin](https://github.com/reorg/pg_repack/tree/master/bin) has the code for the client application, which knows how to interact with the programmability elements implemented in the extension. This client application aims to ease the complexity of interacting with the different interfaces surfaced by the server-side extension. It offers the user some command-line options which are easier to understand. The client application is useless without the extension created on the database it's being pointing to. The server side extension on its own would be fully functional, but would require the user to understand a complicated interaction pattern. That pattern would consist on executing queries to retrieve data that is used as input to functions implemented by the extension, etc.

## Related content

- [Autovacuum tuning in Azure Database for PostgreSQL flexible server](how-to-autovacuum-tuning.md).
