from asgiref.sync import sync_to_async, async_to_sync
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver, Signal

from core.models import AccessLog

credential_accessed = Signal()


def send_email(subject, message, recipient_list):
    async_to_sync(send_mail)(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )


@receiver(credential_accessed)
async def log_credential_access(sender, **kwargs):
    user = kwargs['user']
    credential = kwargs['credential']

    # Create AccessLog entry
    await sync_to_async(AccessLog.objects.create)(user=user, credential=credential)

    # Send email notification if accessed by another user
    if user != credential.created_by:
        subject = f"Your credential '{credential.name}' was accessed"
        latest_access_log = await sync_to_async(AccessLog.objects.latest)('accessed_at')
        message = (f"Your credential '{credential.name}' for service '{credential.service.name}'"
                   f" was accessed by {user.username} at {latest_access_log.accessed_at}.")
        await sync_to_async(send_mail)(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [credential.created_by.email]
        )

        print(f"Emailed {credential.created_by.email} about credential access")

    if user.is_superuser:
        print(f"Admin {user.username} accessed credential {credential.name}")
    else:
        print(f"User {user.username} accessed credential {credential.name}")
