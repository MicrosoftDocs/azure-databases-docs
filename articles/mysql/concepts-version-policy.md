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
| MySQL Version 9.2 | [9.2.0](https://dev.mysql.com/doc/relnotes/mysql/9.1/en/news-9-2-0.html) | Public Preview|

Read the version support policy for retired versions in [version support policy documentation.](concepts-version-policy.md#retired-mysql-engine-versions-not-supported-in-azure-database-for-mysql)

## Major version support

Azure Database for MySQL supports each major version of MySQL from the date Azure begins supporting it until the MySQL community retires it, as provided in the [versioning policy](https://www.mysql.com/support/eol-notice.html).

## Innovation release version support

The MySQL Innovation Release versions are provided to enable access to the latest MySQL features and capabilities. Support for these versions includes core functionalities, but excludes advanced features such as High Availability (HA), replicas, and automated backups. Innovation Release support is limited to the most current version, with previous versions not retained to ensure users have access to the newest advancements. Each Innovation Release server has a 30-day lifecycle from the date of creation, after which it's automatically removed. No monthly maintenance updates are applied during the lifecycle of these versions.
> [!NOTE]  
> Innovation Release versions are intended for early access and experimentation. As such, they don't qualify for customer support cases, and no direct support assistance is provided. Users are encouraged to refer to documentation and community resources for troubleshooting and guidance.

## Minor version support

Azure Database for MySQL automatically performs minor version upgrades to the Azure-preferred version as part of periodic maintenance.

## Major version retirement policy

The retirement details for MySQL major versions are listed in the following table. Dates shown follow the [MySQL versioning policy](https://www.mysql.com/support/eol-notice.html).

| Version | What's New | Azure support start date | Community Retirement date |Azure standard support end date |Azure extend support start date | Azure extend support end date |
| --- | --- | --- | --- | --- | --- | --- |
| [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-31.html) | March 20, 2018 | October 31, 2023 | April 30, 2026 | May 1, 2026 |December 30, 2028 |
| [MySQL 8](https://mysqlserverteam.com/whats-new-in-mysql-8-0-generally-available/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-21.html) | December 11, 2019 | April 30, 2026 | May 31, 2026 | June 1, 2026 |April 30, 2029|
| [MySQL 8.4](https://dev.mysql.com/doc/refman/8.4/introduction.html)|[Features](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)|July 1, 2025| April 30, 2032 | May 31, 2032 | June 1, 2032 | TBD |

> [!NOTE]
> For each deprecated Azure Database for MySQL version, the Azure standard support end date is typically set 1-2 months after the community deprecation date. This grace period provides customers with additional time to decide whether to upgrade to a newer version or to be enrolled in the paid Extended Support plan.
> For Azure Database for MySQL 5.7, the community end of life (EOL) was announced in October 2023. The standard support end date was originally planned for September 2025, but based on customer feedback, we have extended standard support for MySQL 5.7 until April 2026. Extended Support for MySQL 5.7 will begin in May 2026.
> For details on what happens after standard support ends, including the Extended Support policy, see the next section.

## What happens after standard support ends: Extended Support policy

To provide customers with sufficient time to decide whether to upgrade or be enrolled in Extended Support, the Extended Support plan will officially begin in Spring 2026.

After the standard support end date, Azure Database for MySQL servers running on unsupported MySQL versions are automatically enrolled in Extended Support and will be automatically charged for this service. Extended Support provides security and support updates for up to three years after the end of standard support, allowing customers additional time to plan and execute major version upgrades. If you wish to avoid Extended Support charges, you must upgrade your Azure Database for MySQL server to a MySQL version that is still within standard support.

During the Extended Support period, Microsoft prioritizes the service's availability, reliability, and security. Essential modifications are implemented to ensure the service remains accessible and protected, but new features and minor version upgrades may not be guaranteed.

> [!NOTE]  
> Extended Support is automatically applied and charged to servers running on legacy MySQL versions after standard support ends. To opt out of Extended Support and avoid charges, customers must upgrade to a supported major version. For more information or to provide feedback, please contact [Ask Azure DB For MySQL](mailto:AskAzureDBforMySQL@service.microsoft.com).

### FAQs

__Q: What will happen if I don't upgrade my Azure Database for MySQL server to a supported major version after standard support ends?__

A: If you don't upgrade your Azure Database for MySQL server to a supported major version after standard support ends, your server will be automatically enrolled in Extended Support and you'll be automatically charged for this service. To avoid Extended Support charges, you must upgrade your server to a MySQL version that is still within standard support.

__Q: What is the process for performing a major version upgrade on Azure Database for MySQL - Flexible Server?__

A: Azure Database for MySQL - Flexible Server enables you to carry out in-place major version upgrades using the Major Version Upgrade (MVU) feature. Consult the [Major version upgrade in Azure Database for MySQL - Flexible Server](flexible-server/how-to-upgrade.md) document for more detailed information.

__Q: Are there any expected downtime or performance impacts during a major version upgrade?__

A: Yes, it's expected that there will be some downtime during the major version upgrade process. The specific duration varies depending on factors such as the size and complexity of the database. We advise conducting a test upgrade on a nonproduction environment to assess the expected downtime and evaluate the potential performance. To minimize downtime for your applications during the upgrade, you can explore the option of [performing a minimal downtime major version upgrade using read replica](flexible-server/how-to-upgrade.md#perform-minimal-downtime-major-version-upgrade-from-mysql-57-to-mysql-80-using-read-replicas).

__Q: Can I roll back to a previous major version after upgrading?__

A: While it's not recommended to downgrade to a previous major version after upgrading, we acknowledge that there might be specific scenarios where this flexibility becomes necessary. To ensure a smooth upgrade process and alleviate any potential concerns, it's advised to adhere to best practices by performing a comprehensive [on-demand backup](flexible-server/how-to-trigger-on-demand-backup.md) before proceeding with the upgrade. This backup serves as a precautionary measure, allowing you to [restore your database](flexible-server/how-to-restore-server-portal.md) to its previous version on another new Azure Database for MySQL - Flexible Server if needed.

__Q: What are the main advantages of upgrading to a newer major version?__

A: Newer major versions of MySQL come with a host of improvements, including enhanced performance, security, and new features. For details, refer to the relevant MySQL release notes.

__Q: Are there any compatibility issues to be aware of when upgrading to a newer major version?__

A: Changes in newer major versions might cause some compatibility issues. It's important to test your applications with the new version before upgrading the production database. Check [MySQL's official documentation](https://dev.mysql.com/doc/) for a detailed list of compatibility issues.

__Q: What support is available if I encounter issues during the upgrade process?__

A: If you have questions, get answers from community experts in [Microsoft Q&A](https://aka.ms/microsoft-azure-mysql-qa). If you have a support plan and you need technical help, create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest).

__Q: What will happen to my data during the upgrade?__

A: While your data remain unaffected during the upgrade process, it's highly advisable to create a backup before proceeding with the upgrade. This precautionary measure helps mitigate the risk of potential data loss due to any unforeseen complications.

## Retired MySQL engine versions not supported in Azure Database for MySQL

The following restrictions apply only after the Extended Support period has ended and your server is still running a retired MySQL version:

- No further security or support updates will be provided for the retired version. Azure Database for MySQL will not patch the retired database engine for any bugs or security issues, and support for database engine-related issues will no longer be available. However, Azure will continue performing periodic maintenance and patching for the host, OS, containers, and other service-related components.
- You won't be able to create new database servers for the retired version. However, you can perform point-in-time recoveries and create read replicas for your existing servers.
- New service capabilities developed by Azure Database for MySQL might only be available to supported database server versions.
- Uptime S.L.A.s apply solely to Azure Database for MySQL service-related issues and not to any downtime caused by database engine-related bugs.
- In the extreme event of a serious threat to the service caused by the MySQL database engine vulnerability identified in the retired database version, Azure might choose to stop the compute node of your database server from securing the service first. You're asked to upgrade the server before bringing it online. During the upgrade process, your data is always protected using automatic backups performed on the service, which can be used to restore to the older version if desired.

## Related content

- [dump and restore](flexible-server/concepts-migrate-dump-restore.md)
