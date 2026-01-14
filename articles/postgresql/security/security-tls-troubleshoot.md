---
title: Validate the Client Configuration and Troubleshoot Connection Failures
description: This article helps you validate your client configuration and troubleshoot potential connectivity issues after a planned TLS certificate rotation in Azure Database for PostgreSQL flexible server instances.
author: techlake
ms.author: hganten
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: troubleshooting
---

# Troubleshoot TLS connection failures

TLS connection failures can occur for various reasons, especially after a planned TLS certificate rotation in Azure Database for PostgreSQL. This article guides you through validating your client configuration and troubleshooting potential connectivity issues.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Validate client configuration

To validate your client configuration before any planned rotation, make sure you implement the [Recommended configurations for TLS](security-tls.md#recommended-configurations-for-tls).

### Check your root certificate store

Make sure your client's root certificate store contains either the minimum required root certificates or the full set of root certificates.

> [!CAUTION]  
> Trust only Azure root CA certificates in your clients' root certificate store. Don't trust intermediate CAs or individual server certificates. If you trust these certificates, you might encounter unexpected connection problems when Microsoft updates the certificate chain or rotates individual server certificates.

### Determine TLS connection status

To determine your current TLS connection status, load the [sslinfo extension](../extensions/concepts-extensions-versions.md#sslinfo) and then call the `ssl_is_used()` function to determine if TLS is being used. The function returns `t` if the connection uses TLS. Otherwise, it returns `f`. You can also collect all the information about your Azure Database for PostgreSQL flexible server instance's TLS usage by process, client, and application by using the following query:

```sql
SELECT datname AS "Database name",
       usename AS "User name",
       ssl,
       client_addr,
       application_name,
       backend_type
FROM pg_stat_ssl
     INNER JOIN pg_stat_activity
         ON pg_stat_ssl.pid = pg_stat_activity.pid
ORDER BY ssl;
```

### Test TLS connection by using OpenSSL

For testing, use the `openssl` command to connect to your Azure Database for PostgreSQL and display the TLS certificates.

```bash
openssl s_client -starttls postgres -showcerts -connect <your-postgresql-server-name>:5432
```

This command prints low-level protocol information, like the TLS version and cipher. You must use the option `-starttls postgres`. Otherwise, this command reports that no TLS is in use. Using this command requires at least OpenSSL 1.1.1.

## Read replicas

When root CA migration occurs to [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/docs/repository.htm), newly created replicas can use a newer root CA certificate than the primary server if the primary server was created earlier. For clients that use `sslmode=verify-ca` and `sslmode=verify-full` configuration settings, you need to accept the new and previous root CA certificates until the rotation is completed on new and existing servers.

## Troubleshoot

1. Reproduce the problem.
1. Collect diagnostic data, such as client-side error messages, psql output, OpenSSL s_client output, and server logs.
1. Verify server parameters, including `require_secure_transport`, `ssl_min_protocol_version`, and `ssl_max_protocol_version`.
1. Verify the certificate chain and client `sslmode` and `sslrootcert` settings to pinpoint mismatches in protocol versions, cipher suites, or missing or rotated certificates.

### TLS connectivity errors

1. Identify the error messages that you or your users see when they try to access your Azure Database for PostgreSQL flexible server instance under TLS encryption from the client. Depending on the application and platform, the error messages might be different. In many cases, they point to the underlying issue.
1. Check the TLS configuration of the database server and the application client to make sure they support compatible versions and cipher suites.
1. Analyze any discrepancies or gaps between the database server and the client's TLS versions and cipher suites. Try to resolve them by enabling or disabling certain options, upgrading or downgrading software, or changing certificates or keys. For example, you might need to enable or disable specific TLS versions on the server or the client, depending on security and compatibility requirements. You might need to disable TLS 1.0 and TLS 1.1, which are considered nonsecure and deprecated, and enable TLS 1.2 and TLS 1.3, which are more secure and modern.
1. The newest certificate issued by [Microsoft RSA Root CA 2017 has intermediate in the chain cross-signed by Digicert Global Root G2 CA](https://www.microsoft.com/pkiops/docs/repository.htm). Some of the Postgres client libraries, while using `sslmode=verify-full` or `sslmode=verify-ca` settings, might experience connection failures with root CA certificates that are cross-signed with intermediate certificates. The result is alternate trust paths.

To work around these problems, add all the necessary certificates to the client certificate store or explicitly specify the `sslrootcert` parameter. Or, set the `PGSSLROOTCERT` environment variable to the local path where the Microsoft RSA Root CA 2017 root CA certificate is placed, from the default value of `%APPDATA%\postgresql\root.crt`.

### Certificate authority issues

> [!NOTE]  
> If you don't use `sslmode=verify-full` or `sslmode=verify-ca` settings in your client application connection string, certificate rotations don't affect you.
> Therefore, you don't need to follow the steps in this section.

1. Create a list of certificates in your trusted root store.
   - For example, you can [get a list of trusted certificates in Java Key Store programmatically](security-tls-how-to-connect.md#get-a-list-of-trusted-certificates-in-java-key-store-programmatically).
   - For example, you can [check cacerts java keystore to see if it already contains required certificates](security-tls-how-to-connect.md#combine-and-update-root-ca-certificates-for-java-applications).
1. You're using certificate pinning if you have individual intermediate certificates or individual PostgreSQL server certificates. This configuration isn't supported.
1. To remove certificate pinning, remove all the certificates from your trusted root store and [add only root CA certificates](security-tls-how-to-connect.md#download-and-convert-root-ca-certificates).

If you experience issues even after following these steps, contact [Microsoft support](/azure/azure-portal/supportability/how-to-create-azure-support-request). Include *ICA Rotation 2026* in the title.

### Certificate pinning issues

If you don't use `sslmode=verify-full` or `sslmode=verify-ca` settings in your client application connection string, certificate rotations don't affect you. Therefore, you don't need to follow the steps in this section.

1. Verify if you're using certificate pinning in your application.
1. Create a list of certificates in your trusted root store. For example:
   - Get a list of trusted certificates in Java Key Store programmatically.
   - Check cacerts java keystore to see if it already contains required certificates.
1. You're using certificate pinning if you have individual intermediate certificates or individual PostgreSQL server certificates.
1. To remove certificate pinning, remove all the certificates from your trusted root store and add the new certificates.
1. You can download the updated certificates from Microsoft's official repository: Azure Certificate Authority details.

If you experience issues even after following these steps, contact Microsoft support. Include *ICA Rotation 2026* in the title.

### Verify certificate chain

#### Old chain

- DigiCert Global Root G2
  - Microsoft Azure RSA TLS Issuing CA 03 / 04 / 07 / 08
  - Server certificate

#### New chain

- DigiCert Global Root G2
  - Microsoft TLS RSA Root G2
  - Microsoft TLS G2 RSA CA OCSP 02 / 04 / 06 / 08 / 10 / 12 / 14 / 16
  - Server certificate

## Related content

- [Transport Layer Security (TLS) in Azure Database for PostgreSQL](security-tls.md)
- [Connect clients with TLS security to your database](security-tls-how-to-connect.md)
