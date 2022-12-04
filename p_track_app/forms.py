from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):

    username = forms.RegexField(
    label=_("Login"), max_length=30, regex=r"^[\w.@+-]+$",
    help_text=_("Required. 30 characters or fewer. Letters, digits and "
                "@/./+/-/_ only."),
    widget=forms.TextInput(attrs={'class': 'form-control',
                            'required': 'true',
        })
    )

    email = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                    'type': 'email',
                                    'required': 'true',
                                    'autocomplete':'off'
        })
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                        'required': 'true',
        }),
        help_text=_("Must contain atleast 8 characters, can't be commanly used, can't be too similar to other personal details and can't be all numeric.")
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                        'type': 'password',
                                        'required': 'true',
        }),
        help_text=_("Enter the same password as above, for verification.")
    )

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email = email):
            msg = 'Email is already taken.'
            self.add_error('email', msg)




    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NoteCategoryForm(ModelForm):
    class Meta:
        model=Note_category
        fields = '__all__'
        exclude  = ['author']

class NoteForm(ModelForm):
    class Meta:
        model=Note
        fields = '__all__'
        exclude  = ['category']

class UpdateNoteForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UpdateNoteForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['category'].queryset = Note_category.objects.filter(author=user)

    class Meta:
        model = Note
        fields = '__all__'