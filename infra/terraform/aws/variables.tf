variable "environment" {
  description = "Ambiente ao qual pertence os recursos"
  type        = string
  default     = "challange"
}

variable "extra" {
  description = "Extra informações"
  type        = map(string)
  default     = { Owner = "ss-team" }
}

variable "ecs_cpu" {
  description = "CPU das tarefas no ECS"
  type        = string
  default     = 512
}

variable "ecs_memory" {
  description = "Memória das tarefas no ECS"
  type        = string
  default     = 1024
}

variable "region" {
  description = "Região onde os recursos serão criados na aws"
  type        = string
  nullable    = false
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  nullable    = false
}

variable "ecs_desired_count" {
  description = "Número de tasks das tarefas no ECS"
  type        = number
  nullable    = false
}

variable "ecr_repository_tag" {
  description = "Nome do repositório mas tag da imagem a ser utilizada pela task no ec"
  type        = string
  nullable    = false
}

