from django.shortcuts import render, redirect, get_object_or_404
from Shop.models import Vendor, Product

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from Shop.models import ProductImages, Product
from .forms import ProductForm, ProductImagesForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_verified_vendor(user):
    return user.is_authenticated and hasattr(user, 'vendor')

@user_passes_test(is_admin)
# Create your views here.
def approve(request, vid):
    try:
        vendor = Vendor.objects.get(vid=vid)
    except Vendor.DoesNotExist:
        # Vendor with the given vid does not exist, handle the error here
        # return render(request, 'vendor/vendor_not_found.html')
        pass
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            vendor.Vendor_status = 'Approved'
        elif action == 'reject':
            vendor.Vendor_status = 'Rejected'
        vendor.save()
        return redirect('admin:index')  # Redirect to the vendor detail page

    return render(request, 'vendor/approve_vendor.html', {'vendor': vendor})

@user_passes_test(is_verified_vendor)
def dashboard(request):
    
    context={
        'vendor':business(request),
        'products':products_list(request),
        'categories':get_category(),
    }
    
    return render(request,'vendor/vendor_dashboard.html',context)

def business(request):
    user= request.user
    vendor= Vendor.objects.get(user=user.pk)
    return vendor

def products_list(request):
    vendor = Vendor.objects.get(user=request.user)
    products = Product.objects.filter(user=vendor.user)
    return products

from Shop.models import Category
def get_category():
    categories = Category.objects.all().order_by('name')
    
    return categories
    
from django.forms import formset_factory



def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        product_images_form = ProductImagesForm(request.POST, request.FILES)
        

        if product_form.is_valid() and product_images_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            images = request.FILES.getlist('images[]')
            product_images = [ProductImages(product=product, images=image) for image in images]

            # Save the ProductImages objects in a single database query
            ProductImages.objects.bulk_create(product_images)

            # Any other processing or redirection here

            return redirect('Vendor:dashboard')
    else:
        product_form = ProductForm()
        product_images_form = ProductImagesForm()

    context = {
        'product_form': product_form,
        'product_images_form': product_images_form,
    }

    return render(request, 'vendor/product_add.html', context)


# views.py
from django.http import JsonResponse

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_images = product.productimages_set.all()

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        product_images_form = ProductImagesForm(request.POST, request.FILES)

        if product_form.is_valid() and product_images_form.is_valid():
            product = product_form.save()

            # Clear existing product images based on the submitted checkbox values
            for image in existing_images:
                clear_image_key = f'clear_image_{image.id}'
                if request.POST.get(clear_image_key):
                    image.delete()

            images = request.FILES.getlist('images[]')
            product_images = [ProductImages(product=product, images=image) for image in images]

            # Save the new ProductImages objects in a single database query
            ProductImages.objects.bulk_create(product_images)

            # Any other processing or redirection here

            return redirect('Vendor:dashboard')
    else:
        product_form = ProductForm(instance=product)
        product_images_form = ProductImagesForm(instance=product)

    context = {
        'product_form': product_form,
        'product_images_form': product_images_form,
        'existing_images': existing_images,
    }

    return render(request, 'vendor/product_update.html', context)

# Add a view to handle the AJAX request for clearing individual images
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def clear_image(request):
    if request.method == 'POST' and request.is_ajax():
        image_id = request.POST.get('image_id')
        try:
            image = ProductImages.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except ProductImages.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('Vendor:dashboard')

    return render(request, 'vendor/product_delete.html', {'product': product})


from Shop.models import SubCategory
def get_subcategories(request):
    category_id = request.GET.get('category_id')

    if category_id:
        try:
            category_id = int(category_id)
            subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
            return JsonResponse(list(subcategories), safe=False)
        except ValueError:
            # Invalid category_id format
            return JsonResponse([], safe=False)
    else:
        # category_id not provided
        return JsonResponse([], safe=False)