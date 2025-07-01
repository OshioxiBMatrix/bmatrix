// JavaScript Trang Chủ - Chủ Đề Công Nghệ Hiện Đại

// Đợi toàn bộ tài liệu HTML được tải xong trước khi chạy mã
document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo WOW.js để tạo hiệu ứng cuộn trang
    if (typeof WOW !== 'undefined') {
        new WOW({
            boxClass: 'wow',
            animateClass: 'animated',
            offset: 100,
            mobile: true,
            live: true
        }).init();
    }
    
    // Khởi tạo các slider
    initSliders();
    
    // Khởi tạo hiệu ứng cuộn
    initScrollAnimations();
    
    // Khởi tạo hiệu ứng progress bar
    initProgressBars();
    
    // Khởi tạo modal xem nhanh sản phẩm
    initQuickViewModal();
    
    // Khởi tạo form liên hệ
    initContactForm();
});

// Khởi tạo các slider
function initSliders() {
    if (typeof Swiper !== 'undefined') {
        // Slider sản phẩm nổi bật
        const productShowcaseSlider = new Swiper('.product-showcase-slider', {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                640: { slidesPerView: 2 },
                768: { slidesPerView: 3 },
                1024: { slidesPerView: 4 },
            },
            on: {
                init: function() {
                    setTimeout(() => {
                        this.el.classList.add('slider-loaded');
                    }, 500);
                }
            }
        });
    }
}

// Khởi tạo hiệu ứng cuộn
function initScrollAnimations() {
    // Thêm lớp hiệu ứng cho các phần tử khi cuộn vào vùng nhìn thấy
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Hiệu ứng parallax cho hero section
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        // Hiệu ứng cho các shape trong hero section
        const heroShapes = document.querySelectorAll('.hero-shape-1, .hero-shape-2, .hero-shape-3');
        heroShapes.forEach((shape, index) => {
            const speed = 0.1 * (index + 1);
            const yPos = scrollPosition * speed;
            shape.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Khởi tạo hiệu ứng progress bar
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const targetWidth = entry.target.getAttribute('style') || entry.target.style.width;
                
                // Reset width to 0 first
                entry.target.style.width = '0%';
                
                // Then animate to target width
                setTimeout(() => {
                    entry.target.style.width = targetWidth;
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

// Khởi tạo modal xem nhanh sản phẩm
function initQuickViewModal() {
    const modal = document.getElementById('quick-view-modal');
    const closeButton = document.getElementById('quick-view-close');
    
    if (!modal || !closeButton) return;
    
    closeButton.addEventListener('click', function() {
        closeModal(modal);
    });
    
    // Đóng modal khi nhấp ra ngoài
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
    
    // Đóng modal khi nhấn ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal(modal);
        }
    });
}

// Mở modal xem nhanh sản phẩm
function showQuickView(productId) {
    const modal = document.getElementById('quick-view-modal');
    if (!modal) return;
    
    // Hiển thị trạng thái đang tải
    const content = document.getElementById('quick-view-content');
    if (content) {
        content.innerHTML = '<div class="flex justify-center items-center p-10"><div class="loader"></div></div>';
    }
    
    // Hiển thị modal với hiệu ứng
    modal.style.display = 'block';
    modal.classList.add('animate__animated', 'animate__fadeIn');
    
    // Mô phỏng tải dữ liệu sản phẩm
    setTimeout(() => {
        if (content) {
            content.innerHTML = `
                <div class="flex flex-col md:flex-row gap-6">
                    <div class="md:w-1/2">
                        <img src="https://via.placeholder.com/500" alt="Sản phẩm ${productId}" class="w-full h-auto rounded-lg">
                    </div>
                    <div class="md:w-1/2">
                        <h4 class="text-xl font-bold text-gray-800 mb-2">Sản phẩm ${productId}</h4>
                        <div class="text-primary-color font-bold text-xl mb-4">50.000 VNĐ</div>
                        <div class="flex items-center mb-4">
                            <div class="flex text-yellow-400">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star-half-alt"></i>
                            </div>
                            <span class="text-gray-500 ml-2">(4.5/5)</span>
                        </div>
                        <p class="text-gray-600 mb-6">Đây là mô tả sản phẩm mẫu. Trong ứng dụng thực tế, phần này sẽ được điền dữ liệu thật từ cơ sở dữ liệu.</p>
                        <form class="mb-4">
                            <div class="flex items-center mb-4">
                                <label class="mr-2">Số lượng:</label>
                                <div class="flex border rounded">
                                    <button type="button" class="px-3 py-1 bg-gray-100" onclick="decrementQuantity(this)">-</button>
                                    <input type="number" min="1" value="1" class="w-16 text-center border-x" readonly>
                                    <button type="button" class="px-3 py-1 bg-gray-100" onclick="incrementQuantity(this)">+</button>
                                </div>
                            </div>
                            <button type="submit" class="btn-primary w-full">
                                <i class="fas fa-shopping-cart mr-2"></i> Thêm vào giỏ hàng
                            </button>
                        </form>
                    </div>
                </div>
            `;
        }
    }, 800);
    
    setTimeout(() => {
        modal.classList.remove('animate__animated', 'animate__fadeIn');
    }, 1000);
}

// Đóng modal
function closeModal(modal) {
    modal.classList.add('animate__animated', 'animate__fadeOut');
    setTimeout(() => {
        modal.style.display = 'none';
        modal.classList.remove('animate__animated', 'animate__fadeOut');
    }, 500);
}

// Tăng số lượng sản phẩm
function incrementQuantity(button) {
    const input = button.parentNode.querySelector('input');
    input.value = parseInt(input.value) + 1;
}

// Giảm số lượng sản phẩm
function decrementQuantity(button) {
    const input = button.parentNode.querySelector('input');
    const value = parseInt(input.value);
    if (value > 1) {
        input.value = value - 1;
    }
}

// Thêm vào giỏ hàng với hiệu ứng
function addToCartAnimation(button) {
    button.classList.add('adding');
    
    // Hiệu ứng rung
    button.animate([
        { transform: 'scale(1)' },
        { transform: 'scale(1.2)' },
        { transform: 'scale(1)' }
    ], {
        duration: 500,
        iterations: 1
    });
    
    // Hiển thị thông báo
    showNotification('Đã thêm sản phẩm vào giỏ hàng!');
    
    setTimeout(() => {
        button.classList.remove('adding');
    }, 500);
}

// Chuyển đổi trạng thái yêu thích
function toggleWishlist(button, productId) {
    button.classList.toggle('in-wishlist');
    
    if (button.classList.contains('in-wishlist')) {
        // Thêm vào danh sách yêu thích
        button.innerHTML = '<i class="fas fa-heart" style="color: #ef4444;"></i>';
        button.animate([
            { transform: 'scale(1)' },
            { transform: 'scale(1.3)' },
            { transform: 'scale(1)' }
        ], {
            duration: 500,
            iterations: 1
        });
        
        showNotification('Đã thêm sản phẩm vào danh sách yêu thích!');
    } else {
        // Xóa khỏi danh sách yêu thích
        button.innerHTML = '<i class="far fa-heart"></i>';
        showNotification('Đã xóa sản phẩm khỏi danh sách yêu thích!', 'info');
    }
}

// Khởi tạo form liên hệ
function initContactForm() {
    const contactForm = document.querySelector('.contact-form');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Mô phỏng gửi form
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Đang gửi...';
        
        setTimeout(() => {
            submitButton.innerHTML = '<i class="fas fa-check mr-2"></i> Đã gửi';
            
            // Hiển thị thông báo
            showNotification('Tin nhắn của bạn đã được gửi thành công!');
            
            // Reset form
            contactForm.reset();
            
            // Khôi phục nút gửi
            setTimeout(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            }, 2000);
        }, 1500);
    });
}

// Hiển thị thông báo
function showNotification(message, type = 'success') {
    // Tạo phần tử thông báo
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate__animated animate__fadeInRight`;
    
    // Xác định biểu tượng dựa trên loại thông báo
    let icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'info') icon = 'fa-info-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${icon} notification-icon"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">×</button>
    `;
    
    // Thêm vào tài liệu
    document.body.appendChild(notification);
    
    // Tự động xóa sau 3 giây
    setTimeout(() => {
        notification.classList.remove('animate__fadeInRight');
        notification.classList.add('animate__fadeOutRight');
        
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 500);
    }, 3000);
    
    // Chức năng nút đóng
    const closeButton = notification.querySelector('.notification-close');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            notification.classList.remove('animate__fadeInRight');
            notification.classList.add('animate__fadeOutRight');
            
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 500);
        });
    }
}

// Thêm CSS cho thông báo
(function() {
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-width: 300px;
            z-index: 9999;
        }
        
        .notification-content {
            display: flex;
            align-items: center;
        }
        
        .notification-icon {
            margin-right: 10px;
        }
        
        .notification-success .notification-icon {
            color: #10b981;
        }
        
        .notification-error .notification-icon {
            color: #ef4444;
        }
        
        .notification-info .notification-icon {
            color: #3b82f6;
        }
        
        .notification-warning .notification-icon {
            color: #f59e0b;
        }
        
        .notification-close {
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #9ca3af;
        }
        
        .notification-close:hover {
            color: #4b5563;
        }
        
        .loader {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid #4f46e5;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .animated {
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
        }
    `;
    document.head.appendChild(style);
})();