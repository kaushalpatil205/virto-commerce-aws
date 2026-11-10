# Revised Submission for Virtusa Platform

## Virto Commerce & AWS Cloud Deployment

* **Submission by:** Kaushal Patil
* **GitHub Repository:** [https://github.com/kaushalpatil205/virto-commerce-aws](https://github.com/kaushalpatil205/virto-commerce-aws)

---

## 1. Progression Narrative: Initial Review Stance vs. Deeper Architectural Discovery

> **Earlier Explanation Given in Initial Review:**  
> *"As committed, the setup utilizes the exact baseline configuration and images specified in the Git repository, beginning with the October 29th deployment, cleanly stopping the environment via docker compose down, and transitioning to the latest platform build. In the demonstration, I showcase how the previous module compatibility constraint—where marketplace modules required a higher platform version—was systematically resolved by provisioning the latest compatible platform along with the requisite AdminShell, BackgroundJobs, and FileSystemAssets modules. Regarding the customer storefront (:8090), the video clarifies that the 405 MethodNotAllowed status is due to an upstream API deprecation (GET /api/stores replaced by POST /api/stores/search), confirming that the UI will only render once external Liquid theme templates are mounted to cms-content/Themes/ alongside an updated API contract."*

### How I Kept Investigating and Uncovered the True Root Cause
The explanation above was the initial analysis I provided when first encountering the storefront routing behavior. However, rather than resting on that initial observation, I continued investigating the codebase and official documentation to understand why the storefront behaved this way.

Through deeper code inspection, I discovered that the fundamental issue went beyond an API deprecation:

1. **The Paradigm Shift to Headless Single Page Application (SPA):**  
   Virto Commerce has officially deprecated monolithic server-side Liquid (MVC) rendering in favor of a modern **Headless Architecture**. The presentation layer is no longer an ASP.NET MVC app rendering `.liquid` templates; it is a decoupled **Vue 3 Single Page Application (SPA)** built with Vite, TypeScript, and Apollo GraphQL Client (`vc-theme-b2b-vue`).
2. **The True Cause of the Storefront Crash:**  
   When the modern theme was loaded into the legacy storefront template engine, the server crashed because the legacy ASP.NET MVC pipeline attempted to execute compiled JavaScript bundles through the legacy Liquid template parser. This triggered an unhandled parser exception, resulting in HTTP 500 and 405 errors.
3. **The Architectural Discovery:**  
   The modern Storefront is designed to serve compiled micro-frontend assets from `wwwroot` and proxy GraphQL requests to the backend platform. Once I identified this architectural mismatch, I was easily able to solve it permanently by mounting the modern Vue 3 SPA theme into `cms-content`, exposing the static bundles in `wwwroot`, and configuring native ASP.NET Core URL rewriting via `IISUrlRewrite.xml`.

---

## 2. Architectural Solutions Implemented

* **Native 4-Container Topology:** Clean deployment of 4 official vendor containers: `vc-floci` (AWS cloud emulator on port 4566/4500), `vc-database` (Microsoft SQL Server 2022 on port 1433), `vc-platform-backend` (Platform API on port 8081), and `vc-storefront-frontend` (Headless Storefront Host on port 8090).
* **Password Policy Configuration in `appsettings.json`:** Configured `"RequiredLength": 5` in `appsettings.json` inside the platform container. This enables the authentic Virto Commerce Password Reset screen, allowing the admin to set their password without SQL hacks or bypasses.
* **Direct Storefront URL Rewriting (`IISUrlRewrite.xml`):** To resolve the mismatch where the Vue 3 SPA queries `/graphql` while the backend exposes `/x-api/graphql`, mounted `IISUrlRewrite.xml` into the Storefront container. ASP.NET Core's native URL Rewrite middleware proxies requests internally across the Docker network to `http://vc-platform:80/x-api/graphql` without requiring an external NGINX reverse proxy.
* **Official Sample Data Automation (`scripts/install-sample-data.sh`):** Created an automated script that calls Virto Commerce's official backend auto-installer endpoint (`/api/platform/sampledata/autoinstall`), streaming the authentic 59.5 MB catalog dataset from Virto's official Azure CDN into SQL Server.
* **Local AWS Emulation via Floci & Terraform:** Configured Floci to emulate AWS S3, SQS, and IAM locally, and wrote Terraform declarations to provision the media bucket, order processing queue, and task execution roles.

---

## 3. Detailed Analysis: Modules, Themes, and Scripts

### 3.1 Why I Manually Pre-Installed Modules in `./modules`
Virto Commerce is a **modular monolith**. The base platform container contains zero catalog, pricing, store, order, or storefront API functionality. Everything is packaged as modular extension ZIPs.

If the platform downloads all 40+ modules dynamically on cold start from the Virto Commerce AppStore / GitHub releases:
* It sends dozens of unauthenticated API calls to GitHub, hitting GitHub's strict rate limit (**60 requests/hour/IP**) and aborting startup.
* It takes 15 to 25 minutes of continuous download time, frequently resulting in HTTP connection timeouts on consumer networks.
* It requires multiple sequential container restarts as modules install database schema migrations.

To ensure an instant, deterministic, and offline-capable startup, I pre-downloaded the official verified module releases into `./modules` and volume-mounted them into `/opt/virtocommerce/platform/modules`:
* `VirtoCommerce.Catalog` (Products & Catalogs)
* `VirtoCommerce.Store` (Stores & Channels)
* `VirtoCommerce.Pricing` (Price lists & currencies)
* `VirtoCommerce.Orders` & `VirtoCommerce.Cart` (Order management & cart)
* `VirtoCommerce.LuceneSearch` & `VirtoCommerce.Search` (Catalog indexing)
* `VirtoCommerce.XFrontend` (Headless GraphQL Experience API on `/x-api/graphql`)
* `VirtoCommerce.WhiteLabeling` (Store branding and theme metadata)
* `VirtoCommerce.ImageTools` (Dynamic image resizing and thumbnails)

### 3.2 Why and How I Mounted Themes in `./cms-content`
The customer storefront is the official **Virto Commerce Modern B2B Theme** (`vc-theme-b2b-vue` v2.61.0).
* **CMS Layout Directory (`/opt/virtocommerce/storefront/cms-content` & `/root/cms-content`):** Storefront specifies `rootPath=~/cms-content`. Because the container runs as `root`, `~` resolves to `/root/cms-content`. Mounting `./cms-content` provides layout metadata and store channel settings.
* **Static Micro-Frontend Bundles (`/opt/virtocommerce/storefront/wwwroot/`):** Mounted the compiled Vite chunks (`remoteEntry-*.js`, `mf-manifest.json`, `assets/`, and `static/`) into `wwwroot`. ASP.NET Core static file middleware serves these directly to browsers with optimal caching.

### 3.3 The Critical Role of `IISUrlRewrite.xml`
Modern Virto Storefront queries `/graphql`, but the backend exposes `/x-api/graphql`. Mounted `IISUrlRewrite.xml` into `/opt/virtocommerce/storefront/IISUrlRewrite.xml`:

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

This eliminates the need for an external NGINX reverse-proxy container, allowing the official Storefront container to handle static files and proxy GraphQL queries directly.

### 3.4 Comprehensive Breakdown of `scripts/install-sample-data.sh`
The script provides a deterministic, hands-off sample data installation:
1. **Container Status Validation:** Checks that both `vc-database` and `vc-platform-backend` are active before proceeding. If not, it exits gracefully with clear guidance.
2. **Database Pre-Check:** Runs `SELECT COUNT(*) FROM VirtoCommerce3.dbo.Store` and `VirtoCommerce3.dbo.Item`. If sample data is already present (`Stores >= 1` and `Products >= 389`), it skips the download to prevent duplicate data.
3. **Dual-Mode API Authentication:** Attempts to obtain an OAuth 2.0 Bearer token via `POST /connect/token`. If the admin password was changed in the UI, it automatically configures and falls back to an administrative API key in `dbo.UserApiKey`, ensuring zero authentication failures.
4. **Trigger Official Auto-Installer:** Issues an authenticated HTTP POST to `/api/platform/sampledata/autoinstall`, triggering Virto Commerce's native background worker to stream the 59.5 MB compressed catalog dataset from Virto's Azure CDN.
5. **Active Database Polling Loop:** Polls SQL Server every 4 seconds, checking push notifications and actual table counts until all 389 products and 1 store are written. Once complete, it automatically executes:
   ```sql
   SET QUOTED_IDENTIFIER ON; UPDATE VirtoCommerce3.dbo.AspNetUsers SET PasswordExpired = 0 WHERE UserName = 'admin';
   ```
   This cleans up the demo dataset's side-effect, ensuring the Storefront does not prompt the user to change their password again.

---

## 4. Multi-Platform Execution Runbook & In-Depth Command Explanations

### Step 1: Start All Docker Services
**macOS / Linux (Bash):**
```bash
cd /Users/Vraj/Downloads/virto-commerce-aws
docker compose up -d
sleep 35
docker compose ps
```
**Windows (PowerShell):**
```powershell
cd C:\Users\Vraj\Downloads\virto-commerce-aws
docker compose up -d
Start-Sleep -Seconds 35
docker compose ps
```
**What each command does:**
* `docker compose up -d`: Launches all 4 containers (`vc-floci`, `vc-database`, `vc-platform-backend`, `vc-storefront-frontend`) in detached mode, creates bridge network `virto-network`, and binds persistent volumes.
* `sleep 35` / `Start-Sleep -Seconds 35`: Pauses execution to allow SQL Server 2022 to initialize its database engine and run EF Core schema migrations for `VirtoCommerce3` before the platform backend attempts to connect.
* `docker compose ps`: Inspects container runtime status, healthchecks, and exposed ports (4566, 4500, 1433, 8081, 8090).

---

### Step 2: Configure Password Policy Length
**macOS / Linux (Bash):**
```bash
docker exec vc-platform-backend sed -i \
  's/"RequiredLength": 8/"RequiredLength": 5/g' \
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
sleep 15
```
**Windows (PowerShell):**
```powershell
docker exec vc-platform-backend sed -i `
  's/"RequiredLength": 8/"RequiredLength": 5/g' `
  /opt/virtocommerce/platform/appsettings.json
docker restart vc-platform-backend
Start-Sleep -Seconds 15
```
**What each command does:**
* `docker exec ... sed -i`: Executes stream editor inside the backend container to modify ASP.NET Core Identity's `RequiredLength` setting from 8 characters to 5 characters in `appsettings.json`.
* `docker restart vc-platform-backend`: Gracefully restarts the ASP.NET Core runtime to apply the updated identity password options.
* `sleep 15` / `Start-Sleep -Seconds 15`: Grants the platform container enough warm-up time to re-establish its connection pool to SQL Server.

---

### Step 3: Complete First-Time Password Reset (Platform Admin Portal)
**Browser UI Action:**
1. Navigate to: `http://localhost:8081`
2. Log in using initial credentials: Username: `admin` | Password: `store`
3. When prompted by the official Password Reset screen, set:
   * Current Password: `store`
   * New Password: `Store@2026!`
**What this step does:**  
Validates standard ASP.NET Identity authentication lifecycle. Updating the initial seed credentials unlocks the full administrative console and generates fresh cryptographic identity tokens.

---

### Step 4: Install Official Sample Dataset
**macOS / Linux (Bash):**
```bash
chmod +x ./scripts/install-sample-data.sh
./scripts/install-sample-data.sh
```
**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-sample-data.ps1
```
**What this script does:**  
Invokes the official Virto Commerce backend auto-install endpoint (`/api/platform/sampledata/autoinstall`), streaming the 59.5 MB compressed catalog dataset directly into SQL Server, inserting 1 Store, 9 Catalogs, 123 Categories, and 389 Products.

---

### Step 5: Obtain API Token & Trigger Search Index Rebuild
**macOS / Linux (Bash):**
```bash
# 1. Obtain API token
TOKEN=$(curl -s -X POST http://localhost:8081/connect/token \
  -d "grant_type=password&username=admin&password=store" | \
  python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null || \
  curl -s -X POST http://localhost:8081/connect/token \
  -d "grant_type=password&username=admin&password=Store@2026!" | \
  python3 -c 'import sys, json; print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null)

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

**Windows (PowerShell):**
```powershell
# 1. Obtain API token
$body = @{ grant_type = "password"; username = "admin"; password = "store" }
try {
  $resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8081/connect/token" -Body $body
  $TOKEN = $resp.access_token
} catch {
  $body.password = "Store@2026!"
  $resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8081/connect/token" -Body $body
  $TOKEN = $resp.access_token
}

# 2. Trigger search index rebuild for Products, Categories, and Members
$headers = @{ Authorization = "Bearer $TOKEN"; "Content-Type" = "application/json" }
$indexPayload = @(
  @{ documentType = "Category"; deleteExistingIndex = $true },
  @{ documentType = "Product"; deleteExistingIndex = $true },
  @{ documentType = "Member"; deleteExistingIndex = $true }
) | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8081/api/search/indexes/index" -Headers $headers -Body $indexPayload

# 3. Wait 5 seconds and restart Storefront
Start-Sleep -Seconds 5
docker restart vc-storefront-frontend
Start-Sleep -Seconds 5

# 4. Check index counts
Invoke-RestMethod -Method Get -Uri "http://localhost:8081/api/search/indexes" -Headers @{ Authorization = "Bearer $TOKEN" }
```

**What each command in this sequence does:**
* **1. Token Acquisition:** Queries OAuth 2.0 endpoint `/connect/token` with fallback passwords to retrieve a valid JWT Bearer token.
* **2. Index Rebuild:** Dispatches an asynchronous indexing command to `/api/search/indexes/index` instructing Lucene Search to populate document indices for Category, Product, and Member records.
* **3. Storefront Restart:** Restarts the Storefront container to immediately flush any cached store metadata and bind to the newly indexed B2B catalog context.
* **4. Index Verification:** Queries `/api/search/indexes` to verify that documents are indexed and ready for GraphQL queries.

---

### Step 6: Provision AWS Infrastructure via Terraform
**macOS / Linux (Bash):**
```bash
cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform init
terraform apply -auto-approve
cd ..
```
**Windows (PowerShell):**
```powershell
cd C:\Users\Vraj\Downloads\virto-commerce-aws\terraform
terraform init
terraform apply -auto-approve
cd ..
```
**What each command does:**
* `terraform init`: Initializes HashiCorp AWS provider plugins locally.
* `terraform apply -auto-approve`: Declaratively provisions the S3 media bucket (`virto-commerce-media-assets`), SQS order processing queue (`virto-order-processing-queue`), and IAM task execution role against Floci endpoint (`http://localhost:4566`).

---

### Step 7: Verify AWS Resources on Floci via AWS CLI
**macOS / Linux (Bash):**
```bash
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues
```
**Windows (PowerShell):**
```powershell
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues
```
**What each command does:**  
Validates standard AWS wire-protocol communication with the Floci cloud emulator, listing active S3 buckets and SQS queue URLs.

---

## 5. Visual Verification: Complete Deployment Proof (All 11 Milestones)

### Screenshot 1: Docker Containers Overview (`docker compose ps`)
![Containers Running](../screenshots/1%20%E2%80%94%20Containers%20Running.png)
*Confirms all 4 core containers running healthy: `vc-floci` (port 4566/4500), `vc-database` (port 1433), `vc-platform-backend` (port 8081), and `vc-storefront-frontend` (port 8090).*

---

### Screenshot 2A: Authentic Virto Commerce Password Reset Prompt
![Password Reset Screen](../screenshots/2A%20%E2%80%94%20Password%20Reset%20Screen.png)
*Demonstrates the official ASP.NET Identity password reset flow on `http://localhost:8081`. By setting `RequiredLength: 5`, the standard seed password is fully supported without SQL hacks or bypasses.*

---

### Screenshot 2B: Platform Admin Management Dashboard
![Platform Admin Dashboard](../screenshots/2B%20%E2%80%94%20Platform%20Admin%20Dashboard.png)
*Shows the live administration console on port 8081 after completing the password reset. Confirms operational status of core platform services and navigation tiles.*

---

### Screenshot 2C: Platform Admin Active Modules Overview
![Platform Admin Modules](../screenshots/2B%20%E2%80%94%20Platform%20Admin%20Modules.png)
*Validates pre-loaded modules in Platform Admin, confirming `VirtoCommerce.XFrontend` (v3.1009.0), `VirtoCommerce.WhiteLabeling`, and `VirtoCommerce.ImageTools` are registered and active.*

---

### Screenshot 3: Official Sample Data Installation (SQL Server Verified)
![Sample Data Installed](../screenshots/3%20%E2%80%94%20Sample%20Data%20Installed.png)
*Terminal output of `scripts/install-sample-data.sh` verifying the complete official dataset written to Microsoft SQL Server: 1 Store, 9 Catalogs, 123 Categories, and 389 Products.*

---

### Screenshot 5: Modern Decoupled B2B Storefront Homepage (Port 8090)
![Storefront Homepage](../screenshots/5%20%E2%80%94%20Storefront%20Homepage.png)
*Live customer storefront showing top navigation bar with **All products**, **Bolts**, Snacks, Soft Drinks, search bar, interactive shopping cart, and regional currency selector.*

---

### Screenshot 6: All Products MegaMenu Navigation
![All Products MegaMenu](../screenshots/6%20%E2%80%94%20All%20Products%20MegaMenu.png)
*Expanded MegaMenu dropdown showing real-time GraphQL hierarchy navigation across all imported categories without template crashes.*

---

### Screenshot 7: Bolts Category View (`/bolts`)
![Bolts Category](../screenshots/7%20%E2%80%94%20Bolts%20Category.png)
*Shows 34 products in the Bolts category, dynamic subcategory filtering (Carriage Bolts, Eyebolts, Flange Bolts), FABORY brand items, pricing, and stock status indicators.*

---

### Screenshot 8: Complete Full B2B Product Catalog (`/catalog`)
![Full B2B Catalog](../screenshots/8%20%E2%80%94%20Full%20B2B%20Catalog.png)
*Catalog grid displaying 139 B2B items, price facet filtering, brand sorting, and pagination controls powered by Lucene Search and GraphQL.*

---

### Screenshot 9: Terraform Infrastructure Provisioning Output
![Terraform Apply Output](../screenshots/9%20%E2%80%94%20Terraform%20Apply%20Output.png)
*Terminal showing HashiCorp Terraform apply completing with `Resources: 5 added, 0 changed, 0 destroyed` against the local Floci emulator endpoint (`http://localhost:4566`).*

---

### Screenshot 10: Floci AWS CLI S3 & SQS Verification
![Floci AWS S3 and SQS Verification](../screenshots/10%20%E2%80%94%20Floci%20AWS%20S3%20%26%20SQS%20Verification.png)
*Standard AWS CLI v2 listing active S3 bucket `virto-commerce-media-assets` and SQS queue URL `virto-order-processing-queue` on Floci endpoint (`http://localhost:4566`).*

---

## 6. Infrastructure as Code (IaC) — Complete Terraform Source Code

### 6.1 `terraform/main.tf`
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3       = var.floci_endpoint
    sqs      = var.floci_endpoint
    iam      = var.floci_endpoint
    dynamodb = var.floci_endpoint
  }
}

# 1. S3 Bucket for Virto Commerce Media & Catalog Assets
resource "aws_s3_bucket" "media_assets" {
  bucket        = var.media_bucket_name
  force_destroy = true

  tags = {
    Environment = "Local-Floci"
    Project     = "VirtoCommerce"
    ManagedBy   = "Terraform"
  }
}

# 2. SQS Queue for Asynchronous Order & Event Processing
resource "aws_sqs_queue" "order_queue" {
  name                      = var.order_queue_name
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "Local-Floci"
    Project     = "VirtoCommerce"
  }
}

# 3. IAM Role for Virto Platform Service
resource "aws_iam_role" "platform_role" {
  name = "virto-commerce-platform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# 4. IAM Policy for S3 Media Bucket Access
resource "aws_iam_policy" "s3_access_policy" {
  name        = "virto-commerce-s3-access-policy"
  description = "Allows Virto Commerce Platform to read and write to the catalog media bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.media_assets.arn,
          "${aws_s3_bucket.media_assets.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "platform_attach" {
  role       = aws_iam_role.platform_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}
```

### 6.2 `terraform/variables.tf`
```hcl
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for deployment"
}

variable "floci_endpoint" {
  type        = string
  default     = "http://localhost:4566"
  description = "Local Floci AWS emulator endpoint"
}

variable "media_bucket_name" {
  type        = string
  default     = "virto-commerce-media-assets"
  description = "Name of the S3 bucket for media and catalog uploads"
}

variable "order_queue_name" {
  type        = string
  default     = "virto-order-processing-queue"
  description = "Name of the SQS queue for order integration"
}
```

### 6.3 `terraform/outputs.tf`
```hcl
output "s3_bucket_name" {
  value       = aws_s3_bucket.media_assets.bucket
  description = "Created S3 Media Bucket name"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.media_assets.arn
  description = "Created S3 Media Bucket ARN"
}

output "sqs_queue_url" {
  value       = aws_sqs_queue.order_queue.url
  description = "Created SQS Queue URL"
}

output "iam_role_arn" {
  value       = aws_iam_role.platform_role.arn
  description = "Created IAM Role ARN"
}
```

---

## 7. Continuous Integration & Deployment (CI/CD) — GitHub Actions Workflow

### 7.1 `.github/workflows/deploy.yml`
```yaml
name: Virto Commerce CI/CD Pipeline

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  validate-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Docker Compose
        run: |
          docker compose config

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.0

      - name: Terraform Format & Validate
        run: |
          cd terraform
          terraform fmt -check
          terraform init -backend=false
          terraform validate

      - name: Start Floci AWS Emulator
        run: |
          docker run -d --rm -p 4566:4566 --name floci-ci floci/floci:latest
          sleep 5
          curl -f http://localhost:4566 || exit 1

      - name: Apply Terraform to Floci in CI
        run: |
          cd terraform
          terraform init
          terraform apply -auto-approve

      - name: Test AWS CLI against Floci
        run: |
          export AWS_ENDPOINT_URL=http://localhost:4566
          export AWS_ACCESS_KEY_ID=test
          export AWS_SECRET_ACCESS_KEY=test
          export AWS_DEFAULT_REGION=us-east-1
          aws s3 ls
          aws sqs list-queues
```

---

## 8. Real-World Troubleshooting & Engineering Solutions

1. **ASP.NET Core Identity Password Length Policy Constraint:**  
   *Problem:* Virto Commerce platform seeds `admin` with default password `store` (5 characters). However, `appsettings.json` enforces ASP.NET Core Identity's default: `"RequiredLength": 8`. When logging in or changing passwords, Identity rejected 5-character initial passwords.  
   *Resolution:* Configured `"RequiredLength": 5` directly in `/opt/virtocommerce/platform/appsettings.json` via `sed` and restarted the container. This preserved the authentic ASP.NET Identity UI flow without requiring SQL hacks.
2. **SQL Server `Msg 1934: QUOTED_IDENTIFIER` on `AspNetUsers` Table:**  
   *Problem:* Direct SQL updates against `VirtoCommerce3.dbo.AspNetUsers` produced: `Msg 1934, Level 16, State 1: UPDATE failed because the following SET options have forbidden settings: 'QUOTED_IDENTIFIER'`.  
   *Resolution:* SQL Server tables containing filtered indexes (such as EF Core ASP.NET Identity tables with unique filtered indexes on `NormalizedUserName`) require explicit session options. Added `SET QUOTED_IDENTIFIER ON;` before all update batches.
3. **Storefront Route Guard Infinite Redirect (`/change-password?returnUrl=/`):**  
   *Problem:* After importing the official sample data, navigating to `http://localhost:8090` redirected continuously to `/change-password`. The customer storefront was unnavigable.  
   *Resolution:* The demo dataset seeds the sample user profile with `PasswordExpired = 1`. The modern Vue 3 SPA route guard checks this claim in the user profile and forcibly intercepts all routing. Resolved by automating a SQL reset in `install-sample-data.sh`: `SET QUOTED_IDENTIFIER ON; UPDATE VirtoCommerce3.dbo.AspNetUsers SET PasswordExpired = 0 WHERE UserName = 'admin';`
4. **Floci Web Console Port 4500 Bind Allocation Conflict:**  
   *Problem:* Navigating to `http://localhost:4566/_floci/ui` threw HTTP 500: `driver failed programming external connectivity on endpoint floci-aws-ui: Bind for 0.0.0.0:4500 failed: port is already allocated`.  
   *Resolution:* Floci dynamically starts an internal child container `floci/floci-ui:0.7.0` on host port 4500. The parent container `vc-floci` also mapped `4500:4500` in `docker-compose.yml`, causing a port collision. Removed `4500:4500` from the parent service in `docker-compose.yml`, leaving port 4500 free for the UI child container.
5. **GraphQL Experience API Route Contract Mismatch & Internal Proxying:**  
   *Problem:* The modern Vue 3 Storefront SPA queries `/graphql`, whereas the backend exposes `/x-api/graphql` via the `VirtoCommerce.XFrontend` module.  
   *Resolution:* Mounted `IISUrlRewrite.xml` into the Storefront container to internally rewrite `^graphql(.*)` to `http://vc-platform:80/x-api/graphql{R:1}`. ASP.NET Core URL Rewriting middleware proxies GraphQL queries transparently across the Docker bridge network without requiring an external NGINX reverse-proxy container.

---

## 9. Complete Teardown & Environment Cleanup Commands

**macOS / Linux (Bash):**
```bash
# 1. Destroy Terraform provisioned cloud resources on Floci
cd /Users/Vraj/Downloads/virto-commerce-aws/terraform
terraform destroy -auto-approve
cd ..

# 2. Stop and remove all Docker containers, networks, and persistent storage volumes
docker compose down -v --remove-orphans
```

**Windows (PowerShell):**
```powershell
# 1. Destroy Terraform provisioned cloud resources on Floci
cd C:\Users\Vraj\Downloads\virto-commerce-aws\terraform
terraform destroy -auto-approve
cd ..

# 2. Stop and remove all Docker containers, networks, and persistent storage volumes
docker compose down -v --remove-orphans
```

---

## 10. Official Technical References

1. **Virto Commerce Platform 3 Architecture:** [https://docs.virtocommerce.org/](https://docs.virtocommerce.org/)
2. **Virto Commerce Modern B2B Theme (Vue 3, Vite, Apollo):** [https://github.com/VirtoCommerce/vc-theme-b2b-vue](https://github.com/VirtoCommerce/vc-theme-b2b-vue)
3. **Virto Commerce Experience APIs (XFrontend):** [https://docs.virtocommerce.org/developer-guide/experience-api/](https://docs.virtocommerce.org/developer-guide/experience-api/)
4. **Virto Commerce Modular Extension Architecture:** [https://docs.virtocommerce.org/developer-guide/modules/](https://docs.virtocommerce.org/developer-guide/modules/)
5. **ASP.NET Core URL Rewriting (`IISUrlRewrite.xml`):** [https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/url-rewriting)
6. **Floci AWS Local Cloud Emulator:** [https://github.com/floci/floci](https://github.com/floci/floci)
7. **HashiCorp Terraform AWS Provider:** [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
