from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),     # config/urls.py에서 'pybo/' + '' --> 'pybo/'            # 보통 첫페이지를 index 페이지라고 부른다.
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create ,name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    
]