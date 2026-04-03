from django.urls import path
from . import views

urlpatterns = [
    # Home & Info Pages
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    
    # Dogs
    path('dogs/', views.dog_list, name='dog_list'),
    path('dogs/<slug:slug>/', views.dog_detail, name='dog_detail'),
    path('breeds/<slug:slug>/', views.breed_category_detail, name='breed_category_detail'),
    
    # Accessories
    path('accessories/', views.accessory_list, name='accessory_list'),
    path('accessories/<slug:slug>/', views.accessory_detail, name='accessory_detail'),
    path('accessory-categories/<slug:slug>/', views.accessory_category_detail, name='accessory_category_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<str:cart_key>/', views.update_cart, name='update_cart'),
    path('cart/remove/<str:cart_key>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<str:item_type>/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<str:item_type>/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Adoption & Checkout
    path('adoption/<int:dog_id>/', views.adoption_form_view, name='adoption_form'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    
    # Account
    path('orders/', views.order_history, name='order_history'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    
    # Post Ad
    path('post-ad/', views.post_ad_create, name='post_ad_create'),
    path('ads/', views.post_ad_list, name='post_ad_list'),
    path('ads/<int:pk>/', views.post_ad_detail, name='post_ad_detail'),
    path('my-ads/', views.my_ads, name='my_ads'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Share
    path('share/', views.share_item, name='share_item'),
]
