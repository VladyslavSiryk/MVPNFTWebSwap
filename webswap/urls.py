from django.urls import path
from .views import *
from .views import HomeView
from webswap.models import WalletsInfo
from django.contrib.auth import views as auth_views

urlpatterns = [
#...
    path('', HomeView.as_view()),
#...
]


urlpatterns = [
    path('', landing),
    path('home', landing),
    path('index', landing),
    path('404', page_404),
    path('about', about),
    path('base', base),
    path('contacts', contacts),
    path('faq', faq),
    path('forgot', forgot),
    path('privacy', privacy),
    path('ranking', ranking),
    path('swap', swap),
    path("api/web3auth", AddressVerify.user_auth),
    path('update_collection', request_update_collection),
    path('api/load_tokens', AddressVerify.ajax_load_tokens),

    #login modal page#

]

