from itertools import product
from django.http import request
from django.shortcuts import render
from django.views.generic.base import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .cart  import RedisCart
from .models import Product
# Create your views here.




class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,req):
        cart = RedisCart(req.user.id)
        return Response(cart.get_items())

    def post(self,req):
        product_id = req.data.get("product_id")
        quantity = int(req.data.get("quantity",1))


        try:
            product = Product.objects.get(id=product_id,is_active=True)
            cart = RedisCart(req.user.id)
            cart.add(product.id,quantity,product.price)
            return Response({"mssg":"added to cart"})
        except Product.DoesNotExist:
            return Response({"error":"product not found"})
    def delete(self,req):
        product_id = req.data.get("product_id")
        cart= RedisCart(req.user.id)
        cart.remove(product_id)
        return Response({"mssg":"product removed"})

