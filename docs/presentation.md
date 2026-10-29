# Virto Commerce Platform & Storefront Deployment
## Final Engineering Presentation & Demonstration Deck (Task 8)

**Candidate Name:** Kaushal Patil  
**Role:** AWS DevOps Engineer  
**Target Duration:** 10–15 Minutes  
**Live Repository:** [https://github.com/kaushalpatil205/virto-commerce-aws](https://github.com/kaushalpatil205/virto-commerce-aws)

---

## Slide 1: Title Slide & Project Overview

### Slide Content:
* **Project:** Production-Ready Containerization & AWS Emulation of Virto Commerce
* **Candidate:** Kaushal Patil
* **Role:** AWS DevOps Engineer
* **Core Technology Stack:**
  * Application: Virto Commerce Platform (Backend API) & Storefront (Customer UI)
  * Database: Microsoft SQL Server 2022 Express / Linux
  * Cloud Infrastructure: Floci AWS Local Cloud Emulator (S3, SQS, IAM)
  * Orchestration & IaC: Docker Compose & HashiCorp Terraform

> ### 🎙️ Presenter Script (What to Say):
> *"Good morning / afternoon everyone. My name is Kaushal Patil, and today I am presenting the architecture, deployment, and cloud automation for the Virto Commerce Platform and Storefront.*
>
> *The objective of this project was to design, containerize, and demonstrate a production-grade deployment of a decoupled e-commerce system using AWS-compatible infrastructure. Rather than incurring unnecessary cloud costs during development and automated testing, I leveraged Floci—an open-source, lightweight AWS emulator—and provisioned all required cloud resources declaratively using HashiCorp Terraform.*
>
> *Over the next 12 minutes, I will walk you through the architectural design, container orchestration, IaC implementation, live demonstrations, real-world troubleshooting, and the target production migration roadmap on AWS."*

---

## Slide 2: Business Need & Technology Choices

### Slide Content:
* **Why Headless Commerce?**
  * Decouples the backend transactional core from frontend presentation.
  * Allows independent scaling of high-traffic storefronts without impacting heavy catalog management APIs.
* **Why Virto Commerce?**
  * Modern, modular enterprise commerce framework built on ASP.NET Core 8 (.NET).
  * Native microservice-ready architecture supporting pluggable asset storage and message queues.
* **Why Microsoft SQL Server 2022?**
  * Supported enterprise relational database engine for Virto Commerce v3 schema and Entity Framework Core migrations.
* **Why Floci AWS Emulator?**
  * Ultra-fast native startup (~24ms) and tiny memory footprint (~13MB idle).
  * 100% wire-protocol compatibility with standard AWS CLI v2 and Terraform AWS provider.
  * Eliminates cloud charges and security blast radiuses during local CI/CD testing.

> ### 🎙️ Presenter Script (What to Say):
> *"To understand our design, we first look at the business requirement. Modern e-commerce demands a headless architecture where the customer-facing storefront can scale independently from backend administrative workloads.*
>
> *We selected Virto Commerce because it is built on ASP.NET Core 8, providing modularity and high performance. For structured transactional persistence, we deployed Microsoft SQL Server 2022.*
>
> *A key highlight of this project is our cloud emulation strategy: instead of running tests against real AWS accounts with active billing meters, we used Floci. Floci implements AWS's actual wire protocol, meaning our standard AWS CLI commands, Boto3 SDK clients, and Terraform scripts interact with it identically to real AWS without any code modifications."*

---

## Slide 3: Architecture Overview (Local vs. Production AWS)

### Slide Content:

#### 1. Local Emulation Architecture (Docker + Floci):
```text
[ Browser / Engineer ]
         │
         ├───► Storefront (Port 8090) ──(REST/GraphQL)──► Platform API (Port 8081)
         │                                                      │
         │                                                      ├──► SQL Server 2022 (Port 1433)
         │                                                      ├──► Floci AWS S3 (Media Bucket)
         │                                                      └──► Floci AWS SQS (Order Queue)
         │
         └───► Floci Web Console (Port 4500) ──► Floci Runtime (Port 4566)
```

#### 2. Target Production AWS Architecture:
* **Edge & Ingress:** Amazon CloudFront CDN + Application Load Balancer (ALB) with ACM TLS 1.3 termination.
* **Compute:** AWS ECS Fargate running Platform and Storefront tasks across multiple Availability Zones.
* **Database & Cache:** Amazon RDS for SQL Server (Multi-AZ) + Amazon ElastiCache Redis cluster.
* **Storage & Messaging:** Amazon S3 (Media & Catalog assets) + Amazon SQS (Asynchronous order processing queue).
* **Security & Observability:** AWS Secrets Manager, IAM Task Execution Roles, and CloudWatch Alarms.

> ### 🎙️ Presenter Script (What to Say):
> *"Here you can see the side-by-side architectural comparison. On the left is our local deployment environment. All components run within an isolated Docker bridge network called `virto-network`. The Storefront on port 8090 communicates with the Platform backend on port 8081 over HTTP. The Platform connects to SQL Server for relational data, and communicates with Floci on port 4566 for S3 media asset storage and SQS order event dispatching.*
>
> *On the right is our production architecture on AWS. Notice how cleanly the local environment translates: the Docker containers map directly to ECS Fargate tasks across public and private subnets; local SQL Server transitions to Amazon RDS Multi-AZ; and the Floci S3 bucket and SQS queues map directly to production AWS S3 and SQS without changing any application code."*

---

## Slide 4: Container Orchestration & Docker Compose Implementation

### Slide Content:
* **Multi-Container Topology:**
  * `vc-database`: `mcr.microsoft.com/mssql/server:2022-latest` (Port `1433:1433`)
  * `vc-platform-backend`: `virtocommerce/platform:latest` (Port `8081:80`)
  * `vc-storefront-frontend`: `virtocommerce/storefront:latest` (Port `8090:80`)
  * `floci-lab`: Pre-configured Floci emulator on ports `4566:4566` and `4500:4500`
* **Key Orchestration Highlights:**
  * **Health-Check Driven Startup:** `vc-platform` uses `depends_on: { vc-db: { condition: service_healthy } }` to ensure the database is fully operational before executing migrations.
  * **Volume Persistence:** Named Docker volume `vc-db-data` mounted at `/var/opt/mssql` ensures relational schemas survive container lifecycles.
  * **Network Isolation:** All containers communicate via a dedicated bridge network (`virto-network`) with custom DNS aliases.

> ### 🎙️ Presenter Script (What to Say):
> *"Let’s look at how the containerization is implemented. In `docker-compose.yml`, we define our services with strict operational boundaries.*
>
> *A common issue in database-backed containers is race conditions—applications crash if the database isn’t ready. We eliminated this by defining an active health check on SQL Server using `sqlcmd`. The Platform backend explicitly waits for the database to report healthy before starting its boot sequence.*
>
> *To guarantee data persistence, we mounted a named volume `vc-db-data`. Even if the database container is killed or recreated, all relational tables, catalog records, and identity data remain completely intact on the host storage."*

---

## Slide 5: Infrastructure as Code (IaC) with HashiCorp Terraform

### Slide Content:
* **Declarative Cloud Provisioning:**
  * Managed via HashiCorp Terraform AWS Provider v5.x.
  * Points to Floci local endpoint (`http://localhost:4566`) using custom endpoint blocks.
* **Provisioned Resources:**
  1. `aws_s3_bucket.media_assets`: Name `virto-commerce-media-assets` (used for catalog images and attachments).
  2. `aws_sqs_queue.order_queue`: Name `virto-order-processing-queue` (used for decoupling order checkout workflows).
  3. `aws_iam_role.platform_role`: Role `virto-commerce-platform-role` with least-privilege assume role policies.
  4. `aws_iam_policy.s3_access_policy`: Granular read/write permissions scoped strictly to the media bucket ARN.

```hcl
provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  s3_use_path_style           = true
  endpoints {
    s3  = "http://localhost:4566"
    sqs = "http://localhost:4566"
    iam = "http://localhost:4566"
  }
}
```

> ### 🎙️ Presenter Script (What to Say):
> *"For infrastructure provisioning, we strictly adhered to Infrastructure as Code principles using HashiCorp Terraform.*
>
> *In our `terraform/main.tf` file, we configured the AWS provider to point its endpoint URLs to `http://localhost:4566`. With a single command—`terraform apply -auto-approve`—Terraform declaratively created our S3 bucket `virto-commerce-media-assets`, our SQS queue `virto-order-processing-queue`, and an IAM role with least-privilege policies.*
>
> *Because we used standard Terraform AWS provider syntax, this exact same configuration can be deployed to real AWS simply by swapping the endpoint parameter."*

---

## Slide 6: Live Application & Endpoints Walkthrough

### Slide Content:
* **Endpoint 1: Virto Commerce Platform Manager Portal (`http://localhost:8081`)**
  * Displays the administrative sign-in portal.
  * Validates that Entity Framework migrations successfully created over 40+ relational database tables.
* **Endpoint 2: Virto Commerce Storefront (`http://localhost:8090`)**
  * Customer-facing web application.
  * Demonstrates active cross-container HTTP connectivity to the backend API (`StoreModuleApi.GetStoresWithHttpMessagesAsync`).
* **Endpoint 3: Floci Web Console Dashboard (`http://localhost:4500`)**
  * Graphical user interface for inspecting emulated cloud resources.
  * Visually confirms the active S3 media bucket and SQS queue.
* **Endpoint 4: AWS CLI Verification on Port 4566**
  * `aws s3 ls --endpoint-url http://localhost:4566`
  * Confirms standard wire-protocol responses from the local cloud emulator.

> ### 🎙️ Presenter Script (What to Say):
> *"Now let’s review the live deployment endpoints.*
>
> *First, navigating to `http://localhost:8081` presents the Virto Commerce Platform Manager login screen. This confirms that the backend API booted cleanly and executed its database migrations on SQL Server.*
>
> *Second, on `http://localhost:8090`, we have our Storefront. When the Storefront boots, it actively queries the backend API via HTTP. The stack trace verifies that `StoreModuleApi` successfully reached the Platform on port 80.*
>
> *Third, visiting `http://localhost:4500` brings up Floci's Web Console, showing our S3 bucket and SQS queue. And finally, running `aws s3 ls` in our terminal proves that the AWS CLI communicates seamlessly with our local emulator."*

---

## Slide 7: Testing, Resilience & Data Persistence (Task 6)

### Slide Content:
* **1. Data Persistence Test (`docker compose restart vc-db`):**
  * Verified that restarting the SQL Server container preserves all database schemas and tables via the named volume `vc-db-data`.
  * Verified that uploading `test_asset.txt` to the S3 bucket persists across restarts without file loss.
* **2. Deliberate Safe Outage Recovery Test:**
  * Simulated an unexpected infrastructure crash by running `docker compose stop vc-db`.
  * Observed platform error handling and connection retries.
  * Re-launched the database using `docker compose start vc-db` and demonstrated immediate, automatic system recovery.
* **3. Health Check Validation:**
  * Automated script `scripts/validate.ps1` polls all container endpoints and validates HTTP 200 responses.

> ### 🎙️ Presenter Script (What to Say):
> *"A critical requirement of Task 6 was validating data persistence and fault tolerance.*
>
> *To prove persistence, we executed a container restart test on `vc-db`. The database restarted, remounted the `vc-db-data` volume, and immediately returned to healthy status without data loss.*
>
> *Next, we introduced a deliberate safe failure: we forcibly stopped the database container to simulate an infrastructure outage. Once we re-started the container, the platform automatically reconnected and recovered without requiring manual intervention. We also verified S3 persistence by streaming a catalog asset into the bucket and confirming its presence after container cycles."*

---

## Slide 8: Real-World Troubleshooting & Root Cause Analysis

### Slide Content:
* **Issue 1: Host Port 8080 Collision**
  * *Root Cause:* Pre-existing `floci-lab` container was already listening on port 8080.
  * *Resolution:* Re-mapped `vc-platform` to host port `8081:80` in `docker-compose.yml`.
* **Issue 2: Inter-Container DNS Resolution**
  * *Root Cause:* Discrepancy between service name `vc-platform` and container name `vc-platform-backend`.
  * *Resolution:* Added network aliases in Docker Compose, ensuring DNS resolution across both names.
* **Issue 3: Storefront `NotFound` Status Code**
  * *Root Cause:* Storefront called `GetStoresWithHttpMessagesAsync` on an unseeded database.
  * *Resolution:* Verified as proof of cross-container HTTP communication; initialized catalog in Platform Manager.
* **Issue 4: AWS CLI `NoCredentials` Error**
  * *Root Cause:* AWS CLI client requires non-empty dummy credentials to generate HTTP signing headers.
  * *Resolution:* Configured `aws configure set aws_access_key_id test`.
* **Issue 5: Floci Web Console `SocketException`**
  * *Root Cause:* Floci UI sidecar container required host Docker daemon access.
  * *Resolution:* Mounted the engine pipe `//./pipe/docker_engine://./pipe/docker_engine`.

> ### 🎙️ Presenter Script (What to Say):
> *"Real-world DevOps is defined by troubleshooting. During this deployment, we diagnosed and resolved five distinct technical challenges.*
>
> *First, we resolved a host port collision where port 8080 was already occupied by a pre-existing container. We remapped our platform to port 8081.*
>
> *Second, we resolved an inter-container DNS issue where Storefront couldn't resolve the backend by configuring network aliases in Docker Compose.*
>
> *Third, when Storefront displayed a `NotFound` exception, our analysis of the stack trace revealed that the HTTP call to the API actually succeeded, but returned 404 because the database was fresh and unseeded.*
>
> *Documenting these root causes and solutions directly in Section 17 of our README demonstrates rigorous troubleshooting methodology."*

---

## Slide 9: Security & Operational Governance (Task 5)

### Slide Content:
* **Secrets Decoupling:**
  * Zero hardcoded credentials in source code.
  * All sensitive configuration externalized into `.env` (git-ignored) with a sanitized `.env.example` committed.
* **IAM Least-Privilege Implementation:**
  * Execution policy explicitly restricts S3 actions (`s3:GetObject`, `s3:PutObject`) strictly to `arn:aws:s3:::virto-commerce-media-assets/*`.
* **Network Security Boundaries:**
  * Database engine isolated on private bridge network `virto-network` with no exposed external management interfaces.
* **Target Production Security Controls:**
  * Ingress TLS 1.3 encryption terminated at AWS ALB.
  * Automated credential rotation using AWS Secrets Manager.
  * Security group ingress limited to VPC CIDR blocks.

> ### 🎙️ Presenter Script (What to Say):
> *"Security was embedded into every layer of this deployment.*
>
> *We ensured zero secrets were committed to version control. Passwords and keys are managed through environment variables and injected at container runtime.*
>
> *Our Terraform IAM policy follows the principle of least privilege: permissions are locked down exclusively to the specific media bucket ARN rather than using wildcard asterisks.*
>
> *For production, this translates to strict security group boundaries where the database resides in private isolated subnets, and all public traffic is encrypted using TLS 1.3 terminated at the Application Load Balancer."*

---

## Slide 10: Production AWS Migration & Cost Model

### Slide Content:
* **Target AWS Architecture Specification:**
  * **Compute:** 2x ECS Fargate Tasks (2 vCPU, 4GB RAM) with Auto Scaling
  * **Database:** Amazon RDS for SQL Server Standard (db.m5.large, Multi-AZ)
  * **Caching:** Amazon ElastiCache Redis Cluster (cache.t4g.medium)
  * **Networking:** Multi-AZ VPC + Application Load Balancer (ALB) + Route 53
  * **Storage & CDN:** Amazon S3 (100GB) + Amazon CloudFront CDN distribution
* **Estimated Production Monthly Operating Cost:**

| AWS Component | Target Resource Specification | Monthly Estimate |
| :--- | :--- | :--- |
| **Compute** | 2x ECS Fargate Tasks (Multi-AZ) | ~$110.00 |
| **Database** | Amazon RDS SQL Server (Multi-AZ) | ~$320.00 |
| **Caching** | Amazon ElastiCache Redis | ~$45.00 |
| **Networking** | ALB + NAT Gateways + Route 53 | ~$22.00 |
| **Storage & CDN** | Amazon S3 (100GB) + CloudFront | ~$15.00 |
| **Total Cost** | **High-Availability Production Setup** | **~$512.00 / month** |

> ### 🎙️ Presenter Script (What to Say):
> *"Here is our production cost model for deploying Virto Commerce on real AWS.*
>
> *We sized the environment for high availability across two Availability Zones. The major cost driver is the database tier: an Amazon RDS SQL Server Standard Multi-AZ instance at approximately \$320 per month.*
>
> *Compute on ECS Fargate runs at approximately \$110 per month, with ElastiCache Redis at \$45 and networking around \$22. This brings our total production operating expenditure to approximately \$512 per month.*
>
> *By using Floci during development and automated CI/CD, we achieved zero development cloud costs while maintaining an exact 1-to-1 operational mirror of our production AWS infrastructure."*

---

## Slide 11: Deployment Automation & Cleanup Verification

### Slide Content:
* **Full Deployment Sequence:**
  ```powershell
  # 1. Start application stack
  docker compose up -d

  # 2. Deploy AWS infrastructure on Floci via Terraform
  cd terraform ; terraform init ; terraform apply -auto-approve ; cd ..

  # 3. Validate endpoints & health
  .\scripts\validate.ps1
  ```
* **Complete Teardown & Deletion Sequence (Evaluator Demo):**
  ```powershell
  # 1. Destroy Terraform cloud resources
  cd terraform ; terraform destroy -auto-approve ; cd ..

  # 2. Stop and remove all containers, networks, and persistent data volumes
  docker compose down -v --remove-orphans
  ```
* **CI/CD Automation:**
  * GitHub Actions workflow (`.github/workflows/deploy.yml`) validates compose syntax, formats Terraform, and tests against Floci in automated pipelines.

> ### 🎙️ Presenter Script (What to Say):
> *"Automation and repeatability are critical for DevOps deliverables.*
>
> *Our entire deployment is automated through reusable PowerShell and Bash scripts, accompanied by a GitHub Actions CI/CD pipeline that validates Terraform syntax and spins up a Floci container to run automated integration tests on every commit.*
>
> *When it comes to teardown, running `.\scripts\cleanup.ps1` cleanly destroys all Terraform-provisioned resources on Floci and removes the container stack and volumes, leaving zero orphaned processes or storage leaks on the host."*

---

## Slide 12: Conclusion & Q&A Preparation

### Slide Content:
* **Summary of Achievements:**
  * ✅ Full containerization of Virto Commerce Platform, Storefront, and SQL Server.
  * ✅ Declarative cloud provisioning on Floci emulator using HashiCorp Terraform.
  * ✅ Complete verification of data persistence, failure recovery, and cross-tier API connectivity.
  * ✅ 16-point comprehensive README runbook with all 8 uncropped evidence screenshots.
  * ✅ Formal 8.4MB submission PDF report compiled and committed to version control.
* **Repository Link:** [https://github.com/kaushalpatil205/virto-commerce-aws](https://github.com/kaushalpatil205/virto-commerce-aws)

> ### 🎙️ Presenter Script (What to Say):
> *"To conclude, we have delivered a fully functional, containerized Virto Commerce deployment backed by local AWS emulation on Floci and automated via Terraform.*
>
> *All eight assignment criteria have been validated, tested, and documented in our repository and formal submission PDF.*
>
> *Thank you for your time, and I am now ready to answer any technical questions you may have."*

---

## Appendix: Anticipated Interviewer Questions & Model Answers

### Q1: "Why did Storefront return a `NotFound` status code on port 8090?"
* **Answer:** *"Virto Commerce Storefront communicates with the Platform backend over REST APIs. The stack trace proves the HTTP connection was established and reached `StoreModuleApi.GetStoresWithHttpMessagesAsync`. The 404 response occurred simply because this was a fresh, unseeded SQL Server database with no default store catalog registered yet. In production, an administrator logs into the Platform Manager on port 8081 to seed the catalog, after which the Storefront renders product pages."*

### Q2: "How did you know the IAM Role ARN during creation without looking at documentation?"
* **Answer:** *"In AWS, ARNs follow the deterministic structure `arn:aws:service:region:account:resource`. In local emulators like Floci or LocalStack, the dummy account ID is always `000000000000`. More importantly, the `aws iam create-role` command outputs the exact ARN in its JSON response directly in the terminal, allowing us to query or capture it dynamically via `--query 'Role.Arn'`."*

### Q3: "What happens to the database if the SQL Server container crashes?"
* **Answer:** *"All database data survives because we mapped the `/var/opt/mssql` directory to a named Docker volume called `vc-db-data`. We proved this in our Task 6 persistence test: when `vc-database` was restarted, SQL Server remounted the volume and immediately restored the existing `VirtoCommerce3` database with all 40+ schema tables intact."*

### Q4: "Why use Floci instead of LocalStack or real AWS?"
* **Answer:** *"Floci starts in approximately 24 milliseconds and consumes around 13 megabytes of memory because it is compiled natively with Quarkus, compared to LocalStack which requires several gigabytes of RAM. Furthermore, Floci has no paid feature gates or enterprise licensing restrictions, making it ideal for offline development and lightweight CI/CD runners."*
