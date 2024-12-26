---
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 11/27/2024
ms.topic: include
---

In the General settings tab:

1. In the **Startup Command** box, enter the following command: *cp /home/site/wwwroot/default /etc/nginx/sites-available/default && service nginx reload*.

    It replaces the Nginx configuration file in the PHP 8.0 container and restarts Nginx. This configuration ensures that this change is made to the container each time it starts.

1. Select **Save**.
