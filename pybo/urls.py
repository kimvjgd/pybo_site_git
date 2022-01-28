from django.urls import path
from .views import index, detail

app_name = 'pybo'

urlpatterns = [
    path('', index, name='index'),     # config/urls.py에서 'pybo/' + '' --> 'pybo/'            # 보통 첫페이지를 index 페이지라고 부른다.
    path('<int:question_id>/', detail, name='detail'),
]