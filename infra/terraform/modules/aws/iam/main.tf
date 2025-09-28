data "aws_iam_policy_document" "task_exec_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project_name}-task-exec"
  assume_role_policy = data.aws_iam_policy_document.task_exec_assume.json
}

# Permite pull no ECR + logs
resource "aws_iam_role_policy_attachment" "task_exec_ecr" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# (Opcional) Param Store / Secrets Manager
# resource "aws_iam_role_policy_attachment" "task_exec_ssm" {
#   role       = aws_iam_role.task_execution.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
# }

resource "aws_iam_role" "task_role" {
  name               = "${var.project_name}-task"
  assume_role_policy = data.aws_iam_policy_document.task_exec_assume.json
}
