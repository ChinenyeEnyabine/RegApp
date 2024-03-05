from django.urls import path
from account import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",views.LoginView.as_view()),
    path("signup/",views.RegisterView.as_view()),
    # path("logout/",views.LogoutView.as_view()),
    path("transaction/",views.TransactionListCreateView.as_view()),
    ]