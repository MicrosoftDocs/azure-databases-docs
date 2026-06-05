---
title: View Installed Extensions in Azure HorizonDB
description: This article describes how to view installed extensions in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: how-to
# customer intent: As a user, I want to learn how to view installed extensions in an Azure HorizonDB instance.
---

# View installed extensions for Azure HorizonDB (Preview)

You might want to view the extensions that are installed in an Azure HorizonDB instance, and their corresponding versions.

## Steps to view installed extensions

To list the extensions currently installed on your database, use the following SQL command:

```sql
SELECT * FROM pg_extension;
```

## Related content

- [Extensions and modules in Azure HorizonDB (Preview)](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB (Preview)](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB (Preview)](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB (Preview)](concepts-extensions-by-engine.md)
