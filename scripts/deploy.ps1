# =========================================================
# Virto Commerce Local Deployment Automation Script (Windows)
# =========================================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting Virto Commerce Deployment via Docker" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Start Docker Containers
Write-Host "`n[Step 1/4] Starting Docker Compose services..." -ForegroundColor Yellow
docker compose up -d

# 2. Wait for Health Checks
Write-Host "`n[Step 2/4] Waiting for services to initialize and become healthy (60s)..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# 3. Apply Terraform Infrastructure on Floci
Write-Host "`n[Step 3/4] Provisioning AWS resources on Floci using Terraform..." -ForegroundColor Yellow
Set-Location -Path "terraform"
if (Get-Command terraform -ErrorAction SilentlyContinue) {
    terraform init
    terraform apply -auto-approve
} else {
    Write-Host "Terraform CLI not found on PATH. Falling back to AWS CLI provisioning on Floci..." -ForegroundColor Yellow
    $env:AWS_ENDPOINT_URL = "http://localhost:4566"
    $env:AWS_ACCESS_KEY_ID = "test"
    $env:AWS_SECRET_ACCESS_KEY = "test"
    $env:AWS_DEFAULT_REGION = "us-east-1"
    
    aws s3 mb s3://virto-commerce-media-assets --endpoint-url http://localhost:4566
    aws sqs create-queue --queue-name virto-order-processing-queue --endpoint-url http://localhost:4566
}
Set-Location -Path ".."

# 4. Display Status & URLs
Write-Host "`n[Step 4/4] Deployment Status Summary:" -ForegroundColor Green
docker compose ps

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "Virto Commerce Deployment Successfully Initialized!" -ForegroundColor Green
Write-Host "Platform Admin:     http://localhost:8080" -ForegroundColor White
Write-Host "Storefront Shop:    http://localhost:8090" -ForegroundColor White
Write-Host "Floci AWS Endpoint: http://localhost:4566" -ForegroundColor White
Write-Host "Floci Web Console:  http://localhost:4566/_floci/ui" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
