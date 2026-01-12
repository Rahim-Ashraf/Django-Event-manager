from django.shortcuts import render
from django.http import HttpResponse
from events.models import Category, Event, Participant
from events.forms import EventModelForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def event_home(request):
    events = Event.objects.select_related('category').annotate(total_p=Count('participants'))
    context = {
        'events': events,
    }
    return render(request, 'event_home.html', context)


def specific_event(request, event_id):
    event = Event.objects.prefetch_related('participants').get(id=event_id)
    return render(request, 'specific_event.html', {'event': event})


def create_event(request):
    event_form = EventModelForm()
    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event created successfully')
        
    return render(request, 'event_form.html', {'event_form': event_form})


def create_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'participant created successfully')

    return render(request, 'participant_form.html', {'participant_form': participant_form})


def create_category(request):
    category_form = CategoryModelForm()
    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category created successfully')

    return render(request, 'category_form.html', {'category_form': category_form})


def dashboard(request):
    return render(request, 'dashboard.html')