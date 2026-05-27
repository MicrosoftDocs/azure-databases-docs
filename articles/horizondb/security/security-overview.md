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

# Secure your Azure HorizonDB (Preview)

Azure HorizonDB is a fully managed database service that provides built-in high availability, automated backups, and scaling capabilities.
Securing your PostgreSQL database deployments is crucial to protect sensitive data and maintain compliance with industry standards.

This article guides you on how to secure your Azure HorizonDB Server deployment.

## Access control

The access control section focuses on securing the level of access based on the least privilege principle. It emphasizes minimizing the risk of unauthorized access to sensitive resources by restricting and managing elevated permissions, enforcing multifactor authentication, and ensuring that privileged actions are logged and audited.

Here are some possible security services, features, and best practices for the access control section:

- **Use role-based access control**: Implement Azure Role-Based Access Control (RBAC) to manage access to Azure HorizonDB resources. Assign roles based on the principle of least privilege, ensuring users and applications have only the permissions they need. For more information, visit [Azure Role Based Access Control (RBAC)](/azure/role-based-access-control/overview).

- **Follow Azure security best practices**: HorizonDB follows Azure security best practices for identity and access management.

- **Manage local database users, roles, and permissions**: Use PostgreSQL's built-in role
  management to control access at the database level. Create custom roles with specific permissions to enforce the principle of least privilege. Regularly review and audit these roles to ensure compliance with security policies. For more information, visit [Manage users in Azure HorizonDB (Preview)](security-manage-database-users.md).

## Data protection

The data protection section focuses on securing sensitive data at rest and in transit. It ensures that data is encrypted, access is controlled, and sensitive information is protected from unauthorized access. It emphasizes the use of encryption, secure connections, and data masking to safeguard data integrity and confidentiality.

Here are some possible security services, features, and best practices for the data protection section:

### Encrypt data in transit

- **Verify TLS connections**: Azure HorizonDB encrypts data in transit between your application and the database. You should configure your application to verify the server certificate. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB (Preview)](security-tls.md).

- **Ensure client has the latest TLS certificates installed**: Ensure that your client applications have the latest TLS certificates installed to support secure connections. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB (Preview)](security-tls.md).

- **Require the use of TLS 1.3**: Configure your PostgreSQL server to require TLS 1.3 for all connections. For more information, visit [Transport Layer Security (TLS) in Azure HorizonDB (Preview)](security-tls.md).

### Encryption at rest

- **Data is always transparently encrypted at rest with SMK**: Azure HorizonDB automatically encrypts data at rest by using service-managed keys (SMK). This encryption ensures that your data is protected without requiring extra configuration. It relies on the underlying Azure storage infrastructure. It covers the primary server, replicas, point-in-time-recovery (PITR), and backups. For more information, visit [Data encryption at rest in Azure HorizonDB (Preview)](security-data-encryption.md).

- **Encrypt ultra-sensitive data with client-side encryption**: For ultra-sensitive data, consider implementing client-side encryption. This approach involves encrypting data before you send it to the database, ensuring that only encrypted data is stored in the database. This practice provides a more layer of security, as the database itself and therefore the database administrator doesn't have access to the unencrypted data.

### Data masking and redaction

- **Implement data masking**: Use the [PostgreSQL Anonymizer extension](https://postgresql-anonymizer.readthedocs.io/en/stable) to support:

- Anonymous Dumps: Export the masked data into a SQL file.

- Static Masking: Remove the personal data according to the rules.

- Dynamic Masking: Hide personal data only for the masked users.

- Masking Views: Build dedicated views for the masked users.

- Masking Data Wrappers: Apply masking rules on external data.

## Backup and recovery

The backup and recovery section focuses on ensuring that data and configurations across Azure services are regularly backed up, protected, and recoverable in failures or disasters. It emphasizes automating backups, securing backup data, and ensuring that recovery processes are tested and validated to meet recovery time objectives (RTO) and recovery point objectives (RPO). The section also highlights the importance of monitoring and auditing backup processes to ensure compliance and readiness. For an overview, For more information, visit [Overview of business continuity in Azure HorizonDB (Preview)](../backup-restore/concepts-business-continuity.md).

Here are some possible security services, features, and best practices for the backup and recovery detection section:

- **Configure automated backups**: Azure HorizonDB automatically performs daily backups of your database files and continuously backs up transaction logs. You can retain backups from seven days up to 35 days. You can restore your database server to any point in time within your backup retention period. The RTO depends on the size of the data to restore and the time to perform log recovery. It can range from a few minutes up to 12 hours. For more information, visit [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md).

- **Configure read replicas**: Use the read replicas to offload read operations from the primary server, improving performance and availability. You can also use read replicas for disaster recovery scenarios, allowing you to quickly switch to a replica with a primary server failure.

- **Protect backup data with customer-managed key encryption**: Secure your backup data by using encryption at rest.

## Related content

- [What is Azure HorizonDB (Preview)?](../overview.md)
- [Reset administrator password in Azure HorizonDB (Preview)](security-reset-admin-password.md)
- [Networking in Azure HorizonDB (Preview)](../network/how-to-network.md)
- [Azure security baseline for Azure HorizonDB (Preview)](/security/benchmark/azure/baselines/azure-database-for-postgresql-flexible-server-security-baseline)
