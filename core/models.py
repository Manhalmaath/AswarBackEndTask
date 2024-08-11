from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Credential(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True, name='public_key')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('core.Tag', blank=True)

    def __str__(self):
        return f"{self.name} for {self.service.name}"


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.credential.name} at {self.accessed_at}"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
