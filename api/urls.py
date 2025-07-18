from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('user-update/', UserUpdateView.as_view()),
    path('backup/', BackupView.as_view()),
    path('restore/', RestoreView.as_view()),
    path('user-delete/', DeleteAccountView.as_view()),
]

