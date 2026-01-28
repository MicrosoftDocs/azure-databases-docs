---
title: Understanding MongoDB Compatibility in Managed MongoDB Services
description: Learn about MongoDB feature compatibility when choosing a managed MongoDB service.
author: gahl-levy
ms.author: gahllevy
ms.topic: product-comparison
ms.date: 04/17/2025
---

# Understanding MongoDB compatibility in managed MongoDB services


In the realm of managed MongoDB services, understanding the landscape of compatibility and feature support is crucial to remain vendor-agnostic. While it's a common perception that all services strive for full MongoDB compatibility, practical constraints and strategic decisions often lead to selective feature support. This document aims to shed light on these aspects, using MongoDB Atlas as a case study to illustrate the broader industry practice, including how Azure DocumentDB approaches these challenges.


## The reality of managed MongoDB services

### Is MongoDB Atlas Really MongoDB?

Despite perceptions, MongoDB Atlas lacks full compatibility, failing nearly 10% of MongoDB’s own official test suite. Unsupported features include: 

- **Administrative Commands:** Actions such as `setParameter`, `logRotate`, and `shutdown` are either limited or unavailable, affecting the ability to customize and control the database environment fully.
- **Access Control Commands:** Limitations include lack of support for `createUser`, `updateUser`, `dropUser` for user management; `createRole`, `updateRole`, `dropRole` for role management; and `grantRolesToUser`, `revokeRolesFromUser` for privilege management, impacting applications that leverage these. Just like Azure DocumentDB, MongoDB  Atlas requires users to utilize a first-party solution for access and role management. 
- **Session and Replication Commands:** Commands related to session management such as `killAllSessions` and replication configuration such as `replSetReconfig` and `replSetInitiate` are restricted, which can impact operational flexibility.
- **Sharding and User Management:** Key sharding operations such as `sh.disableBalancing` and `removeShard` and user/role management commands such as `createUser`, `dropUser` have limitations.

Lower-tier clusters such as M0, M2, and M5 have many additional notable limitations on commands and functionalities.

These constraints underscore a critical point: managed services, including MongoDB Atlas, must balance offering MongoDB features with ensuring the stability, security, and performance of their platforms.

### Azure DocumentDB's approach

Azure DocumentDB acknowledges these industry-wide practices and adopts a customer-centric [approach to feature support and compatibility](./compatibility-features.md). We prioritize features that deliver the most value to our users, focusing on:

- **AI-First:** Our AI-first approach is embodied in our **Vector Search** features, powered by [DiskANN](./vector-search.md), providing a solid foundation for generative AI applications without the need for complex and expensive integrations. 
- **Performance and Scalability:** Offering customizable performance tiers, decoupled from storage, and global distribution to meet diverse workload requirements. Passing down the cost savings from the Open Source [DocumentDB engine](https://github.com/documentdb/documentdb) (which powers the service) to customers to save money.
- **Security and Compliance:** Providing advanced security features such Private Link and Entra ID integration to ensure data protection and compliance with regulatory standards.
- **Operational Flexibility:** Supporting a broad set of MongoDB features (97% of aggregation operators, 96% of query/projections operators, and 100% of update operators etc.) while also innovating with Azure-specific capabilities such as [instant autoscale](./autoscale.md) to enhance usability and management.
- **Transparent support infrastructure:** No need for separate complex and expensive support contracts from third party vendors.
- **Simplified Versions** Azure DocumentDB uses a unified codebase for all server versions, offering version-dependent features without needing database version upgrades.
- **Full Stack SLA:** Providing an SLA that covers not only the database application, but also the compute and infrastructure it runs on, to give you piece of mind.

## Conclusion

In the managed MongoDB service space, no provider can claim absolute compatibility with open-source MongoDB due to the inherent trade-offs required to offer a managed service. Azure DocumentDB recognizes these industry realities and chooses to focus on transparency, customer feedback, and the continuous evolution of our service. By understanding the limitations across the board, customers can better navigate their options and choose the solution that best fits their needs.

Azure DocumentDB remains dedicated to providing a robust, scalable, and secure platform that meets the demands of modern applications, with a clear commitment to improving based on our customers' real-world use cases.

For detailed information on Azure DocumentDB's features and compatibility, please visit our [documentation](./compatibility-features.md).

## Next steps

> [!div class="nextstepaction"]
> [Get started with Azure DocumentDB](./quickstart-portal.md)
