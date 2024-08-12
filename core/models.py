from django.contrib.auth.models import User
from django.db import models


class CreatedByMixin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Service(CreatedByMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(CreatedByMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Credential(CreatedByMixin):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    text = models.TextField(blank=True, null=True, name='public_key')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    allowed_users = models.ManyToManyField(User, blank=True, name='allowed_users', related_name='allowed_credentials')

    def __str__(self):
        return f"{self.name} for {self.service.name}"


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.credential.name} at {self.accessed_at}"
