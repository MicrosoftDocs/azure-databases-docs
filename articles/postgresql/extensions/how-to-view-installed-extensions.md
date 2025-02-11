---
title: View Installed Extensions
description: This article describes how to view installed extensions in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to view installed extensions in an Azure Database for PostgreSQL flexible server.
---

# View installed extensions

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You might want to view the extensions that are installed in an Azure Database for PostgreSQL flexible server, and their corresponding versions.

## Steps to view installed extensions

To list the extensions currently installed on your database, use the following SQL command:

```sql
SELECT * FROM pg_extension;
```

## Related content

- [Allow extensions](how-to-allow-extensions.md)
- [Load libraries](how-to-load-libraries.md)
- [Create extensions](how-to-create-extensions.md)
- [Drop extensions](how-to-drop-extensions.md)
- [Update extensions](how-to-update-extensions.md)
