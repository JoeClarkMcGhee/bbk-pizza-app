<h1> Pizza Blog App </h1>

A RESTful django API backend that allows users to create blog posts, comment on posts and add 
simple like/dis-like reactions.

<h3>Set up</h3>

1. Install pipenv

`pip install pipenv`

2. Install the project dependencies and activate the venv

`pipenv sync` 

`pipenv shell`

3. Install the app as a package into the project. This makes sibling directories discoverable 
   in `sys.path`
   
`pipenv run pip install -e .`

4. Run the test suite

`export DJANGO_SETTINGS_MODULE=app.pizza.settings && cd src && pytest`

5. Activate the service

`python src/manage.py runserver`

6. Run the test script. Note, edit the IP in test script to point hit a local or production address

`python test_script.py`


<h2>Todo's</h2>
- Add the failing test cases
