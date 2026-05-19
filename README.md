# reality-discord-bot

Personal Discord bot. Python 3.12, discord.py, Tortoise ORM, SQLite.

## Run

```bash
cp .env.example .env
# fill in TOKEN and (optional) PREFIX / INVITE_LINK
mkdir -p data
docker compose up -d --build
```

Logs: `docker compose logs -f`. SQLite file persists at `./data/database.db`.

## Discord setup

1. Enable **Server Members Intent** in the Discord developer portal for the bot.
2. Invite the bot with `Manage Roles`, `Add Reactions`, `Manage Messages`,
   `Kick Members`, `Ban Members` as needed for the features you use.
3. The bot's top role must be above any role it manages (reaction roles, etc).

## Features

- **Reaction roles** on pinned messages — `/reactionrole set #channel 🎉 @Role`
  binds the latest pinned message in `#channel`. `/reactionrole clear #channel`
  / `/reactionrole list` to manage. Requires `Manage Roles`.
- **Moderation** — `/kick`, `/ban`, `/hackban`, `/warning add|remove|list`,
  `/purge`, `/nick`, `/archive`.
- **General** — `/help`, `/botinfo`, `/serverinfo`, `/ping`, `/invite`,
  `/8ball`, `/bitcoin`, `/feedback`.
- **Fun** — `/randomfact`, `/coinflip`, `/rps`.
- **Owner** — `sync` / `unsync` / `load` / `unload` / `reload` / `shutdown`
  (prefix commands, owner only).

## Project layout

```
bot.py                                  # entrypoint
app/
  bot.py                                # DiscordBot class
  config.py                             # pydantic-settings
  container.py                          # service wiring
  db.py                                 # Tortoise init/close
  logging_config.py
  cogs/                                 # Discord adapters
  domain/                               # pure value objects / enums
  models/                               # Tortoise ORM models
  repositories/                         # DB access
  services/                             # business logic
  presentation/                         # embed factories, colors
```

New feature: add a model, repo, service, cog; register the service in
`app/container.py` and the cog name in `app/cogs/__init__.py`.
