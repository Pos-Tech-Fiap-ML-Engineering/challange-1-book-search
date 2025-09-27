variable "region" {
  description = "Região onde os recursos serão criados na aws"
  type        = string
  default     = "eu-central-1"
  nullable    = false
}