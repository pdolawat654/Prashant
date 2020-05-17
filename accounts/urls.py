from . import views
from django.urls import path
urlpatterns=[
    path('register/',views.register,name='register'),
    path('verify/',views.verify,name='verify'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('uprofile',views.uprofile,name='uprofile'),
    path('profile',views.profile,name='profile'),
]