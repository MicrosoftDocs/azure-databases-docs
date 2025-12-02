---
title: Access Management
description: Learn how to manage access permissions for Azure Database for PostgreSQL using roles.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 09/19/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
ms.custom:
  - horz-security
---

# Access management for Azure Database for PostgreSQL

Managing access to your Azure Database for PostgreSQL resources is an important part of maintaining security and compliance. This article explains how to use PostgreSQL roles and Azure features to control permissions and implement best practices for access management.

## Role management

The best way to manage Azure Database for PostgreSQL database access permissions at scale is by using the concept of [roles](https://www.postgresql.org/docs/current/user-manag.html). A role can be either a database user or a group of database users. Roles can own the database objects and assign privileges on those objects to other roles to control who has access to which objects. You can grant membership in a role to another role, which allows the member role to use privileges assigned to another role.
Azure Database for PostgreSQL lets you grant permissions directly to the database users. **As a good security practice, create roles with specific sets of permissions based on minimum application and access requirements. Assign the appropriate roles to each user. Use roles to enforce a *least privilege model* for accessing database objects.**

In addition to the built-in roles that PostgreSQL creates, the Azure Database for PostgreSQL instance includes three default roles. You can see these roles by running the following command:

```sql
SELECT rolname FROM pg_roles;
```
The roles are:

- `azure_pg_admin`
- `azuresu`
- **administrator role**

When you create the Azure Database for PostgreSQL instance, you provide credentials for an **administrator role**. Use this administrator role to create more [PostgreSQL roles](https://www.postgresql.org/docs/current/user-manag.html).

For example, you can create a user or role named `demouser`.

```sql
CREATE USER demouser PASSWORD password123;
```
Don't use the **administrator role** for the application.

In cloud-based PaaS environments, access to an Azure Database for PostgreSQL superuser account is restricted to control plane operations only by cloud operators. Therefore, the `azure_pg_admin` account exists as a pseudo-superuser account. Your administrator role is a member of the `azure_pg_admin` role.
However, the server admin account isn't part of the `azuresu` role, which has superuser privileges and is used to perform control plane operations. Since this service is a managed PaaS service, only Microsoft is part of the superuser role.

You can periodically audit the list of roles in your server.

For example, you can connect by using the `psql` client and query the `pg_roles` table, which lists all the roles along with privileges such as create other roles, create databases, replication, and more.

```sql
select * from pg_roles where rolname='demouser';
-[ RECORD 1 ]--+---------
rolname        | demouser
rolsuper       | f
rolinherit     | t
rolcreaterole  | f
rolcreatedb    | f
rolcanlogin    | f
rolreplication | f
rolconnlimit   | -1
rolpassword    | ********
rolvaliduntil  |
rolbypassrls   | f
rolconfig      |
oid            | 24827
```

> [!IMPORTANT]  
> Recently, Azure Database for PostgreSQL enabled the ability to create **[CAST commands](https://www.postgresql.org/docs/current/sql-createcast.html)**. To run the `CREATE` CAST statement, the user must be a member of the *azure_pg_admin* group. Currently, you can't drop a CAST after you create it.
>
> Azure Database for PostgreSQL only supports CAST commands that use the `WITH FUNCTION` and `WITH INOUT` options. The `WITHOUT FUNCTION` option isn't supported.

[Audit logging in Azure Database for PostgreSQL](../security/security-audit.md) is also available with Azure Database for PostgreSQL to track activity in your databases.

### Control schema access

Newly created databases in Azure Database for PostgreSQL include a default set of privileges in the database's public schema that grant all database users and roles the ability to create objects. To better limit application user access to the databases that you create on your Azure Database for PostgreSQL instance, consider revoking these default public privileges. After revoking these privileges, grant specific privileges to database users on a more granular basis. For example:

- Revoke create privileges to the `public` schema from the `public` role to prevent application database users from creating objects in the public schema.

  ```sql
  REVOKE CREATE ON SCHEMA public FROM PUBLIC;
  ```
- Create a new database.

  ```sql
  CREATE DATABASE Test_db;
  ```
- Revoke all privileges from the PUBLIC schema on this new database.

  ```sql
  REVOKE ALL ON DATABASE Test_db FROM PUBLIC;
  ```
- Create a custom role for application database users.

  ```sql
  CREATE ROLE Test_db_user;
  ```
- Give database users with this role the ability to connect to the database.

  ```sql
  GRANT CONNECT ON DATABASE Test_db TO Test_db_user;
  GRANT ALL PRIVILEGES ON DATABASE Test_db TO Test_db_user;
  ```
- Create a database user.

  ```sql
  CREATE USER user1 PASSWORD 'Password_to_change'
  ```
- Assign the role, with its connect and select privileges, to the user.

  ```sql
  GRANT Test_db_user TO user1;
  ```
In this example, user *user1* can connect and has all privileges in the test database *Test_db*, but not any other database on the server. Instead of giving this user or role *ALL PRIVILEGES* on that database and its objects, consider providing more selective permissions, such as `SELECT`, `INSERT`, `EXECUTE`, and others. For more information about privileges in PostgreSQL databases, see the [GRANT](https://www.postgresql.org/docs/current/sql-grant.html) and [REVOKE](https://www.postgresql.org/docs/current/sql-revoke.html) commands in the PostgreSQL docs.


### Public schema ownership changes in Azure Database for PostgreSQL

In PostgreSQL 15 and later, the ownership of the public schema changed to the new `pg_database_owner` role, which allows database owners to control it. For more information, see the [PostgreSQL release notes](https://www.postgresql.org/docs/release/15.0/).
However, in Azure Database for PostgreSQL, this change doesn't apply. The public schema is owned by the `azure_pg_admin` role across all supported PostgreSQL versions. This managed service behavior provides security and consistency.

### PostgreSQL 16 changes with role based security

In PostgreSQL, the database role can have many attributes that define its privileges. One such attribute is the [**CREATEROLE** attribute](https://www.postgresql.org/docs/current/role-attributes.html), which is important to PostgreSQL database management of users and roles. In PostgreSQL 16, significant changes were introduced to this attribute.

In PostgreSQL 16, users with the **CREATEROLE** attribute no longer have the ability to hand out membership in any role to anyone. Instead, like other users without this attribute, they can only hand out memberships in roles for which they possess `ADMIN OPTION`. Also, in PostgreSQL 16, the **CREATEROLE** attribute still allows a nonsuperuser the ability to provision new users. However, they can only drop users that they themselves created. Attempts to drop users result in an error when the user wasn't created by a user with the **CREATEROLE** attribute.

PostgreSQL 16 also introduces new and improved built-in role. The *pg_create_subscription* role allows superusers to create subscriptions.

In Azure Database for PostgreSQL Flexible server, the azure_pg_admin role is a system-managed, restricted role and cannot be modified by users. Attempts to alter it, such as granting another role to it , will result in an error like:

 ```sql

   GRANT <db_user> TO azure_pg_admin;
 ERROR: permission denied to alter restricted role "azure_pg_admin"
 ```

This is a built-in safeguard to prevent changes to critical administrative roles. If you need to assign privileges or roles, consider creating a custom role instead and granting the necessary permissions to that role.

### Improved control for *azure_pg_admin*

In PostgreSQL 16, a strict role hierarchy structure is implemented for users with the [CREATEROLE](https://www.postgresql.org/docs/16/sql-createrole.html) privilege, specifically related to grant roles. To improve administrative flexibility and address a limitation introduced in PostgreSQL 16, Azure Database for PostgreSQL enhances the capabilities of the *azure_pg_admin* role across all PostgreSQL versions. With this update, members of the *azure_pg_admin* role can manage roles and access objects owned by any nonrestricted role, even if those roles are also members of *azure_pg_admin*. This enhancement ensures that administrative users maintain consistent and comprehensive control over role and permission management, providing a seamless and reliable experience without requiring superuser access.

> [!IMPORTANT]  
> Azure Database for PostgreSQL doesn't allow users to be granted *pg_write_all_data* attribute, which allows user to write all data (tables, views, sequences), as if having `INSERT`, `UPDATE`, and `DELETE` rights on those objects, and USAGE rights on all schemas, even without having it explicitly granted. As a workaround recommended granting similar permissions on a more finite level per database and object.

## Row-level security

[Row-level security (RLS)](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) is an Azure Database for PostgreSQL security feature that enables database administrators to define policies that control how specific rows of data display and operate for one or more roles. Row-level security adds an extra filter to an Azure Database for PostgreSQL database table. When a user tries to perform an action on a table, this filter is applied before the query criteria or other filtering, and the data narrows or rejects according to your security policy. You can create row-level security policies for specific commands like `SELECT`, `INSERT`, `UPDATE`, and `DELETE`, or specify it for all commands. Use cases for row-level security include PCI-compliant implementations, classified environments, and shared hosting or multitenant applications.

Only users with `SET ROW SECURITY` rights can apply row security rights to a table. The table owner can set row security on a table. Like `OVERRIDE ROW SECURITY`, this right is currently an implicit right. Row-level security doesn't override existing `GRANT` permissions. It adds a finer-grained level of control. For example, setting `ROW SECURITY FOR SELECT` to allow a given user to access rows only grants that user access if the user also has `SELECT` privileges on the column or table in question.

The following example shows how to create a policy that ensures only members of the custom-created **manager** [role](#role-management) can access only the rows for a specific account. The code in the following example is shared in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

```sql
CREATE TABLE accounts (manager text, company text, contact_email text);

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY account_managers ON accounts TO managers
  USING (manager = current_user);
```

The `USING` clause implicitly adds a `WITH CHECK` clause, ensuring that members of the manager role can't perform `SELECT`, `DELETE`, or `UPDATE` operations on rows that belong to other managers, and can't `INSERT` new rows belonging to another manager.

You can drop a row security policy by using the `DROP POLICY` command, as shown in this example:

```sql
DROP POLICY account_managers ON accounts;
```
Although you might drop the policy, role manager still can't view any data that belongs to any other manager. This restriction exists because the row-level security policy is still enabled on the accounts table. If row-level security is enabled by default, PostgreSQL uses a default-deny policy.

You can disable row-level security, as shown in the following example:

```sql
ALTER TABLE accounts DISABLE ROW LEVEL SECURITY;
```

## Bypass row-level security

PostgreSQL has **BYPASSRLS** and **NOBYPASSRLS** permissions, which you can assign to a role. NOBYPASSRLS is assigned by default.
With **newly provisioned servers** in Azure Database for PostgreSQL, bypassing row-level security privilege (BYPASSRLS) is implemented as follows:

- For Postgres 16 and later versioned servers, we follow [standard PostgreSQL 16 behavior](#postgresql-16-changes-with-role-based-security). Nonadministrative users created by the **azure_pg_admin** administrator role allow you to create roles with the BYPASSRLS attribute or privilege as necessary.

- For Postgres 15 and earlier versioned servers, you can use the **azure_pg_admin** user to perform administrative tasks that require the BYPASSRLS privilege. However, you can't create nonadmin users with the BypassRLS privilege, since the administrator role has no superuser privileges, as common in cloud-based PaaS PostgreSQL services.

## Related content

- [Secure your Azure Database for PostgreSQL](security-overview.md)
- [Microsoft Entra authentication in Azure Database for PostgreSQL](security-entra-concepts.md)
- [Audit logging in Azure Database for PostgreSQL](security-audit.md)
