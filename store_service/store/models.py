"""
Модели категории, товара, отзыва к товару и истории товара
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from unidecode import unidecode


def upload_to_author_id(instance, filename):
    return f'comment/author/{instance.author}/{filename}'


def upload_to_id(instance, filename):
    return f'comment/{instance.id}/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Goods(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='goods')
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='goods/', blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    times_bought = models.PositiveIntegerField(default=0)
    users_bought = models.JSONField(default=list)

    description = models.TextField()
    amount = models.PositiveIntegerField()

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category'])
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Goods, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class PriceHistory(models.Model):
    """
    Для истории цен товара, создание происходит в signals.py
    """
    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['goods']),
            models.Index(fields=['date'])
        ]

    def __str__(self):
        return f'{self.price} for {self.goods_id} on {self.date}'
    

class Comment(models.Model):
    author = models.PositiveIntegerField()
    author_name = models.CharField(max_length=30)
    author_profile_picture = models.ImageField(upload_to=upload_to_author_id,
                                               blank=True, null=True)

    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              related_name='comments')
    
    body = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ImageModel(models.Model):
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to=upload_to_id,
                              blank=True, null=True)
