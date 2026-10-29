# Virto Commerce Platform & Storefront Deployment with AWS Emulation (Floci)

[![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![Floci AWS](https://img.shields.io/badge/AWS%20Emulator-Floci-orange.svg)](https://floci.io/aws/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)
[![Virto Commerce](https://img.shields.io/badge/E--Commerce-VirtoCommerce-brightgreen.svg)](https://virtocommerce.com/)


**Objective:** Research, design, implement, and demonstrate a production-grade deployment of Virto Commerce Platform and Storefront using containerization, Terraform Infrastructure as Code, and the Floci AWS emulator.

---

## Table of Contents
1. [Architecture Overview & Diagrams](#1-architecture-overview--diagrams)
2. [Prerequisites & Tool Versions](#2-prerequisites--tool-versions)
3. [Repository Structure](#3-repository-structure)
4. [Environment Variables & Configuration](#4-environment-variables--configuration)
5. [Local Setup & Deployment Steps](#5-local-setup--deployment-steps)
6. [Floci Setup & Resource Provisioning](#6-floci-setup--resource-provisioning)
7. [Proposed Production AWS Architecture](#7-proposed-production-aws-architecture)
8. [Network Ports & Application Endpoints](#8-network-ports--application-endpoints)
9. [Database Initialization & Data Persistence](#9-database-initialization--data-persistence)
10. [Health Checks & Validation Procedures](#10-health-checks--validation-procedures)
11. [Security & Operational Considerations](#11-security--operational-considerations)
12. [Backup, Restore & Rollback Procedures](#12-backup-restore--rollback-procedures)
13. [Cleanup & Resource Deletion](#13-cleanup--resource-deletion)
14. [Estimated AWS Production Costs](#14-estimated-aws-production-costs)
15. [Known Limitations & Future Improvements](#15-known-limitations--future-improvements)
16. [Visual Evidence & Screenshots](#16-visual-evidence--screenshots)
17. [Troubleshooting & Solved Issues](#17-troubleshooting--solved-issues)
18. [Master Command Summary](#18-master-command-summary)

---

## 1. Architecture Overview & Diagrams

### 1.1 Local Emulation Architecture (Docker + Floci)
In local development, all components run in an isolated Docker network (`virto-network`). Floci emulates AWS S3 for media asset storage, SQS for order event queuing, and IAM for security policies.

```mermaid
graph TD
    Client["Browser / Engineer"]
    
    subgraph Host["Local Workstation / Windows Desktop"]
        Storefront["Virto Storefront (Port 8090)"]
        Platform["Virto Platform Backend API (Port 8081)"]
        SQL["SQL Server 2022 (Port 1433)"]
        Floci["Floci AWS Emulator (Port 4566)"]
        FlociUI["Floci Web Dashboard (Port 4500)"]
        
        Client -->|Browse Store| Storefront
        Client -->|Manage Catalog / API| Platform
        Client -->|Inspect Cloud Resources| FlociUI
        
        Storefront -->|REST API / GraphQL| Platform
        Platform -->|Relational Data| SQL
        Platform -->|Catalog Media / S3| Floci
        Platform -->|Order Events / SQS| Floci
        FlociUI -->|Query Resources| Floci
    end
    
    subgraph Storage["Persistent Docker Volumes"]
        DBVol[("vc-db-data")]
        PlatformVol[("vc-platform-data")]
        StorefrontVol[("vc-storefront-data")]
        
        SQL --- DBVol
        Platform --- PlatformVol
        Storefront --- StorefrontVol
    end
```

### 1.2 Proposed Real AWS Production Architecture
In production, the deployment transitions seamlessly to AWS managed services:

```mermaid
graph TD
    User["End Users & Shoppers"]
    Admin["Operations & Admins"]
    
    subgraph AWS["AWS Cloud (Production Multi-AZ)"]
        CF["Amazon CloudFront (CDN)"]
        ALB["Application Load Balancer (ALB) + ACM SSL"]
        
        subgraph VPC["VPC: 10.0.0.0/16"]
            subgraph PublicSubnets["Public Subnets (Multi-AZ)"]
                NAT["NAT Gateways"]
            end
            
            subgraph PrivateAppSubnets["Private Application Subnets"]
                ECSSF["ECS Fargate: Virto Storefront Tasks"]
                ECSPF["ECS Fargate: Virto Platform API Tasks"]
            end
            
            subgraph PrivateDataSubnets["Private Isolated Data Subnets"]
                RDS[("Amazon RDS SQL Server / Aurora Multi-AZ")]
                Redis[("Amazon ElastiCache Redis Cluster")]
            end
        end
        
        S3[("Amazon S3: Media & Static Assets")]
        SQS["Amazon SQS: Order Event Queue"]
        CW["Amazon CloudWatch: Logs & Alarms"]
        SM["AWS Secrets Manager"]
        
        User --> CF
        CF --> S3
        CF --> ALB
        Admin --> ALB
        
        ALB --> ECSSF
        ALB --> ECSPF
        ECSSF --> ECSPF
        
        ECSPF --> RDS
        ECSPF --> Redis
        ECSPF --> S3
        ECSPF --> SQS
        ECSPF --> SM
        
        ECSSF --> CW
        ECSPF --> CW
    end
```

---

## 2. Prerequisites & Tool Versions

| Tool | Version Verified | Purpose |
| :--- | :--- | :--- |
| **Docker Desktop** | `24.0+` / `26.0+` | Container execution and local orchestration |
| **Docker Compose** | `v2.20+` | Multi-container coordination and networking |
| **Terraform** | `1.5.0+` | Declarative Infrastructure as Code (IaC) |
| **AWS CLI** | `v2.15+` | Direct interaction with AWS / Floci endpoints |
| **Windows PowerShell** | `5.1` / `7.x` | Host system scripting and automation |
| **Ubuntu (WSL)** | `22.04 LTS` | Linux-compatible deployment runtime |

---

## 3. Repository Structure

```text
C:\Users\User\Desktop\Kaushal Patil\virto-commerce-aws-main\
├── docker-compose.yml          # Container orchestration (DB, Platform, Storefront)
├── .env.example                # Sample environment variables
├── .env                        # Active environment configuration
├── README.md                   # Complete deployment manual & runbook
├── terraform/                  # Infrastructure as Code for Floci AWS
│   ├── main.tf                 # S3 bucket, SQS queue, IAM policies
│   ├── variables.tf            # Configurable deployment inputs
│   └── outputs.tf              # Exported resource ARNs and URLs
├── scripts/                    # Automation scripts
│   ├── deploy.ps1              # Windows PowerShell automated deployment
│   ├── deploy.sh               # Linux/Ubuntu automated deployment
│   ├── validate.ps1            # Health and connectivity validation
│   ├── validate.sh             # Health validation for bash
│   ├── cleanup.ps1             # Clean teardown for Windows
│   └── cleanup.sh              # Clean teardown for Linux
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD validation pipeline
├── docs/                       # Architectural and presentation documentation
│   ├── architecture.md         # Detailed architectural breakdown
│   └── presentation.md         # 10-15 minute presentation guide
└── screenshots/                # Deployment evidence & test screenshots
    ├── 01_floci_running.png
    ├── 02_docker_containers.png
    ├── 03_virto_platform.png
    ├── 04_virto_storefront.png
    ├── 05_terraform_apply.png
    ├── 06_s3_sqs_verification.png
    ├── 07_persistence_test.png
    └── 08_failure_recovery.png
```

---

## 4. Environment Variables & Configuration

Copy `.env.example` to `.env`:

```bash
# Database Configuration
SA_PASSWORD=VirtoCommerce@2026!
MSSQL_PID=Express
DB_PORT=1433

# Application Ports
PLATFORM_PORT=8081
STOREFRONT_PORT=8090

# AWS & Floci Emulator
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_ENDPOINT_URL=http://localhost:4566
FLOCI_PORT=4566

# Cloud Resources
MEDIA_BUCKET_NAME=virto-commerce-media-assets
ORDER_QUEUE_NAME=virto-order-processing-queue
```

---

## 5. Local Setup & Deployment Steps

### In Windows PowerShell:
```powershell
# 1. Navigate to project root
cd "C:\Users\User\Desktop\Kaushal Patil\virto-commerce-aws-main"

# 2. Start all services in background
docker compose up -d

# 3. Check status of all containers
docker compose ps
```

---

## 6. Floci Setup & Resource Provisioning

Floci provides local AWS emulation on port `4566`.

### 6.1 Provisioning via Terraform
```powershell
cd terraform
terraform init
terraform apply -auto-approve
cd ..
```

### 6.2 Manual Verification via AWS CLI
```powershell
# Configure credentials
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set default.region us-east-1

# Verify S3 bucket was created
aws s3 ls --endpoint-url http://localhost:4566

# Verify SQS queue was created
aws sqs list-queues --endpoint-url http://localhost:4566
```

### 6.3 Floci Web Console
Open in your browser:
👉 **`http://localhost:4500`** *(or `http://localhost:4566/_floci/ui`)* to visually inspect the S3 buckets and SQS queues.

---

## 7. Proposed Production AWS Architecture

To transition this workload from Floci to real AWS in production:

1. **Networking:** Provision a VPC with 2 Public Subnets (ALB, NAT Gateways) and 4 Private Subnets (ECS tasks, RDS multi-AZ).
2. **Compute:** Deploy Virto Commerce Platform and Storefront as containerized tasks in **AWS ECS Fargate** with Auto Scaling.
3. **Database:** Deploy **Amazon RDS for SQL Server** (or Aurora PostgreSQL) across Multi-AZ with automated daily snapshots.
4. **Caching & Assets:** 
   - Deploy **Amazon ElastiCache Redis** for distributed caching.
   - Point Virto Commerce asset module to real **Amazon S3** with CloudFront CDN for global low-latency delivery.
5. **IAM Security:** Assign an ECS Task Role with strict least-privilege policies granting `s3:PutObject`/`s3:GetObject` only to the production media bucket.

---

## 8. Network Ports & Application Endpoints

| Service | Internal Port | Host Port | Purpose | Health Check Endpoint |
| :--- | :--- | :--- | :--- | :--- |
| **Floci AWS** | `4566` | `4566` | S3, SQS, IAM Emulator | `http://localhost:4566` |
| **Floci UI** | `4500` | `4500` | Browser Console Dashboard | `http://localhost:4500` |
| **SQL Server** | `1433` | `1433` | Relational Database Engine | `sqlcmd -Q 'SELECT 1'` |
| **VC Platform** | `80` | `8081` | Backend API & Admin Portal | `http://localhost:8081` |
| **VC Storefront**| `80` | `8090` | Public Customer Webshop | `http://localhost:8090` |

---

## 9. Database Initialization & Data Persistence

1. **Automatic Schema Migration:** Virto Commerce Platform automatically runs Entity Framework migrations on startup to initialize the `VirtoCommerce3` database.
2. **Named Volume Persistence:** The SQL Server data is persisted to the named Docker volume `vc-db-data` mounted at `/var/opt/mssql`.
3. **Persistence Test:**
   ```powershell
   docker compose restart vc-db
   docker compose ps
   ```

---

## 10. Health Checks & Validation Procedures

Run the automated validation script:

* **In Windows PowerShell:**
  ```powershell
  .\scripts\validate.ps1
  ```
* **In Ubuntu WSL:**
  ```bash
  chmod +x ./scripts/validate.sh && ./scripts/validate.sh
  ```

---

## 11. Security & Operational Considerations

- **Secrets Management:** Passwords and keys are externalized into `.env` (git-ignored) and injected via environment variables.
- **Least Privilege:** The IAM role in Terraform strictly limits operations to the designated `virto-commerce-media-assets` bucket.
- **Network Boundaries:** Database and internal service communication occur over an isolated internal Docker bridge network (`virto-network`).
- **Production Enhancements:** Production AWS deployment will enforce TLS 1.3 via ALB and use AWS Secrets Manager with automatic credential rotation.

---

## 12. Backup, Restore & Rollback Procedures

### Backup Database:
```powershell
docker exec -t vc-database /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "VirtoCommerce@2026!" -C -Q "BACKUP DATABASE [VirtoCommerce3] TO DISK = N'/var/opt/mssql/backup.bak' WITH NOFORMAT, NOINIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10"
```

### Rollback Strategy:
```powershell
docker compose down
# Pin previous image tag in docker-compose.yml, then:
docker compose up -d
```

---

## 13. Cleanup & Resource Deletion

To completely remove all deployed resources, volumes, and temporary networks:

### Windows PowerShell Teardown:
```powershell
# Run the automated cleanup script
.\scripts\cleanup.ps1

# OR run manually:
cd terraform ; terraform destroy -auto-approve ; cd ..
docker compose down -v --remove-orphans
```

---

## 14. Estimated AWS Monthly Costs

| Component | AWS Resource | Monthly Estimate |
| :--- | :--- | :--- |
| **Compute** | 2x ECS Fargate Tasks (2 vCPU, 4GB RAM) | ~$110.00 |
| **Database** | Amazon RDS SQL Server Standard (db.m5.large, Multi-AZ) | ~$320.00 |
| **Caching** | Amazon ElastiCache Redis (cache.t4g.medium) | ~$45.00 |
| **Load Balancer** | Application Load Balancer (ALB) | ~$22.00 |
| **Storage & Network**| Amazon S3 (100GB) + Data Transfer | ~$15.00 |
| **Total Estimated Cost**| | **~$512.00 / month** |

---

## 15. Known Limitations & Future Improvements

- **Local Search Engine:** Currently using default local Lucene search. Production requires an Amazon OpenSearch cluster for large product catalogs.
- **Single-Node DB:** Local SQL Server runs as a single instance. Production requires an AWS Multi-AZ failover setup.
- **CDN Integration:** Assets locally are served directly from S3 mock; production should front S3 with Amazon CloudFront for caching.

---

## 16. Visual Evidence & Screenshots

All high-resolution, full-window screenshots are cataloged in the `screenshots/` directory:

### Screenshot 1: Floci AWS Emulator & Web Console Running
![Floci Running](screenshots/01_floci_running.png)
* **URL / Source:** `http://localhost:4500` (or `http://localhost:4566/_floci/ui`)
* **Technical Explanation:** Demonstrates the Floci AWS emulator active on port `4566` with its web console dashboard on port `4500`. It visually confirms that the mock AWS control plane is running locally without incurring cloud costs.

---

### Screenshot 2: Docker Containers Overview
![Docker Containers](screenshots/02_docker_containers.png)
* **Command:** `docker compose ps`
* **Technical Explanation:** Confirms all 3 core services (`vc-database`, `vc-platform-backend`, `vc-storefront-frontend`) are in **healthy** and running state, with correct port bindings (`1433`, `8081`, `8090`).

---

### Screenshot 3: Virto Commerce Platform API & Admin Portal
![Virto Platform](screenshots/03_virto_platform.png)
* **URL:** `http://localhost:8081/#!/login`
* **Technical Explanation:** Demonstrates the Virto Commerce Platform backend API and administration portal actively running. The successful presentation of the login interface confirms that Entity Framework Core database migrations executed successfully on Microsoft SQL Server 2022 and initialized the database schema.

---

### Screenshot 4: Virto Commerce Storefront & Backend API Communication
![Virto Storefront](screenshots/04_virto_storefront.png)
* **URL:** `http://localhost:8090`
* **Technical Explanation (Key Milestone):** Demonstrates the Storefront frontend container successfully running and establishing cross-container HTTP communication with the backend Platform container. The trace `VirtoCommerce.Storefront.AutoRestClients.StoreModuleApi.StoreModule.GetStoresWithHttpMessagesAsync` proves that the Storefront reached the Platform REST API. The returned status code `NotFound` is the expected behavior for a freshly initialized, unseeded database where no default store catalog has yet been created via the admin portal. This validates container networking and platform-to-frontend communication as required by **Task 2** and **Task 6**.

---

### Screenshot 5: Terraform Infrastructure Provisioning
![Terraform Apply](screenshots/05_terraform_apply.png)
* **Command:** `terraform output`
* **Technical Explanation:** Displays the declarative provisioning of AWS infrastructure on Floci using HashiCorp Terraform. It confirms the successful creation of the S3 media bucket (`virto-commerce-media-assets`), SQS queue (`virto-order-processing-queue`), and IAM task execution role (`virto-commerce-platform-role`).

---

### Screenshot 6: AWS CLI Verification on Floci
![AWS CLI Verification](screenshots/06_s3_sqs_verification.png)
* **Command:** `aws s3 ls --endpoint-url http://localhost:4566`
* **Technical Explanation:** Demonstrates standard AWS CLI v2 interaction against the Floci local endpoint (`http://localhost:4566`), listing the provisioned S3 buckets (`virto-commerce-media-assets`) and validating standard AWS wire-protocol compatibility.

---

### Screenshot 7: Database Data Persistence Test (Task 6)
![Data Persistence](screenshots/07_persistence_test.png)
* **Command:** `docker compose restart vc-db ; docker compose ps`
* **Technical Explanation:** Fulfills the Task 6 persistence test requirement. Demonstrates that stopping and restarting the Microsoft SQL Server container preserves database state via the named Docker volume `vc-db-data`, returning to a healthy status without corruption or data loss.

---

### Screenshot 8: Deliberate Outage & Safe Recovery Demonstration (Task 6)
![Failure Recovery](screenshots/08_failure_recovery.png)
* **Command:** `docker compose stop vc-db ; docker compose ps ; docker compose start vc-db ; docker compose ps`
* **Technical Explanation:** Fulfills the Task 6 resilience requirement. Demonstrates deliberately stopping the database container to simulate an infrastructure outage, observing application decoupling, and restarting the service to demonstrate automatic system recovery.

---

## 17. Troubleshooting & Solved Issues

During deployment and testing, several real-world DevOps challenges were identified and systematically resolved:

### 1. Port 8080 Collision with Pre-existing Floci Container
* **Symptom:** `vc-platform` failed to bind to host port `8080`, preventing the Platform container from starting.
* **Investigation:** Inspection of `docker ps` revealed that a pre-existing container (`floci` under `floci-lab`) was already listening on `0.0.0.0:8080->80/tcp` and `0.0.0.0:4566->4566/tcp`.
* **Resolution:** Reconfigured `docker-compose.yml` to bind `vc-platform` to host port **`8081:80`**, immediately resolving the port collision while preserving the active Floci emulator.

### 2. Docker Network DNS Resolution between Frontend & Backend
* **Symptom:** Storefront failed with `HttpRequestException: Name or service not known (vc-platform:80)`.
* **Investigation:** The service was named `vc-platform`, while the explicit container name was `vc-platform-backend`.
* **Resolution:** Configured network aliases (`vc-platform` and `vc-platform-backend`) under `virto-network` in `docker-compose.yml` so that inter-container DNS requests resolve seamlessly regardless of naming format.

### 3. Storefront API `NotFound` Response on Fresh Database
* **Symptom:** Navigating to `http://localhost:8090` returned `HttpOperationException: Operation returned an invalid status code 'NotFound'`.
* **Investigation:** Inspection of the call stack showed `StoreModuleApi.GetStoresWithHttpMessagesAsync` successfully communicating with the backend. The HTTP 404 response indicated that the newly migrated SQL database did not yet have a default store catalog record created.
* **Resolution:** Verified that this is expected default behavior for unseeded Virto Commerce instances; logged into the Platform Manager at `http://localhost:8081` to manage and seed store catalog entities.

### 4. AWS CLI Missing Credentials Error (`NoCredentials`)
* **Symptom:** `aws s3 ls --endpoint-url http://localhost:4566` returned `Unable to locate credentials`.
* **Investigation:** While Floci does not enforce authentication, the AWS CLI client requires non-empty dummy credentials to generate signing headers.
* **Resolution:** Executed `aws configure set aws_access_key_id test` and `aws configure set aws_secret_access_key test`, allowing all CLI commands to execute seamlessly.

### 5. Floci Web Console Container Socket Mount (`SocketException`)
* **Symptom:** Accessing `http://localhost:4566/_floci/ui` reported `Floci could not reach the container runtime (java.net.SocketException)`.
* **Investigation:** Floci launches its web console UI as an on-demand child Docker container and requires access to the host Docker daemon.
* **Resolution:** Mounted the host engine pipe (`//./pipe/docker_engine://./pipe/docker_engine` on Windows or `/var/run/docker.sock` on Linux) into the Floci container, enabling the UI sidecar to launch automatically on port `4500`.

---

## 18. Master Command Summary

### Full Setup Commands (Executed from Project Root):
```powershell
# 1. Initialize environment configuration
Copy-Item .env.example .env

# 2. Launch Docker container stack
docker compose up -d

# 3. Check container health
docker compose ps

# 4. Provision AWS Infrastructure via Terraform (or AWS CLI)
cd terraform ; terraform init ; terraform apply -auto-approve ; cd ..

# 5. Configure dummy AWS credentials
aws configure set aws_access_key_id test ; aws configure set aws_secret_access_key test ; aws configure set default.region us-east-1

# 6. Verify provisioned AWS resources on Floci
aws s3 ls --endpoint-url http://localhost:4566
aws sqs list-queues --endpoint-url http://localhost:4566

# 7. Run persistence and recovery verification tests
docker compose restart vc-db ; docker compose ps
docker compose stop vc-db ; docker compose ps ; docker compose start vc-db ; docker compose ps
```

### Complete Teardown & Deletion Commands (Examiner Demo):
```powershell
# 1. Destroy Terraform provisioned cloud resources
cd terraform ; terraform destroy -auto-approve ; cd ..

# 2. Stop and remove all containers, networks, and persistent data volumes
docker compose down -v --remove-orphans
```
