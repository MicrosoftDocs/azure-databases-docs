---
title: Microsoft Defender for Cloud
description: Learn how to use Microsoft Defender for Cloud to secure Azure Database for PostgreSQL.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
---

# Microsoft Defender for Cloud for Azure Database for PostgreSQL flexible server

**[Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)** detects anomalous activities indicating unusual and potentially harmful attempts to access or exploit databases. Defender for Cloud provides [security alerts](/azure/defender-for-cloud/alerts-open-source-relational-databases) on anomalous activities so that you can detect potential threats and respond to them as they occur.
When you enable this plan, Defender for Cloud provides alerts when it detects anomalous database access and query patterns and suspicious database activities.

These alerts appear in Defender for Cloud's security alerts page and include:

- Details of the suspicious activity that triggered them
- The associated MITRE `ATT&CK` tactic
- Recommended actions for how to investigate and mitigate the threat
- Options for continuing your investigations with Microsoft Sentinel

## Microsoft Defender for Cloud and Brute Force Attacks

A brute force attack is among the most common and fairly successful hacking methods, despite being least sophisticated hacking methods. The theory behind such an attack is that if you take an infinite number of attempts to guess a password, you're bound to be right eventually. When Microsoft Defender for Cloud detects a brute force attack, it triggers an [alert](/azure/defender-for-cloud/defender-for-databases-introduction#what-kind-of-alerts-does-microsoft-defender-for-open-source-relational-databases-provide) to bring you awareness that a brute force attack took place. It also can separate simple brute force attack from brute force attack on a valid user or a successful brute force attack.

## Microsoft Defender for Cloud Security Posture Management (CSPM) Assessments - Preview

Microsoft Defender Security Posture Management assessments continuously evaluate the security posture of PostgreSQL servers. Defender scans server- and database-level configurations against PostgreSQL-specific security best practices to identify potential vulnerabilities and misconfigurations that could increase risk. Assessments provide actionable recommendations to help improve security posture, support compliance requirements, and reduce exposure to threats.   

The following recommendations are now available in preview for Azure Database for PostgreSQL servers as part of Defender CSPM with additional assessments planned: 

| Scope    | Recommendation                                                                             |
|----------|--------------------------------------------------------------------------------------------|
| server   | connection_throttle should be set to “on” for PostgreSQL Servers                           |
| server   | logfiles.retention_days should be greater than 3 for PostgreSQL Servers View file changes  |
| server   | pgaudit.log_statement should be set to “on” for Azure Database for PostgreSQL Servers      |
| server   | pgaudit.log_statement_once should be set to “on” for Azure Database for PostgreSQL Servers |
| server   | pgaudit.log should include role, ddl, and misc for Azure Database for PostgreSQL Servers   |
| server   | pgaudit.log_level should be set to “log” for Azure Database for PostgreSQL Servers         |
| server   | Public IP access should be disabled for Azure Database for PostgreSQL Servers              |
| server   | Private endpoint should be configured for Azure Database for PostgreSQL Servers            |
| server   | 'Allow access to Azure services' should be disabled for PostgreSQL Servers                 |


To get security alerts and recommendations from Microsoft Defender, you'll first need to **enable it** as shown in the next section.


## Enable enhanced security with Microsoft Defender for Cloud

1. From the [Azure portal](https://portal.azure.com), navigate to Security menu in the left pane.

1. Pick Microsoft Defender for Cloud.

1. Select Enable in the right pane.

    :::image type="content" source="media/security-defender-for-cloud/defender-for-cloud-azure-portal-postgresql.png" alt-text="screenshot of enable page.":::

    > [!NOTE]  
    > If you have the "open-source relational databases" feature enabled in your Microsoft Defender plan, you'll observe that Microsoft Defender is automatically enabled by default for your Azure Database for PostgreSQL  resource.

## Related content

- [System assigned managed identity](security-configure-managed-identities-system-assigned.md)
- [User assigned managed identity](security-configure-managed-identities-user-assigned.md)
