from django.dispatch import receiver
from django.db.models.signals import post_save

from api.models import Transaction
from logging import getLogger

logger = getLogger(__name__)


@receiver(post_save, sender=Transaction)
def update_user_cache(sender, instance, created, **kwargs):
    if created:
        if instance.type == Transaction.INCOME_TYPE:
            instance.user.cache += instance.amount
        else:
            instance.user.cache -= instance.amount

        instance.user.save()
