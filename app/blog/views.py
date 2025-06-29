from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Post, Comment, Category

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published=True)
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(categories=selected_category)
    
    # Order by latest posts
    posts = posts.order_by('-created_at')
    
    # Get all categories with post count
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    
    context = {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category
    }
    
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:post_detail', slug=post.slug)
    
    # Get all categories for sidebar
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'categories': categories
    })
