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

# Why use Azure Confidential Computing with Azure Database for PostgreSQL Preview?

[Azure Confidential Computing (ACC)](/azure/confidential-computing/overview) enables organizations to process and collaborate on sensitive data—such as personal data or protected health information (PHI)—with built-in protection against unauthorized access. By securing data in use through Trusted Execution Environments (TEEs), ACC allows for secure real-time analytics and collaborative machine learning across organizational boundaries.

Industries with strict regulatory requirements—such as finance, healthcare, and the public sector—can migrate sensitive workloads from on-premises environments to the cloud with minimal code changes and without sacrificing performance by using Azure Confidential Virtual Machines (VMs).

## Architecture

:::image type="content" source="media/concepts-confidential-computing/app-enclave-vs-virtual-machine.jpg" alt-text="Screenshot of the Azure portal showing Azure Confidential Computing options." lightbox="../media/media/concepts-confidential-computing/app-enclave-vs-virtual-machine.jpg":::

A **Trusted Execution Environment (TEE)*- is a hardware-based, isolated memory region within the CPU. Data processed inside the TEE is protected from access by the operating system, hypervisor, or other applications.

- Code runs in plaintext within the TEE but remains encrypted outside the enclave.
- Data is encrypted at rest, in transit, and in use.

**AMD SEV-SNP (Secure Encrypted Virtualization – Secure Nested Paging)*- provides full memory encryption and memory integrity validation to prevent attacks like memory remapping and replay. It supports lift-and-shift migrations of existing applications to Azure Confidential Computing without requiring code changes or affecting performance.

### Remote attestation

Remote attestation is the process of validating that a TEE is secure and running verified code before granting it access to sensitive resources.

**Attestation flow:**

1. The TEE submits a report that includes a cryptographic hash of the loaded code and environment configuration.
1. The attestation service (verifier) validates:
   - The integrity of the certificate.
   - The issuer is trusted.
   - The TEE isn't on a blocklist.
1. If validation succeeds, the verifier issues an attestation token.
1. The TEE presents the token to the secrets manager.
1. The secrets manager validates the token against policy before releasing any secrets.

## Confidential computing

Azure secures data at rest and in transit. Confidential computing adds protection for **data in use** through hardware-backed, attested TEEs.

The [Confidential Computing Consortium (CCC)](https://confidentialcomputing.io/wp-content/uploads/sites/10/2023/03/CCC_outreach_whitepaper_updated_November_2022.pdf) defines confidential computing as:

> [!NOTE]  
> Confidential computing protects data in use by performing computation in a hardware-based, attested Trusted Execution Environment (TEE).

Confidential computing provides:

- **Hardware root of trust** – Anchors TEE security in the processor's trusted hardware.
- **Remote attestation** – Verifies workload integrity before allowing access to data.
- **Trusted launch** – Ensures that VMs start with verified software and configurations.
- **Memory isolation and encryption** – Secures in-memory data from unauthorized access.
- **Secure key management** – Releases keys only to be verified, attested environments.

## Azure Database for PostgreSQL integration

**Azure Confidential Computing** is supported in **Azure Database for PostgreSQL**. Enable ACC by selecting a supported confidential virtual machine (VM) SKU when creating a new server.

> [!IMPORTANT]  
> After the server is created, you can't Switch between confidential and nonconfidential compute options.

You can deploy Azure Database for PostgreSQL with ACC using any supported method (for example, Azure portal, Azure CLI, ARM templates, Bicep, Terraform, Azure PowerShell, REST API, etc.). 

:::image type="content" source="media/concepts-confidential-computing/confidential-computing-general-purpose.jpeg" alt-text="Screenshot of the Azure portal showing Azure Confidential Computing deployment options.":::

## Supported ACC SKUs

Select from the following SKUs based on your compute and I/O requirements:

| **SKU Name*- | **vCores*- | **Memory (GiB)*- | **Max IOPS*- | **Max I/O Bandwidth (MBps)*- |
| --- | --- | --- | --- | --- |
| Standard_EC2ads_v5 | 2 | 16 | 3,750 | 48 |
| Standard_DC4ads_v5 | 4 | 16 | 6,400 | 96 |
| Standard_DC8ads_v5 | 8 | 32 | 12,800 | 192 |
| Standard_DC16ads_v5 | 16 | 64 | 25,600 | 384 |
| Standard_DC32ads_v5 | 32 | 128 | 51,200 | 768 |
| Standard_DC48ads_v5 | 48 | 192 | 76,800 | 1,152 |
| Standard_DC64ads_v5 | 64 | 256 | 80,000 | 1,200 |
| Standard_DC96ads_v5 | 96 | 384 | 80,000 | 1,200 |

[!INCLUDE [pricing](includes/compute-storage-pricing.md)]

## Related content

- [Azure confidential computing](/azure/confidential-computing/trusted-execution-environment)
- [Azure confidential VM options](/azure/confidential-computing/virtual-machine-options)
