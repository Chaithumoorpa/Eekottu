from django import forms
from Shop.models import Product, ProductImages
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'sub_category', 'image', 'business_name', 'description',
                  'price', 'mrp_price', 'specifications', 'brand', 'model', 'net_quantity',
                  'item_weight', 'item_dimension', 'manufacturer', 'importer', 'generic_name',
                  'country_of_origin', 'product_status', 'stock', 'featured']
        
class ProductImagesForm(forms.ModelForm):
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)  # Adjust max_num and max_file_size as needed

    class Meta:
        model = ProductImages
        fields = ['images']
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance and instance.pk:
            images_qs = instance.productimages_set.all()

            for i, image in enumerate(images_qs, start=1):
                self.fields[f'clear_image_{image.id}'] = forms.BooleanField(
                    required=False, initial=False, label=f'Clear Image {i}'
                )
                self.fields[f'new_image_{image.id}'] = forms.ImageField(
                    required=False, label=f'New Image {i}'
                )