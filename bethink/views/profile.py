from bethink.forms.profile import ProfileForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
# from bethink.models.profile import Profile


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('bethink:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        # user = Profile.objects.get_or_create(user=request.user)
        # profile_form = ProfileForm(instance=Profile.objects.get_or_create(user=request.user))
        # userprofile = Profile.objects.create(user=request.user, tg_id='5616515')
    return render(request, 'bethink/profile.djt', {
        'form': profile_form
    })
