from django.db import models
from django.contrib.auth.models import User

class SaladSubscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic Greens (3 Salads/Week)'),
        ('pro', 'Protein Power (5 Salads/Week)'),
        ('keto', 'Keto Cleanse (5 Salads/Week)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Fulfillment'),
        ('preparing', 'Preparing / Chopping'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    
    # Order processing tracking fields
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} ({self.get_order_status_display()})"