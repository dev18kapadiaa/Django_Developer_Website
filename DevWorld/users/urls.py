from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserPage, name='login'),
    path('logout/', views.logoutUserPage, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.all_profile, name='profile'),
    path('user_profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('account/', views.userAccount, name='account'),
    path('editaccount/', views.editAccount, name='edit_account'),
    path('create-skill/', views.createSkill, name='create_skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update_skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete_skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<str:pk>/', views.view_message, name='message'),
    path('create_message/<str:pk>/', views.create_message, name='create_message'),
]