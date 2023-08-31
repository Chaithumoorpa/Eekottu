from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User
from django.utils.timezone import now

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


STATUS_CHOICE={
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
}
STATUS ={
    ("draft","Drafts"),
    ("disabled","Disabled"),
    ("in_review","In Review"),
    ("rejected","Rejected"),
    ("published","Published"),
}
RATING ={
    (1,"★✰✰✰✰"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
}
VENDOR_STATUS = {
        ('In Review', 'In Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    }




def user_directory_path(instance, filename):
    
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=13, prefix="CAT", alphabet="ABCDEF123456789")
    name= models.CharField(max_length=100)
    icon= models.ImageField(upload_to='category')
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"></img>'%{self.icon.url})
    
    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    scid = ShortUUIDField(unique=True, length=10, max_length=14, prefix="SCAT", alphabet="ABCDEF123456789")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name_plural = "SubCategories"

    def __str__(self):
        return self.name
    
class Tags(models.Model):
    pass
    
class Vendor(models.Model):
    vid=ShortUUIDField(unique=True, length=10, max_length=13, prefix="VEN", alphabet="ABCDEF123456789")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to='user_img')
    
    business_name = models.CharField(max_length=255)
    description=models.TextField(null=True)
    address=models.CharField(max_length=100, default="123 main street")
    contact=models.CharField(max_length=100, unique=True,default="+91 9876543210")
    
    pan_number = models.CharField(max_length=10, unique=True)
    gst_number = models.CharField(max_length=15, unique=True)
    
    
    chat_resp_time=models.CharField(max_length=100, default="100")
    shipping_on_time=models.CharField(max_length=100, default="100")
    authentic_rating=models.CharField(max_length=100, default="100")
    days_return=models.CharField(max_length=100, default="100")
    warranty_period=models.CharField(max_length=100, default="100")
    
    terms_accepted = models.BooleanField(default=False)
    
    Vendor_status = models.CharField(choices=VENDOR_STATUS, max_length=20, default='In Review')
    
    
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"></img>'%{self.image.url})
    
    def __str__(self):
        return self.name


            


class Customer(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=13, prefix="CUST", alphabet="ABCDEF123456789")
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to=user_directory_path)
    # Add any customer-specific fields here

    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.user.username


    
class Product(models.Model):
    
    pid=ShortUUIDField(unique=True, length=10, max_length=13, alphabet="ABCDEF123456789")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    
    
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to=user_directory_path)
    business_name = models.CharField(max_length=255)
    description=models.TextField()
    
    price= models.DecimalField(max_digits=10, decimal_places=2,default="1.99")
    mrp_price= models.DecimalField(max_digits=10, decimal_places=2,default="3.00")
    
    specifications= models.TextField(null=True, blank =True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    net_quantity = models.CharField(max_length=100)
    item_weight = models.CharField(max_length=100)
    item_dimension = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    importer = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True, blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10)
    
    status = models.BooleanField(default=True)
    stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    sku=ShortUUIDField(unique=True, length=5, max_length=10,prefix="SKU", alphabet="ABCDEF123456789")
    
    
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"></img>'%{self.image.url})
    
    def __str__(self):
        return self.name
    
    def get_percentage(self):
        new_price=(self.price/self.mrp_price)*100
        
        return new_price
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    images=models.ImageField(upload_to="product_images")
    created_at = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        verbose_name_plural = "Product Images"
        
    
        

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10, decimal_places=2,default="1.99")
    paid_status=models.BooleanField(default=False)
    order_date =models.DateTimeField(default=now, editable=False)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"
        

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=16)
    product_status = models.CharField( max_length=200)
    item= models.CharField(max_length=200)
    image= models.CharField(max_length=200)
    quantity= models.IntegerField(default=0)
    price= models.DecimalField(max_digits=10, decimal_places=2,default="1.99")
    total= models.DecimalField(max_digits=10, decimal_places=2,default="1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"></img>'%{self.image.url})
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating= models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        return self.product.name
    
    def get_rating(self):
        return self.rating
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        verbose_name_plural = "Wishlist"
        
    def __str__(self):
        return self.product.name
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address= models.TextField( null=True)
    status= models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Address"
    