from django.shortcuts import render
from blog.models import Post

# Create your views here.
def home(request):
    # Sample data for demonstration
    featured_products = [
        {'title': 'Gaming Mouse', 'old_price': '40.000', 'price': 23000, 'image': 'https://placehold.co/300x300'},
        {'title': 'Mechanical Keyboard', 'old_price': '120.000', 'price': '89.000', 'image': 'https://placehold.co/300x300'},
        {'title': 'Gaming Headset', 'old_price': '80.000', 'price': '59.000', 'image': 'https://placehold.co/300x300'},
        {'title': 'Gaming Monitor', 'old_price': '350.000', 'price': '299.000', 'image': 'https://placehold.co/300x300'},
    ]
    
    latest_products = [
        {'title': 'RTX 4070 GPU', 'old_price': '650.000', 'price': '599.000', 'image': 'https://placehold.co/300x300'},
        {'title': 'Intel i9', 'old_price': '480.000', 'price': '420.000', 'image': 'https://placehold.co/300x300'},
        {'title': 'RGB Gaming Case', 'old_price': '120.000', 'price': '95.000', 'image': 'https://placehold.co/300x300'},
        {'title': '32GB RAM Kit', 'old_price': '180.000', 'price': '140.000', 'image': 'https://placehold.co/300x300'},
    ]
    
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
