from tortoise import fields
from tortoise.models import Model


class ReactionRoleConfig(Model):
    pk = fields.IntField(pk=True)
    guild_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    message_id = fields.BigIntField()
    emoji = fields.CharField(max_length=64)
    role_id = fields.BigIntField()

    class Meta:
        table = "reaction_roles"
        unique_together = (("message_id", "emoji"),)
