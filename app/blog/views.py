from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment

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
    category = request.GET.get('category', '')
    if category:
        # In a real app, you'd have a Category model and filter by that
        # For now, we'll just simulate category filtering
        if category == 'ai-ml':
            posts = posts.filter(Q(title__icontains='AI') | Q(content__icontains='AI') | 
                                Q(title__icontains='Machine Learning') | Q(content__icontains='Machine Learning'))
        elif category == 'web-dev':
            posts = posts.filter(Q(title__icontains='Web') | Q(content__icontains='Web') |
                                Q(title__icontains='JavaScript') | Q(content__icontains='JavaScript'))
        elif category == 'mobile-dev':
            posts = posts.filter(Q(title__icontains='Mobile') | Q(content__icontains='Mobile') |
                                Q(title__icontains='App') | Q(content__icontains='App'))
        elif category == 'database':
            posts = posts.filter(Q(title__icontains='Database') | Q(content__icontains='Database') |
                                Q(title__icontains='SQL') | Q(content__icontains='SQL'))
        elif category == 'architecture':
            posts = posts.filter(Q(title__icontains='Architecture') | Q(content__icontains='Architecture') |
                                Q(title__icontains='Microservice') | Q(content__icontains='Microservice'))
    
    # Order by latest posts
    posts = posts.order_by('-created_at')
    
    categories = [
        {'name': 'AI & Machine Learning', 'slug': 'ai-ml'},
        {'name': 'Web Development', 'slug': 'web-dev'},
        {'name': 'Mobile Development', 'slug': 'mobile-dev'},
        {'name': 'Database', 'slug': 'database'},
        {'name': 'Architecture', 'slug': 'architecture'}
    ]
    
    context = {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category
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
    
    return render(request, 'blog/post_detail.html', {'post': post})
