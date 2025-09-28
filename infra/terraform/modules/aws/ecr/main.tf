resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}-ecr"
  image_tag_mutability = "MUTABLE"
}

# resource "aws_ecr_lifecycle_policy" "app" {
#   repository = aws_ecr_repository.app.name
#   policy = jsonencode({
#     rules = [
#       {
#         rulePriority = 1
#         description  = "expire old"
#         selection = {
#           tagStatus   = "any"
#           countType   = "imageCountMoreThan"
#           countNumber = 30
#         }
#         action = {
#           type = "expire"
#         }
#       }
#     ]
#   })
# }
