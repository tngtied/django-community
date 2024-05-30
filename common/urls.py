from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'common'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('category/<int:category_id>', views.category, name='category'),
    path('mypage/', views.mypage, name='mypage'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='common/password_change.html', success_url='/common/mypage/'), name='password_change'),
]