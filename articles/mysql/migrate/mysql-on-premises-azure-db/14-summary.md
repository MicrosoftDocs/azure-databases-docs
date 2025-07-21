---
title: "Migrate MySQL On-Premises to Azure Database for MySQL: Summary"
description: "This document has covered several topics related to migrating an application from on-premises MySQL to Azure Database for MySQL."
author: saikondapalli11
ms.author: skondapalli
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
---

# Migrate MySQL on-premises to Azure Database for MySQL: Summary

Migrating MySQL databases from on-premises environments to Azure Database for MySQL offers numerous benefits, including enhanced scalability, security, and performance. This article comprehensively summarizes the key steps and considerations involved in the migration process. By understanding the assessment, planning, migration methods, testing, optimization, and post-migration management, you can ensure a smooth and successful transition to Azure. This guide will equip you with the insights and best practices needed to navigate each migration phase, leveraging Azure's robust features to achieve operational efficiency and cost savings. Whether modernizing your database infrastructure or improving disaster recovery capabilities, this summary will provide you with the essential knowledge to make informed decisions and achieve a seamless migration.

## Prerequisites

[Migrate MySQL on-premises to Azure Database for MySQL: Security](13-security.md)

## Overview

This document has covered several topics related to migrating an application from on-premises MySQL to Azure Database for MySQL. We covered how to begin and assess the project all the way to application cut over.

The migration team needs to review the topics carefully as the choices made can have project timeline effects. The total cost of ownership is enticing given the many enterprise ready features provided.

The migration project approach is important. The team needs to assess the application and database complexity to determine the amount of conversion time. Conversion tools help make the transition easier, but there have always been an element of manual review and updates required. Scripting out pre-migration tasks and post migration testing is important.

Application architecture and design can provide strong indicators as to the level of effort required. For example, applications utilizing ORM frameworks can be great candidates, especially if the business logic is contained in the application instead of database objects.

In the end, several tools exist in the marketplace ranging from free to commercial. This document covered the steps required if the team plans a database migration using one of the more popular open-source tool options. Whichever path that is chosen, Microsoft and the MySQL community have the tools and expertise to make the database migration successful.

## Feedback and support

For any questions or suggestions you might have about working with Azure Database for MySQL flexible server, consider the following points of contact:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/d365community/forum/47b1e71d-ee24-ec11-b6e6-000d3a4f0da0).

## Find a partner to help migrate

This guide can be overwhelming, but don't fret\! There are many experts in the community with a proven migration track record. [Search for a Microsoft Partner](https://appsource.microsoft.com/marketplace/partner-dir) or [Microsoft MVP](https://mvp.microsoft.com/search?target=Profile&program=MVP) to help with finding the most appropriate migration strategy. You aren't alone\!

You can also browse the technical forums and social groups for more detailed real-world information:

  - [Microsoft Community Forum ](/answers/topics/azure-database-mysql.html)

  - [Azure Database for MySQL Tech Community ](https://techcommunity.microsoft.com/category/azuredatabases/blog/adformysql)

  - [StackOverflow for Azure MySQL ](https://stackoverflow.com/questions/tagged/azure-database-mysql)

  - [Azure Facebook Group ](https://www.facebook.com/groups/MsftAzure?_rdr)

  - [LinkedIn Azure Group ](https://www.linkedin.com/error_pages/unsupported-browser.html)

  - [LinkedIn Azure Developers Group ](https://www.linkedin.com/error_pages/unsupported-browser.html)

## Next step

> [!div class="nextstepaction"]
> [appendix](15-appendix.md)
