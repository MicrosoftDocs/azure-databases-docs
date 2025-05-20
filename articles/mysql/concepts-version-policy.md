---
title: Version Support Policy - Azure Database for MySQL - Flexible Server
description: Describes the policy around MySQL major and minor versions in Azure Database for MySQL
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - fasttrack-edit
  - ignite-2024
---

# Azure Database for MySQL version support policy

Azure Database for MySQL provides a fully managed database service powered by the MySQL community edition, enabling developers to build and scale applications efficiently. This article outlines the version support policy for Azure Database for MySQL, detailing the lifecycle management, including version availability, updates, and end-of-support timelines. By understanding this policy, customers can ensure their applications remain secure, performant, and aligned with the latest MySQL innovations while minimizing disruption during version transitions.

## Supported MySQL versions

Azure Database for MySQL was developed from the [MySQL Community Edition](https://www.mysql.com/products/community/), using the InnoDB storage engine. The service supports the community's current major versions, namely MySQL 5.7 and 8.0. MySQL uses the X.Y.Z. naming scheme where X is the major version, Y is the minor version, and Z is the bug fix release. For more information about the scheme, see the [MySQL documentation](https://dev.mysql.com/doc/refman/5.7/en/which-version.html).

Azure Database for MySQL currently supports the following major and minor versions of MySQL:

| Version | [Flexible Server?](flexible-server/overview.md)<br />Current minor version |Release status|
| :--- | :--- |:--- |
| MySQL Version 5.7 | [5.7.44](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-44.html) | GA |
| MySQL Version 8.0 | [8.0.41](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-41.html) | GA |
| MySQL Version 8.4 | [8.4.4](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/news-8-4-4.html) | Public Preview|
| MySQL Version 9.1 | [9.2.0](https://dev.mysql.com/doc/relnotes/mysql/9.1/en/news-9-1-0.html) | Public Preview|

Read the version support policy for retired versions in [version support policy documentation.](concepts-version-policy.md#retired-mysql-engine-versions-not-supported-in-azure-database-for-mysql)

## Major version support

Azure Database for MySQL supports each major version of MySQL from the date Azure begins supporting it until the MySQL community retires it, as provided in the [versioning policy](https://www.mysql.com/support/eol-notice.html).

## Innovation release version support

The MySQL Innovation Release versions are provided to enable access to the latest MySQL features and capabilities. Support for these versions includes core functionalities, but excludes advanced features such as High Availability (HA), replicas, and automated backups. Innovation Release support is limited to the most current version, with previous versions not retained to ensure users have access to the newest advancements. Each Innovation Release server has a 30-day lifecycle from the date of creation, after which it is automatically removed. No monthly maintenance updates are applied during the lifecycle of these versions.
> [!NOTE]  
> Innovation Release versions are intended for early access and experimentation. As such, they do not qualify for customer support cases, and no direct support assistance is provided. Users are encouraged to refer to documentation and community resources for troubleshooting and guidance.

## Minor version support

Azure Database for MySQL automatically performs minor version upgrades to the Azure-preferred version as part of periodic maintenance.

## Major version retirement policy

The retirement details for MySQL major versions are listed in the following table. Dates shown follow the [MySQL versioning policy](https://www.mysql.com/support/eol-notice.html).

| Version | What's New | Azure support start date | Azure support end date | Community Retirement date
| --- | --- | --- | --- | --- |
| [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-31.html) | March 20, 2018 | September 2027 | October 2023 |
| [MySQL 8](https://mysqlserverteam.com/whats-new-in-mysql-8-0-generally-available/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-21.html) | December 11, 2019 | NA | April 2026 |

## What happens to Azure Database for MySQL service after the MySQL community version is retired in October 2023?

In response to the customer's requests, Microsoft decided to prolong the support for Azure Database for MySQL beyond __October 2023__. During the extended support period, which lasts until __September 2027__, Microsoft prioritizes the service's availability, reliability, and security. While there are no guarantees regarding minor version upgrades, we implement essential modifications to ensure the service remains accessible, dependable, and protected. Our plan includes:

- Free Extended support for v5.7 on Azure Database for MySQL- Flexible Servers until __September 2025__, offering ample time for customers to plan and execute their upgrades to MySQL v8.0 without additional charge.
- Paied Extended support for for v5.7 on Azure Database for MySQL- Flexible Servers until __September 2027__, providing customers who require additional time the flexibility to plan and complete their upgrade from MySQL 5.7 to MySQL 8.0. This program offers the same level of SLA, security, and compliance as regular major MySQL versions.

> [!NOTE]  
> After careful consideration and listening to customer feedback, we have decided to further extend support for Azure Database for MySQL version 5.7 by an additional two years. This will be part of a paid extended support program, designed to provide customers with the same SLA support and security compliance as regular major MySQL versions during the extended support period. Pricing details for the extended support program are still being finalized.
> We hope this extension will give customers who need more time the flexibility to plan and execute their upgrade from MySQL 5.7 to MySQL 8.0. If you have any concerns or would like to share your feedback regarding this extended support program, please email us at [Ask Azure DB For MySQL](mailto:AskAzureDBforMySQL@service.microsoft.com). Your input is highly valued, and we look forward to collaborating with you during this transition.

### FAQs

__Q: What will happen if I don't upgrade MySQL 5.7 to 8.0 after September 2025?__

A: Customers who have not upgraded to MySQL 8.0 by September 2025 will automatically be enrolled in the paid extended support program to ensure continued access to SLA support, security, and compliance during the extended support period.

__Q: What is the process for upgrading the Azure database for MySQL - Flexible server from version v5.7 to v8.0?__

A: Starting May 2023, Azure Database for MySQL - Flexible Server enables you to carry out an in-place upgrade from MySQL v5.7 to v8.0 utilizing the Major Version Upgrade (MVU) feature. Consult the [Major version upgrade in Azure Database for MySQL - Flexible Server](flexible-server/how-to-upgrade.md) document for more detailed information.

__Q: Are there any expected downtime or performance impacts during the upgrade process?__

A: Yes, it's expected that there will be some downtime during the upgrade process. The specific duration varies depending on factors such as the size and complexity of the database. We advise conducting a test upgrade on a nonproduction environment to assess the expected downtime and evaluate the potential performance. Suppose you minimize downtime for your applications during the upgrade. In that case, you can explore the option of [perform minimal downtime major version upgrade from MySQL 5.7 to MySQL 8.0 using read replica](flexible-server/how-to-upgrade.md#perform-minimal-downtime-major-version-upgrade-from-mysql-57-to-mysql-80-using-read-replicas).

__Q: Can I roll back to MySQL v5.7 after upgrading to v8.0?__

A: While it's not recommended to downgrade from MySQL v8.0 to v5.7, as the latter is nearing its End of Life status, we acknowledge that there might be specific scenarios where this flexibility becomes necessary. To ensure a smooth upgrade process and alleviate any potential concerns, it's advised to adhere to best practices by performing a comprehensive [on-demand backup](flexible-server/how-to-trigger-on-demand-backup.md) before proceeding with the upgrade to MySQL v8.0. This backup serves as a precautionary measure, allowing you to [restore your database](flexible-server/how-to-restore-server-portal.md) to its previous version on to another new Azure Database for MySQL - Flexible Server for any unexpected issues or complications with MySQL v8.0.

__Q: What are the main advantages of upgrading to MySQL v8.0?__

A: MySQL v8.0 comes with a host of improvements, including a more efficient data dictionary, enhanced security, and other features like common table expressions and window functions. For details, refer to [MySQL 8.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-32.html)

__Q: Are there any compatibility issues to be aware of when upgrading to MySQL v8.0?__

A: Changes in MySQL v8.0 might cause some compatibility issues. It's important to test your applications with MySQL v8.0 before upgrading the production database. Check [MySQL's official documentation](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.html) for a detailed list of compatibility issues.

__Q: What support is available if I encounter issues during the upgrade process?__

A: If you have questions, get answers from community experts in [Microsoft Q&A](https://aka.ms/microsoft-azure-mysql-qa). If you have a support plan and you need technical help, create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest).

__Q: What will happen to my data during the upgrade?__

A: While your data will remain unaffected during the upgrade process, it's highly advisable to create a backup before proceeding with the upgrade. This precautionary measure helps mitigate the risk of potential data loss due to any unforeseen complications.

## Retired MySQL engine versions not supported in Azure Database for MySQL

After the retirement date for each MySQL database version, if you continue running the retired version, note the following restrictions:

As the community won't release any further bug fixes or security fixes, Azure Database for MySQL won't patch the retired database engine for any bugs or security issues or otherwise take security measures regarding it. However, Azure continues performing periodic maintenance and patching for the host, OS, containers, and other service-related components.
- If any support issue you might experience relates to the MySQL database, we might be unable to assist you. In such cases, you must upgrade your database for us to provide you with any support.
- You won't be able to create new database servers for the retired version. However, you can perform point-in-time recoveries and create read replicas for your existing servers.
- New service capabilities developed by Azure Database for MySQL might only be available to supported database server versions.
- Uptime S.L.A.s apply solely to Azure Database for MySQL service-related issues and not to any downtime caused by database engine-related bugs.
In the extreme event of a serious threat to the service caused by the MySQL database engine vulnerability identified in the retired database version, Azure might choose to stop the compute node of your database server from securing the service first. You're asked to upgrade the server before bringing it online. During the upgrade process, your data is always protected using automatic backups performed on the service, which can be used to restore to the older version if desired.

## Related content

- [dump and restore](flexible-server/concepts-migrate-dump-restore.md)
