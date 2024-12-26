---
title: Encrypted connectivity using TLS/SSL
description: Instructions and information on how to connect using TLS/SSL in Azure Database for PostgreSQL - Flexible Server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 12/03/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Encrypted connectivity using Transport Layer Security in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server supports connecting your client applications to Azure Database for PostgreSQL flexible server using Transport Layer Security (TLS), previously known as Secure Sockets Layer (SSL). TLS is an industry standard protocol that ensures encrypted network connections between your database server and client applications, allowing you to adhere to compliance requirements.

Azure Database for PostgreSQL flexible server supports encrypted connections using Transport Layer Security (TLS 1.2+) and all incoming connections with TLS 1.0 and TLS 1.1 will be denied. For all Azure Database for PostgreSQL flexible server instances enforcement of TLS connections is enabled. 

>[!Note]
> By default, secured connectivity between the client and the server is enforced. If you want to disable the enforcement of TLS/SSL, allowing both encrypted and unencrypted client communications, you can change the server parameter *require_secure_transport* to *OFF*. You can also set TLS version by setting *ssl_max_protocol_version* server parameters.

## Applications that require certificate verification for TLS/SSL connectivity
In some cases, applications require a local certificate file generated from a trusted Certificate Authority (CA) certificate file to connect securely. For more information on downloading root CA certificates you can **[visit this document](concepts-networking-ssl-tls.md#configure-ssl-on-the-client)**.
**Detailed information on updating client applications certificate stores with new Root CA certificates has been documented in this [how-to document](../flexible-server/how-to-update-client-certificates-java.md)**. 

> [!NOTE]
> Azure Database for PostgreSQL - Flexible server doesn't support [custom SSL\TLS certificates](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CERTIFICATE-CREATION) at this time.

### Connect using psql
If you created your Azure Database for PostgreSQL flexible server instance with *Private access (VNet Integration)*, you will need to connect to your server from a resource within the same VNet as your server. You can create a virtual machine and add it to the VNet created with your Azure Database for PostgreSQL flexible server instance.

If you created your Azure Database for PostgreSQL flexible server instance with *Public access (allowed IP addresses)*, you can add your local IP address to the list of firewall rules on your server.

The following example shows how to connect to your server using the psql command-line interface. Use the `sslmode=verify-full` connection string setting to enforce TLS/SSL certificate verification. Pass the local certificate file path to the `sslrootcert` parameter.

```bash
 psql "sslmode=verify-full sslrootcert=c:\\ssl\DigiCertGlobalRootCA.crt.pem host=mydemoserver.postgres.database.azure.com dbname=postgres user=myadmin"
```
> [!Note]
> Confirm that the value passed to *sslrootcert* matches the file path for the certificate you saved.

## Ensure your application or framework supports TLS connections

Some application frameworks that use PostgreSQL for their database services do not enable TLS by default during installation. Your Azure Database for PostgreSQL flexible server instance enforces TLS connections but if the application is not configured for TLS, the application may fail to connect to your database server. Consult your application's documentation to learn how to enable TLS connections.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Create and manage Azure Database for PostgreSQL - Flexible Server virtual network using Azure CLI](how-to-manage-virtual-network-cli.md).
- Learn more about [networking in Azure Database for PostgreSQL - Flexible Server](concepts-networking.md)
- Understand more about [Azure Database for PostgreSQL - Flexible Server firewall rules](concepts-networking.md#public-access-allowed-ip-addresses)
