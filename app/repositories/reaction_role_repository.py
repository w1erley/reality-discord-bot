from app.models import ReactionRoleConfig


class ReactionRoleRepository:
    async def upsert(
        self,
        *,
        guild_id: int,
        channel_id: int,
        message_id: int,
        emoji: str,
        role_id: int,
    ) -> ReactionRoleConfig:
        config, _ = await ReactionRoleConfig.update_or_create(
            message_id=message_id,
            emoji=emoji,
            defaults={
                "guild_id": guild_id,
                "channel_id": channel_id,
                "role_id": role_id,
            },
        )
        return config

    async def role_for_reaction(self, message_id: int, emoji: str) -> int | None:
        config = await ReactionRoleConfig.get_or_none(
            message_id=message_id, emoji=emoji
        )
        return config.role_id if config else None

    async def list_for_guild(self, guild_id: int) -> list[ReactionRoleConfig]:
        return await ReactionRoleConfig.filter(guild_id=guild_id)

    async def delete_for_channel(self, guild_id: int, channel_id: int) -> int:
        return await ReactionRoleConfig.filter(
            guild_id=guild_id, channel_id=channel_id
        ).delete()
