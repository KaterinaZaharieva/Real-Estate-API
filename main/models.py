"""import models for creating database tables"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    """ creating post table"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, default='default')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")
    favourites = models.ManyToManyField(
                                        User, related_name='favourite', default=None,blank=True)

    def get_absolute_url(self):
        """returns the single post url"""
        return reverse('post_single', args=[self.slug])


    def __str__(self):
        """ returns the post title"""
        return self.title


class ReviewRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.subject