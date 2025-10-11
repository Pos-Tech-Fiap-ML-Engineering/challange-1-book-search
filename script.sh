#!/usr/bin/env bash

set -Eeuo pipefail

############################################
# Config & helpers
############################################

# Cores (desativa se não for TTY ou se NO_COLOR estiver setado)
if [[ -t 2 && -z "${NO_COLOR:-}" ]]; then
  RED=$'\033[31m'
  YELLOW=$'\033[33m'
  RESET=$'\033[0m'
else
  RED='' ; YELLOW='' ; RESET=''
fi

epoch_ts() {
  date -u +%s 2>/dev/null || python3 - <<'PY'
import time; print(int(time.time()))
PY
}

# Logging
log()       { printf "%s - %s\n" "$(date '+%F %T')" "$*"; }
log_warn()  { printf "${YELLOW}%s - %s${RESET}\n" "$(date '+%F %T')" "$*" >&2; }
log_error() { printf "${RED}%s - %s${RESET}\n"   "$(date '+%F %T')" "$*" >&2; }

die() {
  local code=1
  [[ "${1-}" =~ ^[0-9]+$ ]] && { code="$1"; shift; }
  log_error "ERROR: $*"
  exit "$code"
}

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$ROOT_DIR" || exit

load_default_configs(){
  export AWS_REGION="us-east-1"
  export ENVIRONMENT="dev"
  export PROJECT_NAME="aws-cloud-challange-${ENVIRONMENT}"
  export TF_DIR="${ROOT_DIR}/infra/terraform/aws"
  export TF_VARS=(
    "-var=region=${AWS_REGION}"
    "-var=project_name=${PROJECT_NAME}"
    "-var=ecr_repository_tag=NONE"
  )
  export DOCKER_DIR="${ROOT_DIR}/infra/dockerfile"
  export ECR_REPOSITORY_URL="$(infra_get_output "ecr_repository_url")" || die "Falha ao ler output 'ecr_repository_url' do Terraform"
  export ECR_REPOSITORY_NAME="$(basename "$ECR_REPOSITORY_URL")"
  export ECS_CLUSTER="$(infra_get_output "ecs_cluster_name")" || die "Falha ao ler output 'ecs_cluster_name' do Terraform"
  export ECS_SERVICE="$(infra_get_output "ecs_service_name")" || die "Falha ao ler output 'ecs_service_name' do Terraform"
  export ECS_DESIRED_ON_DEPLOY=2
  export GIT_SHA="$(git rev-parse --short=12 HEAD 2>/dev/null || echo 'local')"
#  export IMAGE_TAG="${GIT_SHA:-latest}"
  export IMAGE_TAG="$(epoch_ts)"
  export DOCKER_IMAGE_NAME="${ECR_REPOSITORY_URL}:${IMAGE_TAG}"
#  export DOCKER_IMAGE_NAME="${ECR_REPOSITORY_URL}:latest"

}

load_aws_secrets() {
  local AWS_CREDENTIALS_FILE="${TF_DIR}/.aws_credentials"

  if [[ -f "$AWS_CREDENTIALS_FILE" ]]; then
    # Não sobrescrever se já vier do ambiente (útil para CI/CD)
    : "${AWS_ACCESS_KEY_ID:=}"
    : "${AWS_SECRET_ACCESS_KEY:=}"
    if [[ -n "$AWS_ACCESS_KEY_ID" && -n "$AWS_SECRET_ACCESS_KEY" ]]; then
      echo "ℹ️  Variáveis AWS já definidas no ambiente; não vou ler o arquivo."
      return 0
    fi

    # Lê o arquivo linha a linha
    while IFS='=' read -r key value || [[ -n "$key" ]]; do
      # Remove \r (CRLF do Windows) e espaços ao redor
      key="$(echo "${key%$'\r'}" | xargs)"
      value="$(echo "${value%$'\r'}" | xargs)"

      # Pula linhas vazias e comentários
      [[ -z "$key" || "$key" =~ ^# ]] && continue

      case "$key" in
        aws_access_key_id)
          if [[ -n "$value" ]]; then
            export AWS_ACCESS_KEY_ID="$value"
          else
            echo "⚠️  aws_access_key_id está vazio em $AWS_CREDENTIALS_FILE"
          fi
          ;;
        aws_secret_access_key)
          if [[ -n "$value" ]]; then
            export AWS_SECRET_ACCESS_KEY="$value"
          else
            echo "⚠️  aws_secret_access_key está vazio em $AWS_CREDENTIALS_FILE"
          fi
          ;;
      esac
    done < "$AWS_CREDENTIALS_FILE"

    # Validação final
    if [[ -z "${AWS_ACCESS_KEY_ID:-}" || -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
      echo "❌ Credenciais AWS incompletas ou inválidas em $AWS_CREDENTIALS_FILE"
      return 1
    fi
  else
    echo "⚠️  Arquivo de credenciais não encontrado: $AWS_CREDENTIALS_FILE"
    return 1
  fi
}

############################################
# Utils
############################################
utils_logs_ecs_events() {
  log "Acompanhando eventos do serviço ECS (últimos 50)..."
  aws ecs describe-services --cluster "$ECS_CLUSTER" --services "$ECS_SERVICE" --region "$AWS_REGION" \
    | jq -r '.services[0].events[] | "\(.createdAt)  \(.message)"' \
    | head -n 50
  echo
  log "Dica: use o CloudWatch Logs para ver os logs das tasks."
}

utils_show_details_version() {
  echo "${PROJECT_NAME}@${ENVIRONMENT} image=${DOCKER_IMAGE_NAME}"
}

############################################
# Dependency checks
############################################
check_required_dependencies_commands() {
  local missing=()
  local required_dependencies="python poetry docker terraform aws jq grep awk"

  for cmd in $required_dependencies; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      printf "❌ %s não encontrado no PATH\n" "$cmd"
      missing+=("$cmd")
    fi
  done

  if [[ ${#missing[@]} -gt 0 ]]; then
    echo
    echo "⚠️  Os seguintes comandos estão faltando: ${missing[*]}"
    echo "Instale-os antes de continuar:"
    echo
    for m in "${missing[@]}"; do
      case "$m" in
        python|python3)
          echo "  • Python: baixe em https://www.python.org/downloads/ ou use winget: winget install Python.Python.3.12"
          ;;
        terraform)
          echo "  • Terraform: https://developer.hashicorp.com/terraform/downloads ou use winget: winget install HashiCorp.Terraform"
          ;;
        jq)
          echo "  • jq: https://jqlang.github.io/jq/download/ ou winget install jqlang.jq"
          ;;
        grep)
          echo "  • grep: no Windows, use Git Bash ou winget install GnuWin32.grep"
          ;;
        *)
          echo "  • $m: instale manualmente e garanta que esteja no PATH"
          ;;
      esac
    done
    exit 1
  fi
}

############################################
# Docker
############################################
docker_in_dir() (
  [[ -d "$DOCKER_DIR" ]] || die "DOCKER_DIR não encontrado: $DOCKER_DIR"
  pushd "$DOCKER_DIR" >/dev/null || return 1
  trap 'popd >/dev/null' RETURN
  "$@"
)

############################################
# Infra (Terraform)
############################################
infra_get_output(){
  local key="$1"
  infra_in_dir terraform output --json | jq -r --arg k "$key" '.[$k].value'
}

infra_show_all_outputs(){
  infra_in_dir terraform output --json
}

aws_ecr_login() {
  log "Fazendo login no ECR: ${ECR_REPOSITORY_URL}"
  aws --region "$AWS_REGION" ecr get-login-password \
    | docker login --username AWS --password-stdin "$ECR_REPOSITORY_URL"
}

infra_in_dir() (
  [[ -d "$TF_DIR" ]] || die "TF_DIR não encontrado: $TF_DIR"
  pushd "$TF_DIR" >/dev/null || return 1
  trap 'popd >/dev/null' RETURN
  "$@"
)

terraform_init_cb() {
  log "terraform init..."
  terraform init -upgrade
  log "Selecionando/criando workspace"
  terraform workspace select "$ENVIRONMENT" 2>/dev/null || terraform workspace new "$ENVIRONMENT"
}

infra_init(){
  infra_in_dir terraform_init_cb
}

infra_plan(){
  log "terraform plan..."
  infra_in_dir terraform plan "${TF_VARS[@]}" -var=ecs_desired_count="$1" -var=ecr_repository_tag="$DOCKER_IMAGE_NAME"
}

infra_apply(){
  log "terraform apply..."
  infra_in_dir terraform apply "${TF_VARS[@]}" -var=ecs_desired_count="$1" -var=ecr_repository_tag="$DOCKER_IMAGE_NAME" # -auto-approve
  infra_show_all_outputs| jq . > infra.${ENVIRONMENT}.json
}

infra_destroy(){
  log "terraform destroy..."
  infra_in_dir terraform destroy "${TF_VARS[@]}" # -auto-approve
}

############################################
# CI (lint, tests unit & integration, coverage)
############################################
poe_run() {
  local task="$1"
  echo "Executando task '${task}'..."
  poetry run poe "$task" || {
    die "task $task não encontrada!"
  }
}

ci_setup_env(){
  poetry sync
}

ci_clean(){
  poe_run clean_all
}

ci_audit(){
  poe_run audit
}

ci_build(){
  poe_run fmt
  poe_run lint
  poe_run typecheck
}

ci_test_unit(){
  poe_run test_unit
}

ci_test_integration(){
  poe_run test_integration
}

ci_test_e2e(){
  poe_run test_e2e
}

############################################
# CD (build/push/deploy)
############################################
cd_scrape_books(){
    local mode="${1:-}"

    log "Scraping books"

    if [[ "$mode" != "execute_scrape" ]]; then
        log "⚠️  Execução do scraping ignorada"
        return 0
    fi


   if poetry run python -m src.scripts.Main; then
      log "✅ Scraping finalizado com sucesso"
   else
      log "❌ Erro ao executar o scraping"
      return 1
   fi
}

cd_build(){
  cd_scrape_books "$1"
  log "Docker build: ${DOCKER_IMAGE_NAME}"
  docker_in_dir docker build -t $DOCKER_IMAGE_NAME -f Dockerfile ../../
}

cd_push(){
  aws_ecr_login
  # Garante repositório ECR (idempotente)
  if ! aws ecr describe-repositories --repository-names "$ECR_REPOSITORY_NAME" --region "$AWS_REGION" >/dev/null 2>&1; then
    log "Criando repositório ECR: $ECR_REPOSITORY_NAME"
    aws ecr create-repository --repository-name "$ECR_REPOSITORY_NAME" --region "$AWS_REGION" >/dev/null
  fi
  log "Fazendo push: ${DOCKER_IMAGE_NAME}"
  docker push "${DOCKER_IMAGE_NAME}"
}


cd_deploy_app_mode() {
  aws_ecr_login
  log "Atualizando serviço ECS '${ECS_SERVICE}' no cluster '${ECS_CLUSTER}' com a imagem ${DOCKER_IMAGE_NAME}"

  # Estado atual do serviço
  local svc_json current desired_flag=() target
  svc_json="$(aws ecs describe-services --cluster "$ECS_CLUSTER" --services "$ECS_SERVICE" --region "$AWS_REGION")"
  current="$(echo "$svc_json" | jq -r '.services[0].desiredCount // 0')"

  # TaskDefinition atual
  TD_ARN="$(echo "$svc_json" | jq -r '.services[0].taskDefinition')"
  [[ -n "$TD_ARN" && "$TD_ARN" != "null" ]] || die "Não foi possível obter a task definition do serviço."

  # Descreve TD e gera nova com imagem atualizada
  NEW_TD_JSON="$(aws ecs describe-task-definition --task-definition "$TD_ARN" --region "$AWS_REGION")"
  UPDATED_TD_JSON="$(
  echo "$NEW_TD_JSON" \
  | jq --arg IMG "$DOCKER_IMAGE_NAME" --arg CN "${ECS_CONTAINER_NAME:-}" '
    .taskDefinition
    # atualiza a imagem do container (por nome se $CN setado, senão o primeiro)
    | .containerDefinitions =
        ( .containerDefinitions
          | if $CN != "" then
              (if any(.name; . == $CN) | not then
                 halt_error(1)
               else
                 map(if .name == $CN then .image = $IMG else . end)
               end)
            else
              (.[0].image = $IMG) as $defs | $defs
            end
        )
    # remove campos somente-leitura/gerados e listas de compatibilidade
    | del(.status, .revision, .taskDefinitionArn, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)
    # remove chaves de nível superior que estejam nulas (ex.: ephemeralStorage, runtimePlatform, cpu/memory nulos)
    | with_entries(select(.value != null))
  '
)"

  # Registra nova TD
  NEW_TD_ARN="$(
    aws ecs register-task-definition \
      --region "$AWS_REGION" \
      --cli-input-json "$(jq -c '.' <<<"$UPDATED_TD_JSON")" \
      | jq -r '.taskDefinition.taskDefinitionArn'
  )"
  log "Nova TaskDefinition: $NEW_TD_ARN"

  # Decide desired_count a aplicar neste deploy
  # 1) Se ECS_DESIRED_ON_DEPLOY foi definido, usa-o.
  # 2) Senão, se current==0, usa 1.
  if [[ -n "$ECS_DESIRED_ON_DEPLOY" ]]; then
    target="$ECS_DESIRED_ON_DEPLOY"
  elif [[ "$current" -eq 0 ]]; then
    target=1
  else
    target=""
  fi
  if [[ -n "$target" ]]; then
    desired_flag=(--desired-count "$target")
    log "DesiredCount atual: $current → escalando para: $target"
  else
    log "Mantendo DesiredCount atual: $current"
  fi

  # Atualiza o serviço com nova TD (e desired_count se aplicável)
  # Ex.: limite de 20 minutos
  trap 'echo "❌ Interrompido pelo usuário"; exit 130' INT

  log "Aguardando serviço estabilizar"

  if command -v timeout >/dev/null 2>&1; then
    timeout 20m aws ecs wait services-stable \
      --cluster "$ECS_CLUSTER" \
      --services "$ECS_SERVICE" \
      --region "$AWS_REGION" || die "Timeout: ECS não estabilizou em 20m."
  else
    aws ecs wait services-stable \
      --cluster "$ECS_CLUSTER" \
      --services "$ECS_SERVICE" \
      --region "$AWS_REGION" || die "Timeout: ECS não estabilizou no tempo padrão."
  fi

  log "Serviço estabilizado."
}

cd_deploy_terraform_mode() {
  aws_ecr_login

  infra_apply 2

   # Atualiza o serviço com nova TD (e desired_count se aplicável)
  # Ex.: limite de 20 minutos
  trap 'echo "❌ Interrompido pelo usuário"; exit 130' INT

  log "Aguardando serviço estabilizar"

  if command -v timeout >/dev/null 2>&1; then
    timeout 20m aws ecs wait services-stable \
      --cluster "$ECS_CLUSTER" \
      --services "$ECS_SERVICE" \
      --region "$AWS_REGION"
  else
    aws ecs wait services-stable \
      --cluster "$ECS_CLUSTER" \
      --services "$ECS_SERVICE" \
      --region "$AWS_REGION"
  fi

  log "Serviço estabilizado."
}

############################################
# Bootstrap script
############################################
check_required_dependencies_commands;
load_default_configs
load_aws_secrets

help() {
  cat <<'USAGE'
Uso: ./script.sh <alvo>

Utils:
  utils:logs_ecs_events               - mostra eventos recentes do ECS service
  utils:show_details_version          - exibe versão/imagem atual

Infra:
  infra_get_output                    - obtém infos output do terraform
  infra:show:all:outputs              - obtém todos outputs do terraform
  infra:init                          - terraform init + workspace
  infra:plan                          - terraform plan
  infra:apply                         - terraform apply
  infra:destroy                       - terraform destroy

CI:
  ci:setup:env                        - inicializar todos setups mecessários para execução CI
  ci:clean                            - limpa todo ambiente antes da execução
  ci:audit                            - realiza auditoria do repositório
  ci:build                            - realiza build do reposit´rio (fmt + lint + typecheck)
  ci:test:unit                        - executa testes unitários do projeto
  ci:test:integration                 - executa testes de integração do projeto
  ci:test:e2e                         - executa testes e2e do projeto
  ci:all                              - executa todo CI do projeto

CD:
  cd:build                            - docker build (tag: ECR/GIT_SHA) param  execute_scrape para fazer webscraping dos livros
  cd:push                             - login ECR, cria repo se preciso, push da imagem
  cd:deploy                           - atualiza ECS service com nova TaskDef (imagem atualizada)
  cd:build:push:deploy                - Realiza todas as tarefas cd:build cd:push cd:deploy

HELP:
  help                                - mostra este help

Exemplos:
  ./script.sh infra:apply
  ./script.sh ci:all
  ./script.sh cd:build && ./script.sh cd:push && ./script.sh cd:deploy
USAGE
}

############################################
# Dispatcher
############################################
target="${1:-help}"

case "$target" in

  utils:logs_ecs_events)
    utils_logs_ecs_events
    ;; 

  utils:show_details_version)
    utils_show_details_version
    ;;
  
  infra:show:all:outputs)
    infra_show_all_outputs
    ;;

  infra:get:output)
    infra_get_output "${2:-}"
    ;;

  infra:init)
    infra_init
    ;;

  infra:plan)
    infra_plan 0
    ;;

  infra:apply)
    infra_apply 0
    ;;

  infra:destroy)
    infra_destroy
    ;;

  ci:setup:env)
    ci_setup_env
    ;;

  ci:clean)
    ci_clean
    ;;

  ci:audit)
    ci_audit
    ;;

  ci:build)
    ci_build
    ;;

  ci:test:unit)
    ci_test_unit
    ;;

  ci:test:integration)
    ci_test_integration
    ;;

  ci:test:e2e)
    ci_test_e2e
    ;;

  ci:all)
    ci_clean
    ci_setup_env
    ci_audit
    ci_build
    ci_test_unit
    ci_test_integration
    ;;

  cd:build)
    cd_build "${2:-}"
    ;;

  cd:push)
    cd_push
    ;;

  cd:deploy)
    cd_deploy_terraform_mode
    ;;

  cd:build:push:deploy)
    cd_build "${2:-}"
    cd_push
    cd_deploy_terraform_mode
    ;;

  help|*)
    help;;
esac