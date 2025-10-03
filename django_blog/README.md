# Authentication System Documentation
## Overview
This Django project uses Django's built-in authentication system for secure user management. The authentication system includes registration, login, logout, and profile management features. Passwords are securely hashed using Django's default algorithms, and all forms are protected against CSRF attacks.

## Features
- **Registration:** Users can create an account using a custom registration form that extends Django's `UserCreationForm` to include an email field. On successful registration, users are redirected to the login page.
- **Login:** Users can log in using their username and password. Authentication errors are displayed if credentials are invalid.
- **Logout:** Users can securely log out using a POST request. After logout, a confirmation page is shown.
- **Profile Management:** Authenticated users can view and edit their profile details, including email, bio, and profile picture. Profile updates are handled via a secure form.

## How Authentication Works
1. **Registration:**
	- Users access `/register/` and fill out the registration form.
	- The form validates input and creates a new user with a hashed password.
	- CSRF protection is enforced via `{% csrf_token %}` in the template.

2. **Login:**
	- Users access `/login/` and submit their credentials.
	- Django authenticates the user and starts a session.
	- CSRF protection is enforced.

3. **Logout:**
	- Users log out via a POST form to `/logout/`.
	- The session is ended and the user is redirected to a confirmation page.

4. **Profile Management:**
	- Authenticated users access `/profile/` to view and edit their details.
	- Profile updates are submitted via a POST form with CSRF protection.
	- Only the logged-in user can edit their own profile.

## Security
- All forms use CSRF tokens to prevent CSRF attacks.
- Passwords are never stored or displayed in plain text.
- Profile editing is restricted to authenticated users.

## Testing Authentication Features
You can test authentication features using Django's test client or manually:

### Automated Tests
Run:
```bash
python manage.py test blog
```
This will test registration, login, logout, and profile editing.

### Manual Testing
1. **Registration:** Go to `/register/`, fill out the form, and submit. Check for success and error messages.
2. **Login:** Go to `/login/`, enter credentials, and submit. Confirm login and error handling.
3. **Logout:** Use the logout button (POST form) to log out. Confirm you see the logged out page.
4. **Profile:** Go to `/profile/` while logged in. Edit your email, bio, or profile picture and submit. Confirm changes are saved.

## Notes
- Make sure Pillow is installed for profile picture uploads: `pip install Pillow`
- Ensure the static directory exists for static files.
- For production, set `DEBUG = False` and configure allowed hosts and secure settings.
