variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for deployment"
}

variable "floci_endpoint" {
  type        = string
  default     = "http://localhost:4566"
  description = "Local Floci AWS emulator endpoint"
}

variable "media_bucket_name" {
  type        = string
  default     = "virto-commerce-media-assets"
  description = "Name of the S3 bucket for media and catalog uploads"
}

variable "order_queue_name" {
  type        = string
  default     = "virto-order-processing-queue"
  description = "Name of the SQS queue for order integration"
}
