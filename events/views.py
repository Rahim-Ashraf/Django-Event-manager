from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Category, Event, Participant
from events.forms import EventModelForm, ParticipantModelForm, CategoryModelForm
from django.contrib import messages
from django.db.models import Count
from datetime import date, datetime

# Create your views here.
def event_home(request):
    events = Event.objects.select_related('category').annotate(total_p=Count('participants'))

    filter_category = request.GET.get('filter_category')
    filter_start_date = request.GET.get('filter_start_date')
    filter_end_date = request.GET.get('filter_end_date')

    search_text_name = request.GET.get('search_by_name', '').strip()
    search_text_location = request.GET.get('search_by_location', '').strip()
    if search_text_name:
        events = Event.objects.filter(name__icontains=search_text_name)
    elif search_text_location:
        events = Event.objects.filter(location__icontains=search_text_location)
    
    if filter_category:
        events = Event.objects.filter(category=filter_category)
    elif filter_start_date and filter_end_date:
        events = Event.objects.filter(date__gte=filter_start_date, date__lte=filter_end_date)
        print(filter_start_date)

    context = {
        'events': events,
        'categories': Category.objects.all()
    }
    return render(request, 'event_home.html', context)


def specific_event(request, event_id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=event_id)
    return render(request, 'specific_event.html', {'event': event})


def create_event(request):
    event_form = EventModelForm()
    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event created successfully')
            return redirect('add_event')
        else:
            messages.error(request, 'something went wrong')
        
    return render(request, 'event_form.html', {'event_form': event_form})


def update_event(request, id):
    task = Event.objects.get(id=id)
    event_form = EventModelForm(instance=task)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=task)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('update_event', id)
        else:
            messages.error(request, 'something went wrong')

    return render(request, "event_form.html", {'event_form': event_form})


def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
    else:
        messages.error(request, 'something went wrong')

    return redirect('home')


def create_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'participant created successfully')
            return redirect('add_participant')
        else:
            messages.error(request, 'something went wrong')

    return render(request, 'participant_form.html', {'participant_form': participant_form})


def create_category(request):
    category_form = CategoryModelForm()
    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category created successfully')
            return redirect('add_category')
        else:
            messages.error(request, 'something went wrong')

    return render(request, 'category_form.html', {'category_form': category_form})


def dashboard(request):
    total_participants = Participant.objects.aggregate(cnt=Count('id'))
    total_events = Event.objects.count()
    total_upcoming_events = Event.objects.filter(date__gt=datetime.now().date()).count()
    total_past_events = Event.objects.filter(date__lt=datetime.now().date()).count()
    events = Event.objects.filter(date=datetime.now().date())
    listing_title = "Today's Events Listing"

    listing_type = request.GET.get('listing')
    print(datetime.now().date(), datetime.now().time())
    if listing_type == 'total':
        events = Event.objects.all()
        listing_title = 'Total Events Listing'
    elif listing_type == 'upcoming':
        events = Event.objects.filter(date__gt=datetime.now().date())
        listing_title = 'Upcoming Events Listing'
    elif listing_type == 'past':
        events = Event.objects.filter(date__lt=datetime.now().date())
        listing_title = 'Past Events Listing'

    context = {
        'total_participants': total_participants['cnt'],
        'total_events': total_events,
        'events': events,
        'listing_title': listing_title,
        'total_upcoming_events': total_upcoming_events,
        'total_past_events': total_past_events
    }
    return render(request, 'dashboard.html', context)