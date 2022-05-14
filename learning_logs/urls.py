"""Find out our URL for learning_logs"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # List of topics
    path('topics/', views.topics, name='topics'),
    # Page with full information about each topic
    path('topics/<int:topic_id>', views.topic, name='topics'),
    # Page for user adding new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for user adding new entry
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    # Page for editing entries
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]