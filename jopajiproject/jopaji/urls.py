from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('about-us/', views.about_us, name="about us"),
    path('franchise/', views.franchise, name="franchise"),
    path('our-menu/', views.our_menu, name="our menu"),
    path('contact-us/', views.contact_us, name="contact us"),
    path('book-order/', views.book_order, name="book order"),
    path('our-menu/<slug:slug>/', views.product_list, name="Product List"),
]