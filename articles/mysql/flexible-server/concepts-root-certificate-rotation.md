---
title: Certificate Rotation for Azure Database for MySQL
description: Learn about the upcoming changes of root certificate rotation that affects Azure Database for MySQL.
author: shih-che
ms.author: shihche
ms.reviewer: talawren, maghan
ms.date: 08/07/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
---

# Changes in the root certificate rotation for Azure Database for MySQL

To maintain our security and compliance standards, we start changing the root certificates for Azure Database for MySQL Flexible Server after September 1, 2025.

The current root certificate **DigiCert Global Root CA** is replaced by two new root certificates:

- **DigiCert Global Root G2**
- **Microsoft RSA Root Certificate Authority 2017**

If you use Transport Layer Security (TLS) with root certificate verification, you must have all three root certificates installed during the transition period. Once all the certificates are changed, you can remove the old SHA-1 root certificate **DigiCert Global Root CA** from the store. If you don't add the new certificates before September 1, 2025, your connections to the databases **fail**.

This article provides instructions on how to add the two new root certificates, and answers to frequently asked questions.

> [!NOTE]  
> If the continued use of SHA-1 is a blocker and you want to have your certificates changed before the general rollout, follow the [instructions in this article for creating a combined certificate authority (CA) certificate on the client](#how-to-update-the-root-certificate-store-on-your-client). Then open a support request to rotate your certificate for Azure Database for MySQL.

## Why is a root certificate update required?

Azure Database for MySQL users can only use the predefined certificate to connect to their MySQL server instances. These certificates are signed by a root certificate authority. The current certificate is signed by **DigiCert Global Root CA**. It uses SHA-1. The SHA-1 hashing algorithm is considerably insecure, due to discovered vulnerabilities. It's no longer compliant with our security standards.

We need to rotate the certificate to one signed by a compliant root certificate authority to remediate the issue.

## How to update the root certificate store on your client

To ensure that your applications can connect to Azure Database for MySQL after the root certificate rotation, update the root certificate store on your client. Update the root certificate store if you're using SSL/TLS with root certificate verification.

The following steps guide you through the process of updating the root certificate store on your client:

- Download the three root certificates. If you installed the **DigiCert Global Root CA** certificate, you can skip the first download:

- [Download the DigiCert Global Root CA certificate](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem).
- [Download the DigiCert Global Root G2 certificate](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem).
- [Download the Microsoft RSA Root Certificate Authority 2017 certificate](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt).

- Add the downloaded certificates to your client certificate store. The process varies depending on the client type.

## Update your Java client

Follow these steps to update your Java client certificates for the root certificate rotation.

## Creating a new trusted root certificate store

For **Java** users, run these commands to create a **new** trusted root **certificate store**:

```bash
keytool -importcert -alias MySqlFlexServerCACert  -file digiCertGlobalRootCA.crt.pem  -keystore truststore -storepass password -noprompt
keytool -importcert -alias MySqlFlexServerCACert2  -file digiCertGlobalRootG2.crt.pem -keystore truststore -storepass password -noprompt
keytool -importcert -alias MicrosoftRSARootCert2017  -file MicrosoftRSARootCertificateAuthority2017.crt -keystore truststore -storepass password -noprompt
```

Then replace the original keystore file with the newly generated one:

- `System.setProperty("javax.net.ssl.trustStore","path_to_truststore_file");`
- `System.setProperty("javax.net.ssl.trustStorePassword","password");`

## Update an existing trusted root certificate store

For **Java** users, run these commands to add the new trusted root certificates to an **existing** trusted root **certificate store**:

```bash
keytool -importcert -alias MySqlFlexServerCACert2  -file digiCertGlobalRootG2.crt.pem -keystore truststore -storepass password -noprompt
keytool -importcert -alias MicrosoftRSARootCert2017  -file MicrosoftRSARootCertificateAuthority2017.crt -keystore truststore -storepass password -noprompt
```

If you update an existing keystore, you don't need to change the `javax.net.ssl.trustStore` and `javax.net.ssl.trustStorePassword` properties.

## Update your .NET client

Follow these steps to update your .NET client certificates for the root certificate rotation.

### .NET on Windows

For .NET users on Windows, make sure that **DigiCert Global Root CA**, **DigiCert Global Root G2**, and **Microsoft RSA Root Certificate Authority 2017** exist in the Windows certificate store under **Trusted Root Certification Authorities**. If any certificate doesn't exist, import it.

:::image type="content" source="media/concepts-root-certificate-rotation/net-connecter-certificates.png" alt-text="Screenshot of Azure Database for MySQL .NET certificates." lightbox="media/concepts-root-certificate-rotation/net-connecter-certificates.png":::

### .NET on Linux

For .NET users on Linux who use `SSL_CERT_DIR`, make sure that `DigiCertGlobalRootCA.crt.pem`, `DigiCertGlobalRootG2.crt.pem`, and `Microsoft RSA Root Certificate Authority 2017.crt.pem` exist in the directory indicated by `SSL_CERT_DIR`. If any certificate doesn't exist, create the missing certificate file.

Convert the `Microsoft RSA Root Certificate Authority 2017.crt` certificate to PEM format by running the following command:

```bash
openssl x509 -inform der -in MicrosoftRSARootCertificateAuthority2017.crt -out MicrosoftRSARootCertificateAuthority2017.crt.pem
```

## Other clients

For other users (MySQL Workbench, C, C++, Go, Python, Ruby, PHP, Node.js, Perl, or Swift), you can merge the CA certificate files in this format:

```output
-----BEGIN CERTIFICATE-----
(Root CA1:DigiCertGlobalRootCA.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA2: DigiCertGlobalRootG2.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA3: .crt.pem)
-----END CERTIFICATE-----
```

## Data-in replication MySQL

For data-in replication where **both primary and replica are hosted on Azure**, you can merge the CA certificate files in this format:

```output
SET @cert = '-----BEGIN CERTIFICATE-----
(Root CA1:DigiCertGlobalRootCA.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA2: DigiCertGlobalRootG2.crt.pem)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Root CA3: .crt.pem)
-----END CERTIFICATE-----'
```

Call `mysql.az_replication_change_master` as follows:

```sql
CALL mysql.az_replication_change_master('master.companya.com', 'syncuser', 'P@ssword!', 3306, 'mysql-bin.000002', 120, @cert);
```

> [!IMPORTANT]  
> Reboot your replica server.

## How do I know if I'm using SSL/TLS with root certificate verification?

You can identify whether your connections verify the root certificate by reviewing your connection string:

- If your connection string includes `sslmode=verify-ca` or `sslmode=verify-identity`, you need to update the trusted root certificates.
- If your connection string includes `sslmode=disable`, `sslmode=allow`, `sslmode=prefer`, or `sslmode=require`, you don't need to update the trusted root certificates.
- If your connection string doesn't specify `sslmode`, you don't need to update certificates.

If you're using a client that abstracts the connection string away, review the client's documentation to understand whether it verifies certificates.

### Can I use a server-side query to verify if I'm using SSL?

To verify if you're using an SSL connection to connect to the server, see [Verify the TLS/SSL connection](/azure/mysql/flexible-server/how-to-connect-tls-ssl#verify-the-tlsssl-connection).

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
