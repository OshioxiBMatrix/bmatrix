from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

def custom_login(request):
    """Custom login view that includes Google SSO option"""
    if request.user.is_authenticated:
        return redirect('shop:home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Xin chào {username}! Bạn đã đăng nhập thành công.")
                next_url = request.GET.get('next', 'shop:home')
                return redirect(next_url)
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def custom_register(request):
    """Custom registration view with option to sign up with Google"""
    if request.user.is_authenticated:
        return redirect('shop:home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the user
            Profile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f"Tài khoản đã được tạo cho {username}. Bạn có thể đăng nhập ngay bây giờ.")
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """View user profile"""
    # Ensure user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    # Ensure user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Thông tin của bạn đã được cập nhật!")
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)
