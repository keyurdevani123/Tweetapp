# 🐦 Django Twitter Clone

A simple Twitter-like social media app built with **Django**, **Bootstrap**, and **SQLite**. Users can post tweets, like, comment, follow others, send messages, and receive notifications.

---

## 🚀 Features

- User authentication (register, login, logout, reset password)
- Tweet, like, comment, and view count
- Follow/unfollow users
- Private messaging system
- Real-time notifications
- Responsive UI with AJAX for dynamic updates

----------------------------------------------------------------

## 🛠 Installation & Setup

### 🔗 Prerequisites
- Python 3.8 or above
- pip
- Git

### 🧱 Setup Steps

```bash
# Clone the repository
git clone https://github.com/your-username/project-name.git
cd project-name

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
