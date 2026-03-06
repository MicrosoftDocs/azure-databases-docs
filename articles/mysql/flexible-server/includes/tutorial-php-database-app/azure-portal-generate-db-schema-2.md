---
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.topic: include
---

In the SSH terminal:
1. CD to the root of your application code:

    ```bash
    cd /home/site/wwwroot
    ```

1. Run [database migrations](https://laravel.com/docs/8.x/migrations) from your application root.

    ```bash
    php artisan migrate --force
    ```

    > [!NOTE]  
    > Only changes to files in `/home` can persist beyond app restarts. Changes outside of `/home` are not persisted.
