from django.db import models
from django.core.exceptions import ValidationError

from store.models import Goods


class Favorite(models.Model):
    user_id = models.PositiveIntegerField()
    goods = models.ForeignKey(
        Goods, related_name='users_favorites', on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        if self.__class__.objects.filter(
            user_id=self.user_id,
            goods=self.goods
        ).exists():
            raise ValidationError(
                'Нарушение уникальности: данная модель уже существует.'
            )
        super().save(**kwargs)
