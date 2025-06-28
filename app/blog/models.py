from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_related_posts(self):
        # Get posts by same author, excluding this post
        related_posts = Post.objects.filter(
            Q(author=self.author) & ~Q(id=self.id) & Q(published=True)
        )[:3]
        
        # If we don't have 3 related posts yet, add some recent posts
        if related_posts.count() < 3:
            more_posts = Post.objects.filter(
                ~Q(id=self.id) & ~Q(id__in=related_posts.values_list('id', flat=True)) & Q(published=True)
            ).order_by('-created_at')[:3-related_posts.count()]
            
            related_posts = list(related_posts) + list(more_posts)
            
        return related_posts

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"
