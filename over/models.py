from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class PostView(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)

  def __str__(self):
      return self.user.username

class Comment(models.Model):
  content = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)  
  post = models.ForeignKey('Post', on_delete=models.CASCADE) 
  date_commented = models.DateTimeField(auto_now_add=True)
  reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='replies')

  def __str__ (self):
    return self.post.title 

class Post(models.Model):
  title = models.CharField(max_length=255)
  thumbnail = models.ImageField()
  content = models.TextField()
  date_created = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  featured = models.BooleanField(default=False)

  
  @property
  def comment_count(self):
    return Comment.objects.filter(post=self)
  
  @property
  def count_view(self):
    return PostView.objects.filter(post=self).count()
  

  def __str__ (self):
    return self.title

  def get_absolute_url(self):
      return reverse("post_detail", kwargs={"pk": self.pk})

  def save(self,  *args, **kwargs):

    if self.featured:

      try:

        current_featured_post = Post.objects.get(featured=True)

        if self != current_featured_post:

          current_featured_post.featured=False

          current_featured_post.save()

      except Post.DoesNotExist:
        pass

    super(Post, self).save(*args, **kwargs)    
     
