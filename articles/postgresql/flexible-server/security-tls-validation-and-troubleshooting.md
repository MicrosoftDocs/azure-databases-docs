---
title: Validate client configuration and troubleshoot connection failures
description: This article helps you validate your client configuration and troubleshoot potential connectivity issues after a planned TLS certificate rotation in Azure Database for PostgreSQL flexible server instances.
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

# Validate client configuration and troubleshoot connection failures

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Validate client configuration

To validate your client configuration prior to any planned rotation, ensure that you implement [Recommended configurations for TLS](security-tls#recommended-configurations-for-tls).

### Checking your root certificate store

You should either have the minimum required root certificates or the full set of root certificates installed in your client's root certificate store.

> [!CAUTION]
> Trust only Azure root CA certificates in your clients' root certificate store. Avoid trusting intermediate CAs or individual server certificates, as these practices can lead to unexpected connection issues when Microsoft updates the certificate chain or rotates individual server certificates.

### Determine TLS connection status

To determine your current TLS connection status, you can load the [sslinfo extension](../extensions/concepts-extensions-versions.md#sslinfo) and then call the `ssl_is_used()` function to determine if TLS is being used. The function returns `t` if the connection is using TLS. Otherwise, it returns `f`. You can also collect all the information about your Azure Database for PostgreSQL flexible server instance's TLS usage by process, client, and application by using the following query:

```sql
SELECT datname as "Database name", usename as "User name", ssl, client_addr, application_name, backend_type
   FROM pg_stat_ssl
   JOIN pg_stat_activity
   ON pg_stat_ssl.pid = pg_stat_activity.pid
   ORDER BY ssl;
```

### Test TLS connection with OpenSSL

For testing, you can use the `openssl` command-line tool to connect to your Azure Database for PostgreSQL flexible server instance and display the TLS certificates.:

```bash
openssl s_client -starttls postgres -showcerts -connect <your-postgresql-server-name>:5432
```

This command prints low-level protocol information, like the TLS version and cipher. You must use the option `-starttls postgres`. Otherwise, this command reports that no TLS is in use. Using this command requires at least OpenSSL 1.1.1.

## Read replicas

With root CA migration to [Microsoft RSA Root CA 2017](https://www.microsoft.com/pkiops/docs/repository.htm), it's feasible for newly created replicas to be on a newer root CA certificate than the primary server that was created earlier. For clients that use `sslmode=verify-ca` and `sslmode=verify-full` configuration settings, it's imperative for to accept the new and previous root CA certificates until the rotation is completed on new and existing servers

## Troubleshoot

Use the guidance in this Troubleshoot section to quickly identify and resolve common TLS issues. Start by reproducing the problem and collecting diagnostic data (client-side error messages, psql output, OpenSSL s_client output, and server logs), then verify server parameters (require_secure_transport, ssl_min_protocol_version, ssl_max_protocol_version), the certificate chain, and client sslmode/sslrootcert settings to pinpoint mismatches in protocol versions, cipher suites, or missing/rotated certificates.

### TLS connectivity errors

1. The first step to troubleshoot TLS protocol version compatibility is to identify the error messages that you or your users are seeing when they try to access your Azure Database for PostgreSQL flexible server instance under TLS encryption from the client. Depending on the application and platform, the error messages might be different. In many cases, they point to the underlying issue.
1. To be certain of TLS protocol version compatibility, check the TLS configuration of the database server and the application client to make sure they support compatible versions and cipher suites.
1. Analyze any discrepancies or gaps between the database server and the client's TLS versions and cipher suites. Try to resolve them by enabling or disabling certain options, upgrading or downgrading software, or changing certificates or keys. For example, you might need to enable or disable specific TLS versions on the server or the client, depending on security and compatibility requirements. For example, you might need to disable TLS 1.0 and TLS 1.1, which are considered nonsecure and deprecated, and enable TLS 1.2 and TLS 1.3, which are more secure and modern.
1. The newest certificate issued with [Microsoft RSA Root CA 2017 has intermediate in the chain cross-signed by Digicert Global Root G2 CA](https://www.microsoft.com/pkiops/docs/repository.htm). Some of the Postgres client libraries, while using `sslmode=verify-full` or `sslmode=verify-ca` settings, might experience connection failures with root CA certificates that are cross-signed with intermediate certificates. The result is alternate trust paths.

To work around these issues, add all the necessary certificates to the client certificate store or explicitly specify the `sslrootcert` parameter. Or, set the `PGSSLROOTCERT` environment variable to the local path where the Microsoft RSA Root CA 2017 root CA certificate is placed, from the default value of `%APPDATA%\postgresql\root.crt`.

### Certificate Authority issues

> [!NOTE]
> If you are **not** using `sslmode=verify-full` or `sslmode=verify-ca` settings in your client application connection string, then certificate rotations don't affect you.
> Therefore, you don't need to follow the steps in this section.

1. Produce your list of certificates that are in your trusted root store
    1. For example, you can [get a list of trusted certificates in Java Key Store programmatically](security-tls-how-to-connect#get-a-list-of-trusted-certificates-in-java-key-store-programmatically).
    1. For example, you can [check cacerts java keystore to see if it already contains required certificates](security-tls-how-to-connect#combine-and-update-root-ca-certificates-for-java-applications).
1. You are using certificate pinning, if you have individual intermediate certificates or individual PostgreSQL server certificates. This is an unsupported configuration.
1. To remove certificate pinning, remove all the certificates from your trusted root store and [add only root CA certificates](security-tls-how-to-connect#download-and-convert-root-ca-certificates).

If you are experiencing issues even after following these steps, contact [Microsoft support](/azure/azure-portal/supportability/how-to-create-azure-support-request). Include in the title *ICA Rotation 2026*.

### Certificate pinning issues

 Note

If you are not using sslmode=verify-full or sslmode=verify-ca settings in your client application connection string, then certificate rotations don't affect you. Therefore, you don't need to follow the steps in this section.

Verify if you are using certificate pinning in your application.
Produce your list of certificates that are in your trusted root store
For example, you can get a list of trusted certificates in Java Key Store programmatically.
For example, you can check cacerts java keystore to see if it already contains required certificates.
You are using certificate pinning, if you have individual intermediate certificates or individual PostgreSQL server certificates.
To remove certificate pinning, remove all the certificates from your trusted root store and add the new certificates.
You can download the updated certificates from Microsoft's official repository: Azure Certificate Authority details.
Current chain:
DigiCert Global Root G2
Microsoft Azure RSA TLS Issuing CA 03 / 04 / 07 / 08
New chain:
DigiCert Global Root G2
Microsoft TLS RSA Root G2
Microsoft TLS G2 RSA CA OCSP 02 / 04 / 06 / 08 / 10 / 12 / 14 / 16
If you are experiencing issues even after following these steps, contact Microsoft support. Include in the title ICA Rotation 2026.