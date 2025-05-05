---
title: Confidential computing
description: This article describes the confidential computing options in Azure Database for PostgreSQL flexible server.
author: cathzhao
ms.author: cathzhao
ms.reviewer: maghan
ms.date: 04/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---
# Why Confidential Computing?

Azure Confidential Computing can prove useful for organizations that need to securely share private sensitive data such as personally identifiable information (PII) or protected health information (PHI). ACC ensures that data remains protected from other collaborators and Azure operators, enabling users to run real-time analytics which can then be used to fine-tune ML models with sensitive data from other organizations for improved accuracy on joint data.

Customers in highly related industries, or with stringent compliance needs such as banking, healthcare, and the public sector can migrate legacy workloads from on-premises environments to the cloud with minimal effect on performance and more code changes by using Azure Confidential VMs. 

# Confidential Computing Architecture

:::image type="content" source="../media/concepts-confidential-computing/app-enclave-vs-virtual-machine.jpg" alt-text="Screenshot of the Azure portal showing an Azure Confidential Computing options.":::

A Trusted Execution Environment (TEE) is a segregated area of memory and CPU that's protected from the rest of the CPU using encryption, and any data within the TEE can't be tampered with by any code external to the environment.

Code executed inside the TEE is processed in the clear but only visible in encrypted form for any external actors. 

AMD Secure Encrypted Virtualization-Secure Nested Paging (SEV-SNP) adds strong memory integrity to mitigate malicious hypervisor-based attacks such as data replay and memory re-mapping. Specifically, AMD SEV-SNP encrypts the entire memory of a VM, allowing customers to migrate their existing workloads to Azure confidential computing without any additional code changes nor performance degradation, supporting both virtual machine and container workloads. 

## Attestation
In a TEE, the attester wants to retrieve secrets from a secret manager and must thus prove that they are trustworthy and genuine by submitting evidence (the hash of its executed code, build environment, and certificate). The verifier, an attestation service, then evaluates whether the evidence provided by the TEE meets the requirements for being trusted:
1. The certificate is valid and has not been altered
2. The issuer of the certificate is trusted
3. TEE evidence isn't part of a restricted list
If the verifier decides that the evidence meets the defined policies, the verifier will then create an attestation result and give it to the TEE. The TEE wants to exchange secrets with the secrets manager, but must present their attestation result to the secrets manager for evaluation first.

The secrets manager will check that the attestation result is authentic and hasn't been altered, the result was produced by a trusted authority, the result isn't expired or revoked, and that the result conforms to configured administrator policy before approving the attestation result and exchanging secrets with the TEE. 

# Confidential Computing (Public Preview)
Although Azure already encrypts data at rest and in transit, confidential computing helps protect data in use by processing data in a hardware-based and attested [Trusted Execution Environment](https://learn.microsoft.com/en-us/azure/confidential-computing/trusted-execution-environment) (TEE). When Azure confidential computing is configured, Microsoft and external actors are unable to access unencrypted customer data.

Confidential computing is defined by the [Confidential Computing Consortium (CCC)](https://confidentialcomputing.io/wp-content/uploads/sites/10/2023/03/CCC_outreach_whitepaper_updated_November_2022.pdf) as the following: 

- Confidential Computing protects data in use by performing computation in a hardware-based, attested Trusted Execution Environment.
- These secure and isolated environments prevent unauthorized access or modification of applications and data while they are in use, thereby increasing the security level of organizations that manage sensitive and regulated data.

Confidential computing includes:
- **Hardware root-of-trust** to ensure that data is protected and anchored to hardware configurations
- **Remote attestation** for customers to ensure environment integrity, so customers are able to verify that both the hardware and software on which workloads run are approved and secured before allowing data access
- **Trusted launch** to ensure that virtual machines boot with authorized software and utilize remote attestation so that customers are able to verify themselves
- **Memory isolation and encryption** ensures that data remains protected during processing, with memory isolation and hardware-based encryption to ensure unauthorized data access
- **Secure key management** ensures that keys remain encrypted during the lifecycle and are only released to the authorized code


# Confidential Computing in Azure PostgreSQL Flexible Server

Azure Confidential Compute (ACC) for Azure Database for PostgreSQL - Flexible Server is enabled by Microsoft per region and per subscription. ACC instances support  regular features of Flexible server except for changing between non-ACC and ACC after server creation.  

ACC can be selected by specifying an ACC Virtual Machine (VM) SKU, as given in the availability section. You can select ACC SKUs during creation using all methods of deployment: Portal, API, ARM template, Bicep, Terraform, Azure CLI, and Azure PowerShell. 

## How to Deploy Azure Confidential Computing

Azure Confidential Computing is available for General Purpose servers, with the ability to choose compute tiers based on vCores, memory, and maximum IOPS need. 

ACC is enabled per region and subscription, with ACC instances supporting all regular features of flexible server apart from changing between non-ACC and ACC upon server creation.

ACC can be selected by specifying an ACC VM during creation (Portal, API, ARM template, Bicep, Terraform, Az CLI, and Az PowerShell).

:::image type="content" source="../media/concepts-confidential-computing/confidential-computing-general-purpose.jpeg" alt-text="Screenshot of the Azure portal showing an Azure Confidential Computing options.":::

# Confidential Computing Availability

You can select confidential computing options based on SKUs, vCores, memory size, maximum support IOPS, and maximum supported I/O bandwidth.

The detailed specifications of the available server types are as follows:


| **SKU Name** | **vCores** | **Memory size** | **Maximum supported IOPS** | **Maximum supported I/O bandwidth** |
| ------------------- | ----------- | ----------- |  ----------- | --------- |
| Standard_EC2ads_v5 | 2 | 16 | 3750 | 48
| Standard_DC4ads_v5 | 4 | 16 | 6400 | 96
| Standard_DC8ads_v5| 8	| 32 | 12800 | 192
| Standard_DC16ads_v5| 16| 64| 25600| 384
| Standard_DC32ads_v5| 32 |	128 | 51200	| 768
| Standard_DC48ads_v5| 48 | 192 | 76800	| 1152
| Standard_DC64ads_v5| 64| 256 | 80000 | 1200
| Standard_DC96ads_v5| 96 | 384 | 80000 | 1200


[!INCLUDE [pricing](includes/compute-storage-pricing.md)]

## Related content
- [Azure confidential computing](https://learn.microsoft.com/en-us/azure/confidential-computing/trusted-execution-environment)
- [Azure confidential VM options](https://learn.microsoft.com/en-us/azure/confidential-computing/virtual-machine-options)
