# Garden Game Manager

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-24.0.1-blue?logo=docker&logoColor=white&style=flat-square)
![SQLModel](https://img.shields.io/badge/SQLModel-0.1.0-blue?logo=sqlmodel&logoColor=white&style=flat-square)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3.0-blue?logo=discord&logoColor=white&style=flat-square)

## Description

The **Garden Game Manager** is a discord bot written in Python using discord.py and SQLModel.

It is designed to manage my homebrew RPG campaign through discord enabling players to track their progress, manage their characters and interact with the game mechanics in a dynamic and integrated way.

It comes with a set of player cogs as well as admin cogs for the DM's use.

The scope of this project is to meet the needs of my campaign and to be easily extensible for future campaigns. As such, new features will be added as needs come up.

## Setup

### Docker

To run the bot, you can use docker compose.

```bash
docker compose up -d
```

### Local

To run the bot locally, you should first create a virtual environment and install the dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then you can run the bot with the following command:

```bash
python src/client.py
```
