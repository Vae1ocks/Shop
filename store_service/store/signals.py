from django.db.models.signals import post_save, pre_delete
from django.db.models import Avg
from django.dispatch import receiver
from .models import PriceHistory, Goods, Comment
from django.urls import reverse

from celery import current_app


@receiver(post_save, sender=Goods)
def add_price_history(sender, instance, created, **kwargs):
    """
    Для создания объекта PriceHistory в случае изменения цены на товар и оповещения
    микросервиса user_service об этом изменении чтобы он уведомил пользователей,
    которые добавили данный товар в ожидаемые, указав определённую цену.
    """
    if created:
        PriceHistory.objects.create(
            goods=instance,
            price=instance.price,
        )
    else:
        # Если цена товара последнего по дате объекта PriceHistory не совпадает с
        # ценой только что сохранённого объекта Goods - instance --> цена изменилась
        # и следует создать новый объект PriceHistory
        previous_price = (
            PriceHistory.objects.filter(
                goods=instance,
            )
            .order_by("-date")
            .first()
            .price
        )
        if previous_price != instance.price:
            relative_url = reverse(
                "store:goods_detail",
                args=[instance.id],
            )
            PriceHistory.objects.create(goods=instance, price=instance.price)
            current_app.send_task(
                "user_service.send_notification",
                kwargs={
                    "goods_id": instance.id,
                    "goods_title": instance.title,
                    "price": instance.price,
                    "relative_url": relative_url,
                },
                queue="user_system_queue",
            )


@receiver(post_save, sender=Comment)
def update_goods_rating_if_comment_save(sender, instance, **kwargs):
    """
    Обновление рейтинга товара в случае сохранения отзыва о данном товаре.
    """
    goods = instance.goods
    comments = goods.comments.all()
    if comments.exists():
        goods.rating = comments.aggregate(Avg("rating"))["rating__avg"]
    else:
        goods.rating = 0
    goods.save()


@receiver(pre_delete, sender=Comment)
def update_goods_rating_if_comment_delete(sender, instance, **kwargs):
    """
    Изменение рейтинга товара в случае удаления отзыва о данном товаре.
    """
    goods = instance.goods
    comments = goods.comments.exclude(id=instance.id)
    if comments.exists():
        goods.rating = comments.aggregate(Avg("rating"))["rating__avg"]
    else:
        goods.rating = 0
    goods.save()
