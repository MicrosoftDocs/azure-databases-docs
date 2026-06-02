---
title: FAQ for Oracle to Azure Database for PostgreSQL schema conversion
description: Frequently asked questions about the Oracle to Azure Database for PostgreSQL schema conversion feature in Visual Studio Code with Microsoft Foundry integration, including supported sources, data privacy, deployment, validation, and getting help.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.service: azure-database-postgresql
ms.topic: faq
ms.collection: ce-skilling-ai-copilot
ms.update-cycle: 180-days
---

# Frequently asked questions about Oracle to Azure Database for PostgreSQL schema conversion

This article answers the most common questions about the Oracle to Azure Database for PostgreSQL schema conversion feature in the [Visual Studio Code PostgreSQL extension](../../extensions/vs-code-extension/overview.md). The feature uses [Microsoft Foundry](/azure/ai-foundry/what-is-azure-ai-foundry) to convert Oracle database schemas into PostgreSQL DDL that you can deploy to [Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/overview).

## Is the converted schema production-ready?

The schema conversion tool generates production-quality PostgreSQL DDL from the Oracle source and helps teams move quickly toward production deployment. For the recommended validation flow, see [Best practices for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-best-practices.md).

## What does the conversion tool do?

The tool reads metadata from the Oracle source schema and generates the equivalent PostgreSQL artifacts that you can deploy to Azure Database for PostgreSQL flexible server:

- **PostgreSQL DDL files**. One file per table, view, function, procedure, trigger, type, sequence, and index.
- **Conversion reports**. Structured summaries of what was converted, what was skipped, and any items that need review.

For a full overview of inputs, outputs, and the conversion pipeline, see [What is Oracle to Azure Database for PostgreSQL schema conversion?](schema-conversions-overview.md).

## Is there an extra cost for the schema conversion feature?

The schema conversion feature in the Visual Studio Code PostgreSQL extension is free. Billing applies only to the Azure resources that the feature uses:

- **Microsoft Foundry usage**: the AI tokens consumed during conversion. For pricing, see [Microsoft Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/).
- **Azure Database for PostgreSQL flexible server**: the target server (and any scratch validation server). For pricing, see [Azure Database for PostgreSQL pricing](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/).

## How do I get started?

Follow the end-to-end walkthrough in the [Tutorial: Convert Oracle schemas to Azure Database for PostgreSQL](schema-conversions-tutorial.md). The tutorial covers installing the extension, connecting to the Oracle source and Azure Database for PostgreSQL target, configuring Microsoft Foundry, and running the first conversion.

## How does the conversion work?

The Visual Studio Code PostgreSQL extension converts an Oracle schema into equivalent PostgreSQL objects by using a Microsoft Foundry model deployment enabled in the Azure environment. It processes the conversion in manageable batches, validates converted objects in a scratch schema, and summarizes the results in a [customer summary report](schema-conversions-reports.md#customer-summary-report).

## Is my schema or data sent to the AI? Is anything retained?

- **Schema metadata is sent** to the Microsoft Foundry model. This includes DDL, table and column names, function bodies, view definitions, and trigger code. The model needs this information to produce accurate PostgreSQL output.
- **Row-level data isn't sent.** The tool reads from the Oracle catalog only; it doesn't query tables.

The model endpoint inherits Microsoft Foundry's enterprise data-handling commitments. For data-handling terms and certifications, see [Microsoft Trust Center](https://www.microsoft.com/trust-center) and [Azure compliance offerings](/azure/compliance/).

## Where does the model run?

The model runs in the customer's Azure environment through the configured Microsoft Foundry deployment. Data residency follows the selected Azure region where the model is available. For region details, see [Microsoft Foundry region availability](/azure/ai-foundry/reference/region-support).

## What do I need before I run a conversion?

On the Azure side:

- An [Azure Database for PostgreSQL flexible server](/azure/postgresql/flexible-server/quickstart-create-server) (PostgreSQL version 15 or later recommended).
- A login with the privileges to create schemas, tables, functions, and extensions. During conversion, the tool creates scratch schemas named with the `_mig_scratch_` prefix in the selected PostgreSQL database to validate converted objects, and drops them when the run completes.
- The required PostgreSQL extensions allowlisted and installed, and `search_path` configured. The canonical list is in [Best practices for schema conversion](schema-conversions-best-practices.md#allow-list-and-install-required-extensions).
- A [Microsoft Foundry deployment](/azure/ai-foundry/how-to/create-projects) with sufficient token-per-minute capacity. See [Microsoft Foundry capacity recommendations](schema-conversions-best-practices.md#configure-microsoft-foundry-capacity).

On the Oracle side, see the [Oracle source requirements in the tutorial](schema-conversions-tutorial.md).

## What Oracle features can't be converted?

See [Oracle to Azure Database for PostgreSQL schema conversion limitations](schema-conversions-limitations.md) for the complete list of unsupported Oracle features and recommended PostgreSQL alternatives.

## What does the conversion success rate mean for my project?

The success rate shows how much of the Oracle schema the tool converted to PostgreSQL DDL without human intervention. For most customers, this rate represents weeks of manual work saved per migration. The remaining objects appear as **review tasks** in the [customer summary report](schema-conversions-reports.md#customer-summary-report) with context, suggested fixes, and links to relevant guidance, so the review step is guided, not open-ended.

## Will two runs of the converter produce the same output?

**Functionally, yes.** The PostgreSQL output behaves the same across runs for the same Oracle input.

**Textually, the output can vary slightly.** AI models can express equivalent logic in more than one valid way. For example, the order of independent statements, comment phrasing, or whitespace can differ. If you need a text-stable artifact for audit, capture the first run's output folder and treat it as the reference for the project.

## What validation should I do before I go to production?

Recommended validation steps:

1. Read the [customer summary report](schema-conversions-reports.md#customer-summary-report) end-to-end and resolve every **review task**.
1. Spot-check business-critical procedures, triggers, and complex views.
1. Run functional smoke tests on representative objects in a nonproduction database.
1. Verify that sequences are advanced past the data's maximum IDs before you re-enable application writes.
1. Confirm that all required extensions are installed and present in `search_path`.

For the full precutover checklist, see [Best practices for schema conversion](schema-conversions-best-practices.md#validate-the-converted-schema).

## How do I deploy the generated DDL?

The tool writes per-object DDL grouped by object kind (types, sequences, tables, indexes, views, functions, procedures, triggers, materialized views). Deploy the DDL files using the Visual Studio Code PostgreSQL extension or psql to execute them against the target Azure Database for PostgreSQL flexible server.

## How do I confirm the schema deployed correctly?

After deployment, compare object counts in Azure Database for PostgreSQL flexible server against the [customer summary report](schema-conversions-reports.md#customer-summary-report). Then smoke-test critical objects: call sample functions and procedures, insert a row that fires a trigger, and query each view.

## Where can I get help?

- **Documentation**: Start with the [schema conversion overview](schema-conversions-overview.md), [tutorial](schema-conversions-tutorial.md), [best practices](schema-conversions-best-practices.md), [limitations](schema-conversions-limitations.md), and [reports](schema-conversions-reports.md) articles.
- **In-product feedback**: Use the feedback option in the Visual Studio Code PostgreSQL extension. Prefix the title with `Schema Conversion:` so the product team can route it quickly.

## Related content

- [What is Oracle to Azure Database for PostgreSQL schema conversion?](schema-conversions-overview.md)
- [Tutorial: Convert Oracle schemas to Azure Database for PostgreSQL](schema-conversions-tutorial.md)
- [Best practices for Oracle to Azure Database for PostgreSQL schema conversion](schema-conversions-best-practices.md)
- [Oracle to Azure Database for PostgreSQL schema conversion limitations](schema-conversions-limitations.md)
- [Schema conversion reports for Oracle to Azure Database for PostgreSQL](schema-conversions-reports.md)
