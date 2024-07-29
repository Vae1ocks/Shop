from django.db import models


class Order(models.Model):
    user = models.PositiveIntegerField()
    status = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id} with status {self.status}'

    def get_total_price(self):
        return sum(item.get_total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    goods = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem {self.id}'

    def get_total_price(self):
        return self.price * self.amount