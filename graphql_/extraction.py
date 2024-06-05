from graphql_.client import GraphQLClient, PaginationQueryResult
from typing import Dict, Any
# This should be removed
from graphql_.queries import GET_TIMESHEETS


class DeltasResult:
    def __init__(self, additions: set, updates: set, deletions: set, last_cursor: str) -> None:
        self.additions = additions
        self.updates = updates
        self.deletions = deletions
        self.last_cursor = last_cursor

        # Methods for getting the latest entries for these dbids?


class DeltasExtractor:
    def __init__(self, client: GraphQLClient, query: str, variables: Dict[str, Any], query_name: str) -> None:
        self.graphql_client = client
        self.query = query
        self.variables = variables
        self.query_name = query_name

    def get_all_deltas(self) -> DeltasResult:
        query_result = self.graphql_client.paginate_gql_query(self.query, self.variables, self.query_name)
        deltas_result = self._extract_all_deltas_from_edges(query_result)
        return deltas_result
    
    def get_all_changed_items(self, ) -> PaginationQueryResult:
        deltas_result = self.get_all_deltas()
        query_results = self.graphql_client.paginate_gql_query(GET_TIMESHEETS, {"first": 10000, "dbIdList": list(deltas_result.additions)}, "timesheets")
        return query_results

    def _extract_all_deltas_from_edges(self, result: PaginationQueryResult) -> None:
        additions = set()
        updates = set()
        deletions = set()

        edges = result.edges
        if not edges:
            return

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

        return DeltasResult(additions, updates, deletions, result.last_cursor)

class DataSyncronizer:
    # name will determine key path for the configuration.
    def __init__(self, name: str, client: GraphQLClient, configuration_manager, deltas_extractor) -> None:
        self.graphql_client = client
        self.configuration_manager = configuration_manager
        self.deltas_extractor = deltas_extractor


    #def sync_data(self, query: str, variables: Dict[str, Any], query_name: str) -> None:
    #    deltas_result = self.deltas_extractor.get_all_changes()
    #    
    #    query_result = self.graphql_client.paginate_gql_query(query, variables, query_name)
    #    self._sync_data(result)

    def _sync_data(self, result: PaginationQueryResult) -> None:
        edges = PaginationQueryResult.edges
        if not edges:
            return

        for edge in edges:
            mutation_type = edge['mutationType']
            db_id = edge['node']['dbId']

            if mutation_type == "DELETED":
                self._delete_item(db_id)

            elif mutation_type in ["UPDATED", "ADDED"]:
                self._update_item(db_id)

            else:
                raise ValueError(f"Unknown mutation type: {mutation_type}")

    def _delete_item(self, db_id: str) -> None:
        pass

    def _update_item(self, db_id: str) -> None:
        pass