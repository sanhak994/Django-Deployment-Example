from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm


##Imports:
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

#To make sure a view requires a user to be logged in
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


# imported logout above so can't call this just logout
# The decorator ensures that a person cannot see the logout request if they are
# not already logged in
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in!") #B/c of decorators only logged in users
                                              # will see this


def register(request):

    registered = False #Assume not registered

    if request.method == "POST": #If form is submitted (==POST) grab info from forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid and profile_form.is_valid(): #Check to see if forms are valid

            user = user_form.save() #grabbing the user form, saving it
            user.set_password(user.password) #hashing the password
            user.save() #saving the hash

            profile = profile_form.save(commit=False) #Check to see if profile form hash
            profile.user = user                       #has picture in it

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True #finally set registered = True

        else: #If something is not valid print out an error
            print(user_form.errors, profile_form.errors)

    else: #form not submitted (!=POST)
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered': registered})




### Logins

# def login... will cause errors in django, so make it more unique
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username") #b/c we're using simple HTML to capture Username
                                                # we can use .get()

        password = request.POST.get('password')

        #Again, we must specify that username = username and such to avoid django confusion
        user = authenticate(username=username, password = password) #all that is needed to authenticate user

        if user: #check if user is authenticated
            if user.is_active:
                login(request, user) #log them in
                return HttpResponseRedirect(reverse('index')) #send them back to homepage
            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed")
            print(f"\n\nUsername: {username} and password: {password}\n\n")
            return HttpResponse("Invalid Login details")

    else:
        return render(request, 'basic_app/login.html', {})
