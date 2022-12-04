from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def verify_user_email(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.is_verified:
            return redirect("/")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def email_not_verified(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.profile.is_verified:
            messages.warning(request, 'You need to verify your account first, to use this feature.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func