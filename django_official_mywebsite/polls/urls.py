from django.urls import path,include
from . import views

app_name='polls'

urlpatterns=[

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('add/question/',views.AddQuestion,name='add_question'),
    path('add/choice/<int:question_id>', views.AddChoice, name='add_choice'),
    path('add/choice/', views.AddChoice, name='add_choice'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('contact/',views.contact,name='contact'),
    path('edit/question/<int:question_id>', views.EditQuestion, name='edit_question'),
    path('edit/choice/<int:choice_id>', views.EditChoice,name='edit_choice'),



]





# urlpatterns=[
#     path('',views.index,name='index'),
#     path('<int:question_id>/',views.detail,name='detail'),
#     path('<int:question_id>/results/',views.results,name='results'),
#     path('<int:question_id>/vote/',views.vote,name='vote'),
# ]