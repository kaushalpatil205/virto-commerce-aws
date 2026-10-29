# Virto Commerce Platform & Storefront Deployment
## Final Technical Presentation & Project Walkthrough (Task 8)



---

## 1. Project Overview

* **Objective:**
  * Design, containerize, and deploy a multi-tier, production-ready Virto Commerce Platform and Storefront system.
  * Integrate offline, zero-cost AWS cloud infrastructure emulation using the **Floci** AWS local emulator.
  * Automate cloud provisioning using **HashiCorp Terraform** and container deployment via **Docker Compose**.
* **Key Achievements:**
  * Deployed full container stack: Backend Platform API, Customer Storefront, and Microsoft SQL Server 2022.
  * Provisioned local AWS cloud resources (S3 Media Bucket, SQS Order Queue, IAM Execution Role) via Terraform.
  * Demonstrated data persistence across database restarts and automated recovery from safe simulated outages.
  * Documented complete 16-point deployment runbook, uncropped visual proof, and real-world troubleshooting case studies.

---

## 2. Business Needs

* **Headless Architecture Requirements:**
  * Complete decoupling of the customer-facing storefront from the backend administrative engine.
  * Independent scaling: Storefront traffic spikes (sales events, marketing campaigns) scale horizontally without straining the core catalog/order database.
* **Cost & Environment Efficiency:**
  * Eliminate high cloud infrastructure testing bills during early-stage development and CI/CD pipelines.
  * Enable 100% offline development capability without requiring live AWS accounts, billing tokens, or cloud permissions.
* **High Availability & Fault Tolerance:**
  * Zero single point of failure in production design.
  * Automated recovery and reliable data persistence for enterprise transactional workloads.

---

## 3. Technology Stack & Justification

* **Virto Commerce Platform (Backend):**
  * Modular, enterprise-grade e-commerce engine built on ASP.NET Core 8 (.NET).
  * Exposes RESTful and GraphQL APIs for catalog management, pricing, customer identity, and checkout.
* **Virto Commerce Storefront (Frontend):**
  * Modern, responsive web frontend consuming the Platform’s backend APIs over HTTP.
* **Microsoft SQL Server 2022 (Database):**
  * Enterprise relational database engine supporting Virto Commerce Entity Framework Core automatic schema migrations.
* **Floci AWS Local Emulator (Cloud Infrastructure):**
  * Quarkus Native AWS emulator with millisecond startup (~24ms) and negligible memory footprint (~13MB).
  * 100% standard AWS wire-protocol compatibility for Amazon S3, Amazon SQS, and Amazon IAM.
  * Provides built-in web console for visual resource inspection on port 4500.
* **HashiCorp Terraform (Infrastructure as Code):**
  * Declarative cloud infrastructure provisioning using standard AWS Provider v5.x.
* **Docker Compose (Container Orchestration):**
  * Multi-container lifecycle management, custom isolated bridge networking, and persistent storage volumes.

---

## 4. System Architecture

### Local Development Architecture (Docker + Floci):
* **Container Bridge Network (`virto-network`):**
  * `vc-storefront` (`http://localhost:8090`) &rarr; communicates over internal network with `vc-platform`.
  * `vc-platform` (`http://localhost:8081`) &rarr; executes queries on `vc-database` (port 1433).
  * `vc-platform` &rarr; stores catalog media in Floci S3 (`virto-commerce-media-assets`).
  * `vc-platform` &rarr; dispatches order events to Floci SQS (`virto-order-processing-queue`).
  * `floci-ui` (`http://localhost:4500`) &rarr; queries Floci runtime on port 4566.
* **Persistent Host Storage:**
  * Named volume `vc-db-data` mounted at `/var/opt/mssql`.
  * Named volume `vc-platform-data` mounted at `/app/App_Data`.
  * Named volume `vc-storefront-data` mounted at `/app/cms-content`.

### Target Production AWS Architecture:
* **Ingress & Edge:** Amazon CloudFront (CDN) + Application Load Balancer (ALB) with ACM TLS 1.3 certificates.
* **Compute Layer:** AWS ECS Fargate running Platform API and Storefront containers across multiple Availability Zones.
* **Database Layer:** Amazon RDS for SQL Server Standard / Aurora Multi-AZ with automated daily snapshots.
* **Caching Layer:** Amazon ElastiCache Redis Cluster for high-speed catalog and session caching.
* **Storage & Queuing:** Amazon S3 (Production Media Assets) + Amazon SQS (Asynchronous Order Queue).
* **Security & Observability:** AWS Secrets Manager for automated secret rotation, IAM Task Execution Roles, and Amazon CloudWatch for metrics and alerting.

---

## 5. Container Orchestration & Deployment

* **Service Coordination & Dependencies:**
  * `vc-platform` startup is strictly guarded by `depends_on: { vc-db: { condition: service_healthy } }`.
  * Eliminates database race conditions by polling SQL Server with `/opt/mssql-tools/bin/sqlcmd` before starting the .NET runtime.
* **Port Mapping Strategy:**
  * Database: Host port `1433` &rarr; Container port `1433`.
  * Platform Backend: Host port `8081` &rarr; Container port `80` (avoids host port 8080 collision).
  * Storefront Frontend: Host port `8090` &rarr; Container port `80`.
  * Floci AWS Runtime: Host port `4566` &rarr; Container port `4566`.
  * Floci Web Console: Host port `4500` &rarr; Container port `4500`.
* **Automated DNS Resolution:**
  * Configured dual network aliases (`vc-platform` and `vc-platform-backend`) on the bridge network to ensure seamless internal routing.

---

## 6. Infrastructure as Code (Terraform on Floci)

* **Declarative Provider Configuration:**
  * Configured standard HashiCorp AWS provider with custom endpoint overrides pointing to `http://localhost:4566`.
  * Enabled `s3_use_path_style = true` and `skip_credentials_validation = true` for local emulation compatibility.
* **Provisioned Cloud Resources:**
  1. `aws_s3_bucket.media_assets`:
     * Bucket Name: `virto-commerce-media-assets`
     * Purpose: High-durability object storage for catalog images, banners, and digital assets.
  2. `aws_sqs_queue.order_queue`:
     * Queue Name: `virto-order-processing-queue`
     * Purpose: Decouples checkout from order fulfillment; absorbs peak transaction spikes.
  3. `aws_iam_role.platform_role` & `aws_iam_policy.s3_access_policy`:
     * Implements least-privilege security by scoping access strictly to the media bucket ARN.

---

## 7. Application Walkthrough & Endpoint Validation

* **1. Virto Commerce Platform Manager (`http://localhost:8081/#!/login`):**
  * Accessible via web browser.
  * Confirms backend API is up and Entity Framework database migrations successfully seeded 40+ database tables.
* **2. Virto Commerce Storefront (`http://localhost:8090`):**
  * Accessible via web browser.
  * Validates cross-container HTTP communication: Storefront invokes `StoreModuleApi.GetStoresWithHttpMessagesAsync` against Platform on port 80.
  * Returns expected `NotFound` status code due to freshly initialized, unseeded catalog database.
* **3. Floci Web Console (`http://localhost:4500`):**
  * Displays visual confirmation of provisioned S3 buckets and SQS queues.
* **4. AWS CLI Verification:**
  * Command: `aws s3 ls --endpoint-url http://localhost:4566`
  * Confirms active bucket: `virto-commerce-media-assets`.

---

## 8. Resilience, Data Persistence & Fault Tolerance (Task 6)

* **Database Restart Persistence Test:**
  * Command: `docker compose restart vc-db ; docker compose ps`
  * Result: SQL Server restarted and successfully remounted the existing `vc-db-data` volume.
  * Verification: No schema wipe, no migration errors; Platform reconnected immediately.
* **Deliberate Outage & Safe Recovery Test:**
  * Command: `docker compose stop vc-db ; docker compose ps ; docker compose start vc-db ; docker compose ps`
  * Result: Simulated an unexpected infrastructure crash.
  * Verification: Application gracefully handled disconnection; upon container restart, services re-established database connectivity automatically.
* **S3 Asset Persistence Verification:**
  * Streamed test file `test_asset.txt` into `s3://virto-commerce-media-assets/`.
  * Verified file retention after multiple container restart cycles.

---

## 9. Real-World Engineering Troubleshooting

* **Issue 1: Host Port 8080 Contention**
  * *Root Cause:* Pre-existing `floci-lab` container was already bound to host port 8080.
  * *Resolution:* Re-mapped `vc-platform` to host port `8081:80` in `docker-compose.yml`.
* **Issue 2: Inter-Container DNS Routing Mismatch**
  * *Root Cause:* Storefront failed with `HttpRequestException: Name or service not known (vc-platform:80)` due to naming differences between service name and container name.
  * *Resolution:* Added network aliases in Docker Compose (`vc-platform`, `vc-platform-backend`) ensuring resolution across all formats.
* **Issue 3: Storefront `NotFound` Status Code on Fresh Boot**
  * *Root Cause:* Storefront called `GetStoresWithHttpMessagesAsync` and received HTTP 404 because an unseeded database contains no default store record.
  * *Resolution:* Verified as proof of working API connectivity; managed via Platform Manager on port 8081.
* **Issue 4: AWS CLI `NoCredentials` Error**
  * *Root Cause:* AWS CLI v2 requires non-empty credential strings to construct authorization headers, even on mock emulators.
  * *Resolution:* Configured dummy credentials via `aws configure set aws_access_key_id test`.
* **Issue 5: Floci Web Console `SocketException`**
  * *Root Cause:* Floci UI runs as an on-demand child container requiring host Docker daemon communication.
  * *Resolution:* Mounted the host engine socket/named pipe into the Floci container.

---

## 10. Security & Operational Governance

* **Zero Hardcoded Secrets:**
  * All credentials, database passwords, and configuration keys externalized into `.env`.
  * Committed a sanitized `.env.example` template; `.env` added to `.gitignore`.
* **Least-Privilege IAM Design:**
  * S3 access policy strictly restricts actions (`s3:GetObject`, `s3:PutObject`, `s3:ListBucket`) to `arn:aws:s3:::virto-commerce-media-assets/*`.
* **Network Isolation:**
  * SQL Server database communicates strictly over internal bridge network with no unnecessary exposed management ports.
* **Production Security Enhancements:**
  * Ingress TLS 1.3 terminated at AWS ALB.
  * Secrets managed and auto-rotated with AWS Secrets Manager.
  * Containers run as unprivileged users (`non-root`).

---

## 11. Production AWS Migration & Cost Model

* **Estimated Production Monthly Operating Cost:**

| AWS Component | Target Production Specification | Monthly Estimate |
| :--- | :--- | :--- |
| **Compute Tier** | 2x ECS Fargate Tasks (2 vCPU, 4GB RAM) with Auto Scaling | ~$110.00 |
| **Database Tier** | Amazon RDS SQL Server Standard (db.m5.large, Multi-AZ) | ~$320.00 |
| **Caching Tier** | Amazon ElastiCache Redis Cluster (cache.t4g.medium) | ~$45.00 |
| **Networking** | Application Load Balancer (ALB) + Multi-AZ NAT Gateways | ~$22.00 |
| **Storage & CDN** | Amazon S3 (100GB) + Amazon CloudFront CDN | ~$15.00 |
| **Total Cost** | **High-Availability Production Multi-AZ Architecture** | **~$512.00 / month** |

* **Cost Optimization Strategy:**
  * Utilize AWS Savings Plans / Reserved Instances for baseline RDS instances (saves up to 35%).
  * Implement S3 Intelligent-Tiering for older catalog media and invoice records.

---

## 12. Deployment Automation, CI/CD & Teardown

* **Automated Deployment Sequence:**
  ```powershell
  # 1. Start application containers
  docker compose up -d

  # 2. Provision AWS infrastructure on Floci via Terraform
  cd terraform ; terraform init ; terraform apply -auto-approve ; cd ..

  # 3. Validate endpoints & health
  .\scripts\validate.ps1
  ```
* **CI/CD Pipeline (`.github/workflows/deploy.yml`):**
  * Automated validation on every push: validates Compose configuration, checks Terraform formatting, and provisions against Floci in GitHub Actions runners.
* **Complete Teardown & Deletion Sequence (Evaluator Demo):**
  ```powershell
  # 1. Destroy Terraform provisioned cloud resources
  cd terraform ; terraform destroy -auto-approve ; cd ..

  # 2. Stop and remove all containers, networks, and persistent data volumes
  docker compose down -v --remove-orphans
  ```

---

## 13. Conclusion & Acceptance Criteria Verification

* ✅ **Platform & Storefront:** Running, healthy, and communicating over internal Docker network.
* ✅ **AWS Infrastructure:** S3 bucket, SQS queue, and IAM policies provisioned on Floci via Terraform.
* ✅ **Resilience Tested:** Relational database persistence and safe outage recovery verified.
* ✅ **Documentation & Proof:** 16-point README runbook, 8 uncropped screenshots, and formal submission PDF generated.
* ✅ **Live Repository:** [https://github.com/kaushalpatil205/virto-commerce-aws](https://github.com/kaushalpatil205/virto-commerce-aws)
