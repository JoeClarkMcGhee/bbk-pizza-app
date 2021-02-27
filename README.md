<h1> Pizza Blog App </h1>

A RESTful django API backend that allows users to create blog posts, comment on posts and add 
simple like/dis-like reactions.

<h3>Set up</h3>

1. Install pipenv

`pip install pipenv`

2. Install the project dependencies and activate the venv

`pipenv sync && pipenv shell`

3. Install the app as a package into the project. This makes sibling directories discoverable 
   in `sys.path`
   
`pipenv run pip install -e .`

4. Run the database migrations

`python src/manage.py migrate`

5. Create a superuser 

`python src/manage.py createsuperuser`

6. Activate the service

`python src/manage.py runserver`

7. Generate (via the Django admin interface) a client ID and client secrete then update the 
   `CLIENT_ID` and `CLIENT_SECRET` in `app/pizza/settings.py`

8. Run the test suite if you feel like it :bowtie:

`export DJANGO_SETTINGS_MODULE=app.pizza.settings && cd src && pytest`


9. Run the test script.
   
   Note, you can edit the IP in test script to point to what ever address you fancy. The 
   default ip is 10.61.64.152 

`python test_script.py`


<h2>Todo's</h2>
- Add the failing test cases

- Fix skipped functional test
