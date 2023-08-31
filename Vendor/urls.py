from django.urls import path
from Vendor import views
app_name='Vendor'
urlpatterns = [
    path('approve/<str:vid>/',views.approve,name='approve'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add-prod/',views.add_product,name='add_product'),
    path('update-prod/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-prod/<int:pk>/', views.delete_product, name='delete_product'),
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
]
