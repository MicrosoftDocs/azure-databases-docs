---
title: Certificate Rotation for Azure Database for MySQL - Flexible Server
description: Learn about the upcoming changes of root certificate rotation that affects Azure Database for MySQL
author: shih-che
ms.author: shihche
ms.reviewer: talawren, maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Understanding the changes in the Root CA rotation for Azure Database for MySQL

Azure Database for MySQL as part of standard maintenance and security best practices completes the root certificate change starting July 2025. This article gives you more details about the changes, the resources affected, and the steps needed to ensure that your application maintains connectivity to your database server.

> [!NOTE]  
> If SHA-1 is a current blocker, follow the instructions below for creating a combined CA certificate on the client and open a support request to rotate your Azure Database for MySQL – Flexible Server root CA.

## Why is a root certificate update required?

Azure Database for MySQL users can only use the predefined certificate to connect to their MySQL server instances. However, DigiCertGlobalRootCA is a SHA-1 based Certificate Authority (CA). The SHA-1 hashing algorithm is considerably less secure than its alternatives due to vulnerabilities that were discovered and thus it's no longer compliant with our security standards. Since Azure Database for MySQL used one of these noncompliant certificates, we needed to rotate the certificate to the compliant version to minimize the potential threat to your MySQL flexible servers.

## Do I need to make any changes on my client to maintain connectivity?

Upon completing the root CA rotation, there's a transition where the old DigiCertGlobalRoot CA can no longer be accepted, and the new DigiCertGlobalRootG2 CA is authorized. **To maintain connectivity before and after this transition, we recommend following the steps outlined below in [Create a combined CA certificate](#create-a-combined-ca-certificate) to bundle both CAs into a single certificate file.**

### Create a combined CA certificate

- Download **DigiCertGlobalRootCA** & **DigiCertGlobalRootG2** CA from the links below:

  - [https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem)
  - [https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem](https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem)

- Generate a combined CA certificate store with both **DigiCertGlobalRootCA** and **DigiCertGlobalRootG2** certificates included.

  - For Java (MariaDB Connector/J) users, execute:

    ```bash
    keytool -importcert -alias MySqlFlexServerCACert  -file D:\DigiCertGlobalRootCA.crt.pem  -keystore truststore -storepass password -noprompt
    ```

    ```bash
    keytool -importcert -alias MySqlFlexServerCACert2  -file D:\DigiCertGlobalRootG2.crt.pem -keystore truststore -storepass password  -noprompt
    ```

    Then replace the original keystore file with the new generated one:

    - `System.setProperty("javax.net.ssl.trustStore","path_to_truststore_file");`
    - `System.setProperty("javax.net.ssl.trustStorePassword","password");`

  - For .NET (MariaDB Connector/NET, MariaDBConnector) users, make sure **BaltimoreCyberTrustRoot** and **DigiCertGlobalRootG2** both exist in the Windows Certificate Store, Trusted Root Certification Authorities. If any certificates don't exist, import the missing certificate.

    :::image type="content" source="media/concepts-root-certificate-rotation/net-connecter-certificates.png" alt-text="Screenshot of Azure Database for MySQL .NET cert." lightbox="media/concepts-root-certificate-rotation/net-connecter-certificates.png":::

  - For .NET users on Linux using SSL_CERT_DIR, make sure **DigiCertGlobalRootCA** and **DigiCertGlobalRootG2** both exist in the directory indicated by SSL_CERT_DIR. If any certificates don't exist, create the missing certificate file.

  - For other (MariaDB Client/MariaDB Workbench/C/C++/Go/Python/Ruby/PHP/NodeJS/Perl/Swift) users, you can merge two CA certificate files like this format below:
  Copy

   ```output
   -----BEGIN CERTIFICATE-----
   (Root CA1:DigiCertGlobalRootCA.crt.pem)
   -----END CERTIFICATE-----
   -----BEGIN CERTIFICATE-----
   (Root CA2: DigiCertGlobalRootG2.crt.pem)
   -----END CERTIFICATE-----
   ```

- Replace the original root CA pem file with the combined root CA file and restart your application/client.
- In the future, after the new certificate is deployed on the server side, you can change your CA pem file to DigiCertGlobalRootG2.crt.pem.

## What if we removed the DigiCertGlobalRootCA certificate?

You start to observe connectivity errors while connecting to your Azure Database for MySQL. You need to [configure SSL](how-to-connect-tls-ssl.md) with [DigiCertGlobalRootCA](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem) certificate again to maintain connectivity.

### What if we would like to make sure the MySQL connections are established upon the DigiCertGlobalRootG2 CA?

After the root certificate change, the newly generated certificate is pushed down to customer servers. However, it requires a server restart for the new certificate to take effect. Therefore, if a customer needs to make sure they're using the DigiCertGlobalRootG2 CA, they have to **restart their servers** after the root certificate change.

## Frequently asked questions

### If I'm not using SSL/TLS, do I still need to update the root CA?

No. There are no actions required if you aren't using SSL/TLS.

### If I'm using SSL/TLS, do I need to restart my database server to update the root CA?

No. IF you're using SSL/TLS, you don't need to restart the database server to start using the new certificate. Certificate update is a client-side change, and the incoming client connections need to use the new certificate to ensure that they can connect to the database server.

### How do I know if I'm using SSL/TLS with root certificate verification?

You can identify whether your connections verify the root certificate by reviewing your connection string.

- If your connection string includes `sslmode=verify-ca` or `sslmode=verify-identity`, you need to update the certificate.
- If your connection string includes `sslmode=disable`, `sslmode=allow`, `sslmode=prefer`, or `sslmode=require`, you don't need to update certificates.
- If your connection string doesn't specify sslmode, you don't need to update certificates.

If you're using a client that abstracts the connection string away, review the client's documentation to understand whether it verifies certificates.

### Do we have a server-side query to verify if SSL is being used?

To verify if you're using an SSL connection to connect to the server refer to [SSL verification](/azure/mysql/flexible-server/how-to-connect-tls-ssl#verify-the-tlsssl-connection).

### Do I need to plan a database server maintenance downtime for this change?

No. Since the change is only on the client side to connect to the database server, there's no maintenance downtime needed for the database server for this change.

### Is there a rollback plan for the root CA rotation?

If your application experiences issues after the CA rotation, replace the CA file by reinstalling the combined CA or SHA-2 based CA depending on your use case. We recommend you don't rollback the change as this change is mandatory.

### How often does Microsoft update their certificates or what is the expiry policy?

These certificates used by Azure Database for MySQL are provided by trusted Certificate Authorities (CA). Our support of these certificates is based on the support the CA provides for these certificates. The DigiCertGlobalRootCA certificate's use of the less secure SHA-1 hashing algorithm compromises the security of applications connecting to Azure Database for MySQL so Microsoft needs to perform a certificate change.

### Is DigiCertGlobalRootG2 CA the same certificate used for Single Server?

Yes. DigiCertGlobalRootG2 CA, the new root CA of SHA-2 for Azure Database for MySQL is the same as Single Server.

### If I'm using read replicas, do I need to perform this update only on the source server or the read replicas?

Since this update is a client-side change, if multiple clients read data from the replica server, you need to apply the changes for those clients as well.

### If I'm using Data-in replication, do I need to perform any action?

If you're using [Data-in replication](/azure/mysql/flexible-server/concepts-data-in-replication) to connect to Azure Database for MySQL, and the data-replication is between two Azure Database for MySQL, then you need to reset the replica by executing CALL mysql.az_replication_change_master and provide the new dual root certificate as last parameter [master_ssl_ca](/azure/mysql/flexible-server/how-to-data-in-replication?tabs=bash%2Ccommand-line#link-source-and-replica-servers-to-start-data-in-replication).

### Is there an action needed if I already have the DigiCertGlobalRootG2 in my certificate file?

No. There's no action needed if your certificate file already has the DigiCertGlobalRootG2.

### What if I have further questions?

If you have questions, get answers from community experts in [Microsoft Q&A](/answers/questions/).

## Related content

- [Create a combined CA certificate](#create-a-combined-ca-certificate)
- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
