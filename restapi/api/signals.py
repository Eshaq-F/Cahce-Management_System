from rest_framework.validators import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from api.models import Transaction
from logging import getLogger

logger = getLogger(__name__)


@receiver(pre_save, sender=Transaction)
def fix_user_cache(sender, instance, **kwargs):
    try:
        original_transaction = Transaction.objects.get(pk=instance.pk)
    except Transaction.DoesNotExist:
        return

    if (instance.amount != original_transaction.amount) or (instance.type != original_transaction.type):
        logger.info(original_transaction.__dict__)
        logger.info(instance.__dict__)
        if original_transaction.type == Transaction.INCOME_TYPE:
            instance.user.cache -= original_transaction.amount
        elif original_transaction.type == Transaction.EXPENSE_TYPE:
            instance.user.cache += original_transaction.amount

        if instance.type == Transaction.INCOME_TYPE:
            instance.user.cache += instance.amount
        elif instance.type == Transaction.EXPENSE_TYPE:
            if instance.user.cache < instance.amount:
                raise ValidationError("User don't have enough cache, invalid update!")
            instance.user.cache -= instance.amount

        instance.user.save()


@receiver(post_save, sender=Transaction)
def update_user_cache(sender, instance, created, **kwargs):
    if created:
        logger.info('here?')
        if instance.type == Transaction.INCOME_TYPE:
            instance.user.cache += instance.amount
        else:
            instance.user.cache -= instance.amount

        instance.user.save()
