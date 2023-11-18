from django.db import models
from django.urls import reverse
#return str('url') to rout & let the view redirect that rout;
# not redirect to that rout specifically !

# Create your models here.
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(
#         'auth.User',
#         on_delete=models.CASCADE,
#     )
#     body = models.TextField()
 
#     def __str__(self):
#         return self.title


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content=models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,  on_delete = models.CASCADE)

    #ImproperlyConfigured at /post/new/
    #No URL to redirect to.
    #Either provide a url or define a get_absolute_url method on the Model.
    
    def get_absolute_url(self):
    #return a full path as str('url') to a specific post
        return reverse('post', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    