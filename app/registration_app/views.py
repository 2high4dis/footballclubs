from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created!')
            return redirect('login')
        else:
            form = UserRegisterForm()
            return render(request=request, template_name='registration/registration.html', context={'form': form})
    else:
        form = UserRegisterForm()
        return render(request=request, template_name='registration/registration.html', context={'form': form})


@login_required
def profile(request):
    return render(request, template_name='registration/profile.html')
