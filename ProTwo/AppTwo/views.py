from django.shortcuts import render

# Create your views here.
from AppTwo.models import User

def index(request):
    return render(request, 'AppTwo/index.html')

def users(request):

    user_list = User.objects.order_by('first_name')
    user_dict = {"users" :user_list}

    return render(request,"AppTwo/users.html", context = user_dict)
