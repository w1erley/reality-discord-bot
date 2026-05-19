import discord

from app.presentation.colors import EmbedColor


def _build(
    description: str | None,
    color: EmbedColor,
    title: str | None = None,
) -> discord.Embed:
    embed = discord.Embed(color=int(color))
    if title is not None:
        embed.title = title
    if description is not None:
        embed.description = description
    return embed


def primary(description: str | None = None, *, title: str | None = None) -> discord.Embed:
    return _build(description, EmbedColor.PRIMARY, title)


def success(description: str | None = None, *, title: str | None = None) -> discord.Embed:
    return _build(description, EmbedColor.SUCCESS, title)


def error(description: str, *, title: str | None = None) -> discord.Embed:
    return _build(description, EmbedColor.ERROR, title)


def warning(description: str | None = None, *, title: str | None = None) -> discord.Embed:
    return _build(description, EmbedColor.WARNING, title)


def info(description: str | None = None, *, title: str | None = None) -> discord.Embed:
    return _build(description, EmbedColor.INFO, title)
