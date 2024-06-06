import logging
import os
import azure.functions as func
from graphql_.extraction import DataSyncronizer, DataSyncronizerQueries
from graphql_.client import GraphQLClient
from graphql_.queries import GET_TIMESHEET_DELTAS, GET_TIMESHEETS_FROM_DBIDS, GET_CUSTOMER_DELTAS, GET_CUSTOMERS_FROM_DBIDS
from utils.data_formatting import flatten_list_of_dicts
from utils.files import convert_dicts_to_parquet, write_buffer_to_file
import json

app = func.FunctionApp()

SYNCRONIZER_NAME = "timesheets"

@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def sync_timesheets(myTimer: func.TimerRequest) -> None:
    # Get the environment variables.
    api_endpoint, api_key = os.getenv("Endpoint"), os.getenv("APIKey")

    # Create a GraphQL client.
    #gql_client = GraphQLClient(api_endpoint, api_key)
    #syncronizer_queries = DataSyncronizerQueries(GET_TIMESHEET_DELTAS, GET_TIMESHEETS_FROM_DBIDS)
    #syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   #
    ## Syncronize the data.
    #items = syncronizer.get_all_changed_items()
#
#
    #print(json.dumps(flatten_list_of_dicts(items.get_nodes()), indent=4))



     # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    syncronizer_queries = DataSyncronizerQueries(GET_CUSTOMER_DELTAS, GET_CUSTOMERS_FROM_DBIDS)
    syncronizer = DataSyncronizer(SYNCRONIZER_NAME, gql_client, syncronizer_queries)
   
    # Syncronize the data.
    items = syncronizer.get_all_changed_items()


    print(json.dumps(flatten_list_of_dicts(items), indent=4))




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


