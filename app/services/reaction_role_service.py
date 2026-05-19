from app.domain.emoji import EmojiToken
from app.models import ReactionRoleConfig
from app.repositories.reaction_role_repository import ReactionRoleRepository


class ReactionRoleService:
    def __init__(self, repo: ReactionRoleRepository) -> None:
        self.repo = repo

    async def bind(
        self,
        *,
        guild_id: int,
        channel_id: int,
        message_id: int,
        emoji: EmojiToken,
        role_id: int,
    ) -> None:
        await self.repo.upsert(
            guild_id=guild_id,
            channel_id=channel_id,
            message_id=message_id,
            emoji=emoji.key,
            role_id=role_id,
        )

    async def role_for_reaction(
        self, message_id: int, emoji: EmojiToken
    ) -> int | None:
        return await self.repo.role_for_reaction(message_id, emoji.key)

    async def list_for_guild(self, guild_id: int) -> list[ReactionRoleConfig]:
        return await self.repo.list_for_guild(guild_id)

    async def clear_channel(self, guild_id: int, channel_id: int) -> int:
        return await self.repo.delete_for_channel(guild_id, channel_id)
