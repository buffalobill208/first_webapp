from django.db import models
from django.utils import timezone
# import the user authentication module so that we use the built in authentication model in this app
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # on_delete function deletes all related posts when a user is deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # dunder or double underscore str method is a String representation of an object.  We can use this method to represent the Post titles.
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
