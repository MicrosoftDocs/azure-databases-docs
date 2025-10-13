---
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.topic: include
---

Create a new `MYSQL_ATTR_SSL_CA` database setting:

1. Select **New application setting**.
1. In the **Name** field, enter *MYSQL_ATTR_SSL_CA*.
1. In the **Value** field, enter */home/site/wwwroot/ssl/DigiCertGlobalRootG2.crt.pem*.

    This app setting points to the path of the [TLS/SSL certificate you need to access the MySQL server](../../how-to-connect-tls-ssl.md#download-the-public-ssl-certificate). It's included in the sample repository for convenience.

1. Select **OK**.
