variable "region" {
  type = string
}

variable "project_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "vpc_private_subnet_ids" {
  type = list(string)
}

variable "vpc_public_subnet_ids" {
  type = list(string)
}

variable "task_execution_role_arn" {
  type = string

}

variable "task_role_arn" {
  type = string
}

variable "ecr_repository_url" {
  type = string
}

variable "ecr_image_tag" {
  type = string
}

variable "ecs_desired_count" {
  type    = number
}

variable "ecs_cpu" {
  type    = string
}

variable "ecs_memory" {
  type    = string
}
