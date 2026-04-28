from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def order_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"Signal: New order {instance.id} created by {instance.buyer.username}")
        # In a real app, you could trigger a Celery task here to send a confirmation email
