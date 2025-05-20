---
title: Azure Confidential Computing
description: This article describes the confidential computing options in Azure Database for PostgreSQL flexible server.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Azure Confidential Computing for Azure Database for PostgreSQL (Preview)

[Azure Confidential Computing (ACC)](/azure/confidential-computing/overview) enables organizations to securely process and collaborate on sensitive data, such as personal data or protected health information (PHI). ACC provides built-in protection against unauthorized access by securing data in use through Trusted Execution Environments (TEEs). This allows for secure real-time analytics and collaborative machine learning across organizational boundaries.

## Understanding the architecture

**Azure Database for PostgreSQL** supports Azure Confidential Computing through Trusted Execution Environments (TEEs), which are hardware-based, isolated memory regions within the CPU. Data processed inside the TEE is protected from access by the operating system, hypervisor, or other applications.

- Code runs in plaintext within the TEE but remains encrypted outside the enclave.
- Data is encrypted at rest, in transit, and use.
- Protected from access by the OS, hypervisor, or other applications.

## Processors

**Azure Confidential Computing** is supported in **Azure Database for PostgreSQL** by selecting a supported confidential virtual machine (VM) SKU when creating a new server. There are two processors to choose from:

- AMD SEV-SNP
- Intel TDX

:::image type="content" source="media/concepts-confidential-computing/processor.jpg" alt-text="Screenshot of Azure Confidential Computing options.":::

## Virtual machine SKUs

The SKUs supporting Azure Confidential Computing (ACC) for Azure Database for PostgreSQL are:

| SKU Name | Processor | vCores | Memory (GiB) | Max IOPS | Max I/O Bandwidth (MBps) |
| --- | --- | --- | --- | --- | --- |
| **Dcadsv5** | AMD SEV-SNP | 2-96 | 8-384 | 3750-80000 | 48-1200 |
| **Dcedsv5** | Intel TDX | 2-96 | 8-384 | 3750-80000 | 85-2600 |
| **Ecadsv5** | AMD SEV-SNP | 2-96 | 16-672 | 3750-80000 | 48-1200 |
| **Ecedsv5** | Intel TDX | 2-128 | 16-1024 | 3750-80000 | 48-1200 |

## Deployment

You can deploy Azure Database for PostgreSQL with ACC using various methods, such as the Azure portal, Azure CLI, ARM templates, Bicep, Terraform, Azure PowerShell, REST API, etc.

For this example, we're using the Azure portal.

1. Go to [Azure portal to deploy an Azure Database for PostgreSQL](https://ms.portal.azure.com/#create/Microsoft.PostgreSQLFlexibleServer).

1. On the **Basics** tab,
   1. Enter your details.
   1. Select **UAE North** as the region.
   1. Select **Configure Server** under **Compute + Storage**.

   :::image type="content" source="media/concepts-confidential-computing/confidential-compute-portal-1.jpg" alt-text="Screenshot of Azure Confidential Computing portal deployment basics page." lightbox="media/concepts-confidential-computing/confidential-compute-portal-1.jpg":::

1. On the **Compute and Storage** tab,
   - Select your Compute Tier and Compute Processor.

    :::image type="content" source="media/concepts-confidential-computing/confidential-compute-portal-2.jpg" alt-text="Screenshot of Azure Confidential Computing portal deployment compute and storage page." lightbox="media/concepts-confidential-computing/confidential-compute-portal-2.jpg":::

1. Select Compute Size and **select a confidential compute SKU** and the size based on your needs.

    :::image type="content" source="media/concepts-confidential-computing/confidential-compute-portal-3.jpg" alt-text="Screenshot of Azure Confidential Computing portal deployment list of compute sizes.":::

1. Deploy your server.

## Compare

Let's compare Azure Confidential Compute virtual machines vs. Azure Confidential Computing.

| Feature | Confidential Compute VMs | ACC for Azure Database for PostgreSQL |
| --- | --- | --- |
| Hardware root of trust | Yes | Yes |
| Trusted launch | Yes | Yes |
| Memory isolation and encryption | Yes | Yes |
| Secure key management | Yes | Yes |
| [Remote attestation](/azure/confidential-computing/attestation-solutions) | Yes | No |

## Limitations and considerations

Be sure to evaluate the limitations carefully before deploying in a production environment.

- Confidential Computing is only available in the UAE North.
- High Availability isn't supported for Confidential Compute SKUs.
- Point-in-time Restore (PITR) from nonconfidential compute SKUs to confidential ones isn't allowed.
- Compute scaling operation between confidential and nonconfidential compute options.

## Related content

- [Azure confidential computing](/azure/confidential-computing/trusted-execution-environment)
- [Azure confidential VM options](/azure/confidential-computing/virtual-machine-options)
