from django import forms
from .models import Question,Choice
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class QuestionForm(forms.Form):
     question_text= forms.CharField(label='Question Text', max_length=200)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(label="send me a copy of response",required=False)

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model= Question
#         fields= ('question_text',)
class ChoiceForm(forms.ModelForm):
    class Meta:
        model= Choice
        fields= ('question','choice_text')

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )

"Password1 and password2 are defined in UserCreationForm whereas Password is defined in User"


# class SignUpForm(forms.ModelForm):
#
#     password=forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model= User
#         fields=['username','email','password']



# class SignUpForm(forms.Form):
#     username = forms.CharField(
#         required = True,
#         label = 'Username',
#         max_length = 32
#     )
#     email = forms.CharField(
#         required = True,
#         label = 'Email',
#         max_length = 32,
#     )
#     password = forms.CharField(
#         required = True,
#         label = 'Password',
#         max_length = 32,
#         widget = forms.PasswordInput()
#     )