from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('login_validate/<int:pk>', views.login_validate),
    path('register', views.register),
    path('account_activation/<id>/<token>', views.account_activation, name="account_activation"),
    path('add_user_location/<int:pk>', views.UserLocationAPIView.as_view())
]