from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    telegram_id = fields.BigIntField(unique=True)
    balance = fields.IntField(default=100)
    is_active = fields.BooleanField(default=True)
    is_chat_session_activated = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    async def deactivate_chat_session(self):
        self.is_chat_session_activated = False
        await self.save()

    async def activate_chat_session(self):
        self.is_chat_session_activated = True
        await self.save()


class Request(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="requests")
    query = fields.TextField(null=True)
    image_data = fields.BinaryField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Response(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="responses")
    request = fields.ForeignKeyField("models.Request", related_name="responses")
    content = fields.TextField()
    is_active_chat_session = fields.BooleanField(default=False)
    additional_data = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    async def deactivate_chat_session(self):
        self.is_active_chat_session = False
        await self.save()
