output "vpc_id" {
  description = "ID da VPC"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Subnets privadas"
  value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
  description = "Subnets públicas"
  value       = module.vpc.public_subnets
}

# Útil quando você cria SGs aqui
output "default_security_group_id" {
  description = "Default SG da VPC (se precisar)"
  value       = module.vpc.default_security_group_id
}

# Exponha outros que precisar:
# output "private_route_table_ids" { value = module.vpc.private_route_table_ids }
# output "natgw_ids"              { value = module.vpc.natgw_ids }
