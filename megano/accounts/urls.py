from django.urls import path

from accounts import views


urlpatterns = [
    path("sign-in", views.SignInView.as_view(), name="login"),
    path("sign-up", views.SignUpView.as_view(), name="register"),
    path("sign-out", views.SignOutView.as_view(), name="logout"),
    path("profile", views.ProfileDetailsView.as_view(), name="profile"),
    path("profile/password", views.UpdatePasswordView.as_view(), name="change_password"),
    path("profile/avatar", views.UpdateAvatarView.as_view(), name="change_password"),
]
