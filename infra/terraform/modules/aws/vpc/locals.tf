locals {
  vpc_cidr = "10.40.0.0/16"

  azs_selected = slice(
    data.aws_availability_zones.available.names,
    0,
    min(var.azs_count, length(data.aws_availability_zones.available.names))
  )

  public_subnets  = [for i, _ in local.azs_selected : cidrsubnet(local.vpc_cidr, 8, i + 1)]
  private_subnets = [for i, _ in local.azs_selected : cidrsubnet(local.vpc_cidr, 8, 10 + (i + 1))]
}
