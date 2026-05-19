import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from app.domain.emoji import EmojiToken
from app.presentation.embeds import error, primary


class ReactionRoles(commands.Cog, name="reaction_roles"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.service = bot.services.reaction_roles

    @commands.hybrid_group(
        name="reactionrole",
        description="Manage reaction-role bindings on pinned messages.",
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True, add_reactions=True)
    async def reactionrole(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            await context.send(
                embed=primary(
                    "**Subcommands:**\n"
                    "`set <channel> <emoji> <role>` — bind an emoji on the channel's latest pinned message to a role.\n"
                    "`clear <channel>` — remove all bindings for a channel.\n"
                    "`list` — list bindings in this server."
                )
            )

    @reactionrole.command(
        name="set",
        description="Bind an emoji on the channel's latest pinned message to a role.",
    )
    @app_commands.describe(
        channel="Channel whose latest pinned message will receive the reaction.",
        emoji="Emoji users react with to get the role.",
        role="Role to grant.",
    )
    async def reactionrole_set(
        self,
        context: Context,
        channel: discord.TextChannel,
        emoji: str,
        role: discord.Role,
    ) -> None:
        try:
            token = EmojiToken.from_string(emoji)
        except ValueError as e:
            await context.send(embed=error(str(e)), ephemeral=True)
            return

        pins = await channel.pins()
        if not pins:
            await context.send(
                embed=error(
                    f"{channel.mention} has no pinned messages. Pin one first."
                ),
                ephemeral=True,
            )
            return

        if role >= context.guild.me.top_role:
            await context.send(
                embed=error("My top role must be above the role you want to assign."),
                ephemeral=True,
            )
            return

        message = pins[0]
        try:
            await message.add_reaction(token.key)
        except discord.HTTPException:
            await context.send(
                embed=error(
                    f"Could not add reaction {token}. Is it a valid emoji I have access to?"
                ),
                ephemeral=True,
            )
            return

        await self.service.bind(
            guild_id=context.guild.id,
            channel_id=channel.id,
            message_id=message.id,
            emoji=token,
            role_id=role.id,
        )
        await context.send(
            embed=primary(
                f"Bound {token} on [this pinned message]({message.jump_url}) "
                f"in {channel.mention} → {role.mention}."
            )
        )

    @reactionrole.command(
        name="clear",
        description="Remove all reaction-role bindings for a channel.",
    )
    @app_commands.describe(channel="Channel to clear bindings for.")
    async def reactionrole_clear(
        self, context: Context, channel: discord.TextChannel
    ) -> None:
        removed = await self.service.clear_channel(context.guild.id, channel.id)
        await context.send(
            embed=primary(f"Removed {removed} binding(s) for {channel.mention}.")
        )

    @reactionrole.command(
        name="list",
        description="List reaction-role bindings in this server.",
    )
    async def reactionrole_list(self, context: Context) -> None:
        configs = await self.service.list_for_guild(context.guild.id)
        embed = primary(title="Reaction roles")
        if not configs:
            embed.description = "No bindings configured."
        else:
            embed.description = "\n".join(
                f"<#{c.channel_id}> · {c.emoji} → <@&{c.role_id}> (msg `{c.message_id}`)"
                for c in configs
            )
        await context.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        await self._toggle_role(payload, add=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        await self._toggle_role(payload, add=False)

    async def _toggle_role(
        self, payload: discord.RawReactionActionEvent, *, add: bool
    ) -> None:
        if payload.guild_id is None or payload.user_id == self.bot.user.id:
            return

        token = EmojiToken.from_string(str(payload.emoji))
        role_id = await self.service.role_for_reaction(payload.message_id, token)
        if role_id is None:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.HTTPException:
                return
        if member.bot:
            return

        try:
            if add:
                await member.add_roles(role, reason="Reaction role")
            else:
                await member.remove_roles(role, reason="Reaction role")
        except discord.Forbidden:
            self.bot.logger.warning(
                f"Missing permissions to {'add' if add else 'remove'} role {role.id} for {member.id} in guild {guild.id}"
            )
        except discord.HTTPException as e:
            self.bot.logger.warning(f"Failed to toggle reaction role: {e}")


async def setup(bot) -> None:
    await bot.add_cog(ReactionRoles(bot))
