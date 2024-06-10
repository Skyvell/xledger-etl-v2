import logging
import os
import azure.functions as func
from shared.extraction import DataSyncronizer, DataSyncronizerQueries
from shared.gql_client import GraphQLClient
from shared.queries import (
    GET_TIMESHEET_DELTAS, 
    GET_TIMESHEETS_FROM_DBIDS, 
    GET_TIMESHEETS_AFTER_CURSOR, 
    GET_CUSTOMER_DELTAS, 
    GET_CUSTOMERS_FROM_DBIDS,
    GET_EMPLOYEE_DELTAS,
    GET_EMPLOYEES_FROM_DBIDS,
    GET_EMPLOYEES_AFTER_CURSOR
)

from shared.utils.data_transformation import flatten_list_of_dicts
from shared.utils.files import convert_dicts_to_parquet, write_buffer_to_file
from shared.utils.time import get_current_time_for_filename
import json

from functions.sync_timesheets.sync_timesheets import bp

app = func.FunctionApp()
app.register_blueprint(bp)

SYNCRONIZER_NAME = "timesheets"

@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def sync_timesheets(myTimer: func.TimerRequest) -> None:
    # Get the environment variables.
    api_endpoint, api_key = os.getenv("Endpoint"), os.getenv("APIKey")

    # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    syncronizer_queries = DataSyncronizerQueries(GET_TIMESHEET_DELTAS, GET_TIMESHEETS_FROM_DBIDS, GET_TIMESHEETS_AFTER_CURSOR)
    syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   
    # Syncronize the data.
    items = syncronizer.get_all_items()


    print(json.dumps(flatten_list_of_dicts(items.get_nodes()), indent=4))



    # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    syncronizer_queries = DataSyncronizerQueries(GET_CUSTOMER_DELTAS, GET_CUSTOMERS_FROM_DBIDS, "test")
    syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   
    # Syncronize the data.
    items = syncronizer.get_all_changed_items()
#
#   print(json.dumps(flatten_list_of_dicts(items.get_nodes()), indent=4))
    flat = flatten_list_of_dicts(items)
    parq = convert_dicts_to_parquet(flat)
    write_buffer_to_file(parq, f"./output/{get_current_time_for_filename()}_customers.parquet")


    # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    syncronizer_queries = DataSyncronizerQueries(GET_EMPLOYEE_DELTAS, GET_EMPLOYEES_FROM_DBIDS, GET_EMPLOYEES_AFTER_CURSOR)
    syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   
    # Syncronize the data.
    items = syncronizer.get_all_items()
#
#
    print(json.dumps(flatten_list_of_dicts(items.get_nodes()), indent=4))
    flat = flatten_list_of_dicts(items.get_nodes())
    parq = convert_dicts_to_parquet(flat)
    write_buffer_to_file(parq, f"./output/{get_current_time_for_filename()}_employees.parquet")



    # Get all the new data since last sync.
    #edges = paginate_gql_query(gql_client, GET_TIMESHEET_DELTAS)
    #print(json.dumps(data, indent=4))
    # If there's no new data, return.
    #if not data:
    #    logging.info("No new data since last sync.")
    #    return
    
    # Transform data and convert to parquet.
    #flattened_data = flatten_list_of_dicts(data)
    #parquet_data = convert_dicts_to_parquet(flattened_data)

    # Write the data to data lake.


    logging.info('Python timer trigger function executed yolo swag.')


SYNCRONIZER_NAME = "TEST"

@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def sync_timesheets_2(myTimer: func.TimerRequest) -> None:
    # Get the environment variables.
    api_endpoint, api_key = os.getenv("Endpoint"), os.getenv("APIKey")

    # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    syncronizer_queries = DataSyncronizerQueries(GET_TIMESHEET_DELTAS, GET_TIMESHEETS_FROM_DBIDS, GET_TIMESHEETS_AFTER_CURSOR)
    syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   
    # Syncronize the data.
    items = syncronizer.get_last_delta()


    print(json.dumps(flatten_list_of_dicts(items), indent=4))



    logging.info('Python timer trigger function executed yolo swag.')