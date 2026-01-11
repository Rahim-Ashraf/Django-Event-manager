from django.urls import path
from events.views import home, dashboard

urlpatterns = [
    path('', home),
    path('dashboard/', dashboard)
]