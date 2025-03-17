---
title: Networking overview using SSL and TLS
description: Learn about secure connectivity with Azure Database for PostgreSQL flexible server using SSL and TLS.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 05/02/2024
ms.service: azure-database-postgresql
ms.subservice: 
ms.topic: conceptual

---

# Secure connectivity with TLS and SSL in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server enforces connecting your client applications to Azure Database for PostgreSQL flexible server by using Transport Layer Security (TLS). TLS is an industry-standard protocol that ensures encrypted network connections between your database server and client applications. TLS is an updated protocol of Secure Sockets Layer (SSL).

## What is TLS?

TLS was made from Netscape's SSL protocol and has regularly replaced it. The terms SSL or TLS/SSL are still sometimes used interchangeably. TLS is made of two layers: the TLS record show and the TLS handshake show. The record show gives association security. The handshake show empowers the server and customer to affirm one another and to coordinate encryption assessments and cryptographic keys before any information is traded.

:::image type="content" source="./media/concepts-networking/tls-1-2.png" alt-text="Diagram that shows typical TLS 1.2 handshake sequence." lightbox="./media/concepts-networking/tls-1-2.png":::

The preceding diagram shows a typical TLS 1.2 handshake sequence, which consists of these steps:

1. The client starts by sending a message called `ClientHello` that expresses willingness to communicate via TLS 1.2 with a set of cipher suites that the client supports.
1. The server receives the message, answers with `ServerHello`, and agrees to communicate with the client via TLS 1.2 by using a particular cipher suite.
1. The server also sends its key share. The specifics of this key share change based on the cipher suite that was selected. For the client and server to agree on a cryptographic key, they need to receive each other's portion, or share.
1. The server sends the certificate (signed by the certificate authority [CA]) and a signature on portions of `ClientHello` and `ServerHello`. It also includes the key share. In this way, the client knows that they're authentic.
1. After the client successfully receives the data and then generates its own key share, it mixes it with the server key share to generate encryption keys for the session.
1. The client sends the server its key share, enables encryption, and sends a `Finished` message. This message is a hash of a transcript of what has happened so far. The server does the same. It mixes the key shares to get the key and sends its own `Finished` message.
1. Now application data can be sent encrypted on the connection.

## Certificate chains

A *certificate chain* is an ordered list of certificates that contain an TLS/SSL certificate and CA certificates. They enable the receiver to verify that the sender and all CAs are trustworthy. The chain or path begins with the TLS/SSL certificate. Each certificate in the chain is signed by the entity identified by the next certificate in the chain.

The chain terminates with a *root CA certificate*. This certificate is always signed by the CA itself. The signatures of all certificates in the chain must be verified up to the root CA certificate.

Any certificate that sits between the TLS/SSL certificate and the root CA certificate in the chain is called an intermediate certificate.

## TLS versions

Several government entities worldwide maintain guidelines for TLS regarding network security. In the United States, these organizations include the Department of Health and Human Services and the National Institute of Standards and Technology. The level of security that TLS provides is most affected by the TLS protocol version and the supported cipher suites.

A cipher suite is a set of algorithms that include a cipher, a key-exchange algorithm, and a hashing algorithm. They're used together to establish a secure TLS connection. Most TLS clients and servers support multiple alternatives. They have to negotiate when they establish a secure connection to select a common TLS version and cipher suite.

Azure Database for PostgreSQL supports TLS version 1.2 and later. In [RFC 8996](https://datatracker.ietf.org/doc/rfc8996/), the Internet Engineering Task Force (IETF) explicitly states that TLS 1.0 and TLS 1.1 must not be used. Both protocols were deprecated by the end of 2019.

All incoming connections that use earlier versions of the TLS protocol, such as TLS 1.0 and TLS 1.1, are denied by default.

The IETF released the TLS 1.3 specification in RFC 8446 in August 2018, and TLS 1.3 is now the most common and recommended TLS version in use. TLS 1.3 is faster and more secure than TLS 1.2.

> [!NOTE]
> SSL and TLS certificates certify that your connection is secured with state-of-the-art encryption protocols. By encrypting your connection on the wire, you prevent unauthorized access to your data while in transit. We strongly recommend that you use the latest versions of TLS to encrypt your connections to Azure Database for PostgreSQL flexible server.
>
> Although we don't recommend it, if needed, you can disable TLS\SSL for connections to Azure Database for PostgreSQL flexible server. You can update the `require_secure_transport` server parameter to `OFF`. You can also set the TLS version by setting `ssl_min_protocol_version` and `ssl_max_protocol_version` server parameters.

[Certificate authentication](https://www.postgresql.org/docs/current/auth-cert.html) is performed by using SSL client certificates for authentication. In this scenario, the PostgreSQL server compares the common name (CN) attribute of the client certificate presented against the requested database user.

At this time, Azure Database for PostgreSQL flexible server doesn't support:

- SSL certificate-based authentication.
- [Custom SSL\TLS certificates](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CERTIFICATE-CREATION).

> [!NOTE]
> Microsoft made root CA changes for various Azure services, including Azure Database for PostgreSQL flexible server. For more information, see [Azure TLS certificate changes](/azure/security/fundamentals/tls-certificate-changes) and the section [Configure SSL on the client](#configure-ssl-on-the-client).

To determine your current TLS\SSL connection status, you can load the [sslinfo extension](../extensions/concepts-extensions-versions.md#sslinfo) and then call the `ssl_is_used()` function to determine if SSL is being used. The function returns `t` if the connection is using SSL. Otherwise, it returns `f`. You can also collect all the information about your Azure Database for PostgreSQL flexible server's SSL usage by process, client, and application by using the following query:

```sql
SELECT datname as "Database name", usename as "User name", ssl, client_addr, application_name, backend_type
   FROM pg_stat_ssl
   JOIN pg_stat_activity
   ON pg_stat_ssl.pid = pg_stat_activity.pid
   ORDER BY ssl;
```

For testing, you can also use the `openssl` command directly:

```bash
openssl s_client -starttls postgres -showcerts -connect <your-postgresql-server-name>:5432
```

This command prints low-level protocol information, like the TLS version and cipher. You must use the option `-starttls postgres`. Otherwise, this command reports that no SSL is in use. Using this command requires at least OpenSSL 1.1.1.

To enforce the latest, most secure TLS version for connectivity protection from the client to Azure Database for PostgreSQL flexible server, set `ssl_min_protocol_version` to `1.3`. That setting *requires* clients that connect to your Azure Database for PostgreSQL flexible server to use *this version of the protocol only* to securely communicate. Older clients might not be able to communicate with the server because they don't support this version.

## Configure SSL on the client

By default, PostgreSQL doesn't perform any verification of the server certificate. For this reason, it's possible to spoof the server identity (for example, by modifying a DNS record or by taking over the server IP address) without the client knowing. All SSL options carry overhead in the form of encryption and key exchange, so a trade-off is made between performance and security.

To prevent spoofing, SSL certificate verification on the client must be used.

There are many connection parameters for configuring the client for SSL. A few important ones are:

- `ssl`: Connect using SSL. This property doesn't need a value associated with it. The mere presence of it specifies an SSL connection. For compatibility with future versions, the value `true` is preferred. In this mode, when you're establishing an SSL connection, the client driver validates the server's identity to prevent man-in-the-middle attacks. It checks that the server certificate is signed by a trusted authority and that the host you're connecting to is the same as the host name in the certificate.
- `sslmode`: If you require encryption and want the connection to fail if it can't be encrypted, set `sslmode=require`. This setting ensures that the server is configured to accept SSL connections for this host/IP address and that the server recognizes the client certificate. If the server doesn't accept SSL connections or the client certificate isn't recognized, the connection fails. The following table lists values for this setting:

    | SSL mode | Explanation |
    |----------|-------------|
    |`disable`   | Encryption isn't used.|
    |`allow`     | Encryption is used if server settings require or enforce it.|
    |`prefer`    | Encryption is used if server settings allow for it.|
    |`require`   | Encryption is used. It ensures that the server is configured to accept SSL connections for this host IP address and that the server recognizes the client certificate.|
    |`verify-ca`| Encryption is used. Verify the server certificate signature against the certificate stored on the client.|
    |`verify-full`| Encryption is used. Verify the server certificate signature and host name against the certificate stored on the client.|
    
    The default `sslmode` mode used is different between libpq-based clients (such as psql) and JDBC. The libpq-based clients default to `prefer`. JDBC clients default to `verify-full`.

- `sslcert`, `sslkey`, and `sslrootcert`: These parameters can override the default location of the client certificate, the PKCS-8 client key, and the root certificate. They default to `/defaultdir/postgresql.crt`, `/defaultdir/postgresql.pk8`, and `/defaultdir/root.crt`, respectively, where `defaultdir` is `${user.home}/.postgresql/` in nix systems and `%appdata%/postgresql/` on Windows.

CAs are the institutions responsible for issuing certificates. A trusted certificate authority is an entity that's entitled to verify that someone is who they say they are. For this model to work, all participants must agree on a set of trusted CAs. All operating systems and most web browsers ship with a set of trusted CAs.

Using `verify-ca` and `verify-full` `sslmode` configuration settings can also be known as [certificate pinning](/azure/security/fundamentals/certificate-pinning#how-to-address-certificate-pinning-in-your-application). In this case, root CA certificates on the PostgreSQL server have to match the certificate signature and even the host name against the certificate on the client.

You might periodically need to update client-stored certificates when CAs change or expire on PostgreSQL server certificates. To determine if you're pinning CAs, see [Certificate pinning and Azure services](/azure/security/fundamentals/certificate-pinning#how-to-address-certificate-pinning-in-your-application).

For more on SSL\TLS configuration on the client, see [PostgreSQL documentation](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CLIENT-CERTIFICATES).

For clients that use `verify-ca` and `verify-full` `sslmode` configuration settings (that is, certificate pinning), they must deploy *three* root CA certificates to the client certificate stores:

- [DigiCert Global Root G2](https://www.digicert.com/kb/digicert-root-certificates.htm) and [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/docs/repository.htm) root CA certificates, because services are migrating from Digicert to Microsoft CA.
- [Digicert Global Root CA](https://www.digicert.com/kb/digicert-root-certificates.htm), for legacy compatibility.

### Download root CA certificates and update application clients in certificate pinning scenarios

To update client applications in certificate pinning scenarios, you can download certificates:

 * [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
 * [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem)
 * [Digicert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt)

To import certificates to client certificate stores, you might have to convert certificate .crt files to .pem format after you download certificate files from the preceding URIs. You can use the OpenSSL utility to do these file conversions:

```powershell
openssl x509 -inform DER -in certificate.crt -out certificate.pem -outform PEM
```

Information on updating client applications certificate stores with new root CA certificates is documented in [Update client TLS certificates for application clients](/azure/postgresql/flexible-server/how-to-update-client-certificates-java).

> [!IMPORTANT]
> Some of the Postgres client libraries, while using the `sslmode=verify-full` setting, might experience connection failures with root CA certificates that are cross-signed with intermediate certificates. The result is alternate trust paths. In this case, we recommend that you explicitly specify the `sslrootcert` parameter. Or, set the `PGSSLROOTCERT` environment variable to a local path where the Microsoft RSA Root CA 2017 root CA certificate is placed, from the default value of `%APPDATA%\postgresql\root.crt`.

### Read replicas with certificate pinning scenarios

With root CA migration to [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/docs/repository.htm), it's feasible for newly created replicas to be on a newer root CA certificate than the primary server that was created earlier. For clients that use `verify-ca` and `verify-full` `sslmode` configuration settings (that is, certificate pinning), it's imperative for interrupted connectivity to accept three root CA certificates:

- [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
- [DigiCert Global Root G2](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem)
- [Digicert Global Root CA](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt)

At this time, Azure Database for PostgreSQL flexible server doesn't support [certificate-based authentication](https://www.postgresql.org/docs/current/auth-cert.html).

### Test client certificates by connecting with psql in certificate pinning scenarios

You can use the `psql` command line from your client to test connectivity to the server in certificate pinning scenarios:

```bash

$ psql "host=hostname.postgres.database.azure.com port=5432 user=myuser dbname=mydatabase sslmode=verify-full sslcert=client.crt sslkey=client.key sslrootcert=ca.crt"

```

For more on SSL and certificate parameters, see [psql documentation](https://www.postgresql.org/docs/current/app-psql.html).

## Test TLS/SSL connectivity

Before you try to access your SSL-enabled server from a client application, make sure you can get to it via psql. If you established an SSL connection, you should see output similar to the following example:

*psql (14.5)*
*SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)*
*Type "help" for help.*

You can also load the [sslinfo extension](../extensions/concepts-extensions-versions.md#sslinfo) and then call the `ssl_is_used()` function to determine if SSL is being used. The function returns `t` if the connection is using SSL. Otherwise, it returns `f`.

## Cipher suites

A *cipher suite* is a set of cryptographic algorithms. TLS/SSL protocols use algorithms from a cipher suite to create keys and encrypt information.

A cipher suite is displayed as a long string of seemingly random information, but each segment of that string contains essential information. Generally, this data string includes several key components:

- Protocol (that is, TLS 1.2 or TLS 1.3)
- Key exchange or agreement algorithm
- Digital signature (authentication) algorithm
- Bulk encryption algorithm
- Message authentication code algorithm (MAC)

Different versions of TLS/SSL support different cipher suites. TLS 1.2 cipher suites can't be negotiated with TLS 1.3 connections, and vice versa.

At this time, Azure Database for PostgreSQL flexible server supports many cipher suites with the TLS 1.2 protocol version that fall into the [HIGH:!aNULL](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-SSL-CIPHERS) category.

## Troubleshoot TLS/SSL connectivity errors

1. The first step to troubleshoot TLS/SSL protocol version compatibility is to identify the error messages that you or your users are seeing when they try to access your Azure Database for PostgreSQL flexible server under TLS encryption from the client. Depending on the application and platform, the error messages might be different. In many cases, they point to the underlying issue.
1. To be certain of TLS/SSL protocol version compatibility, check the TLS/SSL configuration of the database server and the application client to make sure they support compatible versions and cipher suites.
1. Analyze any discrepancies or gaps between the database server and the client's TLS/SSL versions and cipher suites. Try to resolve them by enabling or disabling certain options, upgrading or downgrading software, or changing certificates or keys. For example, you might need to enable or disable specific TLS/SSL versions on the server or the client, depending on security and compatibility requirements. For example, you might need to disable TLS 1.0 and TLS 1.1, which are considered nonsecure and deprecated, and enable TLS 1.2 and TLS 1.3, which are more secure and modern.
1. The newest certificate issued with [Microsoft RSA Root CA 2017 has intermediate in the chain cross-signed by Digicert Global Root G2 CA](https://www.microsoft.com/pkiops/docs/repository.htm). Some of the Postgres client libraries, while using `sslmode=verify-full` or `sslmode=verify-ca` settings, might experience connection failures with root CA certificates that are cross-signed with intermediate certificates. The result is alternate trust paths.

   To work around these issues, add all three necessary certificates to the client certificate store or explicitly specify the `sslrootcert` parameter. Or, set the `PGSSLROOTCERT` environment variable to the local path where the Microsoft RSA Root CA 2017 root CA certificate is placed, from the default value of `%APPDATA%\postgresql\root.crt`.

## Related content

- Learn how to create an Azure Database for PostgreSQL flexible server by using the **Private access (VNet integration)** option in the [Azure portal](how-to-manage-virtual-network-portal.md) or the [Azure CLI](how-to-manage-virtual-network-cli.md).
- Learn how to create an Azure Database for PostgreSQL flexible server by using the **Public access (allowed IP addresses)** option in the [Azure portal](how-to-manage-firewall-portal.md) or the [Azure CLI](how-to-manage-firewall-cli.md).
