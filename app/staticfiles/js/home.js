// JavaScript Trang Chủ - Chủ Đề Công Nghệ

// Đợi toàn bộ tài liệu HTML được tải xong trước khi chạy mã
document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo WOW.js để tạo hiệu ứng cuộn trang
    if (typeof WOW !== 'undefined') {
        new WOW({
            boxClass: 'animate__animated', // Lớp áp dụng cho các phần tử cần hiệu ứng
            animateClass: 'animate__animated', // Lớp kích hoạt hiệu ứng
            offset: 100, // Khoảng cách từ mép dưới viewport để kích hoạt (px)
            mobile: true, // Cho phép hiệu ứng trên thiết bị di động
            live: true // Tự động phát hiện phần tử mới
        }).init();
    }
    
    // Khởi tạo các slider sản phẩm
    initProductSliders();
    
    // Khởi tạo bộ đếm ngược cho ưu đãi đặc biệt
    initCountdownTimer();
    
    // Khởi tạo hiệu ứng hover cho các phần tử tương tác
    initHoverEffects();
    
    // Khởi tạo hiệu ứng parallax cho phần hero
    initParallax();
    
    // Khởi tạo bộ lọc danh mục sản phẩm
    initCategoryFilter();
    
    // Khởi tạo hiệu ứng cuộn trang
    initScrollAnimations();
    
    // Khởi tạo modal xem nhanh sản phẩm
    initQuickViewModal();
    
    // Khởi tạo con trỏ theo chủ đề công nghệ (tùy chọn, hiện bị vô hiệu hóa)
    // initTechCursor();
});

// Hàm xử lý hiệu ứng cuộn trang
function initScrollAnimations() {
    // Thêm lớp hiệu ứng cho các phần tử khi cuộn vào vùng nhìn thấy
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated'); // Thêm lớp animated khi phần tử xuất hiện
                observer.unobserve(entry.target); // Ngừng theo dõi sau khi kích hoạt
            }
        });
    }, { threshold: 0.1 }); // Kích hoạt khi 10% phần tử xuất hiện
    
    animatedElements.forEach(element => {
        observer.observe(element); // Theo dõi từng phần tử
    });
    
    // Thêm hiệu ứng trôi nổi cho các phần tử được chỉ định
    const floatingElements = document.querySelectorAll('.floating:not(.animate__animated)');
    floatingElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.2}s`; // Độ trễ để tạo hiệu ứng xen kẽ
    });
}

// Khởi tạo các slider sản phẩm
function initProductSliders() {
    // Kiểm tra xem Swiper có sẵn không
    if (typeof Swiper !== 'undefined') {
        // Slider Sản Phẩm Nổi Bật
        const featuredSlider = new Swiper('.featured-products-slider', {
            slidesPerView: 1, // Số slide hiển thị mặc định
            spaceBetween: 20, // Khoảng cách giữa các slide (px)
            loop: true, // Lặp vô hạn
            autoplay: {
                delay: 3000, // Tự động chuyển sau 3 giây
                disableOnInteraction: false, // Không tắt tự động khi người dùng tương tác
            },
            pagination: {
                el: '.swiper-pagination', // Phần tử phân trang
                clickable: true, // Cho phép nhấp vào phân trang
                dynamicBullets: true, // Hiển thị dấu chấm động
            },
            navigation: {
                nextEl: '.swiper-button-next', // Nút chuyển tiếp
                prevEl: '.swiper-button-prev', // Nút quay lại
            },
            breakpoints: {
                640: { slidesPerView: 2 }, // 2 slide trên màn hình >= 640px
                768: { slidesPerView: 3 }, // 3 slide trên màn hình >= 768px
                1024: { slidesPerView: 4 }, // 4 slide trên màn hình >= 1024px
            },
            on: {
                init: function() {
                    setTimeout(() => {
                        this.el.classList.add('slider-loaded'); // Thêm lớp khi slider khởi tạo xong
                    }, 500);
                }
            },
            effect: 'coverflow', // Hiệu ứng chuyển slide kiểu coverflow
            coverflowEffect: {
                rotate: 5, // Góc xoay của slide
                stretch: 0, // Kéo dài slide
                depth: 100, // Độ sâu của hiệu ứng
                modifier: 1, // Hệ số hiệu ứng
                slideShadows: true, // Hiển thị bóng cho slide
            }
        });
        
        // Slider Sản Phẩm Mới Nhất
        const latestSlider = new Swiper('.latest-products-slider', {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            autoplay: {
                delay: 4000, // Tự động chuyển sau 4 giây
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

// Bộ đếm ngược cho ưu đãi đặc biệt
function initCountdownTimer() {
    const countdownElement = document.getElementById('special-offer-countdown');
    if (!countdownElement) return; // Thoát nếu không tìm thấy phần tử
    
    // Đặt ngày kết thúc (7 ngày kể từ hiện tại)
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + 7);
    
    function updateCountdown() {
        const now = new Date();
        const distance = endDate - now; // Tính khoảng cách thời gian
        
        // Tính ngày, giờ, phút, giây
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Cập nhật các phần tử đếm ngược với hiệu ứng
        updateCountdownDigit('countdown-days', days);
        updateCountdownDigit('countdown-hours', hours);
        updateCountdownDigit('countdown-minutes', minutes);
        updateCountdownDigit('countdown-seconds', seconds);
        
        // Nếu đếm ngược kết thúc
        if (distance < 0) {
            clearInterval(countdownInterval); // Dừng bộ đếm
            countdownElement.innerHTML = "<div class='text-center py-4'>Ưu đãi đặc biệt đã hết hạn!</div>";
        }
    }
    
    // Hàm trợ giúp để cập nhật số với hiệu ứng
    function updateCountdownDigit(id, value) {
        const element = document.getElementById(id);
        if (!element) return;
        
        const currentValue = element.innerText;
        const newValue = value.toString().padStart(2, '0'); // Đảm bảo số có 2 chữ số
        
        if (currentValue !== newValue) {
            element.classList.add('animate__animated', 'animate__flipInX'); // Thêm hiệu ứng lật
            element.innerText = newValue;
            
            setTimeout(() => {
                element.classList.remove('animate__animated', 'animate__flipInX'); // Xóa hiệu ứng
            }, 1000);
        }
    }
    
    // Cập nhật đếm ngược mỗi giây
    updateCountdown();
    const countdownInterval = setInterval(updateCountdown, 1000);
}

// Hiệu ứng hover cho các phần tử tương tác
function initHoverEffects() {
    // Thêm hiệu ứng phát sáng cho thẻ sản phẩm
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left; // Tọa độ chuột theo X
            const y = e.clientY - rect.top; // Tọa độ chuột theo Y
            
            this.style.setProperty('--mouse-x', `${x}px`); // Cập nhật vị trí chuột
            this.style.setProperty('--mouse-y', `${y}px`);
        });
    });
    
    // Thêm hiệu ứng hover cho các nút
    const buttons = document.querySelectorAll('.hero-cta, .btn-primary, .btn-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('hover-effect'); // Thêm lớp khi hover
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('hover-effect'); // Xóa lớp khi rời chuột
        });
    });
}

// Hiệu ứng parallax cho phần hero
function initParallax() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY; // Vị trí cuộn
        const heroBackground = document.querySelector('.hero-background');
        
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrollPosition * 0.4}px)`; // Di chuyển nền theo cuộn
        }
    });
    
    // Thêm hiệu ứng parallax cho các phần tử khác
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-parallax-speed') || 0.2; // Tốc độ parallax
            element.style.transform = `translateY(${scrollPosition * speed}px)`; // Di chuyển phần tử
        });
    });
}

// Bộ lọc danh mục sản phẩm
function initCategoryFilter() {
    const filterButtons = document.querySelectorAll('.category-filter-btn');
    if (filterButtons.length === 0) return;
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Xóa lớp active từ tất cả các nút
            filterButtons.forEach(btn => btn.classList.remove('active', 'bg-primary', 'text-white'));
            filterButtons.forEach(btn => btn.classList.add('bg-gray-200', 'text-gray-800'));
            
            // Thêm lớp active cho nút được nhấp
            this.classList.add('active', 'bg-primary', 'text-white');
            this.classList.remove('bg-gray-200', 'text-gray-800');
            
            const category = this.getAttribute('data-category'); // Lấy danh mục
            const productItems = document.querySelectorAll('.product-item');
            
            productItems.forEach(item => {
                if (category === 'all') {
                    fadeIn(item); // Hiển thị tất cả sản phẩm
                } else {
                    const itemCategory = item.getAttribute('data-category');
                    if (itemCategory === category) {
                        fadeIn(item); // Hiển thị sản phẩm theo danh mục
                    } else {
                        fadeOut(item); // Ẩn sản phẩm không thuộc danh mục
                    }
                }
            });
        });
    });
    
    // Hàm trợ giúp cho chuyển đổi mượt mà
    function fadeOut(element) {
        element.classList.add('animate__animated', 'animate__fadeOut'); // Thêm hiệu ứng mờ dần
        setTimeout(() => {
            element.style.display = 'none';
            element.classList.remove('animate__animated', 'animate__fadeOut');
        }, 500);
    }
    
    function fadeIn(element) {
        element.classList.add('animate__animated', 'animate__fadeIn'); // Thêm hiệu ứng hiện dần
        element.style.display = 'block';
        setTimeout(() => {
            element.classList.remove('animate__animated', 'animate__fadeIn');
        }, 500);
    }
}

// Khởi tạo modal xem nhanh
function initQuickViewModal() {
    const modal = document.getElementById('quick-view-modal');
    const closeButton = document.getElementById('quick-view-close');
    
    if (!modal || !closeButton) return;
    
    closeButton.addEventListener('click', function() {
        modal.classList.add('animate__animated', 'animate__fadeOut'); // Thêm hiệu ứng mờ dần khi đóng
        setTimeout(() => {
            modal.style.display = 'none';
            modal.classList.remove('animate__animated', 'animate__fadeOut');
        }, 500);
    });
    
    // Đóng modal khi nhấp ra ngoài
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.add('animate__animated', 'animate__fadeOut');
            setTimeout(() => {
                modal.style.display = 'none';
                modal.classList.remove('animate__animated', 'animate__fadeOut');
            }, 500);
        }
    });
}

// Hiệu ứng thêm vào giỏ hàng
function addToCartAnimation(button) {
    button.classList.add('adding'); // Thêm lớp khi bắt đầu
    
    setTimeout(() => {
        button.classList.remove('adding');
        button.classList.add('added'); // Thêm lớp khi hoàn tất
        
        // Hiển thị thông báo giỏ hàng mini
        const miniCart = document.querySelector('.mini-cart-count');
        if (miniCart) {
            const currentCount = parseInt(miniCart.innerText) || 0;
            miniCart.innerText = currentCount + 1; // Cập nhật số lượng
            miniCart.classList.add('animate__animated', 'animate__bounceIn'); // Hiệu ứng nảy
            
            setTimeout(() => {
                miniCart.classList.remove('animate__animated', 'animate__bounceIn');
            }, 1000);
        }
        
        setTimeout(() => {
            button.classList.remove('added');
        }, 1500);
    }, 1000);
}

// Xem nhanh sản phẩm
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
    
    // Trong ứng dụng thực tế, dữ liệu sản phẩm sẽ được lấy qua AJAX
    // Đây là mô phỏng với độ trễ tải
    setTimeout(() => {
        if (content) {
            content.innerHTML = `
                <div class="flex flex-col md:flex-row gap-6">
                    <div class="md:w-1/2">
                        <img src="https://via.placeholder.com/500" alt="Sản phẩm ${productId}" class="w-full h-auto rounded-lg">
                    </div>
                    <div class="md:w-1/2">
                        <h4 class="text-xl font-bold text-gray-800 mb-2">Sản phẩm ${productId}</h4>
                        <div class="text-secondary font-bold text-xl mb-4">50.000 VNĐ</div>
                        <p class="text-gray-600 mb-6">Đây là mô tả sản phẩm mẫu. Trong ứng dụng thực tế, phần này sẽ được điền dữ liệu thật.</p>
                        <form class="mb-4">
                            <div class="flex items-center mb-4">
                                <label class="mr-2">Số lượng:</label>
                                <input type="number" min="1" value="1" class="w-16 border rounded px-2 py-1">
                            </div>
                            <button type="submit" class="bg-secondary hover:bg-secondary-light text-white font-medium py-2 px-6 rounded-md transition">
                                Thêm vào giỏ
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

// Chuyển đổi trạng thái danh sách yêu thích
function toggleWishlist(button, productId) {
    button.classList.toggle('in-wishlist'); // Chuyển đổi lớp
    
    if (button.classList.contains('in-wishlist')) {
        // Thêm vào danh sách yêu thích
        button.innerHTML = '<i class="fas fa-heart text-danger"></i>'; // Biểu tượng trái tim đầy
        button.classList.add('animate__animated', 'animate__heartBeat'); // Hiệu ứng nhịp tim
        
        // Hiển thị thông báo (tùy chọn)
        showNotification('Đã thêm sản phẩm vào danh sách yêu thích!');
    } else {
        // Xóa khỏi danh sách yêu thích
        button.innerHTML = '<i class="far fa-heart"></i>'; // Biểu tượng trái tim rỗng
    }
    
    setTimeout(() => {
        button.classList.remove('animate__animated', 'animate__heartBeat');
    }, 1000);
    
    // Thông thường sẽ cập nhật backend qua AJAX
    console.log(`Chuyển đổi danh sách yêu thích cho sản phẩm ${productId}`);
}

// Hiển thị thông báo
function showNotification(message, type = 'success') {
    // Tạo phần tử thông báo
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate__animated animate__fadeInRight`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-check-circle notification-icon"></i>
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
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
    
    // Chức năng nút đóng
    const closeButton = notification.querySelector('.notification-close');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            notification.classList.remove('animate__fadeInRight');
            notification.classList.add('animate__fadeOutRight');
            
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        });
    }
}

// Hiệu ứng con trỏ theo chủ đề công nghệ (tùy chọn)
function initTechCursor() {
    const cursor = document.createElement('div');
    cursor.classList.add('tech-cursor'); // Thêm lớp cho con trỏ
    document.body.appendChild(cursor);
    
    document.addEventListener('mousemove', function(e) {
        cursor.style.left = e.clientX + 'px'; // Di chuyển theo tọa độ X
        cursor.style.top = e.clientY + 'px'; // Di chuyển theo tọa độ Y
    });
    
    // Thêm hiệu ứng khi hover vào phần tử có thể nhấp
    const clickables = document.querySelectorAll('a, button, .clickable');
    clickables.forEach(element => {
        element.addEventListener('mouseenter', function() {
            cursor.classList.add('cursor-hover'); // Thêm lớp khi hover
        });
        
        element.addEventListener('mouseleave', function() {
            cursor.classList.remove('cursor-hover'); // Xóa lớp khi rời
        });
    });
}

// Thêm CSS cho thông báo
document.addEventListener('DOMContentLoaded', function() {
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
        
        .notification-success {
            border-left: 4px solid var(--success-color); // Viền trái cho thông báo thành công
        }
        
        .notification-success .notification-icon {
            color: var(--success-color); // Màu biểu tượng
        }
        
        .notification-error {
            border-left: 4px solid var(--danger-color); // Viền trái cho thông báo lỗi
        }
        
        .notification-error .notification-icon {
            color: var(--danger-color); // Màu biểu tượng
        }
        
        .notification-close {
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #999;
        }
        
        .notification-close:hover {
            color: #333; // Màu khi hover
        }
        
        .loader {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid var(--secondary-color); // Vòng tải màu
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite; // Hiệu ứng xoay
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style); // Thêm CSS vào tài liệu
});