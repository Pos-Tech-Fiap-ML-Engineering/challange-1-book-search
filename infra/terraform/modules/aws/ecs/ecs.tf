resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 3
}

resource "aws_ecs_cluster" "this" {
  name = var.project_name
}

resource "aws_security_group" "service" {
  name        = "${var.project_name}-svc-sg"
  description = "Allow outbound to internet/NAT"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = var.project_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = tostring(var.ecs_cpu)
  memory                   = tostring(var.ecs_memory)
  execution_role_arn       = var.task_execution_role_arn
  task_role_arn            = var.task_role_arn
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name         = var.project_name
      image        = "${var.ecr_repository_url}:${var.ecr_image_tag}"
      essential    = true
      portMappings = [{ containerPort = 8000, hostPort = 8000, protocol = "tcp" }]
      environment = [
        { name = "GUNICORN_WORKERS", value = "4" },
        { name = "TZ", value = "UTC" },
        { name = "PYTHONUNBUFFERED", value = "1" }
      ]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = aws_cloudwatch_log_group.app.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
      healthCheck = {
        command     = ["CMD-SHELL", "curl -fsS http://127.0.0.1:8000/api/v1/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  lifecycle {
    # Se você REALMENTE quer que o TF não altere a TD quando mudar o JSON:
    ignore_changes = [container_definitions]
    # (opcional) às vezes também ignoram cpu/memory se o time alterna isso fora do TF
    # ignore_changes = [container_definitions, cpu, memory]
  }
}

# Service (ligado ao ALB em alb.tf)
resource "aws_ecs_service" "app" {
  name                               = "${var.project_name}-svc"
  cluster                            = aws_ecs_cluster.this.id
  task_definition                    = aws_ecs_task_definition.app.arn
  desired_count                      = var.ecs_desired_count
  launch_type                        = "FARGATE"
  enable_execute_command             = true
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200

  network_configuration {
    subnets          = var.vpc_private_subnet_ids
    security_groups  = [aws_security_group.service.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.project_name
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.http]

  lifecycle {
    ignore_changes = [task_definition] # ✅ atributo do próprio aws_ecs_service
    # se usar autoscaling, costuma-se ignorar também desired_count:
    # ignore_changes = [task_definition, desired_count]
  }
}
