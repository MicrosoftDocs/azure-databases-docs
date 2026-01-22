---
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.topic: include
---

Create a new `MYSQL_ATTR_SSL_CA` database setting:

1. Select **New application setting**.
1. In the **Name** field, enter *MYSQL_ATTR_SSL_CA*.
1. In the **Value** field, enter */home/site/wwwroot/ssl/DigiCertGlobalRootG2.crt.pem*.

   This app setting points to the path of the [TLS/SSL certificate you need to access the MySQL server](../../security-tls-how-to-connect.md#download-the-public-ssl-certificate). For convenience, the sample repository includes this certificate.

1. Select **OK**.
