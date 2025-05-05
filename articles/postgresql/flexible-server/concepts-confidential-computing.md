---
title: Azure Confidential Computing
description: This article describes the confidential computing options in Azure Database for PostgreSQL flexible server.
author: cathzhao
ms.author: cathzhao
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Why use Azure Confidential Computing?

[Azure Confidential Computing (ACC)](https://learn.microsoft.com/azure/confidential-computing/overview) enables organizations to process and collaborate on sensitive data—such as personally identifiable information (PII) or protected health information (PHI)—with built-in protection against unauthorized access. By securing data in use through Trusted Execution Environments (TEEs), ACC allows for secure real-time analytics and collaborative machine learning across organizational boundaries.

Industries with strict regulatory requirements—such as finance, healthcare, and the public sector—can migrate sensitive workloads from on-premises environments to the cloud with minimal code changes and without sacrificing performance by using Azure Confidential VMs.

# Architecture overview

:::image type="content" source="../media/concepts-confidential-computing/app-enclave-vs-virtual-machine.jpg" alt-text="Screenshot of the Azure portal showing Azure Confidential Computing options." lightbox="../media/concepts-confidential-computing/app-enclave-vs-virtual-machine.jpg":::

A **Trusted Execution Environment (TEE)*- is a hardware-based, isolated memory region within the CPU. Data processed inside the TEE is protected from access by the operating system, hypervisor, or other applications.

- Code runs in plaintext within the TEE but remains encrypted outside the enclave.
- Data is encrypted at rest, in transit, and in use.

**AMD SEV-SNP (Secure Encrypted Virtualization – Secure Nested Paging)*- provides full memory encryption and memory integrity validation to prevent attacks like memory remapping and replay. It supports lift-and-shift migrations of existing applications to Azure Confidential Computing without requiring code changes or affecting performance.

## Remote attestation

Remote attestation is the process of validating that a TEE is secure and running verified code before granting it access to sensitive resources.

**Attestation flow:**

1. The TEE submits a report that includes a cryptographic hash of the loaded code and environment configuration.
1. The attestation service (verifier) validates:

   - The integrity of the certificate.
   - That the issuer is trusted.
   - That the TEE is not on a deny list.
1. If validation succeeds, the verifier issues an attestation token.
1. The TEE presents the token to the secrets manager.
1. The secrets manager validates the token against policy before releasing any secrets.

# Confidential Computing (Public Preview)

Azure already provides data protection at rest and in transit. Confidential computing adds protection for **data in use**, enabling secure processing in a hardware-based, attested TEE.

According to the [Confidential Computing Consortium (CCC)](https://confidentialcomputing.io/wp-content/uploads/sites/10/2023/03/CCC_outreach_whitepaper_updated_November_2022.pdf):

> [!NOTE]
> Confidential Computing protects data in use by performing computation in a hardware-based, attested Trusted Execution Environment (TEE).

Confidential computing provides:

- **Hardware root-of-trust**: Anchors the TEE's security to trusted hardware.
- **Remote attestation**: Validates the integrity of the environment before data access.
- **Trusted launch**: Ensures that virtual machines boot using verified software.
- **Memory isolation and encryption**: Prevents unauthorized access to data in memory.
- **Secure key management**: Keys are released only to attested, authorized code.

# Use with Azure Database for PostgreSQL – Flexible Server

**Azure Confidential Computing*- is available for **Azure Database for PostgreSQL – Flexible Server**. When creating a new server, you can enable ACC by selecting a supported confidential VM SKU.

> [!IMPORTANT]  
> After it's created, you can't change a server between ACC and non-ACC.

You can deploy using any method supported by PostgreSQL Flexible Server:

- Azure portal
- Azure CLI
- ARM templates
- Bicep
- Terraform
- Azure PowerShell
- REST API

    :::image type="content" source="../media/concepts-confidential-computing/confidential-computing-general-purpose.jpeg" alt-text="Screenshot of the Azure portal showing Azure Confidential Computing deployment options.":::

# Supported ACC SKUs

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

- [Azure confidential computing](https://learn.microsoft.com/en-us/azure/confidential-computing/trusted-execution-environment)
- [Azure confidential VM options](https://learn.microsoft.com/en-us/azure/confidential-computing/virtual-machine-options)
