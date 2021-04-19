from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    postId = models.AutoField(primary_key=True,default=None, blank=True) 
    title = models.CharField(max_length=255, default="")
    content = models.TextField()
    author = models.CharField(max_length=25, default="")
    timeStamp = models.DateTimeField(blank=True, default="")
    slug = models.CharField(max_length=130, default="")

    def __str__(self):
        return self.title + " by " + self.author
    


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True, default=None)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.comment[:13]}... by {self.user.first_name}"