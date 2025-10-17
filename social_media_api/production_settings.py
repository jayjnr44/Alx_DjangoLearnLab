# """Production settings for social_media_api.
# This file intentionally keeps secrets and env-specific values out of source control.
# Set environment variables (see .env.example) in your host environment.
# """
# from .settings import *  # noqa: F401,F403 - import base settings
# import dj_database_url, os

# DEBUG = False

# # SECURITY
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'  # or 'SAMEORIGIN' if required
# SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# # HSTS - set only when you are serving HTTPS and ready to enforce
# SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '0'))
# SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False') == 'True'
# SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'False') == 'True'

# # DATABASE (expects a DATABASE_URL env var, e.g. postgres://user:pass@host:5432/dbname)
# DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'))}

# # Static files (WhiteNoise or S3)
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# # Use WhiteNoise to serve static files (works well on Heroku and simple PaaS)
# MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
# STATICFILES_STORAGE = os.getenv('STATICFILES_STORAGE', 'whitenoise.storage.CompressedManifestStaticFilesStorage')

# # Optional: configure S3 if using AWS
# if os.getenv('USE_S3', 'False') == 'True':
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
#     AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
#     AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', None)
#     AWS_QUERYSTRING_AUTH = False  # public files via signed URLs? set True if private

# # Logging - simple console handler for container logs / Heroku
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#     },
# }
