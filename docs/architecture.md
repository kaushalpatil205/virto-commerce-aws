# Virto Commerce Platform & Storefront Architecture Document (Task 1)

## 1. System Overview
Virto Commerce is a modular, enterprise-grade, headless .NET e-commerce platform. It decouples the core commerce business logic and backend engines (Platform) from the customer-facing shopping experience (Storefront).

The platform architecture operates as an asynchronous, API-first ecosystem capable of scaling independently across compute, persistence, and storage layers.

```mermaid
graph TD
    Client["Shopper Browser / Admin Engineer"]
    
    subgraph Host["Containerized Docker Infrastructure (virto-network)"]
        Storefront["vc-storefront-frontend (Port 8090)<br/>- Vue 3 Single Page Application (SPA)<br/>- ASP.NET Core Static Web Host<br/>- IISUrlRewrite.xml Proxy Engine"]
        Platform["vc-platform-backend (Port 8081)<br/>- ASP.NET Core 8 Modular Engine<br/>- VirtoCommerce.XFrontend (GraphQL API)<br/>- Lucene Search & Background Workers"]
        SQL["vc-database (Port 1433)<br/>- Microsoft SQL Server 2022 Express<br/>- Relational Storage (VirtoCommerce3)"]
        Floci["vc-floci (Port 4566 & 4500)<br/>- Floci AWS Local Cloud Emulator<br/>- S3 Bucket: virto-commerce-media-assets<br/>- SQS Queue: virto-order-processing-queue"]
        
        Client -->|Browse Store: Port 8090| Storefront
        Client -->|Platform Admin Portal: Port 8081| Platform
        Client -->|Floci Web Console: Port 4500 / 4566| Floci
        
        Storefront -->|Internal GraphQL Proxy (^graphql -> /x-api/graphql)| Platform
        Platform -->|Relational Queries (Port 1433)| SQL
        Platform -->|Catalog Media S3 & Order Events SQS (Port 4566)| Floci
    end
```

---

## 2. Component Responsibilities & Service Contracts

### 2.1 Virto Commerce Platform Backend (`vc-platform-backend`)
- **Runtime:** ASP.NET Core 8 with Entity Framework Core and Hangfire/InMemory background workers.
- **Port:** Host port `8081` mapped to container port `80`.
- **API Endpoints:**
  - RESTful APIs for catalog administration, inventory control, pricing tiers, customer management, and store configurations.
  - GraphQL Experience API (`/x-api/graphql`) exposed via the `VirtoCommerce.XFrontend` module for high-efficiency frontend queries.
  - OAuth 2.0 Identity Server endpoints (`/connect/token`) handling authentication and Bearer token issuance.
- **Data Access:** Communicates with Microsoft SQL Server 2022 over TCP port `1433` using connection string `ConnectionStrings__VirtoCommerce`.

### 2.2 Virto Commerce Frontend Storefront (`vc-storefront-frontend`)
- **Runtime:** Decoupled Vue 3 Single Page Application (SPA) built with Vite, TypeScript, and Apollo GraphQL Client (`vc-theme-b2b-vue` v2.61.0).
- **Host Engine:** ASP.NET Core web server serving compiled static micro-frontend bundles (`remoteEntry-*.js`, `mf-manifest.json`, CSS, assets) from `/opt/virtocommerce/storefront/wwwroot`.
- **Port:** Host port `8090` mapped to container port `80`.
- **URL Rewriting Middleware:** Uses `IISUrlRewrite.xml` to intercept all browser Apollo client requests matching `^graphql(.*)` and forward them internally to `http://vc-platform:80/x-api/graphql{R:1}` over the Docker bridge network.

### 2.3 Microsoft SQL Server 2022 Express (`vc-database`)
- **Runtime:** `mcr.microsoft.com/mssql/server:2022-latest`
- **Port:** Host port `1433` mapped to container port `1433`.
- **Persistence:** Named persistent Docker volume `vc-db-data` mounted to `/var/opt/mssql`.
- **Healthcheck:** Probes database engine readiness every 10 seconds via `/opt/mssql-tools18/bin/sqlcmd` before allowing the platform backend to connect.

### 2.4 Floci AWS Local Cloud Emulator (`vc-floci`)
- **Runtime:** `floci/floci:latest`
- **Ports:** Host port `4566` (AWS wire API gateway) and dynamic port `4500` (Floci Web Console UI via child container).
- **Emulated Services:**
  - **Amazon S3:** Bucket `virto-commerce-media-assets` for catalog product images, brand logos, and marketing PDFs.
  - **Amazon SQS:** Queue `virto-order-processing-queue` for asynchronous checkout processing and event streaming.
  - **AWS IAM:** Role `virto-commerce-platform-role` and policy attachments defining least-privilege access.

---

## 3. Communication Matrix & Network Topology

| Source Service | Target Service | Protocol / Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Browser / User** | `vc-storefront-frontend` | HTTP / `8090` | Shopper navigation, catalog browsing, shopping cart, and checkout |
| **Browser / User** | `vc-platform-backend` | HTTP / `8081` | Administrative dashboard, catalog management, module configuration |
| **Browser / User** | `vc-floci` (child UI) | HTTP / `4500` | Floci Web Console cloud resource explorer |
| `vc-storefront` | `vc-platform` | HTTP / `80` (Internal) | Native URL Rewrite proxy: `^graphql` &rarr; `/x-api/graphql` |
| `vc-platform` | `vc-database` | TDS / `1433` (Internal) | Relational SQL queries, EF Core migrations, Hangfire jobs |
| `vc-platform` | `vc-floci` | HTTP / `4566` (Internal) | S3 media asset storage and SQS order event dispatch |
| **Terraform CLI** | `vc-floci` | HTTP / `4566` (Host) | Declarative provisioning of AWS infrastructure |

---

## 4. Emulator vs. Production AWS Differences

| Architectural Layer | Local Emulation (Floci & Docker) | Production Architecture (AWS Cloud) |
| :--- | :--- | :--- |
| **Compute Tier** | Single Docker Host running 4 containers via Docker Compose | AWS ECS Fargate tasks in private subnets across multiple Availability Zones |
| **Load Balancing** | Direct port bindings (`:8081`, `:8090`) on `localhost` | AWS Application Load Balancer (ALB) with SSL/TLS termination and route path routing |
| **Relational Database** | Containerized SQL Server Express on named volume `vc-db-data` | Amazon RDS for SQL Server (Multi-AZ) with automated automated daily snapshots |
| **Asset Storage (S3)** | Local Floci emulator bucket (`http://localhost:4566`) | Amazon S3 with AWS CloudFront CDN distribution for edge caching |
| **Event Messaging** | Floci local SQS emulation queue | Amazon SQS Standard/FIFO Queue with Dead-Letter Queue (DLQ) redrive |
| **Security & Secrets** | Static credentials (`test`/`test`) in `.env` | AWS Secrets Manager, Systems Manager Parameter Store, and IAM Task Roles |
| **Search Indexing** | Local Lucene file system indices | Amazon OpenSearch Service cluster with high availability |
