from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Inline để quản lý Profile ngay trên trang User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Hồ sơ'

# Extend User admin
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')

# Gỡ User mặc định và đăng ký lại
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
