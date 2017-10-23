# 1531 Survey System - Group T09B SOMETHING

A simple online system designed for COMP1531 based on Python3, Flask and Vuejs.

## Project Dependencies

### Python Libraries

    alembic==0.9.5
    bcrypt==3.1.3
    blinker==1.4
    cffi==1.11.1
    click==6.7
    Flask==0.12.2
    Flask-Bcrypt==0.7.1
    Flask-Login==0.4.0
    Flask-Mail==0.9.1
    Flask-Migrate==2.1.1
    Flask-Moment==0.5.2
    Flask-Script==2.0.6
    Flask-SQLAlchemy==2.3.1
    itsdangerous==0.24
    Jinja2==2.9.6
    Mako==1.0.7
    MarkupSafe==1.0
    pycparser==2.18
    PyJWT==1.5.3
    python-dateutil==2.6.1
    python-editor==1.0.3
    six==1.11.0
    SQLAlchemy==1.1.14
    Werkzeug==0.12.2

### JavaScript Libraries (Through CDN)

    vue@2.5.2
    vuetify@0.16.9
    axios@0.17.0
    vue-chartjs@3.0.0

## Usage

### Download Project

	$ git clone https://github.com/cse1531S1/survey-system-t09b-something.git
    $ cp -t survey-system-t09b-somthing/data/ courses.csv passwords.csv enrolments.csv  
    $ # put all the csv files under survey-system-t09b-something/data/

### Set Up Local Environment

Installing dependencies in local environment:

	$ cd survey-system-t09b-something/
	$ sudo -H pip3 install -r requirements.txt
    $ python3 deploy.py $config 

Or use virtual environment (let's take virtualenv for example):

    $ virtualenv -p python3 venv
    $ source venv/bin/activate

Type `deactivate` to quit the virtual environment

Running data automatically importing script, `$config` should be replaced with one in `development`, `production`, `testing` or `default`:

    $ python3 deploy.py $config

### Run the Server

	$ python3 manage.py runserver 

The default server runs on 127.0.0.1:5000, you can type `python3 manage.py runserver --help` for more information

### Run unittests

Below is the recommended way:

    $ python3 manage.py test

Another way is also accepted:

    $ python3 tests.py
