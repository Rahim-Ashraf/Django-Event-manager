from django.urls import path
from events.views import event_home, create_event, create_participant, create_category, dashboard, specific_event, update_event, delete_event

urlpatterns = [
    path('', event_home, name='home'),
    path('event/<int:event_id>/', specific_event, name='specific_event'),
    path('create_event/', create_event, name='add_event'),
    path('update_event/<int:id>/', update_event, name='update_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'),
    path('create_participant/', create_participant, name='add_participant'),
    path('create_category/', create_category, name='add_category'),
    path('organizer_dashboard/', dashboard, name='organizer_dashboard')
]