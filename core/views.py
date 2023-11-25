
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import UserProfileForm





@login_required
def view_profile(request):
    # View user profile details
    return render(request, 'profile/view_profile.html')

@login_required
def edit_profile(request):
    # Edit user profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    # Change user password
    # Implement password change logic here
    return render(request, 'registration/change_password.html')


