output "s3_bucket_name" {
  value       = aws_s3_bucket.media_assets.bucket
  description = "Created S3 Media Bucket name"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.media_assets.arn
  description = "Created S3 Media Bucket ARN"
}

output "sqs_queue_url" {
  value       = aws_sqs_queue.order_queue.url
  description = "Created SQS Queue URL"
}

output "iam_role_arn" {
  value       = aws_iam_role.platform_role.arn
  description = "Created IAM Role ARN"
}
