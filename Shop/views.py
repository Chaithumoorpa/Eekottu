from django.shortcuts import render, get_object_or_404
from .models import Product, CartOrder, CartOrderItems, Category, SubCategory, Wishlist, Vendor, ProductImages, ProductReview, Address, Customer

# Create your views here.

from collections import OrderedDict


def index(request):
    # Get all categories
    categories = Category.objects.all().order_by('name')

    products = Product.objects.order_by('brand', '-created_at')
    
    # Initialize a dictionary to store the newly added brands and their products
    newly_arrived_brands = OrderedDict()

    # Loop through the products to filter the newly added brands
    for product in products:
        # Add the product to the newly_arrived_brands dictionary using the brand as the key
        newly_arrived_brands[product.brand] = product
        
        # If the count of newly_arrived_brands exceeds 10, remove the oldest brand
        if len(newly_arrived_brands) > 10:
            oldest_brand = next(iter(newly_arrived_brands.keys()))
            newly_arrived_brands.pop(oldest_brand)

    # Convert the dictionary values to a list to pass to the template
    newly_arrived_brands_list = list(newly_arrived_brands.values())

    context = {
        'categories': categories,
        'newly_arrived_brands': newly_arrived_brands_list,
    }

    return render(request, 'Eekottu/index.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shop(request, name):
    
    category = Category.objects.get(name=name)
    subcategories = SubCategory.objects.filter(category=category)
    
    if request.user.is_authenticated and request.user.is_vendor:
        
        products = Product.objects.filter(category=category).exclude(user=request.user)
        
    else:
        products = Product.objects.filter(category=category)
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context={
        'category':category,
        'subcategories': subcategories,
        'products': products_page,
    }
    
    return render(request, 'Eekottu/shop.html', context)

def single_product(request,category_name, sub_category_name, product_id):
    
    product = get_object_or_404(Product, 
                                category__name__iexact=category_name,
                                sub_category__name__iexact=sub_category_name,
                                pid=product_id)
    
    context={
        'product': product,
    }
    
    return render(request,"Eekottu/single_product.html", context)