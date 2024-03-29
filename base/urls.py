from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('kitchen/<slug:kitchen>', views.kitchen),
    path('cart', views.cart),
    path('add_item_to_cart', views.AddItemToCart.as_view({'get':'cart_items'})),
    path('edit_cart/<int:pk>', views.EditCart.as_view()),
    path('cart_by_user', views.CartByUser.as_view()),
    path('logout', views.logout_func),
    path('order-online/<int:pk>' ,views.order_online),
    path('menu/<int:pk>', views.menu),
    path('ratings-and-reviews/<int:pk>/<int:num>', views.ratings_and_reviews),
    path('overview/<int:pk>', views.overview),
    path('kitchen_locate/<int:pk>', views.KitchenAPIView.as_view()),
    path('user_location', views.user_location),
    path('get_kitchen_name/<slug:slug>', views.KitchenName.as_view()),
    path('kitchen_timings/<int:pk>', views.KitchenTimings.as_view()),
    path('create_order', views.CreateOrder.as_view()),
    path('contact', views.contact),
    path('terms', views.terms),
    path('privacy', views.privacy),
    path('order_history/<int:pk>', views.order_history),
    path('edit_order', views.EditOrder.as_view()),
]