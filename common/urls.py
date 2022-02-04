from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

# LoginView는 클래스이다. (Class Based View: CBV)
urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='common/login.html'),name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

# Get -> Form 화면
# 실패시 Post -> redirect
