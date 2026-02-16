---
title: DocumentDBis the Open-Source Engine Powering Azure DocumentDB
description: Learn about DocumentDB, the open-source document database platform that powers Azure DocumentDB, its features, architecture, and how to get started.
author: patty-chow
ms.author: pattychow
ms.service: azure-documentdb
ms.topic: overview
ms.date: 02/07/2025
---

# DocumentDB: The Open-Source Engine Powering Azure DocumentDB

Azure DocumentDB is built on [DocumentDB](https://aka.ms/documentdb_github), an open-source document database platform. This article provides an overview of DocumentDB, its features, architecture, and how you can contribute to or use this technology.

## What is DocumentDB?

DocumentDB is a fully permissive, open-source platform for document data stores built on the PostgreSQL engine. It serves as the foundation for Azure DocumentDB, providing a powerful and flexible solution for NoSQL database needs.

## DocumentDB is a Truly Open-Source MongoDB Implementation

Unlike other MongoDB engines with restrictive licensing such as [SSPL](https://en.wikipedia.org/wiki/Server_Side_Public_License), DocumentDB uses the permissive MIT license. This means developers have complete freedom to use, modify, and distribute the software without any commercial licensing fees or usage restrictions. In contrast to MongoDB's Server Side Public License (SSPL), which can limit certain uses, DocumentDB's MIT license guarantees true open-source freedom.

## DocumentDB is multicloud and Vendor-Agnostic

DocumentDB provides a portable, interoperable solution for document data stores. Built on PostgreSQL, it allows developers to deploy their applications across various cloud providers or on-premises, avoiding vendor lock-in. This flexibility empowers organizations to choose the best infrastructure for their needs without compromising on database capabilities.

## DocumentDB is Built on PostgreSQL, a Game-Changer for NoSQL Databases

As the distinction between NoSQL and relational databases becomes more blurred, DocumentDB bridges this gap to provide a superior document database experience for most scalable workloads. It combines the strengths of both sides, offering the flexibility and scalability typically associated with NoSQL databases, while harnessing the power and extensive feature set of PostgreSQL – one of the most adopted and respected open-source databases today.
This foundation provides robustness, reliability, and access to PostgreSQL's ecosystem of tools and extensions. Developers can benefit from PostgreSQL's continuous evolution and extensive community support while enjoying the flexibility of a document database.

## Key Features

DocumentDB offers several key features that make it a robust choice for document database operations:
- **BSON document parsing and manipulation:** Efficiently handle Binary JSON (BSON) documents at all levels of nesting.
- **Advanced indexing capabilities:** Support for single field, multi-key, compound, text, and geospatial indexes.
- **Vector search queries:** Powered by the pg_vector PostgreSQL extension, enabling various AI and machine learning applications.
- **Authentication mechanism:** Includes SCRAM (Salted Challenge Response Authentication Mechanism) authentication.
- **Geospatial queries:** Using the capabilities of the PostGIS extension.
- **Full Decimal128 support:** Powered by Intel Floating Point Math Library.
- **Regex support:** Utilizing the PCRE2 Project

## Architecture

DocumentDB consists of two primary components:

1.	pg_documentdb_core: A custom PostgreSQL extension optimizing BSON datatype support in PostgreSQL.
2.	pg_documentdb_api: The data plane implementing CRUD operations, query functionality, and index management.

This architecture allows for building an end-to-end NoSQL database user experience on top of the PostgreSQL engine.

## Contributing to DocumentDB

As an open-source project, DocumentDB welcomes contributions from the community. You can contribute by:
- Starring, forking, and submitting pull requests on [GitHub](https://aka.ms/documentdb_github)
- Reporting issues or suggesting improvements
- Participating in discussions on the #documentdb channel on the [Microsoft OSS Discord server](https://aka.ms/documentdb_discord)

## Getting Started with DocumentDB

To start using DocumentDB locally:

**1. [Install Docker.](https://docs.docker.com/engine/install/)**

**2. Clone the DocumentDB repository.**
```bash
git clone https://github.com/documentdb/documentdb.git
```

**3. Create the Docker image. Navigate to cloned repo.**
```bash
docker build . -f .devcontainer/Dockerfile -t documentdb 
```

**4. Run the Docker image as a container.**
```bash
docker run -v $(pwd):/home/documentdb/code -it documentdb /bin/bash 
```

**5. Build and deploy the binaries.**
```bash
cd code
```
```bash
make
```
```bash
sudo make install
```

**6. Initialize the DocumentDB server and manage dependencies.**

```bash
./scripts/start_oss_server.sh -t documentdb
```

**7. Connect to the psql shell.**
```bash
psql -p 9712 -h localhost -d postgres
```
After following these steps, you're now all set to use DocumentDB locally.

## FAQs

### What is DocumentDB and how does it relate to Azure DocumentDB?

DocumentDB is a fully permissive, open-source platform for document data stores built on the PostgreSQL engine. It serves as the foundation for Azure DocumentDB, providing a powerful and flexible solution for NoSQL database needs.

### How does DocumentDB's licensing compare to other MongoDB implementations?

DocumentDB uses the permissive MIT license, which allows developers complete freedom to use, modify, and distribute the software without any commercial 
licensing fees or usage restrictions. This contrasts with some MongoDB providers’ Server Side Public License (SSPL), which can limit certain uses.

### Can DocumentDB be used across different cloud providers?

Yes, DocumentDB is multicloud and vendor-agnostic. Built on PostgreSQL, it allows developers to deploy their applications across various cloud providers or on-premises, avoiding vendor lock-in and providing flexibility in choosing the best infrastructure for their needs.

### What are the key features of DocumentDB?

DocumentDB offers several key features, including BSON document parsing and manipulation, advanced indexing capabilities (single field, multi-key, compound, text, and geospatial), vector search queries powered by pg_vector, authentication mechanisms including SCRAM, geospatial queries using PostGIS, full Decimal128 support, and regex support using PCRE2.

### How can developers contribute to DocumentDB?

Developers can contribute to DocumentDB by starring, forking, and submitting pull requests on GitHub, reporting issues or suggesting improvements, and participating in discussions on the #documentdb channel on the Microsoft OSS Discord server.
