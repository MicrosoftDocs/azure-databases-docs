---
title: Certificate Rotation for Azure Database for MySQL
description: Learn about the upcoming changes of root certificate rotation that affects Azure Database for MySQL.
author: shih-che
ms.author: shihche
ms.reviewer: talawren, maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Changes in the root certificate rotation for Azure Database for MySQL

To maintain our security and compliance standards, we'll begin changing the root certificates for Azure Database for MySQL Flexible Server after 1 September 2025.

The current root certificate **DigiCert Global Root CA** will be replaced by two new ones:

* **DigiCert Global Root G2**
* **Microsoft RSA Root Certificate Authority 2017**

If you're using Transport Layer Security (TLS) with root certificate verification, you must have all three root certificates installed during the transition period. Once all the certificates are changed, you can remove the old SHA-1 root certificate **DigiCert Global Root CA** from the store.  by adding the two new certificates to the existing store. If you don't add the new certificates before 1 September 2025, your connections to the databases will **fail**.

This article gives you more instructions on how to add the two new root certificates. about the changes, as well as, answering frequently asked questions

> [!NOTE]  
> If the continued use of SHA-1 is a blocker and you want to have your certificates changed before the general rollout, follow the [instructions in this article for creating a combined certificate authority (CA) certificate on the client](#how-to-update-the-root-certificate-store-on-your-client). Then open a support request to rotate your  certificate for Azure Database for MySQL.

## Why is a root certificate update required?

Azure Database for MySQL users can only use the predefined certificate to connect to their MySQL server instances. These certificates are signed by a root certificate authority. The current certificate is signed by **DigiCert Global Root CA**. It is based on SHA-1. The SHA-1 hashing algorithm is considerably insecure, due to discovered vulnerabilities. It's no longer compliant with our security standards.

We needed to rotate the certificate to one signed by a compliant root certificate authority to remediate the issue.

## How to update the root certificate store on your client

To ensure that your applications can connect to Azure Database for MySQL after the root certificate rotation, you need to update the root certificate store on your client. This is necessary if you're using SSL/TLS with root certificate verification.

The following steps guide you through the process of updating the root certificate store on your client:

1. Download the three root certificates. If you have installed the **DigiCert Global Root CA** certificate, you can skip the first download:
    - [Download the DigiCert Global Root CA certificate](https://cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem)
    - [Download the DigiCert Global Root G2 certificate](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem).
    - [Download the Microsoft RSA Root Certificate Authority 2017 certificate](https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt).

1. Add the downloaded certificates to your client certificate store. The process varies depending on the client type

## Update your Java client

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

## Updating an existing trusted root certificate store

For **Java** users, run these commands to add the new trusted root certificates to an **existing** trusted root **certificate store**:

```bash
keytool -importcert -alias MySqlFlexServerCACert2  -file digiCertGlobalRootG2.crt.pem -keystore truststore -storepass password -noprompt
keytool -importcert -alias MicrosoftRSARootCert2017  -file MicrosoftRSARootCertificateAuthority2017.crt -keystore truststore -storepass password -noprompt
```

There is no need change the `javax.net.ssl.trustStore` and `javax.net.ssl.trustStorePassword` properties if you are updating an existing keystore.

## Update your .NET client

### .Net on Windows

For .NET users on Windows, make sure that **DigiCert Global Root CA**, **DigiCert Global Root G2** and **Microsoft RSA Root Certificate Authority 2017** exist in the Windows certificate store under **Trusted Root Certification Authorities**. If any certificate doesn't exist, import it.

:::image type="content" source="media/concepts-root-certificate-rotation/net-connecter-certificates.png" alt-text="Screenshot of Azure Database for MySQL .NET certificates." lightbox="media/concepts-root-certificate-rotation/net-connecter-certificates.png":::

### .Net on Linux

For .NET users on Linux who are using `SSL_CERT_DIR`, make sure that `DigiCertGlobalRootCA.crt.pem`, `DigiCertGlobalRootG2.crt.pem` and `Microsoft RSA Root Certificate Authority 2017.crt.pem` exist in the directory indicated by `SSL_CERT_DIR`. If any certificate doesn't exist, create the missing certificate file.
   
Convert the `Microsoft RSA Root Certificate Authority 2017.crt` certificate to PEM format by running the following command:

```bash
openssl x509 -inform der -in MicrosoftRSARootCertificateAuthority2017.crt -out MicrosoftRSARootCertificateAuthority2017.crt.pem
```

## Other clients

For other (MySQL Workbench, C, C++, Go, Python, Ruby, PHP, Node.js, Perl, or Swift) users, you can merge the CA certificate files in this format:

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

For Data-in replication where **both master and replica are hosted on Azure**, you can merge the CA certificate files in this format:
  
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

Call mysql.az_replication_change_master as follow:

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

To verify if you're using an SSL connection to connect to the server, refer to [Verify the TLS/SSL connection](/azure/mysql/flexible-server/how-to-connect-tls-ssl#verify-the-tlsssl-connection).

## Frequently asked questions

### What if I remove the DigiCert Global Root CA certificate?

If you remove the certificate prior to Microsoft's certificate rotation, your connections will fail. Add the **DigiCert Global Root CA** certificate back to your client certificate store to restore connectivity.

### How do I make sure that the MySQL connections are established after I download the DigiCert Global Root G2 certificate?

After the root certificate change, the newly generated certificate is pushed down to your servers. After the next restart of your server, the new certificate will be used. If you experience connectivity issues, check the instructions above for any mistakes in executing them.

### If I'm not using SSL/TLS, do I still need to update the root certificate?

No. You don't need to take any action if you aren't using SSL/TLS.

### If I'm using SSL/TLS, do I need to restart my database server to update the root certificate?

No. If you're using SSL/TLS, you don't need to restart the database server to start using the new certificate.

The certificate update is a client-side change. The incoming client connections need to use the new certificate to ensure that they can connect to the database server.

### Does this change require me to plan maintenance downtime for the database server?

No. Because the change is only on the client side to connect to the database server, it doesn't require any maintenance downtime for the database server.

### Is there a rollback plan for the root certificate rotation?

If your application experiences problems after the certificate rotation, replace the certificate file by reinstalling the combined certificate or the SHA-2-based certificate, depending on your use case. We recommend that you don't roll back the change, because the change is mandatory.

### Are the certificates that Azure Database for MySQL uses trustworthy?

The certificates that Azure Database for MySQL uses come from trusted certificate authorities. Our support of these certificates is based on the support that the CA provides for them.

The DigiCert Global Root CA certificate's use of the less secure SHA-1 hashing algorithm compromises the security of applications that connect to Azure Database for MySQL. That's why we need to perform a certificate change.

### Is the DigiCert Global Root G2 certificate the same certificate that the Single Server deployment option used?

Yes. The DigiCert Global Root G2 certificate, the SHA-2-based root certificate for Azure Database for MySQL, is the same certificate that the Single Server deployment option used.

### If I'm using read replicas, do I need to perform this update only on the source server or also on the read replicas?

Because this update is a client-side change, if multiple clients read data from the replica server, you also need to apply the changes for those clients.

### If I'm using data-in replication, do I need to perform any action?

If you're using [data-in replication](/azure/mysql/flexible-server/concepts-data-in-replication) to connect to Azure Database for MySQL, and the data replication is between two Azure Database for MySQL databases, you need to reset the replica by running `CALL mysql.az_replication_change_master`. Provide the tripple dual-root certificate as the last parameter, [master_ssl_ca](/azure/mysql/flexible-server/how-to-data-in-replication?tabs=bash%2Ccommand-line#link-source-and-replica-servers-to-start-data-in-replication).

### Do I need to take any action if I already have `DigiCert Global Root G2` and `Microsoft Root Certificate Authority 2017` in my certificate file?

No. You don't need to take any action if your certificate file already has the `DigiCert Global Root G2` certificate and the `Microsoft Root Certificate Authority 2017` certificate.

## What if I have more questions?

If you still have questions, you can get answers from community experts in [Microsoft Q&A](/answers/questions/).

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
