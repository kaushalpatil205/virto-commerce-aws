# Virto Commerce AWS & Floci Deployment — Presentation Guide (Task 8)

## Duration: 10–15 Minutes

### Slide / Topic Walkthrough:

#### 1. Architecture & Technology Choices (2 mins)
- **Business Need:** Modular, headless e-commerce architecture (separation of concern between Storefront and Platform API).
- **Core Stack:** ASP.NET Core 8 (.NET), Microsoft SQL Server 2022, Floci AWS Emulator (local S3, SQS, IAM).
- **Why Floci:** Zero cloud cost, instantaneous feedback loop (~24ms cold starts), exact wire-protocol compatibility with real AWS S3 and SQS.

#### 2. What Was Deployed and How (3 mins)
- **Containerization:** Docker Compose orchestrating 4 services (`floci`, `vc-db`, `vc-platform`, `vc-storefront`).
- **Infrastructure as Code (IaC):** HashiCorp Terraform configuring the local S3 media bucket (`virto-commerce-media-assets`), SQS queue (`virto-order-processing-queue`), and IAM least-privilege roles.
- **Networking:** Isolated bridge network `virto-network`, internal DNS service resolution.

#### 3. Live Walkthrough & Demonstration (4 mins)
- Demonstrate Platform Backend: `http://localhost:8080` (admin/status).
- Demonstrate Storefront: `http://localhost:8090`.
- Demonstrate Floci Web Console: `http://localhost:4566/_floci/ui` showing active S3 buckets and SQS queues.
- Run `aws s3 ls --endpoint-url http://localhost:4566` to prove real-time data persistence.

#### 4. Security, Operations & Troubleshooting (3 mins)
- **Security:** Decoupled secrets into `.env`, non-root execution, path-style S3 isolation.
- **Troubleshooting Case Study:** Resolved Docker socket mount error for Floci Web UI by binding the engine pipe/socket and applying least-privilege policies.
- **Safe Failure Test:** Stopped database container, demonstrated platform graceful retry and reconnection after database recovery.

#### 5. Real AWS Production Readiness & Cost Estimation (3 mins)
- **Target AWS Architecture:** AWS ECS Fargate across multi-AZ, Application Load Balancer with ACM SSL, Amazon Aurora PostgreSQL / RDS Multi-AZ, Amazon ElastiCache Redis, S3 for media assets.
- **Estimated Monthly Cost:** ~$480 - $650/month for high-availability production setup.
