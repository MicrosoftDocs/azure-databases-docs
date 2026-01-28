---
ms.topic: include
ms.date: 10/14/2025
---

Verify that you're successfully connected to your cluster by performing a series of test commands and queries.

1. Check your connection status by running the `connectionStatus` command.

    ```mongo
    db.runCommand({connectionStatus: 1})
    ```

    ```output
    {
      ...
      ok: 1
    }
    ```

1. List the databases in your cluster.

    ```mongo
    show dbs
    ```

1. Switch to a specific database. Replace the `<database-name>` placeholder with the name of any database in your cluster.

    ```mongo
    use <database-name>
    ```

    > [!TIP]
    > For example, if the database name is `inventory`, then the command would be `use inventory`.

1. List the collections within the database.

    ```mongo
    show collections
    ```

1. Find the first five items within a specific collection. Replace the `<collection-name>` placeholder with the name of any collection in your cluster.

    ```mongo
    db.<collection-name>.find().limit(5)
    ```

    > [!TIP]
    > For example, if the collection name is `equipment`, then the command would be `db.equipment.find().limit(5)`.
