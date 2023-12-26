from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout as auth_logout
from .models import Profile



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        profile_instance = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            if profile_instance:  # Save the profile only if it exists
                p_form.save()
            else:  # If profile doesn't exist, create one
                new_profile = p_form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def custom_logout(request):
    auth_logout(request)
    # Render the logout.html template after logout
    return render(request, 'users/logout.html')