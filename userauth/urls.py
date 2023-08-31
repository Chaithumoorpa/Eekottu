from django.urls import path
from userauth import views

app_name= 'userauth'

urlpatterns=[
    path('register/',views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>/<str:is_customer>/', views.ActivateAccountView.as_view(), name = 'activate'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('step-one/<str:uidb64>/<str:token>/<str:is_customer>/', views.StepOneView.as_view(), name='step_one'),
    path('step-two/<str:uidb64>/<str:token>/<str:is_customer>/', views.StepTwoView.as_view(), name='step_two'),
    path('step-three/<str:uidb64>/<str:token>/<str:is_customer>/', views.StepThreeView.as_view(), name='step_three'),
]