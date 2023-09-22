from django.urls import path
from .views import  MyProtectedView

urlpatterns = [
    path('login/', MyProtectedView.as_view(), name='login'),
]


