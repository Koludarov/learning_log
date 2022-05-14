from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """Home page of Learning Log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Page of topics' list"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def check_user(topic, request):
    if topic.owner != request.user:
        raise Http404


@login_required
def topic(request, topic_id):
    """Opens one topic and all it's entries"""
    topic = Topic.objects.get(id=topic_id)
    # Checks topic's owner
    check_user(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Create new topic"""
    if request.method != 'POST':
        # No input - empty form
        form = TopicForm()
    else:
        # Data coming - catch input data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Show empty or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adds new entry to the selected topic"""
    topic = Topic.objects.get(id=topic_id)
    check_user(topic,request)
    if request.method != 'POST':
        # No input - empty form
        form = EntryForm()
    else:
        # Data coming - catch input data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topics', topic_id=topic_id)
    # Show empty or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edits entry that already exists"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_user(topic, request)

    if request.method != 'POST':
        # Current data saves
        form = EntryForm(instance=entry)
    else:
        # Sends data POST, catch data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


