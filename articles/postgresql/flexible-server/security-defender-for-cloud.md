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
ms.custom:
  - horz-security
---

# Microsoft Defender for Cloud for Azure Database for PostgreSQL

**[Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)** detects anomalous activities indicating unusual and potentially harmful attempts to access or exploit databases. Defender for Cloud provides [security alerts](/azure/defender-for-cloud/alerts-open-source-relational-databases) on anomalous activities so that you can detect potential threats and respond to them as they occur.
When you enable this plan, Defender for Cloud provides alerts when it detects anomalous database access and query patterns and suspicious database activities.

These alerts appear in Defender for Cloud's security alerts page and include:

- Details of the suspicious activity that triggered them
- The associated MITRE `ATT&CK` tactic
- Recommended actions for how to investigate and mitigate the threat
- Options for continuing your investigations with Microsoft Sentinel

## Microsoft Defender for Cloud and Brute Force Attacks

A brute force attack is among the most common and fairly successful hacking methods, despite being least sophisticated hacking methods. The theory behind such an attack is that if you take an infinite number of attempts to guess a password, you're bound to be right eventually. When Microsoft Defender for Cloud detects a brute force attack, it triggers an [alert](/azure/defender-for-cloud/defender-for-databases-introduction#what-kind-of-alerts-does-microsoft-defender-for-open-source-relational-databases-provide) to bring you awareness that a brute force attack took place. It also can separate simple brute force attack from brute force attack on a valid user or a successful brute force attack.

To get alerts from the Microsoft Defender plan, you'll first need to **enable it** as shown in the next section.

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
