# 1531 Survey System


## Download Project

	$ git clone https://github.com/cse1531S1/survey-system-t09b-something.git
    $ cp -t survey-system-t09b-somthing/data/ courses.csv passwords.csv enrolments.csv  
    $ # put all the csv files under survey-system-t09b-something/data/

## Set Up Local Environment

	$ cd survey-system-t09b-something/
	$ sudo -H pip3 install -r requirements.txt
    $ # or use virtual environment, let's take package virtualenv for example here
    $ # `virtualenv -p python3 venv`
    $ # `source venv/bin/activate`
    $ # use `deactivate` to quit virtual environment for python3
    $ python3 deploy.py $config # $config is one in development, production, testing and default
    $ # this $config argument will also affect the config of flask server
    $ # run `cat config.py` for more information

## Run the Server

	$ python3 run.py runserver # default server runs on 127.0.0.1:5000
    $ # run `python3 run.py runserver --help` for more information
