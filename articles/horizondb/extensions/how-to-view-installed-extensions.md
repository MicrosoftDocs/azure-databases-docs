---
title: View installed extensions
description: This article describes how to view installed extensions in an Azure HorizonDB flexible server instance.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 02/17/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to view installed extensions in an Azure HorizonDB flexible server instance.
---

# View installed extensions


You might want to view the extensions that are installed in an Azure HorizonDB flexible server instance, and their corresponding versions.

## Steps to view installed extensions

To list the extensions currently installed on your database, use the following SQL command:

```sql
SELECT * FROM pg_extension;
```

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
