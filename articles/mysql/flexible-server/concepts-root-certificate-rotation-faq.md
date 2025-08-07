---
title: Frequently Asked Questions (FAQ) for Certificate Rotation for Azure Database for MySQL
description: Common asked questions about the root certificate rotation that affects Azure Database for MySQL.
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

## Frequently asked questions for certificate rotation for Azure Database for MySQL

This article answers common questions about root certificate rotation.

### What happens if I remove the DigiCert Global Root CA certificate?

If you remove the certificate before Microsoft rotates the certificate, your connections fail. Add the **DigiCert Global Root CA** certificate back to your client certificate store to restore connectivity.

### How can I ensure that MySQL connections work after I download the DigiCert Global Root G2 certificate?

After the root certificate change, the new certificate is pushed to your servers. When you restart your server, it uses the new certificate. If you experience connectivity issues, check the preceding instructions for any mistakes.

### If I'm not using SSL/TLS, do I still need to update the root certificate?

No. You don't need to take any action if you aren't using SSL/TLS.

### If I'm using SSL/TLS, do I need to restart my database server to update the root certificate?

No. If you're using SSL/TLS, you don't need to restart the database server to start using the new certificate.

The certificate update is a client-side change. Incoming client connections need to use the new certificate to connect to the database server.

### Does this change require me to plan maintenance downtime for the database server?

No. Because the change is only on the client side to connect to the database server, it doesn't require any maintenance downtime for the database server.

### Is there a rollback plan for the root certificate rotation?

If your application experiences problems after the certificate rotation, replace the certificate file by reinstalling the combined certificate or the SHA-2-based certificate, depending on your use case. We recommend that you don't roll back the change, because the change is mandatory.

### Are the certificates that Azure Database for MySQL uses trustworthy?

The certificates that Azure Database for MySQL uses come from trusted certificate authorities. We support these certificates based on the support that the certificate authority provides.

The DigiCert Global Root CA certificate uses the less secure SHA-1 hashing algorithm. This algorithm compromises the security of applications that connect to Azure Database for MySQL. For this reason, we need to perform a certificate change.

### Is the DigiCert Global Root G2 certificate the same certificate that the Single Server deployment option used?

Yes. The DigiCert Global Root G2 certificate is the SHA-2-based root certificate for Azure Database for MySQL. It's the same certificate that the Single Server deployment option used.

### If I'm using read replicas, do I need to perform this update only on the source server or also on the read replicas?

Because this update is a client-side change, you need to apply the changes for all clients that read data from the replica server.

### If I'm using data-in replication, do I need to perform any action?

If you're using [data-in replication](/azure/mysql/flexible-server/concepts-data-in-replication) to connect to Azure Database for MySQL, and the data replication is between two Azure Database for MySQL databases, you need to reset the replica by running `CALL mysql.az_replication_change_master`. Provide the triple dual-root certificate as the last parameter, [master_ssl_ca](/azure/mysql/flexible-server/how-to-data-in-replication?tabs=bash%2Ccommand-line#link-source-and-replica-servers-to-start-data-in-replication).

### Do I need to take any action if I already have `DigiCert Global Root G2` and `Microsoft Root Certificate Authority 2017` in my certificate file?

No. You don't need to take any action if your certificate file already has the `DigiCert Global Root G2` certificate and the `Microsoft Root Certificate Authority 2017` certificate.

## What if I have more questions?

If you still have questions, you can get answers from community experts in [Microsoft Q&A](/answers/questions/).

## Related content

- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
