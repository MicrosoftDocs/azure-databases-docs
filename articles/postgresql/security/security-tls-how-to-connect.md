---
title: Configure TLS connection to Azure Database for PostgreSQL
description: Learn how to configure Transport Layer Security (TLS) connections to Azure Database for PostgreSQL.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 12/16/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
---

# Connect clients with TLS security to your database

This article explains how to configure Transport Layer Security (TLS) for secure connections between your client applications and Azure Database for PostgreSQL. You learn how to download and install the necessary root certificates, configure client connection settings, and verify that your connections use TLS encryption.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Overview

Connections between your client applications and the database server are always encrypted using industry standard Transport Layer Security (TLS), previously known as Secure Sockets Layer (SSL).

> [!NOTE]
> The open source PostgreSQL uses the legacy name SSL in its commands, variables, and documentation to avoid breaking existing implementations. This document uses the acronym TLS while using SSL in command names and variables.

Azure Database for PostgreSQL supports encrypted connections using TLS 1.2 and 1.3. All incoming connections that try to encrypt the traffic using TLS 1.0 and TLS 1.1 are denied.

By default, secured connectivity between the client and the server is enforced. If you want to disable the enforcement of TLS, allowing both encrypted and unencrypted client communications, you can change the server parameter `require_secure_transport` to `OFF`. You can also set TLS version by setting the `ssl_max_protocol_version` server parameter. We **strongly advise against disabling** TLS.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Client TLS configuration

By default, PostgreSQL doesn't perform any verification of the server certificate. For this reason, it's possible to spoof the server identity (for example, by modifying a DNS record or by taking over the server IP address) without the client knowing. To prevent such spoofing, TLS certificate verification on the client must be used.

There are many connection parameters for configuring the client for TLS. A few important ones are:

- `ssl`: Connect using TLS. This property doesn't need a value associated with it. The mere presence of it specifies a TLS connection. For compatibility with future versions, the value `true` is preferred. In this mode, when you're establishing a TLS connection, the client driver validates the server's identity to prevent man-in-the-middle attacks.
- `sslmode`: If you require encryption and want the connection to fail if it can't be encrypted, set `sslmode=require`. This setting ensures that the server is configured to accept TLS connections for this host/IP address and that the server recognizes the client certificate. If the server doesn't accept TLS connections or the client certificate isn't recognized, the connection fails. The following table lists values for this setting:

  | `sslmode` | Explanation |
  |--|--|
  | `disable` | Encryption isn't used. Azure Database for PostgreSQL requires TLS connections; therefore this setting shall not be used. |
  | `allow` | Encryption is used if server settings require or enforce it. Azure Database for PostgreSQL requires TLS connections; therefore this setting is equivalent to `prefer`. |
  | `prefer` | Encryption is used if server settings allow for it. Azure Database for PostgreSQL requires TLS connections. |
  | `require` | Encryption is used. It ensures that the server is configured to accept TLS connections. |
  | `verify-ca` | Encryption is used. Verify the server certificate against the trusted root certificates stored on the client. |
  | `verify-full` | Encryption is used. Verify the server certificate against the certificate stored on the client. It also validates that the server certificates use the same host name as the connection. We recommend this setting unless private DNS resolvers use a different name to reference the Azure Database for PostgreSQL server. |

The default `sslmode` mode used is different between `libpq`-based clients (such as `PSQL` and `JDBC`). The libpq-based clients default to `prefer`. `JDBC` clients default to `verify-full`.

- `sslcert`, `sslkey`, and `sslrootcert`: These parameters can override the default location of the client certificate, the PKCS-8 client key, and the root certificate. They default to `/defaultdir/postgresql.crt`, `/defaultdir/postgresql.pk8`, and `/defaultdir/root.crt`, respectively, where `defaultdir` is `${user.home}/.postgresql/` in Linux systems and `%appdata%/postgresql/` on Windows.

> [!IMPORTANT]
> Some of the Postgres client libraries, while using the `sslmode=verify-full` setting, might experience connection failures with root CA certificates that are cross-signed with intermediate certificates. The result is alternate trust paths. In this case, we recommend that you explicitly specify the `sslrootcert` parameter. Or, set the `PGSSLROOTCERT` environment variable to a local path where the Microsoft RSA Root CA 2017 root CA certificate is placed, from the default value of `%APPDATA%\postgresql\root.crt`.

## Install trusted root Certificate Authorities (CAs)

### Download and convert root CA certificates

For Windows clients that use the system certificate store for trusted root certificates no action is required since Windows deploys new root CA certificates through Windows Update.

For Java clients, the VS Code extension, and other clients (for example, `PSQL`, Perl, ...) not using the system store, and clients on Linux: you need to download and combine the root CA certificates into a PEM file. At a minimum, includes the following root CA certificates:

- [Microsoft RSA Root CA 2017 (crt file)](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt)
- [DigiCert Global Root G2 (pem file)](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem)

> [!NOTE]
> For China regions and for customers with rotation extensions: [Digicert Global Root CA (pem file)](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem) is still valid; include it in the combined PEM file.

We do strongly recommend including all Azure root CA certificates to reduce the need for future updates to the combined file if there are changes to the root CAs used by Azure Database for PostgreSQL. The list of Azure root CA certificates can be found at [Azure Certificate Authority details](/azure/security/fundamentals/azure-ca-details?tabs=root-and-subordinate-cas-list).

To import certificates to client certificate stores, you may need to convert any CRT-format certificates to PEM format and concatenate the PEM files into a single file. You can use the [OpenSSL X509 utility](https://docs.openssl.org/master/man1/openssl-x509/) to convert the CRT files to PEM.

```bash
openssl x509 -inform DER -in certificate-filename.crt -out certificate-filename.pem -outform PEM
```

### Combine root CA certificates into a single PEM file

For some clients, you concatenate all PEM files into a single file using any text editor or command line tool.

```
-----BEGIN CERTIFICATE-----
(Root CA1 content: DigiCertGlobalRootG2.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA2 content: Microsoft ECC Root Certificate Authority 2017.crt.pem)
-----END CERTIFICATE-----
```

For China regions and for customers with rotation extensions:

```
-----BEGIN CERTIFICATE-----
(Root CA0 content: DigiCertGlobalRootCA.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA1 content: DigiCertGlobalRootG2.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA2 content: Microsoft ECC Root Certificate Authority 2017.crt.pem)
-----END CERTIFICATE-----
```

### Combine and update root CA certificates for Java applications

Custom-written Java applications use a default keystore, called `cacerts`, which contains trusted certificate authority (CA) certificates. A certificates file named `cacerts` resides in the security properties directory, java.home\lib\security, where java.home is the runtime environment directory (the `jre` directory in the SDK or the top-level directory of the Java™ 2 Runtime Environment).
You can use following directions to update client root CA certificates for client certificate pinning scenarios with PostgreSQL:

1. Check `cacerts` java keystore to see if it already contains required certificates. You can list certificates in Java keystore by using following command:

    ```powershell
    keytool -list -v -keystore ..\lib\security\cacerts > outputfile.txt
    ```

    If the necessary certificates aren't present in the java key store on the client, as can be checked in output, you should proceed with following directions:

1. Make a backup copy of your custom keystore.

1. [Download the certificate files](#download-and-convert-root-ca-certificates), and save them locally where you can reference them.

1. Generate a combined CA certificate store with all needed Root CA certificates are included. Example below shows using DefaultJavaSSLFactory for PostgreSQL Java users.

    ```bash
    keytool -importcert -alias PostgreSQLServerCACert  -file "DigiCertGlobalRootG2.crt.pem" -keystore truststore -storepass password -noprompt

    keytool -importcert -alias PostgreSQLServerCACert2  -file "Microsoft ECC Root Certificate Authority 2017.crt.pem" -keystore truststore -storepass password  -noprompt

    ...
    ```

### Update Root CA certificates in Azure App Services

For Azure App services, connecting to an Azure Database for PostgreSQL flexible server instance, we can have two possible scenarios on updating client certificates and it depends on how on you're using SSL with your application deployed to Azure App Services.

- New certificates are added to App Service at platform level before changes occur in your Azure Database for PostgreSQL flexible server instance. If you're using the SSL certificates included on App Service platform in your application, no action is needed. For more information, see [Add and manage TLS/SSL certificates in Azure App Service](/azure/app-service/configure-ssl-certificate), in the Azure App Service documentation.
- If you're explicitly including the path to SSL certificate file in your code, you would need to download the new certificate, and update the code to use it.

### Update Root CA certificates when using clients in Azure Kubernetes Service (AKS)

If you're trying to connect to the Azure Database for PostgreSQL using applications hosted in Azure Kubernetes Services (AKS), it's similar to access from a dedicated customer's host environment. See detailed [instruction in AKS documentation](/azure/aks/ingress-tls).

### Update Root CA certificates for .NET (`Npgsql`) users on Windows

For .NET (`Npgsql`) users on Windows, connecting to Azure Database for PostgreSQL flexible server instances, make sure **all** root CA certificates are included in Windows Certificate Store, Trusted Root Certification Authorities. Windows Update maintains the standard Azure root CA list. If any certificates listed in our [recommended configuration](security-tls.md#best-configuration) aren't included, import the missing certificates.

## How to use TLS with certificate validation

Some application frameworks that use PostgreSQL for their database services don't enable TLS by default during installation. Your Azure Database for PostgreSQL instance enforces TLS connections, but if the application isn't configured for TLS, the application might fail. Consult your application's documentation to learn how to enable TLS connections.

### Connect using `PSQL`

The following example shows how to connect to your server using the `PSQL` command-line interface. Use the `sslmode=verify-full` or `sslmode=verify-ca` connection string setting to enforce TLS certificate verification. Pass the local certificate file path to the `sslrootcert` parameter.

```bash
 psql "sslmode=verify-full sslrootcert=<path-of-pem-file> host=mydemoserver.postgres.database.azure.com dbname=postgres user=myadmin"
```

### Test TLS connectivity

Before you try to access your TLS-enabled server from a client application, make sure you can get to it via `PSQL`. If you established a TLS connection, you should see output similar to the following example:

```
psql (14.5)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.
```

You can also load the [sslinfo extension](../extensions/concepts-extensions-versions.md#sslinfo) and then call the `ssl_is_used()` function to determine if TLS is being used. The function returns `t` if the connection is using TLS. Otherwise, it returns `f`.

### Get a list of trusted certificates in Java Key Store programmatically

By default, Java stores the trusted certificates in a special file named `cacerts` that is located inside Java installation folder on the client.
Example below first reads `cacerts` and loads it into **KeyStore** object:

```java
private KeyStore loadKeyStore() {
    String relativeCacertsPath = "/lib/security/cacerts".replace("/", File.separator);
    String filename = System.getProperty("java.home") + relativeCacertsPath;
    FileInputStream is = new FileInputStream(filename);
    KeyStore keystore = KeyStore.getInstance(KeyStore.getDefaultType());
    String password = "changeit";
    keystore.load(is, password.toCharArray());

    return keystore;
}
```

The default password for `cacerts` is `changeit` , but should be different on real client, as administrators recommend changing password immediately after Java installation.
Once we loaded **KeyStore** object, we can use the **PKIXParameters** class to read certificates present.

```java
public void whenLoadingCacertsKeyStore_thenCertificatesArePresent() {
    KeyStore keyStore = loadKeyStore();
    PKIXParameters params = new PKIXParameters(keyStore);
    Set<TrustAnchor> trustAnchors = params.getTrustAnchors();
    List<Certificate> certificates = trustAnchors.stream()
      .map(TrustAnchor::getTrustedCert)
      .collect(Collectors.toList());

    assertFalse(certificates.isEmpty());
}
```

## Related content

- [Validate client configuration and troubleshoot connection failures](security-tls-troubleshoot.md)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CLIENT-CERTIFICATES).
