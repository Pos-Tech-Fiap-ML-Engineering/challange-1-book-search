output "task_execution_role_arn" {
  description = "ARN da role de execução do ECS"
  value       = aws_iam_role.task_execution.arn
}

output "task_role_arn" {
  description = "ARN da task role do ECS"
  value       = aws_iam_role.task_role.arn
}
