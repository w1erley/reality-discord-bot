import os
import platform
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from app import db
from app.cogs import COGS
from app.config import Settings, get_settings
from app.container import ServiceContainer
from app.logging_config import build_logger
from app.presentation.colors import EmbedColor


class DiscordBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.prefix),
            intents=intents,
            help_command=None,
        )
        self.settings = settings
        self.logger = build_logger()
        self.bot_prefix = settings.prefix
        self.invite_link = settings.invite_link
        self.services = ServiceContainer()

    async def setup_hook(self) -> None:
        self.logger.info(f"Logged in as {self.user.name if self.user else '?'}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")

        await db.init(self.settings.db_path)

        for name in COGS:
            try:
                await self.load_extension(f"app.cogs.{name}")
                self.logger.info(f"Loaded extension '{name}'")
            except Exception as e:
                self.logger.error(
                    f"Failed to load extension {name}\n{type(e).__name__}: {e}"
                )

        self.status_task.start()

    async def close(self) -> None:
        await db.close()
        await super().close()

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        statuses = ["антон", "крикушенко"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        full_command_name = context.command.qualified_name
        executed_command = str(full_command_name.split(" ")[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=(
                    f"**Please slow down** - You can use this command again in "
                    f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
                    f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
                    f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}."
                ),
                color=EmbedColor.ERROR,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            await context.send(
                embed=discord.Embed(
                    description="You are not the owner of the bot!",
                    color=EmbedColor.ERROR,
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            await context.send(
                embed=discord.Embed(
                    description="You are missing the permission(s) `"
                    + ", ".join(error.missing_permissions)
                    + "` to execute this command!",
                    color=EmbedColor.ERROR,
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await context.send(
                embed=discord.Embed(
                    description="I am missing the permission(s) `"
                    + ", ".join(error.missing_permissions)
                    + "` to fully perform this command!",
                    color=EmbedColor.ERROR,
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await context.send(
                embed=discord.Embed(
                    title="Error!",
                    description=str(error).capitalize(),
                    color=EmbedColor.ERROR,
                )
            )
        else:
            raise error


def run() -> None:
    settings = get_settings()
    DiscordBot(settings).run(settings.token)
