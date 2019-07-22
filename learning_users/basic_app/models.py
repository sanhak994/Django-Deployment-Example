from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete='CASCADE')

    # additional classes
    portfolio_site = models.URLField(blank = True) #blank = T, user can leave it blank

    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True) #must make the new folder under media


    def __str__(self): #Creating this just incase we need to print something out.
        return self.user.username
