---
title: SCRAM Auhtentication in Azure Database for PostgreSQL Flexible Server
description: Instructions and information on how to configure and connect using SCRAM in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to configure SCRAM authentication in Azure Database for PostgreSQL flexible server, so that I can add extra security and prevent password sniffing on untrusted connections.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
---

# SCRAM authentication in Azure Database for PostgreSQL flexible server

Salted Challenge Response Authentication Mechanism (SCRAM) is a password-based mutual authentication protocol. It's a challenge-response scheme that adds several levels of security and prevents password sniffing on untrusted connections. SCRAM supports storing passwords on the server in a cryptographically hashed form, which provides advanced security.

> [!NOTE]  
> To access an Azure Database for PostgreSQL flexible server by using the SCRAM method of authentication, your client libraries need to support SCRAM. For more information, see the **[list of drivers](https://wiki.postgresql.org/wiki/List_of_drivers)** that support SCRAM.

SCRAM authentication adds extra computational load to your application servers, which need to compute the client proof for each authentication. You might reduce the performance overhead SCRAM introduces by limiting the number of connections in your application's connection pool (reducing chattiness in your application) or limiting the number of concurrent transactions that your client allows (bigger transactions). Test your workloads before migrating to SCRAM authentication.

## Configure SCRAM authentication

### Go to Parameters

To configure SCRAM authentication, access the Parameters page in the Azure portal:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Go to your Azure Database for PostgreSQL flexible server.
1. In the left-hand menu under **Settings**, select **Parameters**.
1. Use the search box to find the parameters mentioned in the following steps.

### Configuration steps

1. Change `password_encryption` to `SCRAM-SHA-256`. Currently, Azure Database for PostgreSQL only supports SCRAM using SHA-256.

    :::image type="content" source="media/security-connect-scram/1-password-encryption.png" alt-text="Screenshot of encryption page for SCRAM.":::

1. Allow `SCRAM-SHA-256` as the authentication method.

    :::image type="content" source="media/security-connect-scram/2-authentication-method.png" alt-text="Screenshot of authentication reached by SCRAM.":::

    > [!IMPORTANT]
    > You can enforce SCRAM only authentication by selecting only the `SCRAM-SHA-256` method. When you enforce this method, users with MD5 authentication can't connect to the server. Before you enforce SCRAM, make sure both MD5 and `SCRAM-SHA-256` are authentication methods until you update all user passwords to `SCRAM-SHA-256`. You can verify the authentication type for users by using the query mentioned in step 7.

1. Save the changes. These properties are dynamic and don't require a server restart.

1. From your Azure Database for PostgreSQL flexible server client, connect to the Azure Database for PostgreSQL flexible server. For example,

    ```bash
    psql "host=myPGServer.postgres.database.azure.com port=5432 dbname=postgres user=myDemoUser password=<password> sslmode=require"

    psql (12.3 (Ubuntu 12.3-1.pgdg18.04+1), server 12.6)
    SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
    Type "help" for help.
    ```

1. Verify the password encryption.

    ```sql
    postgres=> show password_encryption;
       password_encryption
    ---------------------
    scram-sha-256
    (1 row)
    ```

1. Update the password for users.

    ```sql
    postgres=> \password myDemoUser
    Enter new password:
    Enter it again:
    postgres=>
    ```

1. Verify user authentication types by using the `azure_roles_authtype()` function.

    ```sql
    postgres=> SELECT * from azure_roles_authtype();
             rolename          | authtype
    ---------------------------+-----------
    azuresu                   | NOLOGIN
    pg_monitor                | NOLOGIN
    pg_read_all_settings      | NOLOGIN
    pg_read_all_stats         | NOLOGIN
    pg_stat_scan_tables       | NOLOGIN
    pg_read_server_files      | NOLOGIN
    pg_write_server_files     | NOLOGIN
    pg_execute_server_program | NOLOGIN
    pg_signal_backend         | NOLOGIN
    replication               | NOLOGIN
    myDemoUser                | SCRAM-256
    azure_pg_admin            | NOLOGIN
    srtest                    | SCRAM-256
    sr_md5                    | MD5
    (14 rows)
    ```

1. Connect from the client that supports SCRAM authentication to your server.

   SCRAM authentication is also supported when connected to the built-in managed [PgBouncer](../connectivity/concepts-pgbouncer.md).

## Related content

- [Networking](../network/how-to-networking.md)
- [Network with private access for Azure Database for PostgreSQL](../network/concepts-networking-private.md)
- [Firewall rules](../network/concepts-networking-public.md#firewall-rules)
