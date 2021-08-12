from django.db import models
from accounts.models import Account

# Create your models here.
METAL_CHOICES = (
    ("yellow_gold", "Yellow-Gold"),
    ("rose_gold", "Rose-Gold"),
    ("white_gold", "White-Gold"),
    ("silver", "Silver"),
)

GOLD_QUALITY_CHOICES = (
    ("14k", "14k"),
    ("18k", "18k"),
)

ORDER_STATUS = (
    ("recieved", "Recieved"),
    ("verified", "Verified"),
    ("started", "Started making"),
    ("almost", "Almost completed"),
    ("complete", "Completed making"),
)

ORDER_QUANTITY = (
    ("1","1"), ("2","2"),("3","3"),("4","4"),("5","5"),
    ("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),
)

DESIGN_INSIGHT = (
    ("1", "I have image of exactly what I want"),
    ("2", "I have some images and knowledge of what I want to make"),
    ("3", "I have some general ideas"),
    ("4", "I have no idea, need help!"),
)

class ornamentOrder(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=250, null=True)
    image_url = models.ImageField(upload_to='orders/images', default="")
    metal_choice = models.CharField(max_length=20, choices=METAL_CHOICES, null=True)
    gold_quality = models.CharField(max_length=20, choices=GOLD_QUALITY_CHOICES, blank=True)
    quantity = models.CharField(max_length=20, choices=ORDER_QUANTITY, blank=True)
    budget = models.CharField(max_length=20, null=True, blank=True)
    design_insight = models.CharField(max_length=100, choices=DESIGN_INSIGHT, blank=True)
    instructions = models.TextField(null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Recieved", null=True)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.email} | Order id: {self.order_id} | Budget: {self.budget}"

