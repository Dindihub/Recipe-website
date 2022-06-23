
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Profile,Recipe,Category,Comment


# Create your views here.
def index(request):
    return render(request,"index.html")

def about_us(request):
    return render(request,"about_us.html")

def home(request):
    recipes=Recipe.objects.all()

    context = {
        'recipes':recipes
    }
    return render(request,"home.html",context)


def register(request):
    form=RegisterUserForm

    if request.method =='POST':
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,("registration successful"))
        
            return redirect('login')
    context={'form':form}

    return render(request,'registration/register.html',context)

def login_in(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("login successful"))
            return redirect('home')
        
    context={}
    return render(request,'registration/login.html')

def log_out(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def profile(request):
    profiles=Profile.objects.get(user=request.user)
       
    context={
        
        'profiles':profiles, 
        }
    return render(request, 'profile.html',context)

@login_required(login_url='login')
def update_profile(request):
    profiles = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        prof_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if  prof_form.is_valid():
            prof_form.save()
            return redirect('profile')
       
    else:
        
        prof_form = UpdateProfileForm(instance=request.user.profile)
             
    context={
        'profiles':profiles,
      
        'prof_form': prof_form,
        
        }
    
    return render(request, 'update_profile.html',context)

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user.profile
            recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'create_recipe.html', {'form': form})

def search_recipe(request):
    if 'recipe' in request.GET and request.GET["recipe"]:
    # if request.method == 'GET':
        search_term= request.GET.get("recipe")
        results = Recipe.search_recipe(search_term)
        print(results)
        message = f'search_term'
        context = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', context)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})

def single_recipe(request, id):
    recipe=Recipe.objects.get(id=id)
    request.user.profile.recipe = recipe
    request.user.profile.save()

    context={
            'recipe' : recipe,
            
            }
    return render(request,'single_recipe.html',context )
