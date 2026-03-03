from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from .models import SellerProfile

@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        store_name = f"{instance.username} Store"

        SellerProfile.objects.create(
            user=instance,
            store_name=store_name,
            store_slug=slugify(store_name),
            gst_number="",
            pan_number="",
            bank_account_number="",
            ifsc_code="",
            business_address=""
        )