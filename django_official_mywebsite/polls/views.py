from .models import Question,Choice
from django.views import generic
from django.urls import reverse,reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import QuestionForm,ContactForm,ChoiceForm,SignUpForm
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms


from django.core.mail import send_mail

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_qlist'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

class SearchView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_qlist'

    def get_queryset(self):

        if(self.request.method=="GET"):
            search_term=self.request.GET.get('search_key')
            return Question.objects.filter(question_text__regex=r'%s'%search_term)
        else:
            return redirect(reverse('polls:index'))



def vote(request, question_id):

    question=get_object_or_404(Question,pk=question_id)

    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])

    except (KeyError,choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message': "Please select a valid choice"
        })

    else:
        selected_choice.votes+=1;
        selected_choice.save();


        return redirect(reverse('polls:results', args=(question_id,)))
        # return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

#Without using model form

def AddQuestion(request):

    if request.method=="POST":
        form= QuestionForm(request.POST)

        if form.is_valid():
            question=Question()
            question.question_text= form.cleaned_data['question_text']
            question.pub_date=timezone.now()
            question.save()
            return redirect(reverse('polls:index'))

    else:
        form=QuestionForm()

    return render(request,'polls/add_form.html',{'form_type': 'question','form':form,'action':'add'})

def EditQuestion(request,question_id):

    question=get_object_or_404(Question,pk=question_id)

    if request.method=='POST':
        form=QuestionForm(request.POST)

        if form.is_valid():
            question.question_text= form.cleaned_data['question_text']
            question.save()
            return redirect(reverse('polls:detail',args=(question.id,)))

    else:
            # form=QuestionForm({'question_text':question.question_text})
            form = QuestionForm(initial={'question_text': question.question_text})
    return render(request,'polls/add_form.html',{'form':form,'action':'edit','form_type': 'question'})


'''

# using model form

def AddQuestion(request):

    if request.method=='POST':
        form=QuestionForm(request.POST)

        if form.is_valid():
            question=form.save(commit=False)
            question.pub_date=timezone.now()
            question.save()
            return redirect(reverse('polls:detail',args=(question.id,)))

    else:
            form=QuestionForm()
    return render(request,'polls/add_form.html',{'form':form,'form_type': 'question','action':'add'})

def EditQuestion(request,question_id):

    question=get_object_or_404(Question,pk=question_id)

    if request.method=='POST':
        form=QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question=form.save(commit=False)
            question.save()
            return redirect(reverse('polls:detail',args=(question.id,)))

    else:
            form=QuestionForm(instance=question)
    return render(request,'polls/add_form.html',{'form':form,'action':'edit','form_type': 'question'})
'''

def AddChoice(request,question_id=0):
    if(question_id):
        question=get_object_or_404(Question,pk=question_id)
    else:
        question=None

    if request.method=="POST":
        form= ChoiceForm(request.POST)

        if form.is_valid():
            choice=form.save()
            return redirect(reverse('polls:detail',args=(choice.question.id,)))

    else:
        form=ChoiceForm(initial={'question':question})

    return render(request,'polls/add_form.html',{'form_type': 'choice','form':form,'action':'add'})

def EditChoice(request,choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)

    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)

        if form.is_valid():
            choice = form.save()
            return redirect(reverse('polls:detail', args=(choice.question.id,)))

    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'polls/add_form.html', {'form': form, 'action': 'edit', 'form_type': 'choice'})



def contact(request):
    if request.method=="POST":
        form= ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            superusers_emails = User.objects.filter(is_superuser=True).values_list('email')
            recipients =list(superusers_emails[0])
            if cc_myself:
                recipients.append(sender)

            #send_mail(subject,message,sender,recipients)


            return redirect(reverse('polls:index'))

    else:
        form=ContactForm()

    return render(request,'polls/form.html',{'form':form})





#Using CreateFormView Signup With Extra Fields without generic view

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



'''
# Using CreateFormView Signup With Extra Fields with generic view

class signup(generic.CreateView):
    form_class=SignUpForm
    success_url=reverse_lazy('home')
    template_name= 'registration/signup.html'


'''


#Extra field without model form or usercreateview ie from the basics
'''
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('home')
            else:

                ####################ask how to return this error back to form#############
                form.fields['email'].errors=['Email address already exists']

                raise forms.ValidationError('Looks like a username with that email or password already exists')


    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


'''



#Using Model Forms with Extra Fields without createformview
"""
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():

            user=form.save(commit=False)
            print(form.cleaned_data)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


"""



#Signup Without Extra Fields using createformview

"""

def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            print(form.cleaned_data)
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user= authenticate(username=username,password=password)

            login(request,user)
            return redirect('home')



    else:
        form= UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})

"""



'''
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse

def index(request):
    latest_qlist= Question.objects.order_by('-pub_date')[:5]

    return render(request,'polls/index.html',{'latest_qlist':latest_qlist})

    # template=loader.get_template('polls/index.html')
    #
    # return HttpResponse(template.render({'latest_qlist':latest_qlist},request))

def detail(request, question_id):

    question= get_object_or_404(Question,pk=question_id)

    return render(request,'polls/detail.html',{'question':question})


    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):

    question=get_object_or_404(Question,pk=question_id)

    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])

    except (KeyError,choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message': "Please select a valid choice"
        })

    else:
        selected_choice.votes+=1;
        selected_choice.save();
        # return redirect(reverse('polls:results', args=(question_id,)))
        # return redirect(results,question_id=question_id)
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))
        

'''