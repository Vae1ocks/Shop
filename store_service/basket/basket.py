"""
Корзина покупок
"""

from decimal import Decimal
from django.conf import settings
from store.models import Goods


class Basket:
    """
    Корзина покупок
    """
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.SHOPPING_BASKET_KEY)
        if not basket:
            basket = self.session[settings.SHOPPING_BASKET_KEY] = {}
        self.basket = basket

    def save(self):
        self.session.modified = True

    def add(self, goods, amount=1, override_amount=False):
        goods_id = str(goods.id)
        if goods_id not in self.basket:
            self.basket[goods_id] = {'amount': amount,
                                     'price': str(goods.price)}
        if override_amount:
            self.basket[goods_id]['amount'] = amount
        else:
            self.basket[goods_id]['amount'] += amount
        self.save()

    def remove(self, goods):
        goods_id = str(goods.id)
        if goods_id in self.basket:
            del self.basket[goods_id]
            self.save()

    def __iter__(self):
        basket = self.basket.copy()
        goods_ids = basket.keys()
        goods_query = Goods.objects.filter(id__in=goods_ids)

        for goods in goods_query:
            basket[str(goods.id)]['goods'] = goods

        for value in basket.values():
            value['price'] = Decimal(value['price'])
            value['total_price'] = value['price'] * value['amount']
            yield value

    def __len__(self):
        return sum(value['amount'] for value in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(value['price']) * value['amount']
                   for value in self.basket.values())

    def get_basket_items(self):
        """
        Для сериализации корзины
        """
        items = []
        for item in self:
            items.append({
                'goods': {'id': item['goods'].id, 'title': item['goods'].title},
                'amount': item['amount'],
                'price': item['price'],
                'total_price': item['total_price']
            })
            return items

    def clear(self):
        del self.session[settings.SHOPPING_BASKET_KEY]
        self.save()
