from app.models import Warn


class WarnRepository:
    async def last_warn_id(self, user_id: int, server_id: int) -> int:
        last = (
            await Warn.filter(user_id=user_id, server_id=server_id)
            .order_by("-warn_id")
            .first()
        )
        return last.warn_id if last else 0

    async def create(
        self,
        *,
        warn_id: int,
        user_id: int,
        server_id: int,
        moderator_id: int,
        reason: str,
    ) -> Warn:
        return await Warn.create(
            warn_id=warn_id,
            user_id=user_id,
            server_id=server_id,
            moderator_id=moderator_id,
            reason=reason,
        )

    async def delete(self, warn_id: int, user_id: int, server_id: int) -> int:
        return await Warn.filter(
            warn_id=warn_id, user_id=user_id, server_id=server_id
        ).delete()

    async def count_for_user(self, user_id: int, server_id: int) -> int:
        return await Warn.filter(user_id=user_id, server_id=server_id).count()

    async def list_for_user(self, user_id: int, server_id: int) -> list[Warn]:
        return await Warn.filter(user_id=user_id, server_id=server_id).order_by(
            "warn_id"
        )
