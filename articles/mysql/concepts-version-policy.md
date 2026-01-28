---
title: Version Support Policy
description: Describes the policy around MySQL major and minor versions in Azure Database for MySQL
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 06/27/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - fasttrack-edit
  - ignite-2024
---

# Azure Database for MySQL version support policy

Azure Database for MySQL provides a fully managed database service powered by the MySQL community edition, enabling developers to build and scale applications efficiently. This article outlines the version support policy for Azure Database for MySQL, detailing the lifecycle management, including version availability, updates, and end-of-support timelines. Customers can ensure their applications remain secure, performant, and aligned with the latest MySQL innovations while minimizing disruption during version transitions, by understanding this policy.

## Supported MySQL versions

Azure Database for MySQL was developed from the [MySQL Community Edition](https://www.mysql.com/products/community/), using the InnoDB storage engine. The service supports the community's current major versions, namely MySQL 5.7 and 8.0. MySQL uses the X.Y.Z. naming scheme where X.Y is the major version, Z is the minor version.Z is incremented for each new LTS release, but is likely always 0 for innovation releases. For more information about the scheme, see the [MySQL documentation](https://dev.mysql.com/doc/refman/8.4/en/which-version.html).

Azure Database for MySQL currently supports the following major and minor versions of MySQL:

| Version | Current minor version | Release status |
| :--- | :--- | :--- |
| MySQL Version 5.7 | [5.7.44](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-44.html) | GA |
| MySQL Version 8.0 | [8.0.42](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-42.html) | GA |
| MySQL Version 8.4 | [8.4.5](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/news-8-4-5.html) | GA |
| MySQL Version 9.3 | [9.3.0](https://dev.mysql.com/doc/relnotes/mysql/9.1/en/news-9-3-0.html) | Public Preview |

Read the version support policy for retired versions in [version support policy documentation.](concepts-version-policy.md#retired-mysql-engine-versions-not-supported-in-azure-database-for-mysql)

## Major version support

Azure Database for MySQL supports each major version of MySQL from the date Azure begins supporting it until the MySQL community retires it, as provided in the [versioning policy](https://www.mysql.com/support/eol-notice.html).

### Major version retirement policy

The retirement details for MySQL major versions are listed in the following table. Dates shown follow the [MySQL versioning policy](https://www.mysql.com/support/eol-notice.html).

| Version | What's New | Azure Support Start Date | Community Retirement Date | Azure Standard Support End Date | Azure Extended Support Start Date | Azure Extended Support End Date |
| --- | --- | --- | --- | --- | --- | --- |
| [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-31.html) | March 20, 2018 | October 31, 2023 | March 31, 2026 | April 1, 2026 | March 31, 2029 |
| [MySQL 8.0](https://mysqlserverteam.com/whats-new-in-mysql-8-0-generally-available/) | [Features](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-21.html) | December 11, 2019 | April 30, 2026 | May 31, 2026 | June 1, 2026 | May 31, 2029 |

### What happens after standard support ends?

To provide customers with sufficient time to decide whether to upgrade to a supported version, Extended Support is planned to begin in spring 2026.

After the standard support end date, Azure Database for MySQL servers running on unsupported MySQL versions are automatically enrolled in Extended Support and are automatically charged for this service after a one-month grace period. Extended Support provides critical security updates for up to three years after the end of standard Support, allowing customers more time to plan and execute major version upgrades. To avoid Extended Support charges, you must upgrade your Azure Database for MySQL server to a MySQL version that is still within standard Support.

During the Extended Support period, Microsoft prioritizes the service's availability, reliability, and security. Essential modifications are implemented to ensure the service remains accessible and protected, but new features and minor version upgrades might not be guaranteed.

> [!NOTE]  
> Extended Support is automatically applied and charged to servers running on legacy MySQL versions after standard Support ends. To opt out of Extended Support and avoid charges, customers must upgrade to a supported major version of the software. For more information or to provide feedback, contact [Ask Azure Database For MySQL](mailto:AskAzureDBforMySQL@service.microsoft.com).
>  
> Pricing is available on the [pricing page](https://azure.microsoft.com/pricing/details/mysql/?cdn=disable) later this year.

## Innovation release version support

The MySQL Innovation Release versions are provided to enable access to the latest MySQL features and capabilities. Support for these versions includes core functionalities but excludes advanced features such as High Availability (HA), replicas, and automated backups. Innovation Release support is limited to the most current version, with previous versions not retained to ensure users have access to the newest advancements. Each Innovation Release server has a 30-day lifecycle from the date of creation, after which it's automatically removed. No monthly maintenance updates are applied during the lifecycle of these versions.

> [!NOTE]  
> Innovation Release versions are intended for early access and experimentation. As such, they don't qualify for customer support cases, and no direct support assistance is provided. Users are encouraged to refer to documentation and community resources for troubleshooting and guidance.

## Minor version support

Azure Database for MySQL automatically performs minor version upgrades to the Azure-preferred version as part of periodic maintenance.

## Retired MySQL engine versions not supported in Azure Database for MySQL

The following restrictions apply only after the extended support period has ended, and your server is still running a retired MySQL version:

- No further security or support updates are provided for the retired version. Azure Database for MySQL can't patch the retired database engine for any bugs or security issues, and support for database engine-related issues are no longer be available. However, Azure continues performing periodic maintenance and patching for the host, OS, containers, and other service-related components.
- You can't create new database servers for the retired version. However, you can perform point-in-time recoveries and create read replicas for your existing servers.
New service capabilities developed by Azure Database for MySQL might only be available for supported database server versions.
- Uptime S.L.A.s apply solely to Azure Database for MySQL service-related issues and not to any downtime caused by database engine-related bugs.
- In the extreme event of a serious threat to the service caused by the MySQL database engine vulnerability identified in the retired database version, Azure might choose to stop the compute node of your database server from securing the service first. You're asked to upgrade the server before bringing it online. During the upgrade process, your data is always protected by automatic backups performed on the service, which can be used to restore it to an older version if desired.

## Frequently asked questions (FAQ)

__Q: What happens if I don't upgrade my Azure Database for MySQL server to a supported major version after standard support ends?__

A: If you don't upgrade your Azure Database for MySQL server to a supported major version before the Azure extended support start date, your server is automatically enrolled in extended support, and you're charged for this service. To avoid extended support charges, you must upgrade your server to a MySQL version that is still within the standard support Period.

__Q: What is the process for performing a major version upgrade on Azure Database for MySQL?__

A: Azure Database for MySQL enables you to carry out in-place major version upgrades using the Major Version Upgrade (MVU) feature. Consult the [Major version upgrade in Azure Database for MySQL](flexible-server/how-to-upgrade.md) [Major version upgrade in Azure Database for MySQL](flexible-server/how-to-upgrade.md) document for more detailed information.

__Q: Are there any expected downtime or performance impacts during a major version upgrade?__

A: Yes, there's some downtime during the major version upgrade process. The specific duration varies depending on factors such as the size and complexity of the database. We recommend conducting a test upgrade in a nonproduction environment to assess the expected downtime and evaluate potential performance. To minimize downtime for your applications during the upgrade, you can explore the option of [performing a minimal downtime major version upgrade using read replica](flexible-server/how-to-upgrade.md#perform-minimal-downtime-major-version-upgrade-using-read-replicas).

__Q: Can I roll back to a previous major version after upgrading?__

A: While it's not recommended to downgrade to a previous major version after upgrading, we acknowledge that there might be specific scenarios where this flexibility becomes necessary. To ensure a smooth upgrade process and alleviate any potential concerns, it's advisable to adhere to best practices by performing a comprehensive [on-demand backup](flexible-server/how-to-trigger-on-demand-backup.md), before proceeding with the upgrade.

This backup serves as a precautionary measure, allowing you to [restore your database](flexible-server/how-to-restore-server-portal.md) to its previous version on another new Azure Database for MySQL if needed.

__Q: What are the main advantages of upgrading to a newer major version?__

A: Newer major versions of MySQL come with a host of improvements, including enhanced performance, security, and new features. For details, refer to the relevant MySQL release notes.

__Q: Are there any compatibility issues to be aware of when upgrading to a newer major version?__

A: Changes in newer major versions might cause some compatibility issues. It's important to test your applications with the new version before upgrading the production database. Refer to [MySQL's official documentation](https://dev.mysql.com/doc/) for a comprehensive list of compatibility issues.

__Q: What support is available if I encounter issues during the upgrade process?__

A: If you have questions, get answers from community experts in [Microsoft Q&A](https://aka.ms/microsoft-azure-mysql-qa). If you have a support plan and you need technical help, create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest).

__Q: What happens to my data during the upgrade?__

A: While your data remains unaffected during the upgrade process, it's highly advisable to create a backup before proceeding with the upgrade. This precautionary measure helps mitigate the risk of potential data loss due to any unforeseen complications.

__Q: What is Azure Database for MySQL – Extended Support?__

A: Extended Support is a feature offering that allows customers to continue running MySQL versions that have reached community end-of-life (end of support), with continued access to SLA-backed availability, security updates, and technical support.

__Q: Is Extended Support a separate support plan like Azure Standard or Professional Direct Support?__

A: No. Extended Support is not a support plan. It is a feature of the Azure Database for MySQL service that applies to specific MySQL versions after their community end of support. It is independent of your Azure Support Plan.

__Q: Do I need to take any action to enable Extended Support?__

A: No action is required. If your server is running a MySQL version that has entered the Extended Support phase, it will be automatically enrolled.

__Q: When does billing for Extended Support begin?__

A: Billing starts one month after the community end of support date of the MySQL version. This one-month grace period gives customers time to plan their upgrade or evaluate options.

__Q: How is Extended Support priced?__

A: Extended Support is billed on a per vCore per hour basis. Pricing details will be published in November 2025 and will be available in the https://azure.microsoft.com/pricing/calculator/.

__Q: How do I exit Extended Support?__

A: Simply upgrade your server to a MySQL version that is still under community support. Once the upgrade is complete, your server will automatically exit Extended Support and billing will stop.

## Related content

- [Major version upgrade in Azure Database for MySQL](flexible-server/how-to-upgrade.md)
- [Dump and restore](flexible-server/concepts-migrate-dump-restore.md)
