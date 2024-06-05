from graphql_.client import GraphQLClient
from typing import Dict


def paginate_gql_query(client: GraphQLClient, query, variables, query_name, extract_data_fn, has_next_page_fn, get_last_cursor_fn):
    """
    Fetches all data by paginating over a GraphQL query.
    
    :param api_url: URL of the GraphQL API endpoint.
    :param query: GQL query string that includes pagination.
    :param variables: Initial variables for the query, typically includes 'first' and optionally 'after'.
    :param extract_data_fn: Function to extract data from the query result.
    :param has_next_page_fn: Function to determine if there's another page.
    :param update_cursor_fn: Function to update the cursor in variables for the next page.
    :return: List of all fetched items.
    """
    all_data = []
    while True:
        # Execute the query
        result = client.execute_graphql_query(query=query, variables=variables)
        data = extract_data_fn(result, query_name)
        all_data.extend(data)

        # Check if there is a next page
        if not has_next_page_fn(result, query_name):
            break

        # Update cursor to the next page
        last_cursor = get_last_cursor_fn(result, query_name)

        # Update variables for the next page.
        variables['after'] = last_cursor

    return all_data


def paginate_gql_query_2(client: GraphQLClient, query, variables, query_name):
    """
    Fetches all data by paginating over a GraphQL query.
    
    :param api_url: URL of the GraphQL API endpoint.
    :param query: GQL query string that includes pagination.
    :param variables: Initial variables for the query, typically includes 'first' and optionally 'after'.
    :param extract_data_fn: Function to extract data from the query result.
    :param has_next_page_fn: Function to determine if there's another page.
    :param update_cursor_fn: Function to update the cursor in variables for the next page.
    :return: List of all fetched items.
    """
    all_results = []
    while True:
        # Execute the query.
        result = client.execute_graphql_query(query=query, variables=variables)
        all_results.append(result)

        # Check if there is a next page.
        if not result[query_name]['pageInfo']['hasNextPage']:
            break

        # Get the last cursor.
        last_cursor = result[query_name]['edges'][-1]['cursor']

        # Update variables for the next page.
        variables['after'] = last_cursor

    return all_results

def get_all_deltas(client: GraphQLClient, query, variables, query_name):
    # return all deltas from the query.
    pass

def extract_deltas_from_results(results: list[dict], delta_query_name: str):
    """
    Extracts the deltas from a list of results.
    
    :param results: List of results from the GraphQL query.
    :return: List of deltas.
    """
    finished_list = []
    additions = set()
    updates = set()
    deletions = set()


    # Return empty list if there are no edges.
    edges = []
    for result in results:
        edges.extend(result[delta_query_name]['edges'])
    
    if edges is None:
        return finished_list
    
    for edge in edges:
        mutation_type = edge['mutationType']
        db_id = edge['node']['dbId']

        if mutation_type == "DELETED":
            deletions.add(db_id)

        elif mutation_type in ["UPDATED"]:
            updates.add(db_id)

        elif mutation_type in ["ADDED"]:
            additions.add(db_id)

        else:
            raise ValueError(f"Unknown mutation type: {mutation_type}")

    for db_id in deletions:
        try: 
            updates.remove(db_id)
            additions.remove(db_id)
        except KeyError:
            pass

    for db_id in additions:
        item = {"dbId": db_id, "mutationType": "ADDED"}
        finished_list.append(item)

    for db_id in updates:
        item = {"dbId": db_id, "mutationType": "UPDATED"}
        finished_list.append(item)

    for db_id in deletions:
        item = {"dbId": db_id, "mutationType": "DELETED"}
        finished_list.append(item)

    return finished_list

def extract_data_deltas_fn(result: Dict[str, any], delta_query_name: str):
    finished_list = []
    additions = set()
    updates = set()
    deletions = set()


    # Return empty list if there are no edges.
    edges = result[delta_query_name]['edges']
    if edges is None:
        return finished_list
    
    for edge in edges:
        mutation_type = edge['mutationType']
        db_id = edge['node']['dbId']

        if mutation_type == "DELETED":
            deletions.add(db_id)

        elif mutation_type in ["UPDATED"]:
            updates.add(db_id)

        elif mutation_type in ["ADDED"]:
            additions.add(db_id)

        else:
            raise ValueError(f"Unknown mutation type: {mutation_type}")

    for db_id in deletions:
        try: 
            updates.remove(db_id)
            additions.remove(db_id)
        except KeyError:
            pass

    for db_id in additions:
        item = {"dbId": db_id, "mutationType": "ADDED"}
        finished_list.append(item)

    for db_id in updates:
        item = {"dbId": db_id, "mutationType": "UPDATED"}
        finished_list.append(item)

    for db_id in deletions:
        item = {"dbId": db_id, "mutationType": "DELETED"}
        finished_list.append(item)

    return finished_list

def has_next_page_fn(result: Dict[str, any], delta_query_name: str):
    return result[delta_query_name]['pageInfo']['hasNextPage']

def get_last_cursor_fn(result: Dict[str, any], delta_query_name: str):
    return result[delta_query_name]['edges'][-1]['node']['syncVersion']

