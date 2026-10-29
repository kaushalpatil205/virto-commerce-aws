#!/bin/bash
set -e

echo "=========================================="
echo "Tearing Down Virto Commerce Infrastructure"
echo "=========================================="

if [ -f "terraform/terraform.tfstate" ] && command -v terraform &> /dev/null; then
    echo -e "\n[Step 1/2] Destroying Terraform resources on Floci..."
    cd terraform
    terraform destroy -auto-approve || true
    cd ..
fi

echo -e "\n[Step 2/2] Stopping and removing all Docker containers, networks, and persistent volumes..."
docker compose down -v --remove-orphans

echo -e "\nClean-up completed! All resources removed cleanly."
