
from django.shortcuts import render, redirect
from .forms import CreateUserForm, NoteCategoryForm, NoteForm, UpdateNoteForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .decorators import unauthenticated_user, verify_user_email, email_not_verified
from django.contrib import messages

'''Models'''
from .models import Note_category, Note, Profile
from django.contrib.auth.models import User

'''Datime'''
import datetime
import pytz

'''Settings'''
from django.conf import settings

'''Email stuff'''
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

'''Token'''
import random

# Create your views here.


@login_required(login_url='login')
def home(request):

    categories = Note_category.objects.filter(
        author=request.user).order_by('-date_created')

    context = {'categories': categories, 'title': 'Home'}
    return render(request, 'p_track_app/home.html', context)


# Authentication starts here ======>
@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in Successfully.')
                username = request.user.username
                email = request.user.email

                if (not request.user.profile.is_verified) and (not request.user.profile.sent_email):
                    token = ''.join([str(random.randrange(1,10)) for i in range(6)])
                    send_email(request, username=username, email = email, token=token)
                    
                    user_obj = User.objects.get(username = username)
                    profile_obj = Profile.objects.get(user= user_obj)
                    profile_obj.verification_code = token
                    profile_obj.save()
                else:
                    if (not request.user.profile.is_verified):
                        messages.warning(request, "Verify You Email.")

                return redirect('home')
            else:
                messages.warning(request, 'Password is incorrect.')
                return redirect('login')
        else:
            messages.warning(request, "No user with this username.")
            return redirect('login')
    else:
        return render(request, 'p_track_app/accounts/login.html')


@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, Account is created for you. ')
            return redirect('login')
        else:
            context = {'form': form}
            return render(request, 'p_track_app/accounts/register.html', context)
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'p_track_app/accounts/register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'You logged out successfully.')
    return redirect('login')

# accounts view ends here.


# Category views =========>
@login_required(login_url='login')
def create_category(request):

    if request.method == "POST":
        create_category_form = NoteCategoryForm(request.POST)
        if create_category_form.is_valid():
            category = create_category_form.save(commit=False)
            category.author = request.user
            create_category_form.save()
            category_id = category.id
            messages.info(request, 'New Category is created!')
            return redirect('view-category', pk=category_id)
    else:
        create_category_form = NoteCategoryForm()
    context = {'form': create_category_form, 'title': 'Create Note Category'}
    return render(request, 'p_track_app/category/create_note_category.html', context)


@login_required(login_url='login')
def view_category(request, pk):
    category = Note_category.objects.filter(id=pk, author = request.user).first()
    if category:
        category_notes = Note.objects.filter(category=category)
        context = {'title': 'View Category', 'category': category,
                'category_notes': category_notes}
        return render(request, 'p_track_app/category/view_note_category.html', context)
    else:
        return redirect('home')


@login_required(login_url='login')
@email_not_verified
def update_category(request, pk):
    category = Note_category.objects.filter(id=pk, author = request.user).first()

    if category:
        if request.method == 'POST':
            update_form = NoteCategoryForm(request.POST, instance=category)
            if update_form.is_valid():
                update_form.save()
                messages.info(request, 'This category is updated.')
                return redirect('view-category', pk=pk)
        else:
            update_form = NoteCategoryForm(instance=category)

        context = {'title': 'Update Category',
                'form': update_form, 'category': category}
        return render(request, 'p_track_app/category/update_note_category.html', context)
    else:
        return redirect("home")


@login_required(login_url='login')
@email_not_verified
def delete_category(request, pk):
    category = Note_category.objects.filter(id=pk, author=request.user).first()
    if category:
        if request.method == 'POST':
            category_name = category.category
            category.delete()
            messages.warning(
                request, f'"{category_name}" is deleted successfully.')
            return redirect('home')

        context = {'title': 'Delete Category', 'category': category}
        return render(request, 'p_track_app/category/delete_note_category.html', context)
    else:
        return redirect('home')

# Category views ends here =========>


# Notes Views starts here ==========>

@login_required(login_url='login')
def create_note(request, pk):
    category = Note_category.objects.filter(id=pk, author=request.user).first()

    if category:
        if request.method == 'POST':
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.category = category
                note_form.save()
                messages.info(request, 'New Note is created!')
                return redirect('view-category', pk=pk)
        else:
            note_form = NoteForm()

        context = {'form': note_form, 'title': 'Create Note', 'category': category}
        return render(request, 'p_track_app/notes/create_note.html', context)
    else:
        return redirect('home')


@login_required(login_url='login')
def view_note(request, pk):
    note = Note.objects.filter(id=pk).first()

    if note:    
        context = {'title': 'View Note', 'note': note}
        return render(request, 'p_track_app/notes/view_note.html', context)
    else:
        return redirect('home')


@login_required(login_url='login')
@email_not_verified
def update_note(request, pk):
    note = Note.objects.filter(id=pk).first()

    if note: 
        if request.method == "POST":
            update_form = UpdateNoteForm(request.user, request.POST, instance=note)
            if update_form.is_valid():
                update_form.save()
                messages.info(request, 'Your Note is Updated!')
                return redirect('view-note', pk=pk)
        else:
            update_form = UpdateNoteForm(request.user, instance=note)
        context = {'title': 'Update Note', 'form': update_form, 'note': note}

        return render(request, 'p_track_app/notes/update_note.html', context)
    else:
        return redirect('home')


@login_required(login_url='login')
@email_not_verified
def delete_note(request, pk):
    note = Note.objects.filter(id=pk).first()

    if note: 
        category = note.category

        if request.method == "POST":
            note.delete()
            messages.warning(request, 'Note delted successfully')
            return redirect('view-category', pk=category.id)

        context = {'title': 'Delete Note', 'note': note, 'category': category}
        return render(request, 'p_track_app/notes/delete_note.html', context)
    else:
        return redirect('home')


@login_required(login_url='login')
@verify_user_email
def verify_email(request):
    if request.method == 'POST':
        token = ''.join([str(random.randrange(1,10)) for i in range(6)])
        send_email(request, username=request.user, email = request.user.email, token=token)
        
        profile_obj = Profile.objects.get(user= request.user)
        profile_obj.verification_code = token
        profile_obj.save()

        return redirect('verify-email')

    return render(request, 'p_track_app/verification/verify-email.html')


@login_required(login_url='login')
@verify_user_email
def send_email(request, username, email, token):
    template_msg = render_to_string('p_track_app/verification/email-template.html', {'name': username, 'token':token})

    subject = 'Verify Your Ptrack Account.'
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, template_msg, email_from, recipient_list)
        email.fail_silently = False
        email.content_subtype = 'html'
        email.send()
        messages.info(request, "An email has been sent to the email address provided by you.")
    except:
        messages.error(request, "An error has occured while sending the email. Try again.")


@login_required(login_url='login')
@verify_user_email
def verify(request):
    if request.method == 'POST':
        user_token = str(request.POST.get('verification-code'))
    
        profile_obj = Profile.objects.get(user = request.user)

        valid_time = (datetime.datetime.now(tz=pytz.utc) < (request.user.profile.created + datetime.timedelta(minutes=5)))
        if not profile_obj.is_verified :
            if (profile_obj.verification_code == user_token) and (valid_time):

                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, 'Email has been verified.')
                return redirect('/')
            else:
                messages.warning(request, f'Code is valid for only 5 minutes. Try Resending the code.')
                return redirect('verify-email')
        else:
            messages.info(request, "You are already verified.")
            return redirect('/')
    else:
        messages.error(request, "An error has occured.")
        return redirect("/")
