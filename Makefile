-include configs/bot.env
export mode

project_name := voice-bot
compose_file := dockerfiles/docker-compose.yml
dev_compose_file := dockerfiles/docker-compose.dev.yml
compose := docker-compose -p $(project_name) -f $(compose_file)

ifeq ($(mode), development)
	compose := $(compose) -f $(dev_compose_file)
endif

h: help
help:
	@echo -e "\033[1mUSAGE\033[0m"
	@echo "  make COMMAND"
	@echo ""
	@echo "Commands:"
	@echo "  rl, run_local		Running locally for development"
	@echo "  b, build		Build all containers"
	@echo "  u, up, run, install	Build and up containers"
	@echo "  bu, build_and_up	Rebuild and up containers"
	@echo "  rm, remove		Stop and remove containers"
	@echo "  stop			Stop containers"
	@echo "  start			Start containers"
	@echo "  restart		Restart containers"
	@echo "  ps			Show information about running containers"
	@echo "  psa			Show information about all containers"
	@echo "  t, top		Show detailed information about all containers"
	@echo "  sh, term		Connect to container with bot"
	@echo "  sl, show_logs		Show logs"
	@echo "  sdl, show_docker_logs	Show docker logs"
	@echo "  style			Run black and isort for python code"
	@echo "  gc, generate_configs	Generate configuration files"
	@echo "  gs, generate_secrets	Generate passwords"
	@echo "  migrate		Apply migrations"
	@echo "  makemigrations	Create migrations"
	@echo "  add_voices_in_db	Add voice messages to the database"
	@echo "  h, help		Show help page"

	@echo ""
	@echo -e "\033[1mEXAMPLES\033[0m"
	@echo "  $$ make up"
	@echo "  $$ make build"
	@echo "  $$ make build_and_up"
	@echo ""
	@echo -e "\033[1mNOTE\033[0m: For other container commands use docker or docker-compose."

rl: run_local
run_local:
	poetry run python src/run.py

b: build
build:
	$(compose) build

u: install
up: install
run: install
install:
	$(compose) up -d

bu: build_and_up
build_and_up:
	$(compose) up -d --build $(service)

rm: remove
remove:
	$(compose) rm -fs

stop:
	$(compose) stop

start:
	$(compose) start

restart:
	$(compose) restart

ps:
	$(compose) ps

psa:
	$(compose) ps -a

t: top
top:
	$(compose) top

sh: term
term:
	$(compose) exec bot bash

sh_db: term_db
term_db:
	$(compose) exec db bash

sl: show_logs
show_logs:
	cat logs/bot.log

sdl: show_docker_logs
show_docker_logs:
	$(compose) logs -f $(service)

style:
	black src
	isort src

gc: generate_configs
generate_configs:
	cp configs/db.env.example configs/db.env
	cp configs/bot.env.example configs/bot.env

migrate:
	$(compose) exec bot alembic upgrade head

makemigrations:
	$(compose) exec bot alembic revision --autogenerate -m "$(title)"

ssm: show_sql_migrations
show_sql_migrations:
	$(compose) exec bot alembic upgrade head --sql

add_voices_in_db:
	$(compose) exec bot python scripts/add_voices_in_db.py

gs: generate_secrets
generate_secrets:
	@echo "postgres password:" $(shell python -c "import os; print(os.urandom(32).hex())")
