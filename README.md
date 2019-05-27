# flask-art-museum

The purpose of this project is to practise web development and understand how to build an API.

This is the directory stucture:

```+-- flaskr/ (python package containing my app)
|   +-- __init__.py (contains the application factory, tells python the flaskr directory should be treated as a package, registers the db and blueprints)
|   +-- db.py (contains functions to initialize db and open/close the db connection)
|   +-- schema.sql (creates empty SQLite tables for users and posts)
|   +-- auth.py (creates blueprint and views for and authentication functions)
|   +-- blog.py (creates blueprint and views for blog post functions)
|   +-- templates/
|   |   +-- base.html (each template will extend this base template and override specific sections)
|   |   +-- auth/
|   |   |   +-- login.html
|   |   |   +-- register.html
|   |   +-- blog/
|   |       +-- create.html
|   |       +-- index.html
|   |       +-- update.html
|   +-- static/
|       +-- style.css (contains basic CSS from Flask tutorial)
+-- venv/ (python virtual environment to install dependencies, untracked)
+-- instance/ (contains sqlite file for an instance of the app, untracked)
```

To run this project:
1. create a python virtual environment with `python3 -m venv venv
2. activate it with `. venv/bin/activate`
3. assure flaskr is installed
4. run in development mode with `export FLASK_APP=flaskr`, `export FLASK_ENV=development`, and `flask run`

Here are the steps I took to build it:
1. Followed Flask tutorial in Python (with basic HTML, CSS, JS) to build a microblog and save users/posts to an SQLite database
2. Added the ability to upload images, saving the upload set to a directory and storing their path in the blog post table
