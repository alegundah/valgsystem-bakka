## Database

Save database seed of gropus and candidates
```text
uv run python manage.py dumpdata auth.group vote.Candidate --indent 2 -o vote/fixtures/seed.json
```

Load database seed and createsuperuser.
username is 123 and you have to input password and then say yes to bypass length
```text
uv run python manage.py migrate
uv run python manage.py loaddata seed
uv run manage.py createsuperuser --username 123
```

## Docker

Build image and run container
```text
docker build . -t vote && docker run -p 8000:8000 vote
```