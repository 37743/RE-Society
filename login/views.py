from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.views.generic import DetailView,ListView
from .models import Worker, Skill
# Create your views here.

def home(request):
    
    return render(request , "login/home.html")

def signIn(request):
    if(request.method == 'POST'):
        username = request.POST.get('Username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username = username , password = pass1)
        
        if(user is not None):
            login(request , user)
            fname = User.objects.filter(username=username)[0].first_name
            return render(request , "login/home.html", {'fname' : fname})
        else:
            messages.error(request, "Wrong User name or password")
            
    return render(request , "login/login.html")


def signUp(request):
    if request.method == 'POST':
        
        username = request.POST.get('Username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'login/signup.html')
        else:
            # Create a new user only if the username is not taken
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
                
        # Uncomment the following lines if you want to set first_name and last_name
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        messages.success(request, 'Your account has been successfully created')
        
        # Return an appropriate response, for example, redirect to a success page
        
    
    # Handle GET request or other cases
    return render(request, 'login/signup.html')

def signOut(request):
    logout(request)
    return redirect('home')   

class WorkerListView(ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "login/search.html"  # Provide the path to your template

    def get_queryset(self):
        skill_id = self.request.GET.get('skill_id')
        if skill_id:
            return Worker.objects.filter(skill__id=skill_id)
        else:
            return Worker.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()  # Pass all skills to the template
        return context
    
class WorkerDetailsView(DetailView):
    model = Worker
    template_name = 'login/worker_detail.html'
    context_object_name = 'worker'