# VoiceBot

VoiceBot is a cool bot that will help you communicate using voice messages in the popular Telegram messenger. Just follow the link below and hit start!

The official bot is only available at this link: https://t.me/vosaybot

- [VoiceBot](#voicebot)
- [Dependencies:](#dependencies)
- [Launch preparation](#launch-preparation)
  - [Configuration files](#configuration-files)
  - [Mode parameter](#mode-parameter)
- [Launch of the project](#launch-of-the-project)
  - [Migrations](#migrations)
    - [Applying migrations](#applying-migrations)
    - [Creating migrations](#creating-migrations)
- [Logs](#logs)
- [Debugging](#debugging)

# Dependencies:

* python 3.10
* poetry
* make
* black
* isort
* docker
* docker-compose

# Launch preparation

## Configuration files

First you need to create configuration files. You can do this with the following command:

```
$ make generate_configs # or make gc
```

After that, fill in the contents of the generated files.

To generate passwords, you can use the command:

```
$ make generate_secrets # or make gs
```

The generated passwords will simply be displayed on the screen, they will not be automatically written to the env file.

## Mode parameter

The mode parameter in the backend.env file determines in which mode the project will be launched. There are two modes available:

* development - to run in developer mode;
* production - to run in production mode.

# Launch of the project

After the configuration files have been created, the project can be run. To do this, you need to use the following command:

```
$ make build_and_install # or make build && make install or make bu
```

The Makefile also has a number of useful commands:

```
$ make help # print help
$ make build # build containers
$ make remove # remove containers
$ make stop # stop containers
$ make start # start containers
$ make restart # restart containers
$ make term # connect to container shell
$ make style # format code with black and isort
```

For a complete list of commands, use the `make help` command.

> Note: If there have been changes to the code, use the `make bu` or `make bu service=bot` command.

## Migrations

### Applying migrations

To apply existing migrations to a database, use the following command:

```
$ make migrate
```

### Creating migrations

To create new migrations, use the following command:

```
$ make makemigrations title="Migration title in lowercase separated by spaces"
```

# Logs

Log files are written to the logs/bot.log file.

To view the logs, use the `make show_logs` command or `make show_docker_logs` to view the logs in the container.

> Note: The commands above have aliases `make sl` and `make sdl` respectively.

# Debugging

In order to enable debugging, you need to enable development mode and set debug to True in the backend.env file:

```
mode=development
debug=True
```

After that, run the project as described in the [Launch of the project](#launch-of-the-project) section.

Debug mode is running and the debugger in the container is waiting for a connection. Connect to it through your IDE using the available tools.

Solutions for VSCode:

* https://code.visualstudio.com/docs/python/debugging
* https://www.youtube.com/watch?v=qCCj7qy72Bg

> Note: In order for VSCode to associate the local and remote project directories, in the launch.json file with the debug settings, set the *localRoot* variable to ${workspaceFolder}/bot.
