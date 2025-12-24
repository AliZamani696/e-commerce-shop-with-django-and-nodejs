from django.db import models
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/', null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =("-created_at",)

    def __str__(self):
        return self.name


    def save(self,*args,**kwargs):
        if not self.slug:
            self.sulg = slugify(self.name, allow_unicode=True) + f"-{str(self.id)[:4]}"
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price
    @property
    def is_in_stock(self):
        return self.inventory > 0

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, allow_unicode=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
