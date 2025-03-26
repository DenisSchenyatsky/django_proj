from typing import Optional, Any
from django.shortcuts import render, redirect, reverse

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse

from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView 
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView, View, UpdateView, DetailView, ListView, FormView

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission

from django.utils.translation import gettext_lazy as _, ngettext

from django.views.decorators.cache import cache_page


from .models import Profile

from .forms import UpdateProfileForm

from random import random    

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"



class UserListView(ListView):
    template_name = "myauth/users-list.html"
    model = Profile
    queryset = Profile.objects.all() # !!! objects переопределен
    context_object_name = "all_users"

class ProfileDetailsView(DetailView):
    template_name = "myauth/profile_detail.html"
    model = Profile
    
    
    
class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    # изменять только если есть разрешение
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.has_perm('myauth.change_profile') 
    
    template_name = "myauth/form_profile_update.html"
    model = Profile
    queryset = (
        Profile.objects
        .select_related("user")
    )
    fields = ('user','bio', 'avatar',)
   
    
    def get_success_url(self):
        return reverse(
            "myauth:profile-details",
            kwargs = {"pk": self.object.pk})

    def form_valid(self, form):
        # Проверка на наличие разрешения
        obj = form.save(commit=False)
        if self.request.user.is_superuser or (obj.user == self.request.user):
            print("Data were change")
            return super(ProfileUpdateView, self).form_valid(form)
        #else
        print("Data were not change")
        return super(ProfileUpdateView, self).form_invalid(form)



      
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        content_type = ContentType.objects.get_for_model(Profile)
        profile_permission = Permission.objects.filter(content_type=content_type)
        for perm in profile_permission:
            user.user_permissions.add(perm)

        
        login(request=self.request, user=user)        
        return response


class MyLoginView(LoginView):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            context = {}
            if request.user.is_authenticated:                
                context = {"user": request.user }
            #else
            return render(request, 'myauth/login.html', context=context)
        #else
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect("/admin/")
        #else
        return render(request, "myauth/login.html", context={"error": "Invalid login data"})

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

def pre_logout_view(request: HttpRequest, username: Optional[str]=None) -> HttpResponse:
    context = {"username": username}
    return render(request, "myauth/logout.html",context=context)



@user_passes_test(lambda u:u.is_superuser)        
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("cheese", "jazz", max_age=3600)
    return response

@cache_page(30)
@permission_required("myauth.view_profile")
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("cheese", "cheese not found")
    return HttpResponse(f"Cookies Values: '{value}   {random()}'")

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["some_session_key"] = "some_session_value"
    return HttpResponse("Session set")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("some_session_key", "key_not_found")
    return HttpResponse(f"Session values = '{value}'")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"some_key": "some_value", "3": 5})
    
    
class HelloView(View):
    wlcm_msg = _("welcome hello world")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items_int = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items_int
        )
        products_line = products_line.format(count=items_int)
        return HttpResponse(f"<h1>{self.wlcm_msg}</h1> <h2>{products_line}</h2>")