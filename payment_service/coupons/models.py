from django.db import models


class Coupon(models.Model):
    title = models.CharField(max_length=100)

    valid_from = models.DateField()
    valid_to = models.DateField()

    discount = models.PositiveIntegerField()
    minimal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximal_price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField()

    def __str__(self):
        return f"Coupon {self.title} for {self.discount}% discount"
