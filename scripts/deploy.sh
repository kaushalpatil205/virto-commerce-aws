#!/bin/bash
set -e

echo "=========================================="
echo "Starting Virto Commerce Deployment via Docker"
echo "=========================================="

echo -e "\n[Step 1/4] Starting Docker Compose services..."
docker compose up -d

echo -e "\n[Step 2/4] Waiting for services to initialize (45s)..."
sleep 45

echo -e "\n[Step 3/4] Provisioning AWS resources on Floci using Terraform..."
if [ -d "terraform" ] && command -v terraform &> /dev/null; then
    cd terraform
    terraform init
    terraform apply -auto-approve
    cd ..
else
    echo "Terraform CLI not found or directory missing. Provisioning via AWS CLI on Floci..."
    export AWS_ENDPOINT_URL=http://localhost:4566
    export AWS_ACCESS_KEY_ID=test
    export AWS_SECRET_ACCESS_KEY=test
    export AWS_DEFAULT_REGION=us-east-1
    aws s3 mb s3://virto-commerce-media-assets --endpoint-url http://localhost:4566 || true
    aws sqs create-queue --queue-name virto-order-processing-queue --endpoint-url http://localhost:4566 || true
fi

echo -e "\n[Step 4/4] Deployment Status Summary:"
docker compose ps

echo -e "\n========================================================"
echo "Virto Commerce Deployment Successfully Initialized!"
echo "Platform Admin:     http://localhost:8080"
echo "Storefront Shop:    http://localhost:8090"
echo "Floci AWS Endpoint: http://localhost:4566"
echo "Floci Web Console:  http://localhost:4566/_floci/ui"
echo "========================================================"
