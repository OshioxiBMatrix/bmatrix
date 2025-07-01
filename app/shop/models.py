from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Product(models.Model):
    AVAILABILITY_CHOICES = (
        ('in_stock', 'Còn hàng'),
        ('out_of_stock', 'Hết hàng'),
        ('pre_order', 'Đặt trước'),
        ('discontinued', 'Ngừng kinh doanh'),
        ('coming_soon', 'Sắp có hàng'),
    )
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])
    
    def get_main_image(self):
        """Return the main product image or the first additional image if no main image exists"""
        if self.image:
            return self.image.url
        
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        
        # Return a placeholder if no images exist
        return '/static/img/placeholder.png'
    
    def get_all_images(self):
        """Return all product images including the main one"""
        images = []
        if self.image:
            images.append({
                'id': 'main',
                'url': self.image.url,
                'is_main': True
            })
        
        for img in self.images.all():
            images.append({
                'id': img.id,
                'url': img.image.url,
                'is_main': False
            })
        
        return images

class ProductImage(models.Model):
    """Model for additional product images"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/additional/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('order',)
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
    
    def __str__(self):
        return f"Image for {self.product.name} ({self.id})"
