# Virto Commerce Platform & Modern Storefront Deployment with AWS Emulation (Floci)

[![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![Floci AWS](https://img.shields.io/badge/AWS%20Emulator-Floci-orange.svg)](https://floci.io/aws/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)
[![Virto Commerce](https://img.shields.io/badge/E--Commerce-VirtoCommerce-brightgreen.svg)](https://virtocommerce.com/)

**Submission by:** Kaushal Patil  
**Assignment:** Virto Commerce Platform & Storefront Deployment with AWS Cloud Emulation (Floci)  
**Architecture:** Modern Decoupled Headless Single Page Application (Vue 3, Vite, Apollo GraphQL) + Modular ASP.NET Core 8 Platform Backend  

---

## Table of Contents
1. [Architecture Overview & System Topology](#1-architecture-overview--system-topology)
2. [Assignment Tasks & Verification Matrix (Tasks 1 to 8)](#2-assignment-tasks--verification-matrix-tasks-1-to-8)
3. [Progression Narrative: Initial Review Stance vs. Deeper Architectural Discovery](#3-progression-narrative-initial-review-stance-vs-deeper-architectural-discovery)
4. [Prerequisites & Docker Image Baseline](#4-prerequisites--docker-image-baseline)
5. [Repository Structure](#5-repository-structure)
6. [Step-by-Step Multi-Platform Execution Runbook (macOS/Linux & Windows)](#6-step-by-step-multi-platform-execution-runbook-macoslinux--windows)
7. [In-Depth Analysis: Modules, Themes, and Scripts](#7-in-depth-analysis-modules-themes-and-scripts)
8. [The Critical Role of `IISUrlRewrite.xml`](#8-the-critical-role-of-iisurlrewritexml)
9. [Floci AWS Cloud Emulation & Terraform IaC](#9-floci-aws-cloud-emulation--terraform-iac)
10. [Network Ports & Service Matrix](#10-network-ports--service-matrix)
11. [Resilience, Data Persistence & Fault Tolerance (Task 6)](#11-resilience-data-persistence--fault-tolerance-task-6)
12. [Visual Verification: All 11 Milestone Screenshots](#12-visual-verification-all-11-milestone-screenshots)
13. [Troubleshooting & Solved Issues](#13-troubleshooting--solved-issues)
14. [Official Technical References](#14-official-technical-references)

---

## 1. Architecture Overview & System Topology

The deployment establishes a clean, modern **4-container native architecture** on Docker bridge network `virto-network`:

```mermaid
graph TD
    Client["Shopper Browser / Admin Engineer"]
    
    subgraph Host["Local Host Workstation"]
        Storefront["vc-storefront-frontend (Port 8090)<br/>- Official Virto Commerce Vue 3 B2B SPA<br/>- ASP.NET Core Static Web Host<br/>- IISUrlRewrite.xml Proxy Engine"]
        Platform["vc-platform-backend (Port 8081)<br/>- ASP.NET Core 8 Modular Backend<br/>- VirtoCommerce.XFrontend (GraphQL API)<br/>- Hangfire Workers & Lucene Search"]
        SQL["vc-database (Port 1433)<br/>- Microsoft SQL Server 2022 Express<br/>- Relational Database VirtoCommerce3"]
        Floci["vc-floci (Port 4566 & 4500)<br/>- Floci AWS Local Cloud Emulator<br/>- S3: virto-commerce-media-assets<br/>- SQS: virto-order-processing-queue"]
        
        Client -->|Browse Store: Port 8090| Storefront
        Client -->|Platform Admin Portal: Port 8081| Platform
        Client -->|Inspect Cloud Resources: Port 4500 / 4566| Floci
        
        Storefront -->|Internal GraphQL Proxy (^graphql -> /x-api/graphql)| Platform
        Platform -->|Relational Queries (Port 1433)| SQL
        Platform -->|Catalog Media S3 & Order Events SQS (Port 4566)| Floci
    end
```

---

## 2. Assignment Tasks & Verification Matrix (Tasks 1 to 8)

| Task # | Task Description | Implementation & Satisfaction Proof | Status |
| :--- | :--- | :--- | :--- |
| **Task 1** | **System Architecture Design & Document** | Detailed architecture documented in [`docs/architecture.md`](docs/architecture.md) and Section 1 of this README. Covers high-level topology, component responsibilities, dependency mapping, port allocations, and emulator vs production AWS comparisons. | **100% Satisfied** |
| **Task 2** | **Containerized Local Deployment (Docker Compose)** | Orchestrates all core services via [`docker-compose.yml`](docker-compose.yml) using official vendor images (`vc-database`, `vc-platform-backend`, `vc-storefront-frontend`, `vc-floci`) with automated healthchecks, environment variables, named persistent volumes (`vc-db-data`, `vc-platform-data`), and bridge networking (`virto-network`). | **100% Satisfied** |
| **Task 3** | **Cloud Resource Emulation (Floci AWS)** | Configured `vc-floci` running `floci/floci:latest` on port `4566` with Docker engine socket mounted. Emulates AWS S3 for media assets, AWS SQS for order queueing, and IAM task execution roles locally without cloud costs. | **100% Satisfied** |
| **Task 4** | **Infrastructure as Code (Terraform)** | Wrote declarative Terraform scripts in [`terraform/main.tf`](terraform/main.tf), `variables.tf`, and `outputs.tf` targeting Floci (`http://localhost:4566`). Provisions S3 bucket (`virto-commerce-media-assets`), SQS queue (`virto-order-processing-queue`), and IAM role (`virto-commerce-platform-role`) with 100% idempotency, verified via AWS CLI v2. | **100% Satisfied** |
| **Task 5** | **Platform & Storefront Operational Validation** | Fully validated both applications: Platform Admin (`http://localhost:8081`) with authentic password reset and installed modules, and Customer Storefront (`http://localhost:8090`) serving the live modern Vue 3 SPA with 389 products, 123 categories, 9 catalogs, Bolts category (34 items), search, and cart. | **100% Satisfied** |
| **Task 6** | **Resilience, Data Persistence & Fault Tolerance Test** | Conducted deliberate persistence tests via `docker compose restart vc-db` and deliberate outage tests via `docker compose stop vc-db ; docker compose start vc-db`. Confirmed SQL Server preserves all database tables and catalog records across restarts via Docker volume `vc-db-data`. | **100% Satisfied** |
| **Task 7** | **CI/CD Pipeline & Automated Deployment Scripts** | Packaged automated deployment scripts for both Linux/macOS (`scripts/deploy.sh`, `scripts/cleanup.sh`, `scripts/install-sample-data.sh`) and Windows PowerShell (`scripts/deploy.ps1`, `scripts/cleanup.ps1`), backed by GitHub Actions workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). | **100% Satisfied** |
| **Task 8** | **Technical Presentation & Documentation Report** | Formulated complete presentation guide in [`docs/presentation.md`](docs/presentation.md), master runbook in [`fresh_restart_runbook.md`](fresh_restart_runbook.md), and compiled formal PDF submission report [`Virto_Commerce_AWS_Technical_Submission_Report.pdf`](Virto_Commerce_AWS_Technical_Submission_Report.pdf) with all 11 verified milestone screenshots. | **100% Satisfied** |

---

## 3. Progression Narrative: Initial Review Stance vs. Deeper Architectural Discovery

### Earlier Explanation Provided in the Initial Review:
> *"As committed, the setup utilizes the exact baseline configuration and images specified in the Git repository, beginning with the October 29th deployment, cleanly stopping the environment via docker compose down, and transitioning to the latest platform build. In the demonstration, I showcase how the previous module compatibility constraint—where marketplace modules required a higher platform version—was systematically resolved by provisioning the latest compatible platform along with the requisite AdminShell, BackgroundJobs, and FileSystemAssets modules. Regarding the customer storefront (:8090), the video clarifies that the 405 MethodNotAllowed status is due to an upstream API deprecation (GET /api/stores replaced by POST /api/stores/search), confirming that the UI will only render once external Liquid theme templates are mounted to cms-content/Themes/ alongside an updated API contract."*

### How I Kept Investigating and Uncovered the True Root Cause:
The statement above was the initial analysis I provided when first diagnosing the storefront routing behavior. Rather than stopping at that hurdle, I conducted a deeper technical investigation into the Virto Commerce codebase and architectural ecosystem.

Through this investigation, I uncovered the true root causes:
1. **Transition to Modern Headless Architecture:** Virto Commerce officially deprecated legacy monolithic server-rendered Liquid (MVC) templates. The customer storefront is now a decoupled **Vue 3 Single Page Application (SPA)** built with Vite, TypeScript, and Apollo GraphQL Client (`vc-theme-b2b-vue`).
2. **The Storefront Crash (`templates/index.liquid`):** The legacy container crashed because it attempted to parse modern compiled JavaScript bundles through an obsolete server-side Liquid parser, throwing:
   ```text
   InvalidOperationException: The relative virtual path 'Themes/B2B-store/default/templates/index.liquid' is not allowed to refer at or above the root directory of the application.
   ```
   Furthermore, on a cold start, SQL Server had 0 stores, causing ASP.NET Core `WorkContextBuildMiddleware` to crash with `NoStoresException: No stores defined`.
3. **Missing GraphQL Experience APIs:** The modern Vue 3 storefront queries `/x-api/graphql`. A blank platform backend only contains basic REST endpoints; it requires the `VirtoCommerce.XFrontend` module to expose the GraphQL experience API.
4. **Password Policy Constraint:** ASP.NET Core Identity defaults to a minimum password length of 8 characters, while seed credentials are `admin` / `store` (5 characters). Setting `RequiredLength: 5` in `appsettings.json` resolves this naturally.

---

## 4. Prerequisites & Docker Image Baseline

Every container image in this deployment is **100% official and untampered**:

| Container Name | Service | Docker Image & Version | Technical Purpose |
| :--- | :--- | :--- | :--- |
| **`vc-floci`** | `vc-floci` | `floci/floci:latest` (v2.4.0) | High-performance GraalVM Quarkus AWS cloud emulator. Exposes port `4566` to emulate S3, SQS, DynamoDB, and IAM locally without cloud costs. |
| **`vc-database`** | `vc-db` | `mcr.microsoft.com/mssql/server:2022-latest` | Microsoft SQL Server 2022 Express on Linux. Hosts relational database `VirtoCommerce3` with automated schema migrations. |
| **`vc-platform-backend`** | `vc-platform` | `virtocommerce/platform:latest` (v3.x) | Virto Commerce Platform API (.NET 8). Provides REST APIs, GraphQL Experience APIs, Hangfire workers, and Platform Admin management UI. |
| **`vc-storefront-frontend`** | `vc-storefront` | `virtocommerce/storefront:latest` (v3.x) | Virto Commerce Storefront host (.NET 8). Serves static SPA assets and proxies GraphQL queries via IIS URL Rewrite middleware. |

---

## 5. Repository Structure

```text
virto-commerce-aws/
├── .github/
│   └── workflows/
│       └── deploy.yml                  # Automated CI/CD deployment & validation workflow
├── assets/                             # Catalog media assets & product photos
├── cms-content/                        # Storefront layouts & compiled Vue 3 B2B theme
│   └── Themes/B2B-store/default/       # Compiled SPA bundles (remoteEntry-*.js, mf-manifest.json)
├── docs/
│   ├── architecture.md                 # System Architecture Document (Task 1)
│   └── presentation.md                 # Final Technical Presentation Guide (Task 8)
├── modules/                            # Pre-loaded official Virto Commerce modules (XFrontend, etc.)
├── screenshots/                        # Deployment evidence & test screenshots (All 11 Milestones)
├── scripts/
│   ├── cleanup.sh / cleanup.ps1        # Teardown automation scripts
│   ├── deploy.sh / deploy.ps1          # Master deployment automation scripts
│   ├── generate_pdf.py                 # Automated PDF report compiler
│   └── install-sample-data.sh          # Official sample data installer & polling script
├── terraform/
│   ├── main.tf                         # Terraform S3, SQS, and IAM declarations (Task 4)
│   ├── outputs.tf                      # Exported bucket names and queue URLs
│   └── variables.tf                    # Configurable endpoints and regions
├── docker-compose.yml                  # 4-container orchestration topology (Task 2 & 3)
├── IISUrlRewrite.xml                   # Native ASP.NET Core GraphQL URL rewrite middleware
├── README.md                           # Master Project Documentation & Runbook
└── Virto_Commerce_AWS_Technical_Submission_Report.pdf # Formal 11-milestone PDF Report
```

---

## 6. Step-by-Step Multi-Platform Execution Runbook (macOS/Linux & Windows)

### Step 1: Start All Docker Services
Launches all 4 containers in detached mode on network `virto-network`.

```bash
# macOS / Linux (Bash)
cd /Users/Vraj/Downloads/virto-commerce-aws
docker compose up -d
sleep 35
docker compose ps
```
```powershell
# Windows (PowerShell)
cd C:\Users\Vraj\Downloads\virto-commerce-aws
docker compose up -d
Start-Sleep -Seconds 35
docker compose ps
```

---

### Step 2: Configure Password Policy Length
Modifies ASP.NET Core Identity's `RequiredLength` from 8 to 5 in `appsettings.json` and restarts the backend:

```bash
# macOS / Linux (Bash)
docker exec vc-platform-backend sed -i \
  's/"RequiredLength": 8/"RequiredLength": 5/g' \
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
sleep 15
```
```powershell
# Windows (PowerShell)
docker exec vc-platform-backend sed -i `
  's/"RequiredLength": 8/"RequiredLength": 5/g' `
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
Start-Sleep -Seconds 15
```

---

### Step 3: Platform Admin Login & Natural Password Reset
1. Open browser to: `http://localhost:8081`
2. Log in with initial credentials: **Username:** `admin` | **Password:** `store`
3. Platform Admin displays the official **Change Password** screen.
4. Fill in: Current: `store` | New: `store` *(or `Store@2026!`)* | Confirm: `store` -> Click **Save**.

---

### Step 4: Install Official Sample Data (Products & Catalogs)
Authenticates, streams the official 59.5 MB compressed catalog dataset from Virto's Azure CDN into SQL Server, and actively verifies 1 Store, 9 Catalogs, 123 Categories, and 389 Products:

```bash
# macOS / Linux (Bash)
./scripts/install-sample-data.sh
```
```powershell
# Windows (PowerShell)
bash ./scripts/install-sample-data.sh
```

---

### Step 5: Build Lucene Search Indexes & Reload Storefront
Rebuilds inverted full-text indexes for Category, Product, and Member entities, flushes Storefront memory cache, and verifies index counts:

```bash
# macOS / Linux (Bash)
# 1. Obtain API token
TOKEN=$(curl -s -X POST http://localhost:8081/connect/token -d "grant_type=password&username=admin&password=store" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))')
[ -z "$TOKEN" ] && TOKEN=$(curl -s -X POST http://localhost:8081/connect/token -d "grant_type=password&username=admin&password=Store@2026!" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))')

# 2. Trigger search index rebuild for Products, Categories, and Members
curl -s -X POST http://localhost:8081/api/search/indexes/index \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"documentType": "Category", "deleteExistingIndex": true},
    {"documentType": "Product", "deleteExistingIndex": true},
    {"documentType": "Member", "deleteExistingIndex": true}
  ]'

# 3. Wait 5 seconds and restart Storefront to bind to the newly imported store context
sleep 5
docker restart vc-storefront-frontend
sleep 5

# 4. Check index counts
curl -s -X GET http://localhost:8081/api/search/indexes -H "Authorization: Bearer $TOKEN"
```

```powershell
# Windows (PowerShell)
# 1. Obtain API token
$tokenResponse = Invoke-RestMethod -Uri "http://localhost:8081/connect/token" `
  -Method Post `
  -Body "grant_type=password&username=admin&password=store" `
  -ContentType "application/x-www-form-urlencoded" `
  -ErrorAction SilentlyContinue
if (-not $tokenResponse.access_token) {
    $tokenResponse = Invoke-RestMethod -Uri "http://localhost:8081/connect/token" `
      -Method Post `
      -Body "grant_type=password&username=admin&password=Store@2026!" `
      -ContentType "application/x-www-form-urlencoded"
}
$TOKEN = $tokenResponse.access_token

# 2. Trigger search index rebuild for Products, Categories, and Members
Invoke-RestMethod -Uri "http://localhost:8081/api/search/indexes/index" `
  -Method Post `
  -Headers @{ "Authorization" = "Bearer $TOKEN"; "Content-Type" = "application/json" } `
  -Body '[{"documentType":"Category","deleteExistingIndex":true},{"documentType":"Product","deleteExistingIndex":true},{"documentType":"Member","deleteExistingIndex":true}]'

# 3. Wait 5 seconds and restart Storefront to bind to the newly imported store context
Start-Sleep -Seconds 5
docker restart vc-storefront-frontend
Start-Sleep -Seconds 5

# 4. Check index counts
Invoke-RestMethod -Uri "http://localhost:8081/api/search/indexes" `
  -Headers @{ "Authorization" = "Bearer $TOKEN" }
```

---

### Step 6: Verify Modern Customer Storefront
Open browser to `http://localhost:8090/`:
* **Homepage:** `http://localhost:8090/` (Navbar with **All products**, **Bolts**, Snacks, Soft Drinks, search bar, cart).
* **MegaMenu:** Click **"All products"** to inspect category tree.
* **Bolts Category:** `http://localhost:8090/bolts` (34 products, brand filters, prices).
* **Catalog Grid:** `http://localhost:8090/catalog` (139 B2B items, price facet filtering).

---

### Step 7: Provision AWS Infrastructure via Terraform against Floci
```bash
# macOS / Linux (Bash)
cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform init
terraform apply -auto-approve
```
```powershell
# Windows (PowerShell)
cd C:\Users\Vraj\Downloads\virto-commerce-aws\terraform
terraform init
terraform apply -auto-approve
```

---

### Step 8: Verify AWS Resources on Floci via AWS CLI
```bash
# macOS / Linux (Bash)
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues
```
```powershell
# Windows (PowerShell)
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

---

### Step 9: Access Floci Web Console Dashboard
Open your browser to: `http://localhost:4566/_floci/ui` (or `http://localhost:4500`) to inspect active S3 buckets and SQS queues.

---

## 7. In-Depth Analysis: Modules, Themes, and Scripts

### 7.1 Why I Pre-Installed Modules in `./modules`
Virto Commerce is a modular monolith. If the platform downloads 40+ modules on cold start from the AppStore:
* It hits GitHub's unauthenticated rate limit (**60 requests/hour/IP**).
* It takes 20+ minutes and encounters HTTP socket timeouts.
* It requires repeated container restarts during database schema migrations.  
Pre-loading verified module releases in `./modules` mounted into `/opt/virtocommerce/platform/modules` provides instant, deterministic, offline-capable boots.

### 7.2 Why I Mounted Themes in `./cms-content`
The customer storefront is the official **Virto Commerce Modern B2B Theme** (`vc-theme-b2b-vue` v2.61.0).
* Mounting `./cms-content` to `/opt/virtocommerce/storefront/cms-content` and `/root/cms-content` supplies store layouts, navigation definitions, and theme configuration.
* Mounting static Vite bundles into `/opt/virtocommerce/storefront/wwwroot/` allows ASP.NET Core to serve JavaScript chunks, CSS, and media directly to the browser.

### 7.3 Breakdown of `scripts/install-sample-data.sh`
1. Validates that `vc-database` and `vc-platform-backend` are running.
2. Checks SQL Server table counts to skip download if sample data is already present.
3. Authenticates via Bearer token or administrative API key in `dbo.UserApiKey`.
4. Streams the 59.5 MB compressed catalog dataset from Virto's Azure CDN.
5. Polls SQL Server every 4 seconds until all 389 products are written, then resets `PasswordExpired = 0` to clean up demo data side-effects.

---

## 8. The Critical Role of `IISUrlRewrite.xml`

* **File Location:** [`IISUrlRewrite.xml`](IISUrlRewrite.xml)
* **Target Container Path:** Mounted into `/opt/virtocommerce/storefront/IISUrlRewrite.xml`.

The modern Vue 3 SPA queries `/graphql`, while the backend exposes `/x-api/graphql`. `IISUrlRewrite.xml` leverages ASP.NET Core URL Rewrite middleware:
```xml
<rewrite>
  <rules>
    <rule name="Rewrite GraphQL to Experience API" stopProcessing="true">
      <match url="^graphql(.*)" />
      <action type="Rewrite" url="http://vc-platform:80/x-api/graphql{R:1}" />
    </rule>
  </rules>
</rewrite>
```
This enables direct Storefront hosting and internal GraphQL proxying across the Docker network without requiring an external NGINX reverse-proxy container.

---

## 9. Floci AWS Cloud Emulation & Terraform IaC

* **Emulator Service:** `vc-floci` running `floci/floci:latest` on port `4566`.
* **Platform Connection:** Wired internally via `VirtoCommerce__AWS__ServiceUrl=http://floci:4566`.
* **Terraform Declarations:**
  * S3 Media Bucket: `virto-commerce-media-assets`
  * SQS Order Queue: `virto-order-processing-queue`
  * IAM Task Role: `virto-commerce-platform-role`
  * IAM Policy: S3 object read/write policy attachment

---

## 10. Network Ports & Service Matrix

| Service | Container Name | Host Port | Container Port | Protocol / Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Floci AWS API** | `vc-floci` | `4566` | `4566` | Emulated S3, SQS, IAM REST APIs |
| **Floci Web Console** | `floci-aws-ui` | `4500` | `4500` | On-demand Web Management UI |
| **SQL Server 2022** | `vc-database` | `1433` | `1433` | Microsoft SQL Server TDS Protocol |
| **Platform Backend** | `vc-platform-backend` | `8081` | `80` | Platform Admin Console & GraphQL APIs |
| **Storefront Host** | `vc-storefront-frontend` | `8090` | `80` | Headless Vue 3 B2B SPA & Reverse Proxy |

---

## 11. Resilience, Data Persistence & Fault Tolerance (Task 6)

1. **Volume Persistence Test:**
   ```bash
   docker compose restart vc-db
   docker compose ps
   ```
   Microsoft SQL Server container restarts and returns to healthy status while retaining all 39 database tables and 389 products via named Docker volume `vc-db-data`.
2. **Deliberate Outage & Recovery Test:**
   ```bash
   docker compose stop vc-db
   docker compose ps
   docker compose start vc-db
   docker compose ps
   ```
   Simulates infrastructure outage, validates service decoupling, and demonstrates automatic recovery upon restart.

---

## 12. Visual Verification: All 11 Milestone Screenshots

### Screenshot 1: Docker Containers Overview (`docker compose ps`)
![Containers Running](screenshots/1%20%E2%80%94%20Containers%20Running.png)
*Confirms all 4 core containers running healthy: `vc-floci` (port 4566), `vc-database` (port 1433), `vc-platform-backend` (port 8081), and `vc-storefront-frontend` (port 8090).*

---

### Screenshot 2A: Authentic Virto Commerce Password Reset Prompt
![Password Reset Screen](screenshots/2A%20%E2%80%94%20Password%20Reset%20Screen.png)
*Demonstrates the official ASP.NET Identity password reset flow on `http://localhost:8081` with `RequiredLength: 5`.*

---

### Screenshot 2B: Platform Admin Management Dashboard
![Platform Admin Dashboard](screenshots/2B%20%E2%80%94%20Platform%20Admin%20Dashboard.png)
*Shows the live administration console on port 8081 after completing the password reset.*

---

### Screenshot 2C: Platform Admin Installed Modules
![Platform Admin Modules](screenshots/2B%20%E2%80%94%20Platform%20Admin%20Modules.png)
*Validates pre-loaded modules in Platform Admin, confirming `VirtoCommerce.XFrontend` (v3.1009.0), `VirtoCommerce.WhiteLabeling`, and `VirtoCommerce.ImageTools` are active.*

---

### Screenshot 3: Official Sample Data Installation (SQL Server Verified)
![Sample Data Installed](screenshots/3%20%E2%80%94%20Sample%20Data%20Installed.png)
*Terminal output of `scripts/install-sample-data.sh` verifying 1 Store, 9 Catalogs, 123 Categories, and 389 Products.*

---

### Screenshot 5: Modern Decoupled B2B Storefront Homepage
![Storefront Homepage](screenshots/5%20%E2%80%94%20Storefront%20Homepage.png)
*Live customer storefront showing top navigation bar with **All products**, **Bolts**, Snacks, Soft Drinks, search bar, and cart.*

---

### Screenshot 6: All Products MegaMenu Navigation
![All Products MegaMenu](screenshots/6%20%E2%80%94%20All%20Products%20MegaMenu.png)
*Expanded MegaMenu dropdown showing real-time GraphQL hierarchy navigation across all imported categories.*

---

### Screenshot 7: Bolts Category View (`/bolts`)
![Bolts Category](screenshots/7%20%E2%80%94%20Bolts%20Category.png)
*Shows 34 products in the Bolts category, dynamic subcategory filtering (Carriage Bolts, Eyebolts, Flange Bolts), FABORY items, and prices.*

---

### Screenshot 8: Complete Full B2B Product Catalog (`/catalog`)
![Full B2B Catalog](screenshots/8%20%E2%80%94%20Full%20B2B%20Catalog.png)
*Catalog grid displaying 139 B2B items, price facet filtering, brand sorting, and pagination controls.*

---

### Screenshot 9: Terraform Infrastructure Provisioning Output
![Terraform Apply Output](screenshots/9%20%E2%80%94%20Terraform%20Apply%20Output.png)
*Terminal showing HashiCorp Terraform apply completing with `Resources: 5 added, 0 changed, 0 destroyed` against Floci.*

---

### Screenshot 10: Floci AWS CLI S3 & SQS Verification
![Floci AWS S3 and SQS Verification](screenshots/10%20%E2%80%94%20Floci%20AWS%20S3%20%26%20SQS%20Verification.png)
*Standard AWS CLI v2 listing active S3 bucket `virto-commerce-media-assets` and SQS queue URL `virto-order-processing-queue` on Floci.*

---

## 13. Troubleshooting & Solved Issues

1. **Port 4500 Collision with Floci UI Child Container:**  
   *Symptom:* `Bind for 0.0.0.0:4500 failed: port is already allocated`.  
   *Investigation:* Floci launches `floci-aws-ui:0.7.0` as an on-demand child container binding to host port 4500. Having `4500:4500` on the parent container blocked the child from starting.  
   *Resolution:* Removed static port 4500 from parent `vc-floci` in `docker-compose.yml`, leaving port 4500 completely free for the UI child container.
2. **Password Policy 8-Character Block:**  
   *Resolution:* Configured `"RequiredLength": 5` in `/opt/virtocommerce/platform/appsettings.json`, allowing the seed password `store` to be accepted naturally.
3. **Storefront Route Guard Redirect (`/change-password`):**  
   *Resolution:* Added automatic post-import reset in `scripts/install-sample-data.sh`: `SET QUOTED_IDENTIFIER ON; UPDATE AspNetUsers SET PasswordExpired = 0 WHERE UserName = 'admin'`, preventing demo dataset side-effects.

---

## 14. Official Technical References

1. **Virto Commerce Platform 3 Architecture:** [https://docs.virtocommerce.org/](https://docs.virtocommerce.org/)
2. **Virto Commerce Modern B2B Theme (Vue 3, Vite, Apollo):** [https://github.com/VirtoCommerce/vc-theme-b2b-vue](https://github.com/VirtoCommerce/vc-theme-b2b-vue)
3. **Virto Commerce Experience APIs (XFrontend):** [https://docs.virtocommerce.org/developer-guide/experience-api/](https://docs.virtocommerce.org/developer-guide/experience-api/)
4. **Virto Commerce Modular Extension Architecture:** [https://docs.virtocommerce.org/developer-guide/modules/](https://docs.virtocommerce.org/developer-guide/modules/)
5. **ASP.NET Core URL Rewriting (`IISUrlRewrite.xml`):** [https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting)
6. **Floci AWS Local Cloud Emulator:** [https://github.com/floci/floci](https://github.com/floci/floci)
7. **HashiCorp Terraform AWS Provider:** [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
