# Source file structure
    
    |-survey-system-t09b-something/
      |-app/
        |-__init__.py
        |-auth/
          |-__init__.py
          |-api.py
          |-errors.py
          |-views.py
          |-...
        |-main/
          |-__init__.py
          |-api.py
          |-errors.py
          |-views.py
          |-...
        |-model/
          |-__init__.py
          |-models.py
          |-...
        |-static/ # may be modified later
          |-*.css
          |-*.js
          |-...
        |-templates/
          |-*.html
          |-...
      |-data/ # store data to be imported at setup stage
        |-*.csv
      |-docs/ # store project docs
        |-*.md
        |-*.pdf
      |-tests/
        |-...
      |-venv/ # if using
        |-...
      |-config.py
      |-run.py
      |-deploy.py
      |-... # and other project files 
