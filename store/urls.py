from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.home, name='store'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'), # Dynamic URL for product details
    # pk stands for primary key (unique identifier for each product)
    path('category/<str:cn>', views.category, name='category'), # Dynamic URL for category details  
    # cn stands for category name (unique identifier for each category)


]