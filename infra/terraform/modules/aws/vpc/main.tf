module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name               = "${var.project_name}-vpc"
  cidr               = local.vpc_cidr
  azs                = local.azs_selected
  public_subnets     = local.public_subnets
  private_subnets    = local.private_subnets
  enable_nat_gateway = true
  single_nat_gateway = true
}