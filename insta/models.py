from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    photo = models.ImageField(
        default='default.jpg', upload_to='profiles/')
    bio = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    @classmethod
    def search_user(cls,username):    
        user = User.objects.get(username=username)
        return user

    @classmethod
    def get_profile(cls,name):
        profile= cls.objects.filter(user = name)
        return profile

    def save_profile(self):
        self.save()


    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.bio


class Post(models.Model):
    image = models.ImageField(upload_to='image_posts/')
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    posted_on = models.DateTimeField(auto_now_add=True, null=True)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def single_image(cls,image_id):
        '''
        function gets a single image posted by id
        '''
        image_posted=cls.objects.get(id=image_id)
        return image_posted

    @classmethod
    def get_image_id(cls,imageId):
        '''
        function that gets an image id    
        '''
        image_id=cls.objects.filter(id=imageId)
        return image_id


    @classmethod
    def get_user_posts(cls, user_id):
        '''
        function that gets user's posts
        '''
        posts = cls.objects.filter(
            posted_by__id__contains=user_id).order_by('-id')
        return posts

    @classmethod
    def get_posts(cls, search_term):
        '''
        function tha searches for posts with a similar name
        '''
        posts=cls.objects.filter(image_name__icontains=search_term)
        return posts

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.CharField(max_length=300)
    username = models.CharField(max_length=30)
    posted_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_post_comments(cls, id):
        '''
        function that gets all comments
        '''
        comments = cls.objects.filter(post__in=id)
        return comments

    @classmethod
    def update_caption(cls,comment_id, text):
        '''
        function that updates a comment
        '''
        searched=cls.objects.get(id=comment_id)
        searched.body=text
        searched.save()
        return searched

    def __str__(self):
        return self.body
