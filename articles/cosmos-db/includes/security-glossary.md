---
ms.service: azure-cosmos-db
ms.topic: include
ms.date: 04/18/2025
ms.custom: subject-msia
ai-usage: ai-assisted
---

### Role-based access control

Role-based access control refers to a method to manage access to resources in Azure. This method is based on specific [identities](#identityprincipal) being assigned [roles](#role-definition) that manage what level of access they have to one or more resources. Role-based access control provides a flexible system of fine-grained access management that ensures identities only have the [least privileged](#least-privilege) level of access they need to perform their task.

For more information, see [role-based access control overview](/azure/role-based-access-control/overview).

### Identity/Principal

Identities refer to objects within Microsoft Entra that represents some entity that might need a level of access to your system. In the context of Azure and Microsoft Entra, identities could refer to one of the following types of entities:

| | Description |
| --- | --- |
| **Workload identities** | A workload identity represents a software workload that needs to access other services or resources |
| **Human identities** | A human identity represents a user that can be either native to your tenant or added as a guest |
| **Managed identities** | Managed identities are distinct resources in Azure that represent the identity of an Azure service |
| **Service principals** | A service principal is a a service account that can be used in a flexible number of authentication scenarios |
| **Device identities** | A device identity is an object in Microsoft Entra that is mapped to a device |
| **Groups** | Groups are objects used to manage access to one or more identities as a single operation |

For more information, see [identity fundamentals](/entra/fundamentals/identity-fundamental-concepts).

### Role

Roles are the primary units of enforcing access and permissions. You [assign](#role-assignment) a role to an identity and the [definition](#role-definition) of the role dictates what level of access that identity can have. The [scope](#scope) of the assignment dictates what exactly the identity has access to.

Azure has a large set of built-in roles that you can use to grant access to various resources. Consider this example:

| | Value |
| --- | --- |
| **Role** | [`CosmosBackupOperator`](/azure/role-based-access-control/built-in-roles/databases#cosmosbackupoperator) |
| **Definition** | `Microsoft.DocumentDB/databaseAccounts/backup/action` & `Microsoft.DocumentDB/databaseAccounts/restore/action` |
| **Scope** | *A resource group* |

In this example, you're assigned the `CosmosBackupOperator` role for a specific resource group. This assignment gives you access to either perform the `backup` or `restore` actions on any Azure Cosmos DB account within that resource group.

> [!IMPORTANT]
> Some Azure services, like Azure Cosmos DB, have their own native role-based access control implementation that uses different Azure Resource Manager properties, Azure CLI commands, and Azure PowerShell cmdLets. Azure Cosmos DB data plane access doesn't work with commands you typically use to manage role-based access control. Some of the commands for Azure role-based access control might work with Azure Cosmos DB control plane access.

For more information, see [built-in Azure roles](/azure/role-based-access-control/built-in-roles)

### Role definition

A role definition is a JSON object that contains the list of [control plane](#control-plane) and [data plane](#data-plane) actions that are allowed and aren't allowed. Consider this truncated example from the [`CosmosRestoreOperator`](/azure/role-based-access-control/built-in-roles/databases#cosmosrestoreoperator) built-in role:

```json
{
  "roleName": "CosmosRestoreOperator",
  "type": "Microsoft.Authorization/roleDefinitions",
  ...
  "permissions": [
    {
      "actions": [
        "Microsoft.DocumentDB/locations/restorableDatabaseAccounts/restore/action",
        "Microsoft.DocumentDB/locations/restorableDatabaseAccounts/*/read",
        "Microsoft.DocumentDB/locations/restorableDatabaseAccounts/read"
      ],
      "notActions": [],
      "dataActions": [],
      "notDataActions": []
    }
  ],
  ...
}
```

In this definition, an identity assigned this role can perform a `restore` action. Once the restoration operation is complete, the identity then can read various resources to validate that the restore was successful. We can determine that it can read these resources because of the `*` (wildcard) operator for `read`.

For more information, see [role definition concepts](/azure/role-based-access-control/role-definitions).

### Role assignment

A role assignment grants an identity access to a specific Azure resource. Role assignments consist of the following components:

| | Description |
| --- | --- |
| **Principal** | What identity is assigned this role |
| **Role** | The role that is assigned to the identity |
| **Scope** | The target Azure resource or group of the assignment |
| **Name/Description** | Metadata that makes it easier to manage assignments at scale |

> [!TIP]
> In role-based access control, you can see the terms **identity** and **principal** used interchangeably.

For more information, see [role assignment concepts](/azure/role-based-access-control/role-assignments).

### Actions

Actions define what specific permissions a [role](#role) has for a target resource. Actions are strings that typically include the resource type and a descriptive name detailing what permissions the action grants. Here are a few common examples:

| | Description | Plane |
| --- | --- | --- |
| **`Microsoft.DocumentDB/databaseAccounts/listKeys/action`** | Read account keys only | Control plane |
| **`Microsoft.DocumentDB/databaseAccounts/backup/action`** | Perform backups | Control plane |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/replace`** | Entirely replace an existing item | Data plane |
| **`Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeQuery`** | Execute a NoSQL query | Data plane |

Actions can also contain `*` (wildcard) characters so you don't have to manually detail every specific subpermission. Here's a few examples of actions with wildcards:

| | Description |
| --- | --- |
| **`Microsoft.DocumentDb/databaseAccounts/*`** | Create and manage Azure Cosmos DB accounts |
| **`Microsoft.DocumentDB/*/read`** | Read any container or database |

Actions are separated into [control plane](#control-plane) and [data plane](#data-plane). You must separately define actions on control plane resources and actions that can influence data. In a [role definition](#role-definition), control plane actions use the `actions` property and data plane actions are within the `dataActions` property. You can also define actions that an identity can’t perform using the respective `notActions` and `notDataActions` properties.

> [!NOTE]
> The separation of actions into control and data plane is a security measure to prevent wildcard actions from legacy role definitions from having unrestricted and unintentional access to data.

For more information, see [control and data actions](/azure/role-based-access-control/role-definitions#control-and-data-actions).

### Least privilege

The concept of "least privilege" refers to an operational best practice to ensure that all users only have the minimal level of access they need to perform their task or job. For example, an application that reads data from a database would only need read access to the data store. If that application had read and write access to the data store, a few things could happen including, but not limited to:

- The application could errantly destroy data
- An unauthorized user could get access to the application's credentials and modify data

Following the practice of least privilege ensures that any potential data breaches are limited in scope. This practice maximizes operational security while allowing users to remain effective.

For more information, see [recommended least privileged roles by task](/entra/identity/role-based-access-control/delegate-by-task).

### Control plane

Control plane access refers to the ability to manage resources for an Azure service without managing data. For example, Azure Cosmos DB control plane access could include the ability to:

- Read all account and resource metadata
- Read and regenerate account keys and connection strings
- Perform account backups and restore
- Start and track data transfer jobs
- Manage databases and containers
- Modify account properties

> [!IMPORTANT]
> In Azure Cosmos DB, you need control plane access to manage native data-plane role-based access control definitions and assignments. Since Azure Cosmos DB's data plane role-based access control mechanism is native, you need control plane access to create definitions and assignments and store them as resources within an Azure Cosmos DB account.

### Data plane

Data plane access refers to the ability to read and write data within an Azure service without the ability to manage resources in the account. For exmaple, Azure Cosmos DB data plane access could include the ability to:

- Read some account and resource metadata
- Create, read, update, patch, and delete items
- Execute NoSQL queries
- Read from a container's change feed
- Execute stored procedures
- Manage conflicts in the conflict feed

### Portable authentication

In development, it's common to write two sets of distinct authentication logic for local development and production instances. With the Azure SDK, you can write your logic using a single technique and expect the authentication code to work seamlessly in development and production.

The **Azure Identity** client library is available in multiple programming languages as part of the Azure SDK. Using this library, you can create a `DefaultAzureCredential` object that intelligently walks through multiple options, in order, to find the right credential based on your environment. These authentication options include (in order):

1. Client secret or certificate stored as an environment variable
1. [Microsoft Entra Workload ID](/entra/workload-id/workload-identities-overview)
1. User-assigned or system-assigned managed identity
1. Azure credentials derived from Visual Studio's settings
1. Credentials used in Visual Studio Code's Azure Account extension
1. Current credentials from Azure CLI
1. Current credentials from Azure PowerShell
1. Current credentials from Azure Developer CLI
1. An interactive session that launches the system's browser for sign in

Each modern Azure SDK library supports a constructor for their respective client objects or classes that accept a `DefaultAzureCredential` instance or its base type.

> [!TIP]
> To make your production code easier to debug and more predictable, you can opt to use `DefaultAzureCredential` in development and swap to a more specific credential like `WorkloadIdentityCredential` or `ManagedIdentityCredential` once the application is deployed. All of these classes are based on the `TokenCredential` class that many Azure software development kits (SDKs) expect as part of their client initialization logic making it straightforward to swap back and forth.

### Unique identifier

Each [identity](#identityprincipal) in Microsoft Entra has a unique identifier. You sometimes see this unique identifier referred to as the `id`, `objectId`, or `principalId`. When creating [role assignments](#role-assignment), you need the unique identifier for the identity that you with to use with the assignment.

### Scope

When you assign a role, you must decide what Azure resources or groups to grant access to. The scope of a role assignment defines the level at which an assignment is made.

For example:

- A single resource scope applies permissions to just that singular resource
- A scope set at the resource group level applies the permissions to all relevant resources within the group
- Scopes at the management group or subscription levels apply to all child groups and resources

When you assign a role in Azure role-based access control, it's ideal to set the scope of that assignment to include as little resources as required for your workload. For example, you can set the scope of an assignment to a resource group. That resource group scope includes all Azure Cosmos DB resources within the resource group:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>
```

Alternatively, you can set the scope to a single Azure resource and make your assignment of permissions more granular and narrow. In this example, the provider and name of the Azure Cosmos DB resource are used to narrow the scope:

```output
/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.DocumentDB/databaseAccounts/<account-name>
```

For more information, see [Azure role-based access control scope](/azure/role-based-access-control/scope-overview).
