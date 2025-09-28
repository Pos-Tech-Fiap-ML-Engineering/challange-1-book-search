# ECR
output "ecr_repository_url" {
  value = module.ecr.repository_url
}

# ECS
output "ecs_cluster_name" {
  value = module.ecs.ecs_cluster_name
}

output "ecs_cluster_arn" {
  value = module.ecs.ecs_cluster_arn
}

output "ecs_service_name" {
  value = module.ecs.ecs_service_name
}

output "ecs_service_id" {
  value = module.ecs.ecs_service_id
}

# Task Definition
output "ecs_task_definition_arn" {
  value = module.ecs.task_definition_arn
}
output "ecs_task_definition_family" {
  value = module.ecs.task_definition_family
}

# Logs / SG
output "ecs_log_group_name" {
  value = module.ecs.cw_log_group_name
}
output "ecs_service_security_group_id" {
  value = module.ecs.sg_service_security_group_id
}

# ALB
output "alb_lb_target_group_arn" {
  value = module.ecs.alb_lb_target_group_arn
}

output "alb_dns_name" {
  value = module.ecs.alb_dns_name
}

output "alb_service_url" {
  value = module.ecs.alb_service_url
}

output "alb_health_url" {
  value = module.ecs.alb_health_url
}
