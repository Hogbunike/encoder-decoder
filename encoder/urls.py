from django.urls import path
from .views import encode_view, decode_view

urlpatterns = [
    path('encode/', encode_view, name='encode'),
    path('decode/', decode_view, name='decode'),
]