---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 04/18/2025
ai-usage: ai-assisted
---

While using keys and resource owner password credentials might seem like a convenient option, it isn't recommended due to several reasons. Firstly, these methods lack the robustness and flexibility provided by Microsoft Entra authentication. Microsoft Entra offers enhanced security features such as multifactor authentication and conditional access policies, which greatly reduce the risk of unauthorized access. By using Microsoft Entra, you can significantly enhance the security posture of your applications and protect sensitive data from potential threats.

## Manage access

Role-based access control using Microsoft Entra gives you the ability to manage which users, devices, or workloads can access your data and to what extent they can access that data. Using fine-grained permissions in a role definition gives you the flexibility to enforce the security principal of "least privilege" while keeping data access simple and streamlined for development.

## Grant access in production

In production applications, Microsoft Entra offers many identity types including, but not limited to:

- Workload identities for specific application workloads
- System-assigned managed identities native to an Azure service
- User-assigned managed identities that can be flexibly reused between multiple Azure services
- Service principals for custom and more sophisticated scenarios
- Device identities for edge workloads

With these identities, you can grant specific production applications or workloads fine-grained access to query, read, or manipulate resources in Azure Cosmos DB.

## Grant access in development

In development, Microsoft Entra offers the same level of flexibility to your developer's human identities. You can use the same role-based access control definitions and assignment techniques to grant your developers access to test, staging, or development database accounts.

Your security team has a single suite of tools to manage identities and permissions for your accounts across all of your environments.

## Streamline authentication code

With the Azure SDK, the techniques used to access Azure Cosmos DB data programatically across many different scenarios:

- If your application is in development or production
- If you're using human, workload, managed, or device identities
- If your team prefers using Azure CLI, Azure PowerShell, Azure Developer CLI, Visual Studio, or Visual Studio Code
- If your team uses Python, JavaScript, TypeScript, .NET, Go, or Java

The Azure SDK provides an identity library that's compatible with many platforms, development language, and authentication techniques. Once you learn how to enable Microsoft Entra authentication, the technique remains the same across all of your scenarios. There's no need to build distinct authentication stacks for each environment.
