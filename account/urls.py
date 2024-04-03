from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account import views
from django.contrib import admin
router = DefaultRouter()
router.register(r'transaction', views.TransactionView, basename='transaction')
urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",views.LoginView.as_view()),
    path("signup/",views.RegisterView.as_view()),
    # path("logout/",views.LogoutView.as_view()),
    # path("transaction/",views.TransactionView.as_view()),
    path('', include(router.urls)),
    ]