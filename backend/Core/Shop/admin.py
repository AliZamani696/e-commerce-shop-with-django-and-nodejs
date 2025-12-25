from django.contrib import admin
from .models import Category,Product

from django.utils.html import format_html
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'inventory', 'is_premium', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_premium', 'category', 'created_at')
    list_editable = ('price', 'inventory', 'is_premium')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('name', 'sku')
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'name', 'slug', 'category', 'description', 'image')
        }),
        ('بخش مالی و موجودی', {
            'fields': ('price', 'discount_price', 'inventory')
        }),
        ('دسترسی و وضعیت', {
            'fields': ('is_active', 'is_premium')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# داخل کلاس ProductAdmin:
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "بدون تصویر"

    list_display = ('thumbnail', 'name', 'category', 'price', 'inventory', 'is_premium')
