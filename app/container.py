from app.repositories.reaction_role_repository import ReactionRoleRepository
from app.repositories.warn_repository import WarnRepository
from app.services.moderation_service import ModerationService
from app.services.reaction_role_service import ReactionRoleService


class ServiceContainer:
    def __init__(self) -> None:
        self.moderation = ModerationService(WarnRepository())
        self.reaction_roles = ReactionRoleService(ReactionRoleRepository())
