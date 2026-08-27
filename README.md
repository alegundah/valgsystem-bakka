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


## Missing stuff

- Statistics page.  [figma page](https://www.figma.com/design/OQAvTrYkmZOmgSk8x8JHoW/valgsystem-design?node-id=59-65&t=Zs9TWnJrjcbhCid9-4) 
- Create a way to end the vote and show data.
- Plan how to share codes. We have a page for codes(/brukere/) but how do we share them?
- Make a button to log out that is available on all screens
