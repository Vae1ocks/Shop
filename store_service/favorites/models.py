from django.db import models
from django.core.exceptions import ValidationError

from store.models import Goods


class Favorite(models.Model):
    user_id = models.PositiveIntegerField()
    goods = models.ForeignKey(
        Goods, related_name='users_favorites', on_delete=models.CASCADE
    )

