---
title: |
  Tutorial: Security and Authentication in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial provides an in-depth guide to securing Azure Cosmos DB for MongoDB vCore. It covers authentication methods, including username and password usage, encryption for data at rest and in transit, and role-based access control (RBAC) for fine-grained permissions. The documentation also explains network security features such as private endpoints, firewall rules, and Virtual Network (VNet) integration. By following the best practices outlined, developers and IT professionals can ensure the security, compliance, and reliability of their database solutions.

author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer or IT professional, I need to understand how to secure Azure Cosmos DB for MongoDB vCore, configure authentication and RBAC, enable encryption, and leverage network security features to build a robust and secure database solution.
---


# Security and Authentication in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Ensuring the security of your database and its data is paramount when working with Azure Cosmos DB for MongoDB vCore. This document outlines the various authentication methods, authorization mechanisms, and best practices to secure your database. It also highlights encryption methods and key considerations for safeguarding sensitive data.

## Key Concepts in Security and Authentication

1. **Authentication**

    - Verifies the identity of a user or application trying to access the database.
    - Supports connection strings with username and password.

1. **Authorization**

    - Determines what actions an authenticated user or application can perform on the database.
    - Role-based access control (RBAC) is supported.

1. **Encryption**

    - Data in Transit: Secured using TLS (Transport Layer Security).
    - Data at Rest: Automatically encrypted by Azure Cosmos DB.

1. **Network Security**

    - Leverages Virtual Network (VNet) Integration and private endpoints to isolate the database and restrict access.

## Authentication Methods  

1. **Username and Password Authentication**

    - Connection strings must include credentials:
        ```bash
        mongodb://<username>:<password>@<cluster-url>/<database>?ssl=true
        ```
    - Ensure strong passwords and rotate them periodically.

1. **Managed Identity Authentication (Future Enhancements)**

    - Utilize Azure Active Directory (Azure AD) for secure, passwordless authentication when supported.  

## Role-Based Access Control (RBAC)

1. **Default Roles**

    - **Read:** Grants read-only access to collections.
    - **ReadWrite:** Allows reading and writing to collections.
    - **DBAdmin:** Provides administrative privileges over a database.

1. **Custom Roles**

    - Define custom roles with fine-grained permissions to meet specific business requirements.

1. **Assigning Roles**

    - Assign roles to users or applications during account setup or via the Azure Portal.

## Encryption

1. **Encryption in Transit**
    - TLS 1.2 ensures secure communication between the client application and Cosmos DB.
    - Always use the `ssl=true` parameter in the connection string.

1. **Encryption at Rest**

    - All data stored in Azure Cosmos DB is automatically encrypted with Microsoft-managed keys.
    - Optionally, use customer-managed keys (CMK) for additional control.    


## Network Security Features

1. **Private Endpoints**

    - Isolate database traffic to your Virtual Network (VNet).
    - Prevent public internet exposure.

1. **Firewall Rules**

    - Restrict access to specific IP addresses or IP ranges.
    - Configure firewall rules via the Azure Portal.
1. **Virtual Network (VNet) Integration**

    - Enable secure, private access to your database.

## Best Practices for Security and Authentication

1. **Use Secure Connection Strings**

    - Always include `ssl=true` and use environment variables to store sensitive credentials.

1. **Enable Role-Based Access Control (RBAC)**

    - Follow the principle of least privilege by assigning the minimum roles required for users.

1. **Monitor Activity**

    - Enable Azure Monitor and set up alerts for unauthorized access attempts or unusual activities.

1. **Regular Key Rotation**

    - Rotate keys and credentials periodically to mitigate the impact of key compromise.

1. **Audit and Logging**

    - Use tools like Azure Monitor Logs to audit access and maintain compliance.

## Example Configuration
**Connection String with Authentication**
```bash
mongodb://username:password@cosmosdb-account.mongo.cosmos.azure.com:10255/mydatabase?ssl=true&replicaSet=globaldb&retrywrites=false
```
**Assigning Roles to a User**
1. Log in to the Azure Portal.
1. Navigate to your Cosmos DB account.
1. Open the **Access Control (IAM)** tab.
1. Assign roles to users or applications.   

## Common Challenges and Solutions
1. **Challenge:** Invalid Credentials Error
    **Solution:** Verify username, password, and connection string formatting.

1. **Challenge:** Unsecured Connections
**Solution:** Ensure ssl=true is included in your connection string.

1. **Challenge:** Excessive Privileges Assigned
**Solution:** Review and implement RBAC to restrict access appropriately.

## Conclusion
Security and authentication are vital for protecting your data in Azure Cosmos DB for MongoDB vCore. By following the recommended practices, leveraging encryption, and utilizing RBAC, you can build a secure and compliant database system.
