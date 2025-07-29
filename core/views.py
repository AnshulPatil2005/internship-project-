# core/views.py
# This file contains views for user authentication, client management, and video handling
#this file cntains all the functions that handle the logic for the application
# Ensure to import necessary modules from Django and boto3.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
import boto3

from .forms import (
    ClientUserForm,
    CustomUserCreationForm,
    AdminUploadVideoForm,
    VideoFilterForm,
    VideoUploadForm,
)
from .models import Client, Video
from .utils import delete_s3_client_data, list_videos_from_s3

User = get_user_model()

# Authentication

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, "core/register.html", {"form": form})


@login_required
def home(request):
    return render(request, 'home.html')


# Client Management
@transaction.atomic
def add_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')

        if password != confirm_password:
            return render(request, 'core/add_client.html', {
                'error': 'Passwords do not match.'
            })

        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            if Client.objects.filter(user=existing_user).exists():
                return render(request, 'core/add_client.html', {
                    'error': 'A client with this username already exists.'
                })
            else:
                return render(request, 'core/add_client.html', {
                    'error': 'User exists but is not linked to any client. Please delete the user or choose another username.'
                })

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            Client.objects.create(user=user, company_name=company_name)
            return redirect('list_clients')

        except Exception as e:
            return render(request, 'core/add_client.html', {
                'error': f'Client creation failed: {e}'
            })

    return render(request, 'core/add_client.html')


@login_required
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'core/list_clients.html', {'clients': clients})



@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        # Delete the user, which will also delete client due to cascade
        client.user.delete()
        return redirect('list_clients')

    return render(request, 'core/delete_client.html', {'client': client})


# Show Map
@login_required
def show_map(request):
    selected_map = request.GET.get("client_map", "")
    return render(request, 'core/show_map.html', {'selected_map': selected_map})


# Video Upload
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_videos')
    else:
        form = VideoUploadForm()

    return render(request, 'core/upload_video.html', {'form': form})


@login_required
def list_videos(request):
    videos = None
    if request.method == 'POST':
        form = VideoFilterForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            site = form.cleaned_data['site_name']  # site_name from form, field in model is site
            videos = Video.objects.filter(client=client, site=site)
    else:
        form = VideoFilterForm()

    return render(request, 'core/list_videos.html', {'form': form, 'videos': videos})

# AWS S3: Show all signals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import boto3
import botocore.exceptions
import re
from django.conf import settings
from core.models import Client

@login_required
def show_all_signals(request):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )

    client_data = []
    clients = Client.objects.all()

    for client in clients:
        bucket_name = re.sub(r'[^a-z0-9-]', '-', client.company_name.lower().strip().replace(' ', '-'))

        try:
            result = s3.list_objects_v2(Bucket=bucket_name)
            files = [content['Key'] for content in result.get('Contents', [])]
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                files = ['No S3 bucket found for this client']
            else:
                files = [f"AWS Error: {e.response['Error']['Message']}"]

        client_data.append({
            'client': client,
            'files': files
        })

    return render(request, 'core/show_signals.html', {'client_data': client_data})

# Client-specific video list

def client_required(view_func):
    return user_passes_test(lambda u: not u.is_staff and not u.is_superuser, login_url='/admin/')(view_func)



from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Client, Video

@login_required
def dashboard_view(request):
    context = {
        'total_clients': Client.objects.count(),
        'total_videos': Video.objects.count(),
        'active_signals': 0,  # placeholder until Signal model exists
        'alert_count': 0      # placeholder until Alert model exists
    }
    return render(request, 'home.html', context)
