# Deployment guide for social_media_api (prepared files included)
This document explains how to deploy the project to common providers and the files included in this package.

## What I prepared for you (files added to project root)
- `social_media_api/production_settings.py` : Production-ready settings template (imports from base `settings.py`)
- `Procfile` : For Heroku deployment (uses Gunicorn)
- `requirements-prod.txt` : Additional recommended packages for production
- `.env.example` : Example environment variables (do not commit secrets)
- `Dockerfile` : Simple Dockerfile to run the app in a container
- `gunicorn.service` : systemd unit example for Ubuntu
- `nginx_conf.conf` : Nginx reverse proxy template

------------------------------------------------------------------
## Quick checklist (full steps below)
1. Use Postgres in production (managed DB or provision one on the server).
2. Configure environment variables (SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS).
3. Install production dependencies (pip install -r requirements.txt).
4. Run `python manage.py migrate` and `python manage.py collectstatic`.
5. Start Gunicorn and configure Nginx as reverse proxy (or deploy via Heroku/Docker/EB).
6. Serve media via S3 or a cloud storage solution.

------------------------------------------------------------------
## Heroku (quick)
1. Create Heroku app: `heroku create your-app-name`
2. Add Heroku Postgres add-on or use `heroku addons:create heroku-postgresql:hobby-basic`
3. Set buildpacks if necessary; set config vars from `.env` (use `heroku config:set`)
4. Push to heroku: `git push heroku main`
5. Run migrations: `heroku run python manage.py migrate`
6. Collect static: `heroku run python manage.py collectstatic --noinput`
Documentation: https://devcenter.heroku.com/articles/deploying-python

## DigitalOcean (Droplet)
Follow DigitalOcean's guide to set up Django + Postgres + Gunicorn + Nginx on Ubuntu. Key steps:
- Create droplet (Ubuntu)
- Install Python, pip, virtualenv, PostgreSQL, Nginx
- Clone repo, create virtualenv, install requirements
- Configure systemd unit and Nginx (use provided templates)
- Set environment variables in `/home/ubuntu/social_media_api/.env`
- Run migrations and collectstatic
Reference: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu

## AWS Elastic Beanstalk (quick)
- Initialize EB: `eb init -p python-3.8 your-app-name`
- Create environment: `eb create your-env-name --single`
- Configure DB (attach RDS) or use external RDS instance
- Configure environment variables via the EB console or `eb setenv`
Documentation: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

------------------------------------------------------------------
## Security & Hardening checklist
- Ensure `DEBUG=False`
- Set a strong `SECRET_KEY` via env var
- Use HTTPS - obtain certificates with Let's Encrypt (certbot) or use provider-managed TLS
- Enable HSTS only after HTTPS is confirmed working
- Keep dependencies up to date and pin versions in `requirements.txt`

------------------------------------------------------------------
## What I cannot do from here
I prepared the configuration files, templates, and step-by-step instructions, but I cannot create the cloud account, provision resources, or publish a live URL from this environment. To complete deployment, follow the provider-specific steps above or share provider credentials (not recommended publicly).

------------------------------------------------------------------
## Next steps I can help with (choose any)
- Create a Docker Compose setup for local testing.
- Customize `production_settings.py` for AWS S3 or Cloudflare R2.
- Create GitHub Actions workflow to deploy to Heroku/EB on push.
- Review security headers and set recommended HSTS values.
