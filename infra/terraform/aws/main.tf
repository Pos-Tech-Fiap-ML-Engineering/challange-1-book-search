terraform {
  required_version = ">=1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.63.0"
    }
  }
}

provider "aws" {
  region                   = var.region
  default_tags {
    tags = module.common-metadata.common_tags
  }
}

module "common-metadata" {
  source       = "../modules/common/metadata"
  project_name = var.project_name
  environment  = var.environment
  extra        = var.extra
}

module "iam" {
  source       = "../modules/aws/iam"
  project_name = module.common-metadata.project_name
}

module "vpc" {
  source       = "../modules/aws/vpc"
  project_name = module.common-metadata.project_name
}

module "ecr" {
  source       = "../modules/aws/ecr"
  project_name = module.common-metadata.project_name
}

module "ecs" {
  source                  = "../modules/aws/ecs"
  region                  = var.region
  project_name            = module.common-metadata.project_name
  ecs_desired_count       = var.ecs_desired_count
  ecs_cpu                 = var.ecs_cpu
  ecs_memory              = var.ecs_memory
  vpc_id                  = module.vpc.vpc_id
  vpc_private_subnet_ids  = module.vpc.private_subnet_ids
  vpc_public_subnet_ids   = module.vpc.public_subnet_ids
  task_execution_role_arn = module.iam.task_execution_role_arn
  task_role_arn           = module.iam.task_role_arn
  ecr_repository_url      = module.ecr.repository_url
  ecr_image_tag           = var.ecr_image_tag
}
