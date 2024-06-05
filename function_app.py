import logging
import os
import azure.functions as func
from graphql_.extraction import DeltasExtractor
from graphql_.client import GraphQLClient
from graphql_.queries import GET_TIMESHEET_DELTAS
from utils.data_formatting import flatten_list_of_dicts
from utils.files import convert_dicts_to_parquet, write_buffer_to_file
import json

app = func.FunctionApp()

def extract_data_fn(result):
    deletions = set()
    updates = []

    edges = result['timesheet_deltas']['edges']
    if edges is None:
        return updates

    for edge in result['timesheet_deltas']['edges']:
        mutation_type = edge['mutationType']
        current = edge['node']['_current']

        if mutation_type == "DELETION" or current is None:
            deletions.add(edge['node']['dbId'])


        elif mutation_type in ["UPDATED", "ADDED"]:
            current['mutationType'] = mutation_type
            updates.append(current)

        else:
            raise ValueError(f"Unknown mutation type: {mutation_type}")

    for db_id in deletions:
        item = {"dbId": db_id, "mutationType": "DELETION"}
        updates.append(item)

    return updates

def extract_data_fn_2(result):
    deletions = set()
    updates = []

    # Return empty list if there are no edges.
    edges = result['timesheet_deltas']['edges']
    if edges is None:
        return updates
    
    for edge in edges:
        mutation_type = edge['mutationType']
        current = edge['node']['_current']

        if mutation_type == "DELETION" or current is None:
            deletions.add(edge['node']['dbId'])


        elif mutation_type in ["UPDATED", "ADDED"]:
            item = {"dbId": edge['node']['dbId'], "mutationType": mutation_type}
            updates.append(item)

        else:
            raise ValueError(f"Unknown mutation type: {mutation_type}")

    for db_id in deletions:
        item = {"dbId": db_id, "mutationType": "DELETION"}
        updates.append(item)

    return updates

##def has_next_page_fn(result):
##    return result['timesheet_deltas']['pageInfo']['hasNextPage']
##
##def get_last_cursor_fn(result):
##    return result['timesheet_deltas']['edges'][-1]['node']['syncVersion']


@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def sync_timesheets(myTimer: func.TimerRequest) -> None:
    # Get the environment variables.
    api_endpoint, api_key = os.getenv("Endpoint"), os.getenv("APIKey")

    # Create a GraphQL client.
    gql_client = GraphQLClient(api_endpoint, api_key)
    delta_extractor = DeltasExtractor(
        gql_client, 
        GET_TIMESHEET_DELTAS,
        {"first": 1000},
        "timesheet_deltas"
    )

    deltas = delta_extractor.get_all_deltas()
    query_result = delta_extractor.get_all_changed_items()
    query_result.add_key_to_all_nodes("mutationType", "ADDED")


    print(json.dumps(flatten_list_of_dicts(query_result.get_nodes()), indent=4))

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

    print(deltas.additions, deltas.updates, deltas.deletions, deltas.last_cursor)
    # Write the data to data lake.


    logging.info('Python timer trigger function executed yolo swag.')


