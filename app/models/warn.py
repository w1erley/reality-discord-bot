from tortoise import fields
from tortoise.models import Model


class Warn(Model):
    warn_id = fields.IntField()
    user_id = fields.BigIntField()
    server_id = fields.BigIntField()
    moderator_id = fields.BigIntField()
    reason = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "warns"
