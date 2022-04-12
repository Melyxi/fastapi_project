from django.contrib import admin
from django.urls import path, include

from main.views import main, transaction
app_name = 'main'

urlpatterns = [
    path('', main, name="index"),
    path('transaction/', transaction, name="transaction")
]
