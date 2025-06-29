from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:post_list') + f'?category={self.slug}'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    def get_related_posts(self):
        # First try to get posts with the same categories
        if self.categories.exists():
            related_posts = Post.objects.filter(
                categories__in=self.categories.all()
            ).exclude(id=self.id).filter(published=True).distinct()[:3]
            
            if related_posts.count() >= 3:
                return related_posts
        
        # If we don't have enough category-related posts, add posts by the same author
        author_posts = Post.objects.filter(
            Q(author=self.author) & ~Q(id=self.id) & Q(published=True)
        )
        
        if self.categories.exists():
            combined_posts = list(related_posts) + list(author_posts.exclude(id__in=related_posts.values_list('id', flat=True)))[:3]
        else:
            combined_posts = list(author_posts)[:3]
        
        # If we still don't have 3 related posts, add some recent posts
        if len(combined_posts) < 3:
            more_posts = Post.objects.filter(
                ~Q(id=self.id) & ~Q(id__in=[p.id for p in combined_posts]) & Q(published=True)
            ).order_by('-created_at')[:3-len(combined_posts)]
            
            combined_posts = combined_posts + list(more_posts)
            
        return combined_posts[:3]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"
