---
title: Secure Your MySQL Database Server
description: Learn how to secure an Azure Database for MySQL flexible server instance, with best practices for security and compliance.
author: techlake
ms.author: hganten
ms.reviewer: maghan, randolphwest
ms.date: 01/07/2026
ms.service: azure-database-mysql
ms.subservice: security
ms.topic: overview
ms.custom:
  - horz-security
---

# Secure your Azure Database for MySQL Server

Azure Database for MySQL is a fully managed database service that provides built-in high availability, automated backups, and scaling capabilities.
Securing your MySQL database deployments is crucial to protect sensitive data and maintain compliance with industry standards.

This article guides you on how to secure your Azure Database for MySQL Server deployment.

## Network security

The Network Security section guides you through preventing public access and using the networking features to integrate your MySQL into a secure, segmented cloud network architecture. For conceptual details, see [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md).

To enhance the security of your MySQL database server, consider the following best practices:

- **Disable public network access**: Disable public network access for your MySQL to prevent exposure to the internet. This action ensures that only trusted networks can access your database.
- **Private Endpoints**: Use [Private Endpoints](concepts-networking-private-link.md) to securely connect to your MySQL from within your virtual network.
- **Alternatively, use virtual network integration**: [Use virtual network integration](concepts-networking-vnet.md) to connect your MySQL to your virtual network. This integration allows secure access from your Azure resources and from the server to resources consumed, such as AI.
- **Legacy firewall rules**: If you need to allow access from specific IP addresses, use [legacy firewall rules and service endpoints](concepts-networking-public.md#public-access-allowed-ip-addresses). However, this approach isn't recommended. Instead, prefer using private endpoints or virtual network integration.

Network security articles are in the networking sections:

- [Connectivity and networking concepts for Azure Database for MySQL](concepts-networking.md)
- [Private Link for Azure Database for MySQL](concepts-networking-private-link.md)
- [Private Network Access using virtual network integration for Azure Database for MySQL](concepts-networking-vnet.md)
- [Public Network Access for Azure Database for MySQL](concepts-networking-public.md)

## Identity management

The Identity Management section focuses on authentication, securing identities, and access controls using centralized identity and access management systems. It covers best practices such as strong authentication mechanisms and managed identities for applications.

- **Use Entra instead of database local authentication**: You should disallow local authentication for your MySQL server. Instead, use Microsoft Entra authentication only (not mixed mode) to manage access to your database. Microsoft Entra provides centralized authentication with strong security controls and Defender for Identity real-time protection. For more information, visit [Microsoft Entra](/entra) in general and [Microsoft Entra authentication with Azure Database for MySQL](security-entra-authentication.md).

- **Use managed identities for secure application access**: Use managed identities in Azure to securely authenticate applications and services without the need to manage credentials. Managed identities provide a secure and simplified way to access resources like Azure Database for MySQL. For more information, visit [Managed Identities](/entra/identity/managed-identities-azure-resources/overview).

- **Enforce security through conditional access policies**: Set up conditional access policies in Microsoft Entra to enforce security controls based on user, location, or device context. These policies allow dynamic enforcement of security requirements based on risk, enhancing overall security posture. For more information, visit [Microsoft Entra Conditional Access](/entra/identity/conditional-access/overview).

- **Local authentication is based on MySQL's authentication capabilities**: If you must use local authentication, ensure that you're following the official MySQL documentation about [Access Control and Account Management](https://dev.mysql.com/doc/refman/8.4/en/access-control.html). Azure specific instructions for managing MySQL users can be found in [Create users in Azure Database for MySQL](security-how-to-create-users.md).

## Access control

The access control section focuses on securing the level of access based on the least privilege principle to reduce the risk of unauthorized access by

- Restricting and managing elevated permissions.
- Enforcing multifactor authentication.
- Ensuring that privileged actions are logged and audited.

Security services, features, and best practices for access control include:

- **Use Entra roles for access control**: Implement Azure Role-Based Access Control (RBAC) to manage access to Azure Database for MySQL resources. Assign roles based on the principle of least privilege, ensuring users and applications have only the permissions they need. For more information, visit [Azure Role Based Access Control (RBAC)](/azure/role-based-access-control/overview) in general and [Set up Microsoft Entra authentication for Azure Database for MySQL](security-entra-authentication.md).

- **Follow Entra best practices**:
  - Utilize multifactor authentication (MFA) to add an extra layer of security for user access.
  - Implement Privileged Identity Management (PIM) to manage, control, and monitor access.
  - [Conditional Access policies](/entra/identity/conditional-access/overview), just in time (JIT) access to protect your users and databases.

- **Manage local database users, roles, and permissions**: Use MySQL's built-in role
  management to control access at the database level. Create custom roles with specific permissions to enforce the principle of least privilege. Regularly review and audit these roles to ensure compliance with security policies. For more information, visit [Create users in Azure Database for MySQL](security-how-to-create-users.md).

## Data protection

The data protection section focuses on securing sensitive data at rest and in transit. It ensures that data is encrypted, access is controlled, and sensitive information is protected from unauthorized access. It emphasizes the use of encryption, secure connections, and data masking to safeguard data integrity and confidentiality.

Here are some possible security services, features, and best practices for the data protection section:

### Encrypt data in transit

- **Verify TLS connections**: Azure MySQL always uses TLS to encrypt data in transit between your application and the database. You should configure your application to verify the certificate used, such as the root CA, expired certificates, host name mismatch, and certificate revocation. This practice helps protect sensitive information from eavesdropping and man-in-the-middle attacks. For more information, visit [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

- **Ensure client has the latest TLS certificates installed**: Ensure that your client applications have the latest TLS certificates installed to support secure connections. This practice helps prevent connection failures and ensures that your application can establish secure connections with the MySQL server. For more information, visit [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

- **Require the use of TLS 1.3**: Configure your MySQL server to require TLS 1.3 for all connections. This configuration ensures that only the latest and most secure version of the protocol is used, providing better security and performance. For more information, visit [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

### Encryption at rest

- **Data is always transparently encrypted at rest with SMK**: Azure Database for MySQL automatically encrypts data at rest by using service-managed keys (SMK). This encryption ensures that your data is protected without requiring extra configuration. It relies on the underlying Azure storage infrastructure. It covers the primary server, replicas, point-in-time-recovery (PITR), and backups. For more information, visit [Data encryption for Azure Database for MySQL with the Azure portal](security-how-to-data-encryption-portal.md).
- **Use customer-managed keys for additional control**: If you require more control over encryption keys, use customer-managed keys (CMK) stored in Azure Key Vault or Azure HSM. This option allows you to manage your encryption keys and provides more security and compliance options. For more information, visit [Data encryption with customer managed keys for Azure Database for MySQL](security-customer-managed-key.md).

- **Setup automatic key rotation in KV or Managed HSM**: If you use customer managed keys, configure automatic key rotation in Azure Key Vault to ensure that your encryption keys are regularly updated. Azure Database for MySQL supports automatic key version updates after a key is rotated. For more information, visit [Configure key autorotation in Azure Managed HSM](/azure/key-vault/managed-hsm/key-rotation) or [Understanding autorotation in Azure Key Vault](/azure/key-vault/general/autorotation) for more Key Vault details.

- **Encrypt ultra-sensitive data with client-side encryption**: For ultra-sensitive data, consider implementing client-side encryption. This approach involves encrypting data before you send it to the database, ensuring that only encrypted data is stored in the database. This practice provides a more layer of security, as the database itself and therefore the database administrator doesn't have access to the unencrypted data.

## Logging and threat detection

The logging and threat detection section covers controls for detecting threats in Azure environments.

Security services, features, and best practices for logging and threat detection section:

- **Enable collection of diagnostic logs**: Ensure that diagnostic logging is enabled by selecting category Group "audit." Use Azure Policy to implement:

  - Policy [Enable logging by category group for Azure Database for MySQL servers (microsoft.dbformysql/servers) to Log Analytics](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetail.ReactView/id/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F041fdf14-0dd4-4ce0-83ff-de5456be0c85)
  - Initiative [Enable audit category group resource logging for supported resources to Log Analytics](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/InitiativeDetail.ReactView/id/%2Fproviders%2FMicrosoft.Authorization%2FpolicySetDefinitions%2Ff5b29bc4-feca-4cc6-a58a-772dd5e290a5)

- **Utilize Microsoft Defender for Open-Source Relational Databases**: Use Microsoft Defender for Open-Source Relational Databases to enhance the security posture of your PostgreSQL flexible server instance. This service provides advanced threat protection, vulnerability assessments, and security recommendations tailored for open-source databases. For more information, visit [Overview of Microsoft Defender for Open-Source Relational Databases](/azure/defender-for-cloud/defender-for-databases-introduction) for more details.

## Related content

- [Azure security baseline for Azure Database for MySQL - Flexible ServerL](/security/benchmark/azure/baselines/azure-database-for-mysql-flexible-server-security-baseline)
