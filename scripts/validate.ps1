# =========================================================
# Virto Commerce Health & Connectivity Validation Script
# =========================================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Running Virto Commerce Health Checks" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check Docker Container States
Write-Host "`n1. Checking Container Statuses:" -ForegroundColor Yellow
docker compose ps

# Check Floci Emulator
Write-Host "`n2. Checking Floci AWS Endpoint (Port 4566):" -ForegroundColor Yellow
try {
    $flociResponse = Invoke-WebRequest -Uri "http://localhost:4566" -UseBasicParsing -TimeoutSec 5
    Write-Host "Floci AWS Emulator is UP! Status: $($flociResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Floci check failed: $_" -ForegroundColor Red
}

# Check Virto Platform API
Write-Host "`n3. Checking Virto Commerce Platform API (Port 8080):" -ForegroundColor Yellow
try {
    $platformResponse = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 10
    Write-Host "Virto Commerce Platform is UP! Status: $($platformResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Platform check response: $_" -ForegroundColor Yellow
}

# Check Virto Storefront
Write-Host "`n4. Checking Virto Commerce Storefront (Port 8090):" -ForegroundColor Yellow
try {
    $storefrontResponse = Invoke-WebRequest -Uri "http://localhost:8090" -UseBasicParsing -TimeoutSec 10
    Write-Host "Virto Commerce Storefront is UP! Status: $($storefrontResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Storefront check response: $_" -ForegroundColor Yellow
}

# Verify AWS S3 and SQS Resources
Write-Host "`n5. Verifying AWS S3 & SQS on Floci:" -ForegroundColor Yellow
$env:AWS_ENDPOINT_URL = "http://localhost:4566"
$env:AWS_ACCESS_KEY_ID = "test"
$env:AWS_SECRET_ACCESS_KEY = "test"
$env:AWS_DEFAULT_REGION = "us-east-1"

aws s3 ls --endpoint-url http://localhost:4566
aws sqs list-queues --endpoint-url http://localhost:4566

Write-Host "`nAll validation checks completed." -ForegroundColor Cyan
