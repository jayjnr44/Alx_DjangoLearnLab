# 🧾 Social Media API (Django + Django REST Framework)

A social media backend built with **Django** and **Django REST Framework (DRF)** that supports:
- User authentication (token-based)
- User profiles (bio, profile picture)
- Follow/unfollow system
- Posts and comments
- Personalized feed (posts from followed users)
- Pagination and search

---

## 🚀 Features

✅ Custom user model extending `AbstractUser`  
✅ Token authentication  
✅ CRUD for posts and comments  
✅ Follow/unfollow users  
✅ Personalized user feed  
✅ Paginated and filterable post list  

---

## 🧩 Project Structure

social_media_api/
│
├── accounts/ # User management and authentication
│ ├── models.py # Custom user model (with follow system)
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── posts/ # Posts and comments
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── social_media_api/
│ ├── settings.py # DRF + token auth config
│ ├── urls.py
│
└── manage.py

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone and create virtual environment
```bash
git clone https://github.com/yourusername/social_media_api.git
cd social_media_api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Apply migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
4️⃣ Create superuser
bash
Copy code
python manage.py createsuperuser
5️⃣ Run the development server
bash
Copy code
python manage.py runserver
Server runs at 👉 http://127.0.0.1:8000/

🔐 Authentication
This project uses Token Authentication.

Get Token
swift
Copy code
POST /api/accounts/login/
{
  "username": "alice",
  "password": "password123"
}
Include Token in Requests
makefile
Copy code
Authorization: Token <your_token>
👥 User Model
Located in accounts/models.py

python
Copy code
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)
🔗 Follow Management Endpoints
Base URL: /api/accounts/users/

▶️ Follow a User
POST /api/accounts/users/<user_id>/follow/

Headers:

makefile
Copy code
Authorization: Token <your_token>
Response:

json
Copy code
{
  "message": "You are now following bob."
}
⏹️ Unfollow a User
POST /api/accounts/users/<user_id>/unfollow/

Response:

json
Copy code
{
  "message": "You have unfollowed bob."
}
👥 List Followers / Following (optional)
GET /api/accounts/users/<user_id>/followers/
GET /api/accounts/users/<user_id>/following/

📰 Feed Endpoint
URL: /api/posts/feed/
Method: GET
Auth Required: ✅

Returns posts from users the current user follows.

Response Example:

json
Copy code
{
  "count": 2,
  "results": [
    {
      "id": 7,
      "title": "Carol's latest post",
      "content": "Hello from Carol!",
      "author": {"id": 3, "username": "carol"},
      "created_at": "2025-10-12T15:42:31Z"
    },
    {
      "id": 5,
      "title": "Bob’s weekend update",
      "content": "Just posted a new update!",
      "author": {"id": 2, "username": "bob"},
      "created_at": "2025-10-12T15:30:12Z"
    }
  ]
}
🔍 Filtering & Pagination
Posts Search
Filter posts by title or content:

sql
Copy code
GET /api/posts/?search=holiday
Pagination
Configured via DRF settings or view pagination class:

python
Copy code
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
🧪 Testing
Use Postman, Insomnia, or DRF’s browsable API to test endpoints.

Example Test Flow
Register users (/api/accounts/register/)

Log in each and get their tokens

Follow a user (/api/accounts/users/<id>/follow/)

Create posts as followed users

View /api/posts/feed/ to confirm feed works

Unfollow and verify feed updates

Run automated tests (if created):

bash
Copy code
python manage.py test
🧭 Example Workflow (Quick Reference)
http
Copy code
# Register
POST /api/accounts/register/
{
  "username": "alice",
  "password": "pass123"
}

# Login
POST /api/accounts/login/
{
  "username": "alice",
  "password": "pass123"
}

# Follow user 2
POST /api/accounts/users/2/follow/
Authorization: Token <alice_token>

# Get feed
GET /api/posts/feed/
Authorization: Token <alice_token>

# Unfollow user 2
POST /api/accounts/users/2/unfollow/
Authorization: Token <alice_token>
⚠️ Common Errors
Code	Message	Cause
400	"You cannot follow yourself."	Tried to follow own account
401	"Authentication credentials were not provided."	Missing or invalid token
404	"User not found."	Invalid user ID
403	"Permission denied."	Tried to modify another user’s follow list

🧭 URLs Overview
Endpoint	Method	Description	Auth
/api/accounts/users/	GET, POST	List or create users	✅
/api/accounts/users/<id>/	GET, PUT, DELETE	Retrieve/update user	✅
/api/accounts/users/<id>/follow/	POST	Follow a user	✅
/api/accounts/users/<id>/unfollow/	POST	Unfollow a user	✅
/api/posts/	GET, POST	CRUD for posts	✅
/api/posts/feed/	GET	Feed (followed users’ posts)	✅

🧰 Technologies Used
Python 3.12+

Django 5+

Django REST Framework

Django REST Auth / Authtoken

SQLite / PostgreSQL

Postman / DRF Browsable API for testing

💡 Future Enhancements
Add likes and notifications

Add user suggestions (“People you may know”)

Implement JWT authentication

Add user activity feed analytics

🧑‍💻 Author
Your Name
📧 your.email@example.com
🌐 GitHub