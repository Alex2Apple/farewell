import uuid
from django.db import models

class Accessor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField("邮箱", unique = True, max_length = 30)
    name = models.CharField('昵称', unique = True, max_length = 30)
    website = models.CharField('网址', max_length = 40, default = '')

    def __str__(self):
        return self.name
    
    @classmethod
    def create_accessor(cls, email, username, website):
        ac = cls(email = email, name = username, website = website)
        ac.save()
        return ac