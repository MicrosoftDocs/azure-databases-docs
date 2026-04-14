---
title: Extended Support
description: Describes the extended support offering for Postgres major versions for Azure Database for PostgreSQL flexible server instances.
author: andtapia
ms.author: andreatapia
ms.reviewer: maghan
ms.date: 03/26/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
---

# Azure Database for PostgreSQL extended support

To help you maintain secure and compliant workloads beyond community end-of-life (end of support), Azure is introducing Extended Support for Azure Database for PostgreSQL.

Extended support gives you continued access to critical security updates and technical assistance. By using Extended Support, you have time to plan and implement your upgrade strategy with confidence.

Extended support provides:

- Up to three extra years of support after standard support ends
- Security patches and critical bug fixes
- Technical support through Azure Support channels (per your existing plan)

> [!NOTE]  
> Extended Support doesn't include new feature releases, performance enhancements, or support for minor version upgrades.

### Why use Extended Support?

Extended Support is ideal for customers who...

- Need more time to upgrade complex workloads.
- Require compliance and security coverage during upgrade planning.
- Depend on uninterrupted technical support for critical environments.

### Best practices

- Treat Extended Support as a temporary bridge, not a long-term solution.
- Start upgrade planning well before the end-of-life (end of support) date.
- Consider upgrading to newer versions such as PostgreSQL 15 or 16 for improved performance and support.

### Eligible PostgreSQL versions

| PostgreSQL Version | Azure Standard Support Start Date | Community Retirement Date | Azure Standard Support End Date | Paid Extended Support Start Date | Paid Extended Support End Date |
| --- | --- | --- | --- | --- | --- |
| 11 | July 24, 2019 | November 9, 2023 | July 31, 2026 | August 1, 2026 | November 8, 2026 |
| 12 | September 22, 2020 | November 14, 2024 | July 31, 2026 | August 1, 2026 | November 13, 2027 |
| 13 | May 25, 2021 | November 13, 2025 | July 31, 2026 | August 1, 2026 | November 12, 2028 |
| 14 | June 29, 2022 | November 12, 2026 | December 11, 2026 | December 12, 2026 | November 11, 2029 |

### Enrollment and price

- Automatic enrollment: PostgreSQL servers running unsupported versions are automatically enrolled in Extended Support on July 1, 2026.
- Opt-out option: You can opt out at any time by upgrading to a supported version.
- Grace period: A grace period applies and billing begins on August 1, 2026.
- Pricing: Details are published on this [page](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/?cdn=disable).

### Frequently asked questions (FAQs)

**Q: What if I want to keep running without extended support? Can I opt out?**

A: No.

**Q: What happens if I continue running an unsupported PostgreSQL version on Azure after its community end of support?**

A: Your server is automatically enrolled in Extended Support one month after the community end of support date.

**Q: Can I continue using my PostgreSQL instance without Extended Support?**

A: No, extended support is not optional. After the grace period, you're automatically enrolled in paid Extended Support unless you upgrade to a supported version. 

**Q: Will I be charged for Extended Support if my server is stopped, failed, or not running??**

A: No. Extended support billing charges apply only to servers that are in a Succeeded (running) state. If a server is stopped, deleted, or in a failed provisioning state, extended support charges will not be applied for that period. Billing automatically resumes once the server returns to a succeeded state and continues running an end‑of‑life engine version under extended support.

**Q: What happens if I’m ready to upgrade to a supported PostgreSQL version, but capacity constraints in my region prevent me from upgrading before Extended Support billing begins?**

A: If regional capacity constraints prevent you from upgrading, your server will be temporarily excluded from Extended Support billing until capacity becomes available and an upgrade path is offered, ensuring you’re not charged for factors outside your control.

**Q: Can my applications break during a major version upgrade?**

A: PostgreSQL major version upgrades can introduce changes that might affect your application - such as deprecated configuration parameters, incompatible extensions, or SQL behavior differences. Validate upgrades in a nonproduction environment before applying them in production. For more details, review the key considerations and limitations in [Major Version Upgrades](./concepts-major-version-upgrade.md) docs.

[!INCLUDE [supported-upgrades](includes/supported-upgrades.md)]

**Q: How do I know if my server is in Extended Support?**

A: The Azure portal and CLI clearly indicate if a server is enrolled in Extended Support.

**Q: Do I need to update Server Parameters post major version upgrades?**

A: No manual change is required. The upgrade workflow automatically updates the parameters for the new PostgreSQL Version.

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

A: Azure provides visibility through the portal.

**Q: What support options are available during the Extended Support phase?**

A: Servers in Extended Support can raise support cases for security-related issues only. Feature requests, performance tuning, and general bug fixes aren't supported for end of support versions. Improvements to existing features for end of support versions aren't backported.

**Q: How will the period between November 13, 2025, and March 1, 2026, be handled for PostgreSQL version 13? Will support be continued during this time? How will it differ from the period before November 13, 2025?**

A: According to the [PostgreSQL community versioning policy](https://www.postgresql.org/support/versioning/), each major version is supported until retired by the community. Free Extended support from Azure is provided through July 31, 2026. Customers are charged for Extended Support starting August 1. To ensure continued support and access to new features, upgrade to newer versions.
