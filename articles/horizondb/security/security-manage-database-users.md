---
title: Manage User in Azure HorizonDB
description: This article describes how you can create new user accounts to interact with an Azure HorizonDB cluster.
#customer intent: As a user, I want to create additional admin users in Azure HorizonDB, so that I can delegate administrative responsibilities across my team.
author: DDL-PM
ms.author: ludingding
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# Manage users in Azure HorizonDB (Preview)

This article describes how to create users within an Azure HorizonDB cluster.

To learn how to create and manage Azure subscription users and their privileges, see [Azure role-based access control (Azure RBAC) article](/azure/role-based-access-control/built-in-roles) or review [how to customize roles](/azure/role-based-access-control/custom-roles).

## The server admin account

When you first create your Azure HorizonDB cluster, you provide a cluster administrator authentication name and password. For more information, see [Create an Azure HorizonDB cluster](../configure-maintain/quickstart-create-cluster.md) to see the step-by-step approach. Because the cluster administrator authentication name is a custom name, you can find the chosen server admin user name in the Azure portal.

The Azure HorizonDB cluster is created with three default roles. You can see these roles by running the command: `SELECT rolname FROM pg_roles;`

- azure_pg_admin
- azuresu
- your server admin user

Your administrator authentication is a member of the `azure_pg_admin` role. However, the admin account isn't part of the `azuresu` role. Since this service is a managed PaaS service, only Microsoft is part of the super user role.

The PostgreSQL engine uses privileges to control access to database objects, as discussed in the [PostgreSQL product documentation](https://www.postgresql.org/docs/current/sql-createrole.html). In Azure HorizonDB, the server admin user is granted these privileges: LOGIN, NOSUPERUSER, INHERIT, CREATEDB, and CREATEROLE.

The cluster administrator authentication can create more users and grant those users the `azure_pg_admin` role. Also, the cluster administrator authentication can create less privileged users and roles that have access to individual databases and schemas.

## How to create more admin users in Azure HorizonDB

1. Get the connection information and admin user name.
   You need the full server name and admin sign-in credentials to connect to your Azure HorizonDB cluster. You can easily find the server name and sign-in information from the server **Overview** page or the **Properties** page in the Azure portal.

1. Use the admin account and password to connect to your Azure HorizonDB cluster. Use your preferred client tool, such as pgAdmin or psql.
   If you're unsure of how to connect, see [Create an Azure HorizonDB cluster](../configure-maintain/quickstart-create-cluster.md).

1. Edit and run the following SQL code. Replace your new user name with the placeholder value `<new_user>`, and replace the placeholder password with your own strong password.

   ```sql
   CREATE USER <new_user> CREATEDB CREATEROLE PASSWORD '<StrongPassword!>';

   GRANT azure_pg_admin TO <new_user>;
   ```

## How to create database users in Azure HorizonDB

1. Get the connection information and admin user name.
   You need the full server name and admin sign-in credentials to connect to your Azure HorizonDB cluster. You can easily find the server name and sign-in information from the server **Overview** page or the **Properties** page in the Azure portal.

1. Use the admin account and password to connect to your Azure HorizonDB cluster. Use your preferred client tool, such as [PostgreSQL for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql), pgAdmin, or psql.

1. Edit and run the following SQL code. Replace the placeholder value `<db_user>` with your intended new user name and placeholder value `<newdb>` with your own database name. Replace the placeholder password with your own strong password.

   This SQL code creates a new database, then it creates a new user in the Azure HorizonDB cluster and grants connect privilege to the new database for that user.

   ```sql
   CREATE DATABASE <newdb>;

   CREATE USER <db_user> PASSWORD '<StrongPassword!>';

   GRANT CONNECT ON DATABASE <newdb> TO <db_user>;
   ```

1. Using an admin account, you might need to grant other privileges to secure the objects in the database. For more information, refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/current/ddl-priv.html) for further details on database roles and privileges. For example:

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE <newdb> TO <db_user>;
   ```

   If a user creates a table "role," the table belongs to that user. If another user needs access to the table, you must grant privileges to the other user on the table level.

   For example:

   ```sql
   GRANT SELECT ON ALL TABLES IN SCHEMA <schema_name> TO <db_user>;
   ```

1. Sign in to your server, specifying the designated database, using the new username and password. This example shows the psql command line. With this command, you're prompted for the password for the user name. Replace your own server name, database name, and user name.

   ```bash
   psql --host="{clustername}.{clusteridentifier}.{region}.horizondb.azure.com" --port=5432 --username=db_user --dbname=newdb
   ```

## Related content

- [Networking in Azure HorizonDB (Preview)](../network/how-to-network.md)
- [Database Roles and Privileges](https://www.postgresql.org/docs/current/user-manag.html)
- [GRANT Syntax](https://www.postgresql.org/docs/current/sql-grant.html)
- [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
