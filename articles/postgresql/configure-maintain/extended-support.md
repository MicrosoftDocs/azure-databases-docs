---
title: Extended Support in Azure Database for PostgreSQL Flexible Server
description: Describes the extended support offering for Postgres major versions for Azure Database for PostgreSQL flexible servers.
#customer intent: As a user running an older PostgreSQL version, I want to understand what Extended Support provides so that I can keep my workloads secure and compliant beyond community end-of-life.
author: andtapia
ms.author: andreatapia
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
ai-usage: ai-assisted
---

# Azure Database for PostgreSQL flexible server extended support

To help you maintain secure and compliant workloads beyond community end-of-life (end of support), Azure is introducing extended support for Azure Database for PostgreSQL.

Extended support gives you continued access to critical security updates and technical assistance. By using Extended Support, you have time to plan and implement your upgrade strategy with confidence.

Extended support provides:

- Up to three extra years of support after standard support ends
- Security patches and critical bug fixes
- Technical support through Azure Support channels (per your existing plan)

Extended support doesn't include:

- New features
- Performance enhancements
- General bug fixes
- Performance tuning assistance
- Backports unrelated to security or critical servicing

> [!NOTE]  
> Extended Support doesn't include new feature releases, performance enhancements, or support for minor version upgrades.

### Why use extended support?

Use extended support if you...

- Need more time to upgrade complex workloads.
- Require compliance and security coverage during upgrade planning.
- Depend on uninterrupted technical support for critical environments.

### Best practices

- Treat Extended Support as a temporary bridge, not a long-term solution.
- Start upgrade planning well before the end-of-life (end of support) date.
- Consider upgrading to newer versions such as PostgreSQL 15 or 16 for improved performance and support.
- For more details on supported upgrade paths and limitations, see [Major version upgrade documentation](/azure/postgresql/configure-maintain/concepts-major-version-upgrade).

### Eligible PostgreSQL versions

| PostgreSQL Version | Azure Standard Support Start Date | Community Retirement Date | Azure Standard Support End Date | Extended Support Start Date | Extended Support End Date |
| --- | --- | --- | --- | --- | --- |
| 11 | July 24, 2019 | November 9, 2023 | July 31, 2026 | August 1, 2026 | March 31, 2027 |
| 12 | September 22, 2020 | November 14, 2024 | July 31, 2026 | August 1, 2026 | November 13, 2027 |
| 13 | May 25, 2021 | November 13, 2025 | July 31, 2026 | August 1, 2026 | November 12, 2028 |
| 14 | June 29, 2022 | November 12, 2026 | December 11, 2026 | December 12, 2026 | November 11, 2029 |

### Enrollment and price

- Automatic enrollment: On August 1, 2026, the service automatically enrolls PostgreSQL servers running unsupported versions in Extended Support.
- Opt-out option: You can opt out at any time by upgrading to a supported version.
- Grace period: A grace period applies and billing begins on September 1, 2026.
- Pricing: Details are published on this [page](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/?cdn=disable).

### Frequently asked questions (FAQs)

**Q: How do I stop Extended Support charges?**

A: Upgrade the server to a supported PostgreSQL version. Once the upgrade is successfully completed and the server is running a supported PostgreSQL version, extended support charges no longer apply.

**Q: What if I want to keep running without extended support? Can I opt out?**

A: No. Extended support is automatically applied to eligible servers running unsupported PostgreSQL versions. To stop extended support charges, upgrade to a supported PostgreSQL version.

**Q: Is there a gap in support coverage between Azure Standard Support ending and Extended Support billing beginning?**

A: No. There is no gap in support coverage. Eligible servers transition into extended support immediately after Azure Standard Support ends. If a grace period applies, customers continue receiving extended support benefits during that period at no additional charge. Billing begins after the grace period ends.

**Q: What happens if I continue running an unsupported PostgreSQL version on Azure after its community end of support?**

A: Your server is automatically enrolled in extended support once the Azure Standard Support period ends for that PostgreSQL version. If a grace period applies, your server continues receiving extended support benefits during that period before billing begins.

**Q: Can I continue using my PostgreSQL instance without Extended Support?**

A: No. Servers running unsupported PostgreSQL versions are automatically enrolled in extended support. After any applicable grace period ends, extended support charges apply unless the server is upgraded to a supported PostgreSQL version.

**Q: Will I be charged for extended support if my server is stopped, failed, or not running?**

A: No. Extended support billing charges apply only to servers that are in a Succeeded (running) state in Azure. If a server is stopped, deleted, or in a failed provisioning state, extended support charges aren't applied for that period. Billing automatically resumes once the server returns to a succeeded state and continues running an end‑of‑life engine version under extended support.

**Q: I upgraded during the billing month. Will I still be charged?**

A: Yes. Extended support charges are billed based on the time a server runs on an unsupported PostgreSQL version. If you upgrade during a billing period, charges apply only for the time the server was operating under extended support before the upgrade was completed.

**Q: What happens if I'm ready to upgrade to a supported PostgreSQL version, but capacity constraints in my region prevent me from upgrading before Extended Support billing begins?**

A: If regional capacity constraints prevent you from upgrading to a supported PostgreSQL version, your server might be temporarily excluded from extended support billing until capacity becomes available and an upgrade path is offered. Microsoft support channels provide additional guidance on eligibility and validation criteria.

**Q: Can my applications break during a major version upgrade?**

A: PostgreSQL major version upgrades can introduce changes that might affect your application - such as deprecated configuration parameters, incompatible extensions, or SQL behavior differences. Validate upgrades in a nonproduction environment before applying them in production. For more details, review the key considerations and limitations in [Major Version Upgrades](./concepts-major-version-upgrade.md) docs. Customers should thoroughly validate application compatibility and extension support in a nonproduction environment before scheduling a production upgrade.

[!INCLUDE [supported-upgrades](includes/supported-upgrades.md)]

**Q: How do I know if my server is in Extended Support?**

A: The Azure portal and Azure CLI indicate whether a server is enrolled in extended support. You can also find information about support status and eligibility through server properties and associated service notifications.

**Q: Do I need to update Parameters post major version upgrades?**

A: In most cases, no manual changes are required. The upgrade workflow automatically updates parameter defaults as needed for the target PostgreSQL version. Review application-specific settings after the upgrade to ensure they continue to meet your requirements.

**Q: Are PostgreSQL extensions automatically upgraded during a major version upgrade?**

A: No. While Azure upgrades the database engine, noncore extensions (for example, pgvector, timescaledb) require manual updates. Use `ALTER EXTENSION ... UPDATE` or recreate unsupported extensions after the upgrade.

**Q: How can I reduce downtime during a major upgrade?**

A: To minimize downtime:
- Plan upgrades during low-traffic hours.
- Identify and fix any upgrade blockers (for example, extensions, roles, replication slots) ahead of the upgrade.
- Pause background jobs and long-running sessions.
- Temporarily scale up compute to speed up pg_upgrade.
- Clean up bloat with VACUUM or REINDEX if needed.
- Run ANALYZE after upgrade to restore performance.

**Q: Where can I track which of my servers are nearing end of support?**

A: The Azure portal provides visibility, including indicators for servers approaching end of support and servers enrolled in extended support.

**Q: What support options are available during the Extended Support phase?**

A: Extended support includes access to security updates, critical bug fixes, and technical assistance through Azure Support channels in accordance with your support plan. Extended support doesn't include new features, performance enhancements, support for minor version upgrades, or backporting improvements to end-of-support versions.

**Q: How will the period between November 13, 2025, and March 1, 2026, be handled for PostgreSQL version 13? Will support be continued during this time? How will it differ from the period before November 13, 2025?**

A: According to the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/), the community supports each major version until it retires. Azure provides free extended support through August 31, 2026. Starting September 1, customers pay for extended support. To ensure continued support and access to new features, upgrade to newer versions.

## Related content

- [Major version upgrade](concepts-major-version-upgrade.md)
- [Supported PostgreSQL versions](concepts-supported-versions.md)
- [Version support policy](concepts-version-policy.md)
