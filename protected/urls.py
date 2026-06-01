from django.urls import path

from .views import *

urlpatterns = [
    path('mobile-combos/<slug:slug>/',combo_detail_view,name='combo_detail'),
    path('mobile-parts/<slug:slug>/',category_detail_view,name='category_detail'),
    path('profile/',profile_view,name="profile")
]
    