from django.urls import path

from .views import view_profile, edit_profile, change_password, listen_webhook, LoginAPIView, SignupAPIView

urlpatterns = [
    path("api/user/login/", LoginAPIView.as_view(), name="user-login"),

    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path("webhooks/github/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",listen_webhook,),
    # Add other profile-related URLs as needed
    path("api/user/signup/", SignupAPIView.as_view(), name="user-signup"),

]
