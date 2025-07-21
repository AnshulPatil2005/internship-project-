
# 🚦 Smart Signal Traffic System

Smart Signal Traffic System is a web-based application designed to integrate with existing traffic infrastructure to broadcast safety messages and advertisements at traffic signals. It supports multi-user roles (Admin and Clients) and allows video uploads, client/site management, and map-based signal views.

---

## Features

### Admin Functionalities
- Add, show, and delete clients
- Upload and list videos by site
- Show signal map with static locations
- Manual AWS S3 bucket setup for each client

### Client Functionalities
- Upload videos to specific sites
- View site-specific video listings
- View live signal statuses on a map
- Show CCTV footage (if integrated)

---

##  Installation Guide

### Prerequisites
- Python 3.x
- Virtualenv
- Django
- AWS CLI
- Ubuntu-based system recommended

---

##  Setup Instructions

### 1. Create Virtual Environment

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
pip3 install virtualenv
virtualenv venv -p python3
source venv/bin/activate
```

### 2. Install Django

```bash
pip3 install django
django-admin --version  # To confirm installation
```

### 3. Install AWS CLI

#### Option A: APT Package Manager

```bash
sudo apt install awscli
aws --version
```

#### Option B: Python Pip

```bash
pip3 install awscli --upgrade --user
python3 -m awscli --version
```

#### Configure AWS CLI

```bash
aws configure
# Provide Access Key, Secret, Region (ap-south-1), and output format (json/text)
```

---

##  AWS S3 Setup

1. Admin must manually create a bucket per client:  
   Format: `ecube-eis/<company_name>/<site_name>`

2. Bucket naming rules:
   - No spaces or special characters
   - Use lowercase (e.g., `ecubemedia`, `mumbai-central`)

3. Upload videos under relevant paths for each site.

---

##  Map Integration

1. Use [Google Maps Custom Map Tool](https://www.howtogeek.com/664890/how-to-create-a-custom-map-in-google-maps/)
2. Save static map image at:
   ```
   /home/ubuntu/ecubesolutions.in/venv/smart_signal/static/images/maps/
   ```
3. Edit `get_map.html`:
   - Add `<button>` overlays on signal positions
   - Update associated JavaScript and CSS

---

##  Project Structure

```
smart_signal/
├── core/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   └── urls.py
├── media/
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

##  License

This project is proprietary and developed for Smart Signal systems under Ecube Solutions. All rights reserved.
