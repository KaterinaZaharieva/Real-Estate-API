"""import models for creating database tables"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    """extends the default database and adds field is_agent"""
    user = models.ForeignKey(User, related_name='userprofile', on_delete=models.CASCADE)
    is_agent = models.BooleanField()

User.userprofile = property(lambda u:UserProfile.objects.get_or_create(user=u)[1])

class Post(models.Model):
    """creating post table"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    price = models.CharField(max_length=10)
    contact_us = models.TextField()
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
        """returns the post title"""
        return self.title


class ReviewRating(models.Model):
    """ database for Review"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    internet_protocol = models.CharField(max_length=20, blank=True)

    def __str__(self):
        """how to show Reviews in admin site"""
        return self.post.title

class Inspection(models.Model):
    """database for inspections """
    post = models.ForeignKey(Post, related_name='inspection', on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    contact_info = models.TextField()

    created_by = models.ForeignKey(User, related_name='inspection', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ConversationMessage(models.Model):
    """database for message """
    post = models.ForeignKey(Post, related_name='converstionmessage',on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name='converstionmessage',
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """how to show messages"""
        ordering = ['created_at']

class Notification(models.Model):
    """database for notifications"""
    MESSAGE = 'message'
    INSPECTION = 'inspection'

    CHOICES = (
        (MESSAGE, 'Message'),
        (INSPECTION, 'inspection')
    )

    to_user = models.ForeignKey(User, related_name='announcment', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """how to be displayed (in what order) on the site"""
        ordering = ['-created_at']
