variable "project_name" {
  type = string
}

variable "azs_count" {
  type        = number
  default     = 2
  description = "Quantidade de AZs a usar (2 ou 3)"
}
