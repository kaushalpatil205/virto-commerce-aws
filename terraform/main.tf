terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3       = var.floci_endpoint
    sqs      = var.floci_endpoint
    iam      = var.floci_endpoint
    dynamodb = var.floci_endpoint
  }
}

# 1. S3 Bucket for Virto Commerce Media & Catalog Assets
resource "aws_s3_bucket" "media_assets" {
  bucket        = var.media_bucket_name
  force_destroy = true

  tags = {
    Environment = "Local-Floci"
    Project     = "VirtoCommerce"
    ManagedBy   = "Terraform"
  }
}

# 2. SQS Queue for Asynchronous Order & Event Processing
resource "aws_sqs_queue" "order_queue" {
  name                      = var.order_queue_name
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "Local-Floci"
    Project     = "VirtoCommerce"
  }
}

# 3. IAM Role for Virto Platform Service
resource "aws_iam_role" "platform_role" {
  name = "virto-commerce-platform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# 4. IAM Policy for S3 Media Bucket Access
resource "aws_iam_policy" "s3_access_policy" {
  name        = "virto-commerce-s3-access-policy"
  description = "Allows Virto Commerce Platform to read and write to the catalog media bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.media_assets.arn,
          "${aws_s3_bucket.media_assets.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "platform_attach" {
  role       = aws_iam_role.platform_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}
