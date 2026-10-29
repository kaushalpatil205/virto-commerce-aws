# Virto Commerce Platform & Storefront Architecture Document (Task 1)

## 1. Overview
Virto Commerce is a modular, headless enterprise .NET e-commerce platform. It decouples the core commerce engine and business logic (Platform) from the customer-facing user interface (Storefront).

## 2. Responsibilities
- **Virto Commerce Platform Backend:** 
  - Exposes RESTful and GraphQL APIs for catalog management, pricing, customer management, inventory, cart, and checkout.
  - Handles business workflows, integrations, and administration.
- **Virto Commerce Storefront:**
  - Responsive web front-end application consuming the Platform's APIs.
  - Serves product catalogs, product detail pages, search results, shopping cart, and checkout experiences to shoppers.

## 3. Dependencies & Services
- **Relational Database:** Microsoft SQL Server 2022 (Stores structured entities, customers, orders, catalog data).
- **Search Engine:** Lucene (Local default) / OpenSearch (Production).
- **Caching & Bus:** Distributed caching for session and catalog caching via Redis.
- **Cloud Asset Storage:** Amazon S3 (emulated locally by Floci) for storing catalog images, product PDFs, and media assets.
- **Cloud Event Queues:** Amazon SQS (emulated by Floci) for asynchronous order event handling.

## 4. Port Allocations & Communication Matrix
- `8080` (Platform HTTP): Exposed to host for Admin Console & API.
- `8090` (Storefront HTTP): Exposed to host for shopper UI.
- `1433` (SQL Server): Accessible internally to Platform container.
- `4566` (Floci AWS): Accessible to Platform and host tools for S3/SQS emulation.
- `4500` (Floci UI): Web dashboard for inspecting emulated cloud resources.

## 5. Emulator vs. Real AWS Deployment Differences
| Feature | Local (Floci) | Production (AWS) |
| :--- | :--- | :--- |
| **Compute** | Single Docker Host | AWS ECS Fargate Multi-AZ Auto-Scaling |
| **Database** | SQL Server Container on Docker Volume | Amazon RDS SQL Server Multi-AZ with automated backups |
| **S3 Storage** | Local path emulation on port 4566 | Globally distributed Amazon S3 with CloudFront CDN |
| **Security** | Dummy credentials (`test`/`test`) | AWS IAM Roles with STS temporary tokens and Secrets Manager |
