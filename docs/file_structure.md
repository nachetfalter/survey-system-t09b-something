# Source file structure
    
    |-survey-system-t09b-something/
      |-templates/
        |-base.html
        |-index.html
        |-*.html # some other templates
      |-static/
        |-*.js # JavaScript files if necessary 
        |-*.css # CSS files if necessary
      |-csv/ # to be changed
        |-*.csv # files storing data
      |-main/
        |-__init__.py
        |-views.py # alias to routes.py
        |-errors.py # handle errors like 404
        |-forms.py
        |-*.py # other python source
      |-tests/
        |-__init__.py
        |-test*.py
      |-venv/ # if using
      |-config.py # to be added
      |-models.py # DB models # to be added
      |-run.py # or manage.py
      |-... # and other project files 
      ... # as well as other modules

