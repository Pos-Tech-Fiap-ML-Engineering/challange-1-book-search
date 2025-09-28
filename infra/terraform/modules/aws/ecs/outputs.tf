# ECS
output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.this.arn
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "ecs_service_id" {
  value = aws_ecs_service.app.id
}

# Task Definition
output "task_definition_arn" {
  value = aws_ecs_task_definition.app.arn
}
output "task_definition_family" {
  value = aws_ecs_task_definition.app.family
}

# Logs / SG
output "cw_log_group_name" {
  value = aws_cloudwatch_log_group.app.name
}
output "sg_service_security_group_id" {
  value = aws_security_group.service.id
}

# ALB
output "alb_lb_target_group_arn" {
  value = aws_lb_target_group.app.arn
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "alb_service_url" {
  value = "${local.http_schema}://${aws_lb.app.dns_name}"
}

output "alb_health_url" {
  value = "${local.http_schema}://${aws_lb.app.dns_name}/api/v1/health"
}