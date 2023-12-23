from django.urls import path
from shop import views
from ecommerce import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('main',views.main,name="main"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)