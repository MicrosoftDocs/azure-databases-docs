---
title: Secure Your Azure HorizonDB
description: Learn how to secure an Azure HorizonDB, with best practices for security and compliance.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: overview
ms.custom:
  - horz-security
---

# Secure your Azure HorizonDB

Azure HorizonDB is a fully managed database service that provides built-in high availability, automated backups, and scaling capabilities.
Securing your PostgreSQL database deployments is crucial to protect sensitive data and maintain compliance with industry standards.

This article guides you on how to secure your Azure HorizonDB Server deployment.

[!INCLUDE [certificate-rotation](includes/certificate-rotation.md)]

## Network security

The Network Security section guides you through preventing public access and using the networking features to integrate your PostgreSQL into a secure, segmented cloud network architecture.

- **Disable public network access**: Disable public network access for your PostgreSQL to prevent exposure to the internet. This action ensures that only trusted networks can access your database.

- **Legacy firewall rules and service endpoints**: If you need to allow access from specific IP addresses, use [legacy firewall rules and service endpoints](../network/how-to-networking-servers-deployed-public-access-add-firewall-rules.md). However, this approach isn't recommended. Instead, prefer using private endpoints or virtual network integration.

Network security articles are in the networking sections:

- [Networking overview with public access (allowed IP addresses) in Azure HorizonDB](../network/concepts-networking-public.md)


- **Use managed identities for secure application access**: Use managed identities in Azure to securely authenticate applications and services without the need to manage credentials. This provides a secure and simplified way to access resources like Azure HorizonDB. For more information, visit [Managed Identities](/entra/identity/managed-identities-azure-resources/overview).

- **Enforce security through conditional access policies**: Set up conditional access policies in Microsoft Entra to enforce security controls based on user, location, or device context. These policies allow dynamic enforcement of security requirements based on risk, enhancing overall security posture. For more information, visit [Microsoft Entra Conditional Access](/entra/identity/conditional-access/overview).

- **Local authentication should use SCRAM authentication**: If you must use local authentication, ensure that strong password policies are enforced. Use password complexity requirements and regular password rotation to minimize the risk of compromised accounts. For more information, visit [SCRAM authentication in Azure HorizonDB](security-connect-scram.md).

## Access control

The access control section focuses on securing the level of access based on the least privilege principle. It emphasizes minimizing the risk of unauthorized access to sensitive resources by restricting and managing elevated permissions, enforcing multifactor authentication, and ensuring that privileged actions are logged and audited.

Here are some possible security services, features, and best practices for the access control section:

- **Use Entra roles for access control**: Implement Azure Role-Based Access Control (Role-Based Access Control (RBAC) to manage access to Azure HorizonDB resources. Assign roles based on the principle of least privilege, ensuring users and applications have only the permissions they need. For more information, visit [Azure Role Based Access Control (RBAC)](/azure/role-based-access-control/overview) in general.

- **Follow Entra best practices**: Utilize MFA, [Conditional Access policies](/entra/identity/conditional-access/overview), just in time (JIT) access to protect your users and databases.

- **Manage local database users, roles, and permissions**: Use PostgreSQL's built-in role
  management to control access at the database level. Create custom roles with specific permissions to enforce the principle of least privilege. Regularly review and audit these roles to ensure compliance with security policies. For more information, visit [Manage users in Azure HorizonDB](security-manage-database-users.md).

## Data protection

The data protection section focuses on securing sensitive data at rest and in transit. It ensures that data is encrypted, access is controlled, and sensitive information is protected from unauthorized access. It emphasizes the use of encryption, secure connections, and data masking to safeguard data integrity and confidentiality.

Here are some possible security services, features, and best practices for the data protection section:

### Encrypt data in transit

- **Verify TLS connections**: Azure PostgreSQL always uses SSL or TLS to encrypt data in transit between your application and the database. You should configure your application to verify the certificate used, such as the root CA, expired certificates, host name mismatch, and certificate revocation. This practice helps protect sensitive information from eavesdropping and man-in-the-middle attacks. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB](security-tls.md).

- **Ensure client has the latest TLS certificates installed**: Ensure that your client applications have the latest TLS certificates installed to support secure connections. This practice helps prevent connection failures and ensures that your application can establish secure connections with the PostgreSQL server. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB](security-tls.md).

- **Require the use of TLS 1.3**: Configure your PostgreSQL server to require TLS 1.3 for all connections. This configuration ensures that only the latest and most secure version of the protocol is used, providing better security and performance. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB](security-tls.md).

### Encryption at rest

- **Data is always transparently encrypted at rest with SMK**: Azure HorizonDB automatically encrypts data at rest by using service-managed keys (SMK). This encryption ensures that your data is protected without requiring extra configuration. It relies on the underlying Azure storage infrastructure. It covers the primary server, replicas, point-in-time-recovery (PITR), and backups. For more information, visit [Data encryption at rest in Azure HorizonDB](security-data-encryption.md).


- **Encrypt ultra-sensitive data with client-side encryption**: For ultra-sensitive data, consider implementing client-side encryption. This approach involves encrypting data before you send it to the database, ensuring that only encrypted data is stored in the database. This practice provides a more layer of security, as the database itself and therefore the database administrator doesn't have access to the unencrypted data.

### Confidential compute

[Azure Confidential Computing (ACC)](/azure/confidential-computing/overview) enables organizations to securely process and collaborate on sensitive data, such as personal data or protected health information (PHI). ACC provides built-in protection against unauthorized access by securing data in use through Trusted Execution Environments (TEEs).

- **SaaS and hosting providers consider configure confidential compute**: If you're a Software as a service (SaaS) or hosting provider and your PostgreSQL workloads involve processing sensitive data, consider using Azure Confidential Computing to protect data in use. This solution provides a more layer of security by ensuring that data is processed in a secure environment, preventing unauthorized access even from privileged users. For more information, visit [Azure Confidential Computing in Azure HorizonDB](security-confidential-computing.md) for more details.

### Data masking and redaction

- **Implement data masking**: Use the [PostgreSQL Anonymizer extension](https://postgresql-anonymizer.readthedocs.io/en/stable) to support:

- Anonymous Dumps: Export the masked data into a SQL file.

- Static Masking: Remove the personal data according to the rules.

- Dynamic Masking: Hide personal data only for the masked users.

- Masking Views: Build dedicated views for the masked users.

- Masking Data Wrappers: Apply masking rules on external data.

<a id="logging-and-threat-detection"></a>

## Log and threat detection

The logging and threat detection section covers controls for detecting threats in Azure environments. It covers enabling, collecting, and storing audit logs for Azure services. It emphasizes the use of native threat detection capabilities, centralized log management, and proper log retention for security investigations and compliance. This section focuses on generating high-quality alerts, centralizing security analysis through Azure tools, maintaining accurate time synchronization, and ensuring effective log retention strategies.

Here are some possible security services, features, and best practices for the logging and threat detection section:

- **Enable collection of diagnostic logs**: Ensure that diagnostic logging is enabled by selecting category Group "audit." Use Azure Policy to implement:

- Policy [Enable logging by category group for PostgreSQL (microsoft.dbforpostgresql/flexibleservers) to Log Analytics](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetail.ReactView/id/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Fcdd1dbc6-0004-4fcd-afd7-b67550de37ff/version/1.0.0/scopes~/%5B%22%2Fsubscriptions%2F5c5037e5-d3f1-4e7b-b3a9-f6bf94902b30%22%5D/contextRender~/false)

- Initiative [Enable audit category group resource logging for supported resources to Log Analytics](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/InitiativeDetail.ReactView/id/%2Fproviders%2FMicrosoft.Authorization%2FpolicySetDefinitions%2Ff5b29bc4-feca-4cc6-a58a-772dd5e290a5/version/1.1.0/scopes~/%5B%22%2Fsubscriptions%2F5c5037e5-d3f1-4e7b-b3a9-f6bf94902b30%22%5D)
- **Utilize Microsoft Defender for Open-Source Relational Databases**: Use Microsoft Defender for Open-Source Relational Databases to enhance the security posture of your PostgreSQL flexible server instance. This service provides advanced threat protection, vulnerability assessments, and security recommendations tailored for open-source databases. For more information, visit [Overview of Microsoft Defender for Open-Source Relational Databases](/azure/defender-for-cloud/defender-for-databases-introduction) for more details.

- **Enable audit logging**: Configure audit logging for your PostgreSQL to track and log database activities by using the [pgaudit extension](https://www.pgaudit.org/). For more information, visit [Audit logging in Azure HorizonDB](security-audit.md) for more details.

## Backup and recovery

The backup and recovery section focuses on ensuring that data and configurations across Azure services are regularly backed up, protected, and recoverable in failures or disasters. It emphasizes automating backups, securing backup data, and ensuring that recovery processes are tested and validated to meet recovery time objectives (RTO) and recovery point objectives (RPO). The section also highlights the importance of monitoring and auditing backup processes to ensure compliance and readiness. For an overview, For more information, visit [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md).

Here are some possible security services, features, and best practices for the backup and recovery detection section:

- **Configure automated backups**: Azure HorizonDB automatically performs daily backups of your database files and continuously backs up transaction logs. You can retain backups from seven days up to 35 days. You can restore your database server to any point in time within your backup retention period. The RTO depends on the size of the data to restore and the time to perform log recovery. It can range from a few minutes up to 12 hours. For more information, visit [Backup and restore in Azure HorizonDB](../backup-restore/concepts-backup-restore.md).

- **Configure read replicas**: Use the read replicas to offload read operations from the primary server, improving performance and availability. You can also use read replicas for disaster recovery scenarios, allowing you to quickly switch to a replica with a primary server failure.

- **Protect backup data with customer-managed key encryption**: Secure your backup data by using encryption at rest.

## Related content

- [What is Azure HorizonDB?](../overview.md)
- [Reset administrator password in Azure HorizonDB](security-reset-admin-password.md)
- [Networking in Azure HorizonDB](../network/how-to-networking.md)
- [Azure security baseline for Azure HorizonDB](/security/benchmark/azure/baselines/azure-database-for-postgresql-flexible-server-security-baseline)
