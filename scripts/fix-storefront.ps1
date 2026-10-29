# Fix Docker DNS name resolution for Storefront to Platform
(Get-Content docker-compose.yml) -replace 'http://vc-platform', 'http://vc-platform-backend' | Set-Content docker-compose.yml
docker compose up -d vc-storefront
Write-Host "Storefront configuration updated and container restarted!" -ForegroundColor Green
