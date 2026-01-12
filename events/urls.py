from django.urls import path
from events.views import event_home, create_event, create_participant, create_category, dashboard, specific_event

urlpatterns = [
    path('', event_home),
    path('event/<int:event_id>', specific_event, name='specific_event'),
    path('create_event/', create_event),
    path('create_participant', create_participant),
    path('create_category', create_category),
    path('organizer_dashboard/', dashboard)
]