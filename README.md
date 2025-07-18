# django-blog

# Setup

You have to run `docker compose -f docker-compose-stage.yml up -d`
Then you can go to `localhost` and see the website

# Superuser

to create new superuser run this command:
`docker compose -f docker-compose-stage.yml exec backend sh -c "uv run /app/core/manage.py createsuperuser"`
