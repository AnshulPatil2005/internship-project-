# core/utils.py
#contains all the utility to automate the process of uploading videos to AWS S3
# This file contains utility functions for handling video uploads to AWS S3.
# It includes functions to list videos from S3 and delete client data from S3.      
# Ensure to import necessary modules from Django and boto3.
#this is not currently in use as there is no AWS S3 bucket configured
from django.conf import settings
import os
import boto3
from django.conf import settings

def list_videos_from_s3(company, site):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )
    
    prefix = f"{company.replace(' ', '').lower()}/{site.replace(' ', '-').lower()}/"
    response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=prefix)

    videos = []
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('.mp4'):
            url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION_NAME}.amazonaws.com/{key}"
            videos.append({'name': key.split('/')[-1], 'url': url})

    return videos



def delete_s3_client_data(company, site):
    import boto3
    from django.conf import settings
    company_name = company.replace(" ", "").lower()
    site_path = site.replace(" ", "-").lower()
    prefix = f"{company_name}/{site_path}/"
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )
    try:
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=prefix)
        objects = [{'Key': obj['Key']} for obj in response.get('Contents', [])]
        if objects:
            s3.delete_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Delete={'Objects': objects})
    except Exception as e:
        print("Error deleting from S3:", e)
