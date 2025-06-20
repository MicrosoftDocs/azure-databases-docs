---
title: Certificate Rotation for Azure Database for MySQL
description: Learn about the upcoming changes of root certificate rotation that affects Azure Database for MySQL.
author: shih-che
ms.author: shihche
ms.reviewer: talawren, maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom: sfi-image-nochange
---

# Changes in the root certificate rotation for Azure Database for MySQL

In July 2025, the root certificate for Azure Database for MySQL is changing as part of standard maintenance and security best practices. This article gives you more details about the changes, the affected resources, and the steps for ensuring that your application maintains connectivity to your database server.

> [!NOTE]  
> If SHA-1 is a current blocker, follow the [instructions in this article for creating a combined certificate authority (CA) certificate on the client](#do-i-need-to-make-any-changes-on-my-client-to-maintain-connectivity). Then open a support request to rotate your root certificate for Azure Database for MySQL.

## Why is a root certificate update required?

Azure Database for MySQL users can use only the predefined certificate to connect to their MySQL server instances. However, the DigiCert Global Root CA certificate is based on SHA-1. The SHA-1 hashing algorithm is considerably less secure than its alternatives, due to discovered vulnerabilities. It's no longer compliant with our security standards.

We needed to rotate the certificate to a compliant version to minimize the potential threat to your MySQL flexible servers.

## Do I need to make any changes on my client to maintain connectivity?

After you complete the root certificate rotation, there's a transition where the old DigiCert Global Root CA certificate is no longer accepted and the new DigiCert Global Root G2 certificate is authorized.

To maintain connectivity before and after this transition, we recommend that you use the following steps to bundle both certificates into a single certificate file:

1. [Download the DigiCert Global Root CA certificate](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem), and [download the DigiCert Global Root G2 certificate](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem).

1. Generate a combined CA certificate store with both the DigiCert Global Root CA and DigiCert Global Root G2 certificates included.

   - For Java (MariaDB Connector/J) users, run these commands:

     ```bash
     keytool -importcert -alias MySqlFlexServerCACert  -file D:\DigiCertGlobalRootCA.crt.pem  -keystore truststore -storepass password -noprompt
     ```

     ```bash
     keytool -importcert -alias MySqlFlexServerCACert2  -file D:\DigiCertGlobalRootG2.crt.pem -keystore truststore -storepass password  -noprompt
     ```

     Then replace the original keystore file with the newly generated one:

     - `System.setProperty("javax.net.ssl.trustStore","path_to_truststore_file");`
     - `System.setProperty("javax.net.ssl.trustStorePassword","password");`

   - For .NET (MariaDB Connector/NET) users, make sure that **Baltimore CyberTrust Root** and **DigiCert Global Root G2** both exist in the Windows certificate store under **Trusted Root Certification Authorities**. If either certificate doesn't exist, import it.

     :::image type="content" source="media/concepts-root-certificate-rotation/net-connecter-certificates.png" alt-text="Screenshot of Azure Database for MySQL .NET certificates." lightbox="media/concepts-root-certificate-rotation/net-connecter-certificates.png":::

   - For .NET users on Linux who are using `SSL_CERT_DIR`, make sure that `DigiCertGlobalRootCA.crt.pem` and `DigiCertGlobalRootG2.crt.pem` both exist in the directory indicated by `SSL_CERT_DIR`. If either certificate doesn't exist, create the missing certificate file.

   - For other (MariaDB Client, MySQL Workbench, C, C++, Go, Python, Ruby, PHP, Node.js, Perl, or Swift) users, you can merge two CA certificate files in this format:
  
     ```output
     -----BEGIN CERTIFICATE-----
     (Root CA1:DigiCertGlobalRootCA.crt.pem)
     -----END CERTIFICATE-----
     -----BEGIN CERTIFICATE-----
     (Root CA2: DigiCertGlobalRootG2.crt.pem)
     -----END CERTIFICATE-----
     ```

1. Replace the original root certificate .pem file with the combined root certificate file, and restart your application or client.

In the future, after the new certificate is deployed on the server side, you can change your certificate .pem file to `DigiCertGlobalRootG2.crt.pem`.

## What if I remove the DigiCert Global Root CA certificate?

If you remove the certificate, you start to observe connectivity errors while connecting to Azure Database for MySQL. To maintain connectivity, you need to [configure SSL](how-to-connect-tls-ssl.md) by [downloading the DigiCert Global Root CA certificate](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem) again.

## How do I make sure that the MySQL connections are established after I download the DigiCert Global Root G2 certificate?

After the root certificate change, the newly generated certificate is pushed down to customer servers. Restart your servers for the new DigiCert Global Root G2 certificate to take effect on your connections.

## If I'm not using SSL/TLS, do I still need to update the root certificate?

No. You don't need to take any action if you aren't using SSL/TLS.

## If I'm using SSL/TLS, do I need to restart my database server to update the root certificate?

No. If you're using SSL/TLS, you don't need to restart the database server to start using the new certificate.

The certificate update is a client-side change. The incoming client connections need to use the new certificate to ensure that they can connect to the database server.

## How do I know if I'm using SSL/TLS with root certificate verification?

You can identify whether your connections verify the root certificate by reviewing your connection string:

- If your connection string includes `sslmode=verify-ca` or `sslmode=verify-identity`, you need to update certificates.
- If your connection string includes `sslmode=disable`, `sslmode=allow`, `sslmode=prefer`, or `sslmode=require`, you don't need to update certificates.
- If your connection string doesn't specify `sslmode`, you don't need to update certificates.

If you're using a client that abstracts the connection string away, review the client's documentation to understand whether it verifies certificates.

## Can I use a server-side query to verify if I'm using SSL?

To verify if you're using an SSL connection to connect to the server, refer to [Verify the TLS/SSL connection](/azure/mysql/flexible-server/how-to-connect-tls-ssl#verify-the-tlsssl-connection).

## Does this change require me to plan maintenance downtime for the database server?

No. Because the change is only on the client side to connect to the database server, it doesn't require any maintenance downtime for the database server.

## Is there a rollback plan for the root certificate rotation?

If your application experiences problems after the certificate rotation, replace the certificate file by reinstalling the combined certificate or the SHA-2-based certificate, depending on your use case. We recommend that you don't roll back the change, because the change is mandatory.

## Are the certificates that Azure Database for MySQL uses trustworthy?

The certificates that Azure Database for MySQL uses come from trusted certificate authorities. Our support of these certificates is based on the support that the CA provides for them.

The DigiCert Global Root CA certificate's use of the less secure SHA-1 hashing algorithm compromises the security of applications that connect to Azure Database for MySQL. That's why we need to perform a certificate change.

## Is the DigiCert Global Root G2 certificate the same certificate that the Single Server deployment option used?

Yes. The DigiCert Global Root G2 certificate, the SHA-2-based root certificate for Azure Database for MySQL, is the same certificate that the Single Server deployment option used.

## If I'm using read replicas, do I need to perform this update only on the source server or also on the read replicas?

Because this update is a client-side change, if multiple clients read data from the replica server, you also need to apply the changes for those clients.

## If I'm using data-in replication, do I need to perform any action?

If you're using [data-in replication](/azure/mysql/flexible-server/concepts-data-in-replication) to connect to Azure Database for MySQL, and the data replication is between two Azure Database for MySQL databases, you need to reset the replica by running `CALL mysql.az_replication_change_master`. Provide the new dual-root certificate as the last parameter, [master_ssl_ca](/azure/mysql/flexible-server/how-to-data-in-replication?tabs=bash%2Ccommand-line#link-source-and-replica-servers-to-start-data-in-replication).

## Do I need to take any action if I already have DigiCert Global Root G2 in my certificate file?

No. You don't need to take any action if your certificate file already has the DigiCert Global Root G2 certificate.

## What if I have more questions?

If you still have questions, you can get answers from community experts in [Microsoft Q&A](/answers/questions/).

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
