from django.contrib import admin
from .models import Product, CartOrder, CartOrderItems, Category, SubCategory, Wishlist, Vendor, ProductImages, ProductReview, Address, Customer
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class CategoryAdmin(admin.ModelAdmin):
    
    list_display=['cid','name']
    
class SubCategoryAdmin(admin.ModelAdmin):
    
    list_display=['scid','category','name']
    
class VendorAdmin(admin.ModelAdmin):
    
    list_display = ['vid', 'user', 'name', 'approval_status']

    def approval_status(self, obj):
        if obj.Vendor_status == 'Approved':
            return format_html('<span style="color: green;">Approved</span>')
        elif obj.Vendor_status == 'Rejected':
            return format_html('<span style="color: red;">Rejected</span>')
        else:
            return format_html('<a class="button" href="{}"  >Approve</a>', reverse('Vendor:approve', args=[obj.vid]))

    approval_status.short_description = 'Approval Status'
    
    
class CustomerAdmin(admin.ModelAdmin):
    
    list_display=['cid','user','name','image']
    
class CartOrderAdmin(admin.ModelAdmin):
    
    list_display=['user','price','paid_status','order_date','product_status']
    
class CartOrderItemsAdmin(admin.ModelAdmin):
    
    list_display=['order','image','item','price','quantity','total','product_status']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display=['pid','user','category','sub_category','name','price','created_at','featured','product_status']


class ProductReviewAdmin(admin.ModelAdmin):
    
    list_display=['user','product','review','rating']
    
class WishlistAdmin(admin.ModelAdmin):
    
    list_display=['user','product']
    
class AddressAdmin(admin.ModelAdmin):
    
    list_display=['user','address','status']
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)

    