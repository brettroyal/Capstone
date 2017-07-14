# TDI Capstone Project- Identifying Secret Ingredients

# Project Prereqs

* Python
* Pip
* Virtual Environment
* Flask - make sure you have latest version (Can be installed with pip: `pip install https://github.com/mitsuhiko/flask/tarball/master`)

# Running the Project Locally

* Download the repository or a fork of the repository.
* CD into the repo `cd Capstone`.
* Install packages: `pip install requirements.txt --user`
* In a new terminal window, create virtual environment:
  1. set up virtual env: `virtualenv ENV`;
  2. `source ENV/bin/activate`
* In root directory, run FLASK:
  ```
   export FLASK_APP=capstone.py // sets the Application for Flask to run
   flask run // runs the project; should spin up a local server for you to browse @ 127.0.0.1:5000
  ```
