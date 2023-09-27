from time import sleep

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def notify_order_created():
    message = (
        f"Hello!"
        "\n\n"
        "We've got your order."
        "\n\n"
        f"We'll let you know when your order has been shipped."
        "\n\n"
        "Sincerely,\nYour admin"
    )
    send_mail(
        subject=f"New order",
        message=message,
        from_email="admin@example.com",
        recipient_list=["managers@example.com"],
    )
    return True