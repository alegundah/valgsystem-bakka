## Database

Save database seed of gropus and candidates
```text
uv run python manage.py dumpdata auth.group vote.Candidate --indent 2 -o vote/fixtures/seed.json
```

Load database seed
```text
uv run python manage.py migrate
uv run python manage.py loaddata seed
```