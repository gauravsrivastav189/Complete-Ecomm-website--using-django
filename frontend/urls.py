from django.urls import path
from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-single-item/<slug>/', views.remove_single_item, name='remove-single-item'),
    path('summary/', views.OrderSummaryView.as_view(), name='summary'),
    path('shipping-address/', views.ShippingAddressView.as_view(), name='shipping-address'),
    path('add-coupon/', views.addCouponView.as_view(), name='add-coupon'),
    path('payment/', views.PaymentView.as_view(), name='payment')
]