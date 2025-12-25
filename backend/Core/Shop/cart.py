

import json
from django.conf import settings
from django_redis import get_redis_connection



class RedisCart:
    def __init__(self,user_id) -> None:
        self.conn = get_redis_connection("default")
        self.key = f"cart{user_id}"

    def add(self,product_id,quantity=1,price=0):
        cart_data = self.conn.get(self.key)
        cart = json.loads(cart_data) if cart_data else {}
        p_id = str(product_id)
        if p_id in cart:
            cart[p_id]["quantity"] += quantity
        else:
            cart[p_id] = {"quantity":quantity,"price":str(price)}
        self.conn.set(self.key,json.dumps(cart),ex=86400)
        notification = {
            "event": "item_added",
            "user_id": self.key.split(':')[-1],
            "product_id": str(product_id),
            "quantity": quantity
            }
        self.conn.publish("cart_notification",json.dumps(notification))


    def get_items(self):
        cart_data = self.conn.get(self.key)
        return json.loads(cart_data) if cart_data else {}

    def remove(self):
        cart_data = self.cconn.get(self.key)
        if cart_data:
            cart = json.loads(cart_data)
            if str(product_id) in cart:
                del cart[str(product_id)]
                self.conn.set(self.key,json.dumps(cart),ex=86400)
        notification = {
            "event": "item_removed",
            "user_id": self.key.split(':')[-1],
            "product_id": str(product_id)
            }
        self.conn.publish('cart_notifications', json.dumps(notification))
    def clear(self):
        self.conn.delete(self.key)
