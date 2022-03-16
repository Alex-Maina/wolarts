from django.urls import path, include
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('product/<str:pk>/', views.product, name="product"),
    path('contact-us/', views.contactUs, name="contact-us"),
    path('our-story/', views.ourStory, name="our-story"),
    path('articles/', views.articles, name="articles"),
]
