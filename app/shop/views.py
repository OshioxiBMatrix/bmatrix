from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from blog.models import Post
from .models import Product, Category, Brand
from .templatetags.shop_tags import format_price

# Create your views here.
def home(request):
    # Get featured products from the database
    featured_products = Product.objects.filter(featured=True).order_by('-created_at')[:4]
    
    # Get latest products from the database
    latest_products = Product.objects.all().order_by('-created_at')[:4]
    
    testimonials = [
        {'name': 'John William', 'text': 'Đánh giá tốt về sản phẩm. Chúng tôi rất hài lòng về sản phẩm và chất lượng dịch vụ được cung cấp cho chúng tôi.'},
        {'name': 'Sarah Johnson', 'text': 'Hỗ trợ khách hàng tốt và chất lượng sản phẩm. Sẽ khuyến khích bạn bè và gia đình sử dụng.'},
        {'name': 'Michael Chen', 'text': 'Vận chuyển nhanh chóng và đóng gói tốt. Sản phẩm vượt xa mong đợi của tôi.'},
    ]
    
    # Get real blog posts from the database
    blog_posts = Post.objects.filter(published=True).order_by('-created_at')[:3]
    
    # Fallback to sample data if no blog posts exist
    if not blog_posts:
        blog_posts = [
            {'title': 'Chúng tôi rất hài lòng về sản phẩm và chất lượng', 'date': '14/06/2023', 'author': 'Admin', 'excerpt': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel ultricies.'},
            {'title': 'Top 10 phụ kiện chơi game năm 2023', 'date': '10/06/2023', 'author': 'Tech Team', 'excerpt': 'Khám phá những phụ kiện chơi game tốt nhất để nâng cao trải nghiệm chơi game của bạn.'},
            {'title': 'Hướng dẫn xây dựng PC chơi game đầu tiên', 'date': '05/06/2023', 'author': 'Build Team', 'excerpt': 'Hướng dẫn từng bước để xây dựng PC chơi game đầu tiên cho người mới bắt đầu.'},
        ]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
    }
    
    return render(request, 'shop/home.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    
    # Filter by category if provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Get filter parameters
    selected_availability = request.GET.getlist('availability')
    selected_brands = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Filter by availability
    if selected_availability:
        products = products.filter(availability__in=selected_availability)
    
    # Filter by brand
    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)
    
    # Filter by price range
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort products
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        # Default sorting by newest
        products = products.order_by('-created_at')
    
    # Prepare selected values for the template
    selected_brands_ids = [int(b) for b in selected_brands] if selected_brands else []
    
    context = {
        'category': category,
        'categories': categories,
        'brands': brands,
        'products': products,
        'availability_choices': Product.AVAILABILITY_CHOICES,
        'selected_availability': selected_availability,
        'selected_brands_ids': selected_brands_ids,
        'min_price': min_price or 0,
        'max_price': max_price or 10000000,
        'sort_by': sort_by or 'created_at',
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'shop/product_detail.html', context)

def product_quickview(request, product_id):
    """API endpoint to get product data for quick view"""
    try:
        # Try to find product by ID first, then by slug if ID is not numeric
        if product_id.isdigit():
            product = get_object_or_404(Product, id=product_id)
        else:
            product = get_object_or_404(Product, slug=product_id)
        
        # Get all product images
        images = []
        if product.image:
            images.append({
                'id': 'main',
                'url': request.build_absolute_uri(product.image.url),
                'is_main': True
            })
        
        for img in product.images.all():
            images.append({
                'id': img.id,
                'url': request.build_absolute_uri(img.image.url),
                'alt': img.alt_text or product.name
            })
        
        # Format product data
        data = {
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'description': product.description,
            'price': float(product.price),
            'price_formatted': format_price(product.price),
            'availability': product.availability,
            'availability_display': dict(Product.AVAILABILITY_CHOICES).get(product.availability),
            'stock': product.stock,
            'images': images,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
                'slug': product.category.slug,
                'url': request.build_absolute_uri(product.category.get_absolute_url())
            },
            'url': request.build_absolute_uri(product.get_absolute_url())
        }
        
        # Add brand info if available
        if product.brand:
            data['brand'] = {
                'id': product.brand.id,
                'name': product.brand.name,
                'slug': product.brand.slug
            }
        else:
            data['brand'] = None
        
        return JsonResponse({'success': True, 'product': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
