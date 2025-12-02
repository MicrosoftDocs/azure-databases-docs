---
title: Encrypted Connectivity with TLS/SSL
description: This article describes how to connect using TLS/SSL in an Azure Database for PostgreSQL flexible server instance.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# Encrypted connectivity using TLS/SSL

You can connect your client applications to an Azure Database for PostgreSQL flexible server instance using Transport Layer Security (TLS), previously known as Secure Sockets Layer (SSL). TLS is an industry standard protocol that ensures encrypted network connections between your database server and client applications, allowing you to adhere to compliance requirements.

Azure Database for PostgreSQL supports encrypted connections using Transport Layer Security (TLS 1.2+). All incoming connections which try to encrypt the traffic using TLS 1.0 and TLS 1.1 are denied.

For all Azure Database for PostgreSQL flexible server instances, enforcement of TLS connections is enabled.

> [!NOTE]  
> By default, secured connectivity between the client and the server is enforced. If you want to disable the enforcement of TLS/SSL, allowing both encrypted and unencrypted client communications, you can change the server parameter `require_secure_transport` to `OFF`. You can also set TLS version by setting the `ssl_max_protocol_version` server parameter.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Applications that require certificate verification for TLS/SSL connectivity

In some cases, applications require a local certificate file generated from a trusted Certificate Authority (CA) certificate file, so that they can connect securely. For more information on downloading root CA certificates, see [Configure SSL on the client](../security/security-tls.md#configure-ssl-on-the-client).

**Detailed information on updating client applications certificate stores with new Root CA certificates has been documented in this [how-to document](../flexible-server/how-to-update-client-certificates-java.md)**.

> [!NOTE]  
> Azure Database for PostgreSQL doesn't support [custom SSL\TLS certificates](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CERTIFICATE-CREATION).

### Connect using psql

If you created your Azure Database for PostgreSQL flexible server instance with **Private access (VNet Integration)** networking mode, you must connect to your server from a resource within the same virtual network as your server, or from one that can route traffic to the virtual network in which your server is integrated.

If you created your Azure Database for PostgreSQL flexible server instance with **Public access (allowed IP addresses)**, you can add a firewall rule with your public IP address, so that you're allowed to connect to your server. Alternatively, you can create a private endpoint to your instance, and connect through that private endpoint.

The following example shows how to connect to your server using the psql command-line interface. Use the `sslmode=verify-full` connection string setting to enforce TLS/SSL certificate verification. Pass the local certificate file path to the `sslrootcert` parameter.

```bash
 psql "sslmode=verify-full sslrootcert=c:\\ssl\DigiCertGlobalRootCA.crt.pem host=mydemoserver.postgres.database.azure.com dbname=postgres user=myadmin"
```

> [!NOTE]  
> Confirm that the value passed to `sslrootcert` matches the file path for the certificate you saved.

## Ensure your application or framework supports TLS connections

Some application frameworks that use PostgreSQL for their database services don't enable TLS by default during installation. Your Azure Database for PostgreSQL flexible server instance enforces TLS connections, but if the application isn't configured for TLS, the application might fail to connect to your database server. Consult your application's documentation to learn how to enable TLS connections.

## Related content

- [Networking](../network/how-to-networking.md)
- [Network with private access for Azure Database for PostgreSQL](../network/concepts-networking-private.md)
- [Firewall rules](../network/concepts-networking-public.md#firewall-rules)
