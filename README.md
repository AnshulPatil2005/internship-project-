
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

## Installation Guide

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git
- AWS CLI (optional, for S3 integration)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-signal-traffic-system.git
cd smart-signal-traffic-system
```

### 2. Create Virtual Environment

#### On Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate
```

#### On Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django boto3
```

Or if a `requirements.txt` file exists:
```bash
pip install -r requirements.txt
```

### 4. Configure the Application

1. Update the `STATICFILES_DIRS` in `smart_signal_main/settings.py` to point to your local static folder:
   ```python
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static'),
   ]
   ```

2. (Optional) Configure AWS credentials for S3 integration by adding to `settings.py`:
   ```python
   AWS_ACCESS_KEY_ID = 'your-access-key'
   AWS_SECRET_ACCESS_KEY = 'your-secret-key'
   AWS_REGION_NAME = 'ap-south-1'
   AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
   ```

### 5. Initialize the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

---

## AWS CLI Setup (Optional)

If you plan to use AWS S3 for video storage:

### Install AWS CLI

#### On Windows
Download and install from: https://aws.amazon.com/cli/

#### On macOS
```bash
brew install awscli
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt install awscli
```

Or via pip:
```bash
pip install awscli
```

### Configure AWS CLI

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
