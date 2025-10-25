---
title: "Oracle to PostgreSQL Schema Conversion - Prerequisites"
description: "System requirements, supported versions, and prerequisites for Oracle to PostgreSQL schema conversion using VS Code PostgreSQL extension with Azure OpenAI integration."
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 10/17/2025
ms.service: azure-database-postgresql
ms.subservice: schema-conversion
ms.topic: reference
ms.custom:
  - devx-track-vscode
  - schema-conversion
  - oracle-to-postgresql
  - system-requirements
---

# Prerequisites

This document outlines the system requirements, supported versions, and prerequisites for using the Oracle to PostgreSQL Schema Conversion feature in VS Code.

## System Requirements

| Category | Details |
|----------|---------|
| **VS Code Version** | 1.95.2 or higher |
| **GitHub Copilot Subscription** | Pro+, Business, Enterprise |

## Operating System Support

| Operating System | Support Details |
|------------------|-----------------|
| **Windows** | x64 architecture only |
| **Linux** | x64 architecture |
| **macOS** | macOS 13+ |

## Database Versions

### Oracle Database Support

The following Oracle database versions are supported:
- Oracle 12.1
- Oracle 12.2
- Oracle 18c
- Oracle 19c
- Oracle 21c

### PostgreSQL Version Support

| Component | Version Requirement |
|-----------|-------------------|
| **Azure Database for PostgreSQL** | PostgreSQL version 15 or higher |
| **Scratch Database** | Azure Database for PostgreSQL flexible server |

## Supported Schema Objects

### Database Schema Objects

The conversion tool supports the following Oracle database objects:

- **Tables** - Table definitions, column specifications, and table-level constraints
- **Constraints** - Primary keys, foreign keys, unique constraints, check constraints
- **Indexes** - B-tree indexes, unique indexes, composite indexes
- **Sequences** - Oracle sequence objects for auto-incrementing values
- **Triggers** - Row-level and statement-level triggers
- **Views** - Standard database views
- **Materialized Views** - Oracle materialized views and refresh logic
- **Schemas** - Schema-level objects and organization
- **Synonyms** - Public and private synonyms (with limitations)

### Oracle Code Objects

Advanced Oracle code constructs supported for conversion:

- **Triggers** - Complex trigger logic and event handling
- **Packages** - Oracle package specifications and bodies
- **Functions** - User-defined functions with complex logic
- **Stored Procedures** - Oracle stored procedures and parameter handling

## AI Model Requirements

You need **any one** of the following AI components configured:

| AI Component | Model Version |
|--------------|---------------|
| **Azure OpenAI** | GPT-4.1 deployment |
| **GitHub Copilot** | GitHub Copilot with Agent Mode support |

### Azure OpenAI Deployment Configuration

The Azure OpenAI deployment must be configured with the model name **gpt-4.1**. 

Example endpoint format:
```
https://{your-resource}.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview
```

## Required Database Privileges

### Source Oracle Database Privileges

The following minimum privileges are required on the source Oracle database:

| Privilege | Purpose |
|-----------|---------|
| **CONNECT** | Basic database connection |
| **SELECT_CATALOG_ROLE** | Access to data dictionary views |
| **SELECT ANY DICTIONARY** | Read system metadata and dictionary objects |
| **SELECT ON SYS.ARGUMENT$** | Access to procedure/function argument information |

### Scratch Database Privileges

The following privileges are required on the Azure Database for PostgreSQL Flexible Server (Scratch DB):

| Privilege | Purpose |
|-----------|---------|
| **CREATE SCHEMA** | Create validation schemas |
| **CREATE ON DATABASE** | Create database objects for validation |
| **GRANT CONNECT ON DATABASE** | Connection permissions for validation processes |

## Network Requirements

- **Outbound connectivity** to Azure OpenAI endpoints
- **Database connectivity** to both source Oracle and target PostgreSQL databases
- **HTTPS access** for VS Code extension marketplace and GitHub Copilot services
- **GitHub repository access** to https://github.com/microsoft/pgsql-tools/
