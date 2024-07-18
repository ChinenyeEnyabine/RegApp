"""
URL configuration for skisubpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from docs.swagger_config import urlpatterns as docs_urlpatterns

from skisub import views
router=DefaultRouter()
router.register('billoperation',views.AirtimeTransactionCreateView)
router.register('billoperation',views.DataTransactionCreateView)
# path('buy-airtime/', AirtimeTransactionCreateView.as_view(), name='buy-airtime'),
#     path('buy-data/', DataTransactionCreateView.as_view(), name='buy-data'),

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    # path("login/",views.LoginView.as_view()),
    # path("signup/",views.RegisterView.as_view()),
    # path("logout/",views.LogoutView.as_view()),

    path('flight/', include('flightbooking.urls')),
    path('account/', include('account.urls')),
    # path('car/', include('carbooking.urls')),
    path('car/',include('carbook.urls')),
    path('hotel/', include('hotelbooking.urls')),
    path('hotelad/', include('hotelbooking.urls')),
    path('docs/', include(docs_urlpatterns)),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
admin.site.site_header = "Skisub Administrator"
admin.site.site_title = "Skisub Administrator"
admin.site.index_title = "Welcome to the Skisub Administration"