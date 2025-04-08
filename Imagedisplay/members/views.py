from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .image_processor import get_image_dimensions

@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.username})
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()

            # Get image dimensions using the external script
            width, height = get_image_dimensions(str(uploaded_image.image))

            return render(request, 'upload.html', {
                'form': form,
                'uploaded_image': uploaded_image,
                'width': width,
                'height': height
            })
    else:
        form = ImageUploadForm()
    
    return render(request, 'upload.html', {'form': form})



