from azure import functions as func
import logging


SYNCRONIZER_NAME = "TIMESHEETS"


bp = func.Blueprint()

@bp.function_name("SyncronizeTimesheets")
@bp.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def syncronize_timesheets(myTimer: func.TimerRequest) -> None:
    logging.info('Triggered function in another folder.')