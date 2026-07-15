---
title: Azure Confidential Computing in Azure Database for PostgreSQL Flexible Server
description: This article describes the confidential computing options in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand how Azure Confidential Computing protects data in Azure Database for PostgreSQL flexible server, so that I can decide whether it meets my organization's security requirements.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: concept-article
---

# Azure confidential computing in Azure Database for PostgreSQL flexible server

[Azure Confidential Computing (ACC)](/azure/confidential-computing/overview) enables organizations to securely process and collaborate on sensitive data, such as personal data or protected health information (PHI). ACC provides built-in protection against unauthorized access by securing data in use through Trusted Execution Environments (TEEs). This protection enables secure real-time analytics and collaborative machine learning across organizational boundaries.

## Understanding the architecture

**Azure Database for PostgreSQL flexible server** supports Azure Confidential Computing through Trusted Execution Environments (TEEs), which are hardware-based, isolated memory regions within the CPU. The operating system, hypervisor, and other applications can't access data processed inside the TEE.

- Code runs in plaintext within the TEE but remains encrypted outside the enclave.
- Data is encrypted at rest, in transit, and use.
- The operating system, hypervisor, and other applications can't access protected data.

## Processors

You enable Azure Confidential Computing in Azure Database for PostgreSQL flexible server by selecting a supported confidential virtual machine (VM) SKU when creating a new server. Only **AMD SEV-SNP** processors are supported.

> [!NOTE]
> Intel TDX processors aren't currently supported for Azure Database for PostgreSQL flexible server.

## Virtual machine SKUs

The SKUs that support Azure Confidential Computing (ACC) for Azure Database for PostgreSQL flexible server are:

| SKU Name | Processor | vCores | Memory (GiB) | Max IOPS | Max I/O Bandwidth (MBps) |
| --- | --- | --- | --- | --- | --- |
| **Dcadsv5** | AMD SEV-SNP | 2-96 | 8-384 | 3750-80000 | 48-1200 |
| **Ecadsv5** | AMD SEV-SNP | 2-96 | 16-672 | 3750-80000 | 48-1200 |

## Steps to deploy a server with confidential computing

### [Portal](#tab/portal-azure-confidential-computing)

Use the [Azure portal](https://portal.azure.com/#create/Microsoft.PostgreSQLFlexibleServer):

1. Select a region that supports Azure Confidential Computing for Azure Database for PostgreSQL flexible server. Then, in the **Compute + storage** section, select **Configure Server**.

   :::image type="content" source="media/security-confidential-computing/configure-server.png" alt-text="Screenshot showing Basics tab of New Azure Database for PostgreSQL flexible server wizard." lightbox="media/security-confidential-computing/configure-server.png":::

1. Select your **Compute tier** and **Compute processor**.

   :::image type="content" source="media/security-confidential-computing/tier-processor.png" alt-text="Screenshot showing where you can select the compute tier and processor." lightbox="media/security-confidential-computing/tier-processor.png":::

1. Expand the **Compute size** and select one of the confidential compute SKUs with an appropriate size to satisfy your needs.

   :::image type="content" source="media/security-confidential-computing/tier-processor.png" alt-text="Screenshot showing where you can select the compute size." lightbox="media/security-confidential-computing/tier-processor.png":::

1. Deploy your server.

### [CLI](#tab/cli-azure-confidential-computing)

Use the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command to deploy a server using confidential computing.

```azurecli-interactive
az postgres flexible-server create \
  --location <location>
  --resource-group <resource_group> \
  --name <server> \
  --tier <tier> \
  --sku-name <any_confidential_compute_sku> ...
```

---

## Compare

Let's compare Azure Confidential Compute virtual machines and Azure Confidential Computing.

| Feature | Confidential Compute VMs | ACC for Azure Database for PostgreSQL |
| --- | --- | --- |
| Hardware root of trust | Yes | Yes |
| Trusted launch | Yes | Yes |
| Memory isolation and encryption | Yes | Yes |
| Secure key management | Yes | Yes |
| [Remote attestation](/azure/confidential-computing/attestation-solutions) | Yes | No |

## Limitations and considerations

Evaluate the limitations carefully before deploying in a production environment.

- Confidential Computing is only available in the following regions: UAE North region, and West Europe.
- Only AMD SEV-SNP processors are supported. Intel TDX processors aren't currently compatible with Azure Database for PostgreSQL flexible server.
- Point-in-time restore (PITR) from nonconfidential compute versions to confidential ones isn't allowed.

## Related content

- [Azure confidential computing](/azure/confidential-computing/trusted-execution-environment)
- [Azure confidential VM options](/azure/confidential-computing/virtual-machine-options)
