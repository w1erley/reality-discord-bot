from tortoise.transactions import in_transaction

from app.models import Warn
from app.repositories.warn_repository import WarnRepository


class ModerationService:
    def __init__(self, warns: WarnRepository) -> None:
        self.warns = warns

    async def warn_user(
        self, *, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        async with in_transaction():
            next_id = await self.warns.last_warn_id(user_id, server_id) + 1
            await self.warns.create(
                warn_id=next_id,
                user_id=user_id,
                server_id=server_id,
                moderator_id=moderator_id,
                reason=reason,
            )
            return next_id

    async def remove_warn(
        self, *, warn_id: int, user_id: int, server_id: int
    ) -> int:
        await self.warns.delete(warn_id, user_id, server_id)
        return await self.warns.count_for_user(user_id, server_id)

    async def list_warnings(self, *, user_id: int, server_id: int) -> list[Warn]:
        return await self.warns.list_for_user(user_id, server_id)
