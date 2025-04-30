from django.db import models
from django.utils import timezone


class Image(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    ip_address = models.GenericIPAddressField()
    upload_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-upload_date']
        db_table = 'image'


class OrderForms(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    TELEGRAM = 'telegram'
    WHATSAPP = 'whatsapp'
    BOTH = 'both'

    CONTACT_METHOD_CHOICES = [
        (TELEGRAM, 'Telegram'),
        (WHATSAPP, 'WhatsApp'),
        (BOTH, 'Both Telegram and WhatsApp'),
    ]

    contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default=WHATSAPP,
        verbose_name='Preferred contact method'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order form {self.id} - {self.name}"

    class Meta:
        ordering = ['-created_at']
        db_table = 'order_forms'
