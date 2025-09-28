resource "aws_security_group" "alb" {
  name   = "${var.project_name}-alb-sg"
  vpc_id = var.vpc_id

  # Habilita somente HTTP 80 (para demo)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "app" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.vpc_public_subnet_ids
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project_name}-tg"
  port        = 8000
  protocol    = "HTTP" # ALB -> ECS segue HTTP interno
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path                = "/api/v1/health"
    matcher             = "200"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    interval            = 30
    timeout             = 5
  }
}

# Listener HTTP :80 fazendo forward pro TG
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Permite tráfego do ALB (SG) para a porta 8000 do serviço no ECS
resource "aws_security_group_rule" "alb_to_service" {
  type                     = "ingress"
  from_port                = 8000
  to_port                  = 8000
  protocol                 = "tcp"
  security_group_id        = aws_security_group.service.id
  source_security_group_id = aws_security_group.alb.id
}
