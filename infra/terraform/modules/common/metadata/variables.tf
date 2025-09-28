variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "extra" {
  type    = map(string)
  default = {}
}
