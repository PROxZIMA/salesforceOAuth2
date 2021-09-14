from django.contrib.auth.views import LogoutView
from django.urls import path
from salesforceApp.views import oauth2, oauth2_callback, viewData
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('viewData', viewData, name='view-data'),
    path('oauth2', oauth2, name='oauth2'),
    path('oauth2/callback/', oauth2_callback, name='oauth2-callback'),
    path('oauth2/logout/', LogoutView.as_view(), name='logout'),
]