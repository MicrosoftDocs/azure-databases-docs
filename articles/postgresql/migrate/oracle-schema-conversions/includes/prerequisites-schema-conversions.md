---
title: "Prerequisites for Oracle to PostgreSQL Schema Conversion"
description: "System requirements, supported versions, and prerequisites for Oracle to PostgreSQL schema conversion using Visual Studio Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: include
---

## Prerequisites

This article outlines the system requirements, supported versions, and prerequisites for using the Oracle to PostgreSQL Schema Conversion feature in Visual Studio Code.

### System requirements

Before using the Oracle to PostgreSQL Schema Conversion feature in Visual Studio Code, confirm your environment meets the system, tooling, AI model, and access requirements outlined in the following sections. This article helps database engineers and developers prepare local workstations, Azure resources (including Azure OpenAI deployments), and database accounts so you can perform conversions reliably and safely in a nonproduction validation environment.

| Category | Details |
| --- | --- |
| **Visual Studio Code** version | 1.95.2 or higher |
| **GitHub Copilot** subscription | Pro+, Business, Enterprise |

### Operating system support

The Visual Studio Code extension and conversion tooling support common desktop operating systems (Windows, Linux, and macOS). Confirm your workstation meets Visual Studio Code system requirements and uses the x64 architecture where required. For reliable conversions, run the extension on a nonproduction machine with current OS updates, adequate CPU and memory, and network access to any required Azure services and database endpoints.

| Operating System | Support Details |
| --- | --- |
| **Windows** | x64 architecture only |
| **Linux** | x64 architecture |
| **macOS** | macOS 13+ |

#### PostgreSQL version support

| Component | Version Requirement |
| --- | --- |
| **Azure Database for PostgreSQL** | PostgreSQL version 15 or higher |
| **Scratch Database** | Azure Database for PostgreSQL |

### AI model requirements

You need one of the following AI components configured:

| AI Component | Model Version |
| --- | --- |
| **Azure OpenAI** | GPT-4.1 deployment |
| **GitHub Copilot** | GitHub Copilot with Agent Mode support |

#### Azure OpenAI deployment configuration

You must configure the Azure OpenAI deployment with the model name **gpt-4.1**.

Example endpoint format:

```http
https://{your-resource}.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview
```

### Required database privileges

Before running the schema conversion, ensure the accounts, you use have the minimum privileges required on both the source Oracle database and the scratch Azure Database for PostgreSQL. The Oracle account needs read access to data and dictionary views so the tool can analyze schema and code. The PostgreSQL scratch account must be able to create schemas, tables, and other objects for validation. Use a dedicated service account where possible. Follow the principle of least privilege. Coordinate with your DBAs to grant any temporary elevated rights and to validate connectivity and access before starting the conversion.

#### Source Oracle privileges

The following minimum privileges are required on the source Oracle database:

| Privilege | Purpose |
| --- | --- |
| **CONNECT** | Basic database connection |
| **SELECT_CATALOG_ROLE** | Access to data dictionary views |
| **SELECT ANY DICTIONARY** | Read system metadata and dictionary objects |
| **SELECT `SYS.ARGUMENT$`** | Access to procedure and function argument information |

#### Scratch Database privileges

The following privileges are required on the Azure Database for PostgreSQL Flexible Server (Scratch DB):

| Privilege | Purpose |
| --- | --- |
| **CREATE SCHEMA** | Create validation schemas |
| **CREATE ON DATABASE** | Create database objects for validation |
| **GRANT CONNECT ON DATABASE** | Connection permissions for validation processes |

### Network requirements

- **Outbound connectivity** to Azure OpenAI endpoints
- **Database connectivity** to both source Oracle and target PostgreSQL databases
- **HTTPS access** for Visual Studio Code extension marketplace and GitHub Copilot services
- **GitHub repository access** to https://github.com/microsoft/pgsql-tools/
