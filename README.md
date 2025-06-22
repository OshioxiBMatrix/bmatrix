
---

# 🛍️ **BMATRIX — Website Bán Hàng & Blog Cộng Đồng**

---

## 📌 **Mục tiêu**

* Xây dựng một website **thương mại điện tử quy mô vừa**, kèm **blog cộng đồng** để chia sẻ tin tức, bài viết.
* Cho phép **người dùng đăng ký, đăng nhập, quản lý giỏ hàng, đặt hàng, xem lịch sử đơn hàng**.
* Quản lý **sản phẩm, đơn hàng, người dùng, bài viết, bình luận** thông qua **admin riêng** (`admin.bountymatrix.net`).
* Dễ dàng mở rộng, bảo trì & triển khai production bằng **Docker, NGINX, Gunicorn**.

---

## 🧩 **Tính năng**

✅ Quản lý tài khoản, hồ sơ người dùng
✅ Xem sản phẩm, chi tiết sản phẩm
✅ Thêm giỏ hàng, thanh toán
✅ Xem & quản lý đơn hàng
✅ Blog cộng đồng: bài viết & bình luận
✅ Hệ thống quản trị riêng bảo mật
✅ Deploy dễ dàng bằng Docker Compose

---

## 🗂️ **Cấu trúc dự án**

```plaintext
bmatrix/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── nginx/
│   └── default.conf
├── app/
│   ├── manage.py
│   ├── bmatrix/   # settings.py, urls.py, wsgi.py
│   ├── accounts/
│   ├── shop/
│   ├── cart/
│   ├── orders/
│   ├── blog/
│   ├── static/         # Static files build Tailwind
│   ├── media/          # Upload media files
├── requirements.txt
└── README.md
```

---

## ⚙️ **Công nghệ sử dụng**

* **Python 3.13+**
* **Django 5.x**
* **Gunicorn** (WSGI server)
* **NGINX** (reverse proxy + serve static/media)
* **PostgreSQL** (Database)
* **Redis** (cache/session, optional)
* **Tailwind CSS** (giao diện đẹp, responsive)
* **Vue.js / Vanilla JS** (dynamic UI nếu cần)
* **Docker & Docker Compose** (triển khai production)

---

## 🚀 **Hướng dẫn cài đặt & chạy local**

### 1️⃣ Clone & tạo `.env`

```bash
git clone https://github.com/<YOUR-USERNAME>/bmatrix.git
cd bmatrix
cp .env.example .env
```

👉 Trong file `.env` bạn cần khai báo:

```env
DEBUG=1
SECRET_KEY=your-django-secret-key
POSTGRES_DB=bmatrix_db
POSTGRES_USER=bmatrix_user
POSTGRES_PASSWORD=bmatrix_pass
```

---

### 2️⃣ Build & chạy Docker

```bash
docker-compose build
docker-compose up -d
```

---

### 3️⃣ Tạo database & superuser

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

### 4️⃣ Truy cập website

* Website: [http://localhost](http://localhost)
* Admin Django: [http://localhost/admin](http://localhost/admin)
* Quản trị riêng: [http://admin.bmatrix.net](http://admin.bmatrix.net) *(cần cấu hình DNS & SSL)*

---

## 🗃️ **Mô hình CSDL**

* **accounts**: User & Profile
* **shop**: Category, Product
* **cart**: Cart, CartItem
* **orders**: Order, OrderItem
* **blog**: Post, Comment

Chi tiết bảng & quan hệ đã được thiết kế chuẩn Django ORM.

---

## 📄 **Dockerfile (mẫu)**

```Dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "bmatrix_site.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🗄️ **docker-compose.yml (mẫu)**

```yaml
version: "3.9"

services:
  web:
    build: .
    command: gunicorn bmatrix_site.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/code
      - static_volume:/code/static
      - media_volume:/code/media
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/code/static
      - media_volume:/code/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

## 🔑 **Một số lệnh hữu ích**

| Lệnh                                                     | Mô tả                           |
| -------------------------------------------------------- | ------------------------------- |
| `docker-compose up -d`                                   | Chạy toàn bộ container          |
| `docker-compose down`                                    | Dừng và xoá container           |
| `docker-compose logs -f`                                 | Xem log realtime                |
| `docker-compose exec web bash`                           | Truy cập terminal container web |
| `docker-compose exec web python manage.py collectstatic` | Build static                    |

---

## 🔐 **Best Practice Security**

* Bật SSL & HTTPS bằng NGINX + Certbot.
* `DEBUG=False` khi chạy production.
* Luôn giữ `.env` bảo mật, không commit lên Git.

---

## ✅ **Triển khai Production**

1️⃣ Build Docker image production
2️⃣ Sử dụng `docker-compose up -d` trên server thật
3️⃣ Cấu hình domain, SSL
4️⃣ Setup cron backup database & media

---

## 💪 **Team phát triển**

* **Tác giả:** Bạn & Team Bmatrix
* **Liên hệ:** [support@bmatrix.net](mailto:support@bmatrix.net)

---

## 📜 **License**

**MIT License — Free for commercial & personal use.**

---

## 🎉 **Enjoy building & scale your community eCommerce!**

---

## ✔️ **READY TO DEPLOY!**

---

## 📎 **Checklist kèm theo**

✅ `README.md`
✅ `.env.example`
✅ `Dockerfile`
✅ `docker-compose.yml`
✅ `nginx/default.conf`
✅ Migrations + Superuser + Collectstatic

---

## 📌 **Nếu cần file DOCX hoặc PDF để gửi khách hàng, hãy bảo mình làm luôn! 🚀✨**

---

🎁 **Copy toàn bộ nội dung này** vào `README.md` → Commit lên GitHub là chuyên nghiệp ngay! 🚀🔥
