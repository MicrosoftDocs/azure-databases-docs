---
title: Troubleshoot common errors in Azure DocumentDB
description: This doc discusses the ways to troubleshoot common issues encountered in Azure DocumentDB.
ms.topic: troubleshooting
ms.date: 06/02/2025
author: khelanmodi
ms.author: khelanmodi
ms.custom:
  - sfi-image-nochange
---

# Troubleshoot common issues in Azure DocumentDB
This guide is tailored to assist you in resolving issues you may encounter when using Azure DocumentDB. The guide provides solutions for connectivity problems, error scenarios, and optimization challenges, offering practical insights to improve your experience. 

>[!Note]
> Please note that these solutions are general guidelines and may require specific configurations based on individual situations. Always refer to official documentation and support resources for the most accurate and up-to-date information.

## Common errors and solutions

### Unable to Connect to Azure DocumentDB - Timeout error 
This issue might occur when the cluster doesn't have the correct firewall rule(s) enabled. If you're trying to access the cluster from a non-Azure IP range, you need to add extra firewall rules. Refer to [Security options and features - Azure DocumentDB](./security.md#network-security) for detailed steps. Firewall rules can be configured in the portal's Networking setting for the cluster. Options include adding a known IP address/range or enabling public IP access.

:::image type="content" source="./media/troubleshoot-guide/timeout-error-solution.png" alt-text="Screenshot of the Timeout error solution for Azure DocumentDB." lightbox="./media/troubleshoot-guide/timeout-error-solution-expanded.png":::


### Unable to Connect with DNSClient.DnsResponseException Error
#### Debugging Connectivity Issues: 
Windows User: <br>
PsPing doesn't work. The use of nslookup confirms cluster reachability and discoverability, indicating network issues are unlikely.

Unix Users: <br>
For Socket/Network-related exceptions, potential network connectivity issues might be hindering the application from establishing a connection with the Azure DocumentDB Mongo API endpoint.

To check connectivity, follow these steps:
```
nc -v <accountName>.mongocluster.cosmos.azure.com 10260
```
If TCP connect to port 10260 fails, an environment firewall may be blocking the Azure DocumentDB connection. Kindly scroll down to the page's bottom to submit a support ticket.



#### Verify your connection string: 
Only use the connection string provided in the Azure portal. Ensure that it includes the mongodb+srv:// protocol, as this is required for proper connectivity. Avoid using any variations or prefixes like c. If you encounter issues with connectivity, share the application or client-side driver logs for debugging by submitting a support ticket.

### Error Codes
This table lists error codes returned by Azure DocumentDB to help identify and resolve issues. These are also useful for troubleshooting issues using [diagnostic logs](./how-to-monitor-diagnostics-logs.md).

| Error Code | Error Name                        |
|---------------|----------------------------------|
| 1             | InternalError                    |
| 2             | BadValue                         |
| 5             | GraphContainsCycle               |
| 9             | FailedToParse                    |
| 14            | TypeMismatch                     |
| 15            | Overflow                         |
| 20            | IllegalOperation                 |
| 23            | AlreadyInitialized               |
| 26            | NamespaceNotFound                |
| 27            | IndexNotFound                    |
| 28            | PathNotViable                    |
| 31            | RoleNotFound                     |
| 34            | CannotBackfillArray              |
| 40            | ConflictingUpdateOperators       |
| 43            | CursorNotFound                   |
| 48            | NamespaceExists                  |
| 52            | DollarPrefixedFieldName          |
| 53            | CanNotBeTypeArray                |
| 54            | NotSingleValueField              |
| 56            | EmptyFieldName                   |
| 57            | DottedFieldName                  |
| 61            | ShardKeyNotFound                 |
| 66            | ImmutableField                   |
| 67            | CannotCreateIndex                |
| 68            | IndexAlreadyExists               |
| 72            | InvalidOptions                   |
| 73            | InvalidNamespace                 |
| 85            | IndexOptionsConflict             |
| 86            | IndexKeySpecsConflict            |
| 111           | NotExactValueField               |
| 115           | CommandNotSupported              |
| 118           | NamespaceNotSharded              |
| 146           | ExceededMemoryLimit              |
| 159           | DurationOverflow                 |
| 165           | ViewDepthLimitExceeded           |
| 166           | CommandNotSupportedOnView        |
| 167           | OptionNotSupportedOnView         |
| 181           | AmbiguousIndexKeyPattern         |
| 197           | InvalidIndexSpecificationOption  |
| 224           | QueryFeatureNotAllowed           |
| 232           | MaxSubPipelineDepthExceeded      |
| 241           | ConversionFailure                |
| 263           | OperationNotSupportedInTransaction |
| 276           | IndexBuildAborted                |
| 291           | UnableToFindIndex                |
| 361           | CollectionUUIDMismatch           |
| 10334         | BsonObjectTooLarge               |
| 11000         | DuplicateKey                     |
| 12587         | BackgroundOperationInProgressForNamespace |
| 13113         | MergeStageNoMatchingDocument     |
| 13297         | DbAlreadyExists                  |

## Next steps
- If you followed all the troubleshooting steps and still can't resolve your issue, you can open a [support request](https://azure.microsoft.com/support/create-ticket/) for further assistance.
- If you're troubleshooting cross-region replication, see [troubleshooting guide for cross-region replication](./troubleshoot-replication.md).
