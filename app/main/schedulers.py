'''
app/main/scheduler.py
- - - - - - -
scheduled tasks manager for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import atexit
import datetime

from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.base import JobLookupError

from .. import scheduler
from ..model.models import Survey


# XXX timezone to be added


scheduler.start()


class Scheduler:

    ''' encapsulation for scheduler operation '''

    @staticmethod
    def add_survey_schedule_job(survey_id):
        ''' add two scheduler for certain survey '''
        scheduler.add_job(
            func=lambda: trigger_survey_status(survey_id),
            trigger=DateTrigger(run_date=survey_start_date(survey_id)),
            id='survey_'+str(survey_id)+'_start',
            name='survey_'+str(survey_id)+'_start')
        scheduler.add_job(
            func=lambda: trigger_survey_status(survey_id),
            trigger=DateTrigger(run_date=survey_close_date(survey_id)),
            id='survey_'+str(survey_id)+'_close',
            name='survey_'+str(survey_id)+'_close')

    @staticmethod
    def remove_survey_schedule_job(survey_id):
        ''' clean up when survey is removed or modified '''
        try:
            scheduler.remove_job('survey_'+str(survey_id)+'_start')
        except JobLookupError:
            pass
        try:
            scheduler.remove_job('survey_'+str(survey_id)+'_close')
        except JobLookupError:
            pass


def trigger_survey_status(survey_id):
    Survey.status_operation(survey_id)


def survey_start_date(survey_id):
    survey = Survey.load(survey_id)
    return survey.start_date


def survey_close_date(survey_id):
    survey = Survey.load(survey_id)
    return survey.close_date


atexit.register(lambda: scheduler.shutdown())
