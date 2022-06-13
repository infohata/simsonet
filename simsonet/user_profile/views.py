from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework import generics, permissions, exceptions
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from . forms import UserUpdateForm, UserProfileUpdateForm
from . import serializers, models
from simsonet_friends.models import Friend


@login_required
def view_my_profile(request):
    return render(request, 'user_profile/view_profile.html', {'user_': request.user })


def view_user_profile(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    friendship = Friend.objects.filter(friend=user_id, user=request.user).first()
    return render(request, 'user_profile/view_profile.html', {'user_': user, 'friendship': friendship })


@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('User {} profile was updated').format(request.user))
            return redirect('view_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.user_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user_profile/edit_profile.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # duomenu surinkimas
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validuosim forma, tikrindami ar sutampa slaptažodžiai, ar egzistuoja vartotojas
        error = False
        if not password or password != password2:
            messages.error(request, _('Passwords do not match or not entered.'))
            error = True
        if not username or get_user_model().objects.filter(username=username).exists():
            messages.error(request, _('User with username {} already exists.').format(username))
            error = True
        if not email or get_user_model().objects.filter(email=email).exists():
            messages.error(request, _('User with e-mail address {} already exists.').format(email))
            error = True
        if error:
            return redirect('register')
        else:
            get_user_model().objects.create_user(username=username, email=email, password=password)
            messages.success(request, _('User {} has been registered successfully. You can login now.').format(username))
            return redirect('index')
    return render(request, 'user_profile/register.html')


class UpdateProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        if self.request.user.is_authenticated:
            return models.UserProfile.objects.filter(user=self.request.user).first()
        else:
            raise exceptions.ValidationError(_('you must be logged in to update your profile').capitalize())

    def put(self, request, *args, **kwargs):
        profile = models.UserProfile.objects.filter(pk=self.request.user.user_profile.id)
        if profile.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise exceptions.ValidationError(_('you cannot edit profiles of other users').capitalize())


class CreateUserAPI(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

