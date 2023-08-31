from django.urls import path
from Shop import views

app_name= 'Shop'

urlpatterns=[
    path('',views.index, name='index'),
    path('<str:name>/',views.shop, name="shop"),
    path('<str:category_name>/<str:sub_category_name>/<str:product_id>/', views.single_product, name='product'),
    
]