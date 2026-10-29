# =========================================================
# Virto Commerce Cleanup & Teardown Script (Windows)
# =========================================================

Write-Host "==========================================" -ForegroundColor Red
Write-Host "Tearing Down Virto Commerce Infrastructure" -ForegroundColor Red
Write-Host "==========================================" -ForegroundColor Red

# 1. Destroy Terraform Resources
if (Test-Path "terraform/terraform.tfstate") {
    Write-Host "`n[Step 1/2] Destroying Terraform resources on Floci..." -ForegroundColor Yellow
    Set-Location -Path "terraform"
    if (Get-Command terraform -ErrorAction SilentlyContinue) {
        terraform destroy -auto-approve
    }
    Set-Location -Path ".."
}

# 2. Stop and Remove Containers and Named Volumes
Write-Host "`n[Step 2/2] Stopping and removing all Docker containers, networks, and persistent volumes..." -ForegroundColor Yellow
docker compose down -v --remove-orphans

Write-Host "`nClean-up completed! All resources removed cleanly." -ForegroundColor Green
