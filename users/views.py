from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Registers new user"""
    if request.method != 'POST':
        # Shows empty form of registration
        form = UserCreationForm()
    else:
        # Processed input form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # User's log in and redirects to home page
            login(request, new_user)
            return redirect('learning_logs:index')

    # Shows empty or invalid form
    context = {'form': form}
    return render(request, 'users/register.html', context)