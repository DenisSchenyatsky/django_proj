from django.urls import path
from .views import (
    pre_logout_view,
    set_cookie_view, 
    get_cookie_view,
    set_session_view,
    get_session_view,
    
    MyLogoutView,
    MyLoginView,
    
    AboutMeView,
    RegisterView,
    
    UserListView,
    ProfileDetailsView,
    ProfileUpdateView,
    
    FooBarView,
    
    HelloView,
)

app_name = "myauth"

urlpatterns = [
    path("login/", 
         MyLoginView.as_view(template_name="myauth/login.html"),
         name="login"),
   
    path("prelogout/<str:username>/", pre_logout_view, name="pre_logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
         
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/set", set_session_view, name="session-set"),
    path("session/get", get_session_view, name="session-get"),
    
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    
    path("users/", UserListView.as_view(), name="users-list"),
    path("profile/<int:pk>/details/", ProfileDetailsView.as_view(), name="profile-details"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    
    path("register/", RegisterView.as_view(), name="register"),
    
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
    
    path("hello/", HelloView.as_view(), name="hello"),
    
]