---
title: Read and read/write privileges with secondary native users
description: Learn how to create and configure secondary native users with read and read/write privileges in Azure DocumentDB. Discover how to delegate access securely and get started today.
author: sajeetharan
ms.author: sasinnat
ms.topic: feature-guide
ms.date: 09/24/2025
ms.custom:
  - sfi-ropc-nochange
---

# Read and read/write privileges with secondary native users on Azure DocumentDB

Azure DocumentDB supports secondary native [DocumentDB](oss.md) users with specialized read-write and read-only roles, enabling secure delegation of data access. The built-in administrative account, created during cluster provisioning, has full privileges, including user management. Secondary users are automatically replicated to cluster replicas, but user management must be performed on the primary cluster.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- MongoDB Shell. For more information, see [install MongoDB shell](https://www.mongodb.com/try/download/shell)

- Firewall rules that allow your client to connect to the cluster. For more information, see [configure firewall](how-to-configure-firewall.md).

## Native roles

Azure DocumentDB supports native role-based access control for secondary users with the following roles:

| | Description |
| --- | --- |
| **`readWriteAnyDatabase`** | Full read-write permissions, including database management |
| **`clusterAdmin`** | Full read-write permissions, including database management |
| **`readAnyDatabase`** | Read-only permissions |

Manage users and roles using MongoDB drivers or tools like MongoDB Shell (`mongosh`).

> [!NOTE]
> Only full read-write users with both database management and operations privileges are supported. Roles can't be assigned separately.

## Authenticate and perform operations via MongoDB Shell

Authenticate using the built-in administrative account created during cluster provisioning. This account has exclusive user management privileges (`userAdmin`) on the cluster.

1. Open a terminal on a client with MongoDB shell installed.

1. Get the **name** of your Azure DocumentDB cluster and your current credentials.

    > [!TIP]
    > You can get the native connection string for the cluster in the Azure portal using the **Connection strings** section.

1. Connect by using the following connection string:
    
    ```console
    mongosh "mongodb+srv://<username>:<password>@<cluster-name>?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    ```

## Manage users

Creates a new user on the cluster where you run the command. The `createUser` command returns a duplicate user error if the user already exists.

1. Create a data plane administrative user.

    ```mongo
    db.runCommand(
      {
        createUser:"yourUserName",
        pwd : "yourPassword",
        roles : [
          { role:"clusterAdmin",db:"admin" },
          { role:"readWriteAnyDatabase", db:"admin" }
        ]
      }
    )
    ```

1. Create a read-only user.

    ```mongo
    db.runCommand(
      {
        createUser:"yourUserName",
        pwd : "yourPassword",
        roles : [
          { role:"readAnyDatabase",db:"admin" }
        ]
      }
    )
    ```

1. Update a user on the database by running the `updateUser` command.

    ```mongo
    use admin
    
    db.runCommand(
      {
        updateUser:"<username>",
        pwd : "<new cleartext password>"
      }
    )
    ```

    > [!NOTE]
    > The command supports only updating the password.

1. Remove a user from the cluster.

    ```mongo
    use admin
    
    db.runCommand(
      {
        dropUser:"<username>"
      }
    )
    ```

1. Retrieve details about all native users on the cluster or specify a single user to get information about their roles and other attributes.

    ```mongo
    use admin
    
    db.runCommand(
      {
        usersInfo:1
      }
    )
    ```

## Related content

- Learn about [security in Azure DocumentDB](security.md)
- Check [limitations](limitations.md#native-documentdb-secondary-users)
- Learn about [Microsoft Entra ID in Azure DocumentDB](how-to-connect-role-based-access-control.md)
