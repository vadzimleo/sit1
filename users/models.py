from django.db import models
from PIL import Image
# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='picture.jpg', upload_to='profile_pics')
    #browser will look for default image in “C:\Users\Dell\New project\sit\media\picture.jpg”
    #http://127.0.0.1:8000/media/profile_pics/P10726-100510.jpg
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        #initially saving original size by running parent class's .save() method
        super().save()
        #then we grab this image and resize it 
        pct = Image.open(self.picture.path)
        output_size=(300, 300)
        if pct.height>300 or pct.width>300:
            pct.thumbnail(output_size)
            #overriding parent class's .save() method
            pct.save(self.picture.path)
            